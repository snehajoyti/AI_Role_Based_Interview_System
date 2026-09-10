import os
import json
import faiss
from sentence_transformers import SentenceTransformer 

from app.rag.pdf_loader import extract_text_from_pdf
from app.rag.chunker import create_chunks 


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def build_vector_store(pdf_path: str, index_path: str, metadata_path: str):
    #  1. Extract text from PDF
    pages = extract_text_from_pdf(pdf_path)

    #2. Create chunks
    chunks = create_chunks(pages)

    if not chunks:
        raise ValueError(f"No text chunks found in PDF: {pdf_path}")

    # 3. Prepare texts
    texts = [chunk["text"] for chunk in chunks]

    # 4.Generate embeddings
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True 
    )

    #5. Create FAISS index
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # 6. Create output directions
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)

    #7. Save FAISS index
    faiss.write_index(index, index_path)

    #8. Save chunk metadata 
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"PDF: {pdf_path}")
    print(f"Pages: {len(pages)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Embedding dimension: {dimension}")
    print(f"FAISS vectors: {index.ntotal}")
    print(f"Index saved: {index_path}")
    print(f"Metadata saved: {metadata_path}")
