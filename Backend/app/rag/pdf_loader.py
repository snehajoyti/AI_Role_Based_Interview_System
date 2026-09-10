import pymupdf

def extract_text_from_pdf(pdf_path: str):
    document = pymupdf.open(pdf_path)

    pages_data = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        if text.strip():
            pages_data.append({
                "page_number": page_number,
                "text": text.strip()
            })

    document.close()

    return pages_data 
