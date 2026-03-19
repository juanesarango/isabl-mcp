"""LLM-based document summarizer with async concurrency and incremental saving."""

from __future__ import annotations

import asyncio
import json
import logging
import re
from pathlib import Path

from tqdm import tqdm

from isabl_knowledge.llm import get_async_client, get_default_model
from isabl_knowledge.models import Document

logger = logging.getLogger(__name__)

BATCH_SIZE = 10
MAX_CONCURRENCY = 10
MAX_RETRIES = 3

SUMMARIZE_BATCH_PROMPT = """Analyze these {count} documents from the Isabl genomics platform.

For EACH document, produce a JSON object with:
- "doc_id": the exact doc_id from the input (REQUIRED)
- "title": descriptive title (5-10 words)
- "summary": 2-3 sentence summary explaining what this document covers
- "tags": 3-5 topic tags
- "questions": 3-5 questions this document answers

The audience is researchers, bioinformaticians, and engineers learning about Isabl.

Documents:
{documents}

Respond with a JSON array of {count} objects, one per document. No markdown fencing."""


def _parse_batch_response(text: str, docs: list[Document]) -> dict[str, dict]:
    """Parse LLM batch response, return mapping of doc_id -> summary data."""
    text = re.sub(r"^```(?:json)?\s*\n?", "", text.strip())
    text = re.sub(r"\n?```\s*$", "", text)

    try:
        items = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("Failed to parse batch response as JSON")
        return {}

    if isinstance(items, dict):
        items = [items]

    return {item["doc_id"]: item for item in items if item.get("doc_id")}


async def _summarize_batch_async(
    docs: list[Document],
    client,
    model: str,
    semaphore: asyncio.Semaphore,
) -> list[Document]:
    """Summarize a batch of documents with retry and concurrency control."""
    doc_inputs = json.dumps(
        [{"doc_id": d.doc_id, "content": d.content[:3000]} for d in docs],
        indent=2,
    )
    prompt = SUMMARIZE_BATCH_PROMPT.format(count=len(docs), documents=doc_inputs)

    async with semaphore:
        for attempt in range(MAX_RETRIES):
            try:
                response = await client.chat.completions.create(
                    model=model,
                    max_completion_tokens=8192,
                    messages=[{"role": "user", "content": prompt}],
                )
                break
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    wait = 2 ** (attempt + 1)
                    logger.warning(f"Batch failed ({e}), retrying in {wait}s...")
                    await asyncio.sleep(wait)
                else:
                    logger.error(f"Batch failed after {MAX_RETRIES} attempts: {e}")
                    return docs

    text = response.choices[0].message.content or ""
    parsed = _parse_batch_response(text, docs)

    for doc in docs:
        data = parsed.get(doc.doc_id, {})
        if data:
            doc.title = data.get("title", "")
            doc.summary = data.get("summary", "")
            doc.tags = data.get("tags", [])
            doc.questions = data.get("questions", [])

    return docs


def _save(docs: list[Document], done: dict, all_docs: list[Document], path: Path):
    """Save current progress to disk."""
    merged = [done.get(d.doc_id, d) for d in all_docs]
    path.write_text(json.dumps([d.model_dump() for d in merged], indent=2))


async def _summarize_all_async(
    docs: list[Document],
    model: str,
    output_path: Path | None,
    batch_size: int,
    max_concurrency: int,
) -> list[Document]:
    """Run all batches concurrently with a semaphore limit."""
    client = get_async_client()
    semaphore = asyncio.Semaphore(max_concurrency)

    done = {d.doc_id: d for d in docs if d.summary}
    pending = [d for d in docs if not d.summary]

    if done:
        logger.info(f"Skipping {len(done)} already-summarized documents")

    if not pending:
        return docs

    # Create batches
    batches = [pending[i : i + batch_size] for i in range(0, len(pending), batch_size)]

    # Launch all batches concurrently
    pbar = tqdm(total=len(pending), desc="Summarizing", unit="doc")

    async def run_batch(batch):
        result = await _summarize_batch_async(batch, client, model, semaphore)
        for doc in result:
            done[doc.doc_id] = doc
        pbar.update(len(batch))
        if output_path:
            _save(docs, done, docs, output_path)
        return result

    tasks = [run_batch(batch) for batch in batches]
    await asyncio.gather(*tasks)
    pbar.close()

    return [done.get(d.doc_id, d) for d in docs]


def summarize_documents(
    docs: list[Document],
    model: str | None = None,
    output_path: Path | None = None,
    batch_size: int = BATCH_SIZE,
    max_concurrency: int = MAX_CONCURRENCY,
) -> list[Document]:
    """Summarize documents with async concurrency, progress bar, and incremental saving.

    Sends up to max_concurrency batches in parallel. Already-summarized documents
    are skipped. Progress is saved to output_path after each batch completes.
    """
    model = model or get_default_model()
    return asyncio.run(
        _summarize_all_async(docs, model, output_path, batch_size, max_concurrency)
    )
