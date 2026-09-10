def create_chunks(pages_data, chunk_size=1000, overlap=200):
    chunks = []

    for page in pages_data:
        text = page["text"]
        page_number = page["page_number"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page_number": page_number 
                })

            start += chunk_size - overlap

    return chunks 