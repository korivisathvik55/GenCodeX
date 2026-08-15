def chunk_code(
    content: str,
    chunk_size: int = 1200,
    overlap: int = 200
):
    if not content:
        return []

    chunks = []

    start = 0
    content_length = len(content)

    while start < content_length:
        end = start + chunk_size

        chunk = content[start:end]

        if chunk.strip():
            chunks.append(chunk)

        if end >= content_length:
            break

        start = end - overlap

    return chunks