"""Document inspection script to analyze the structure and text extractability of both PDFs."""
import os
import json
import fitz  # PyMuPDF

def inspect_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    empty_pages = 0
    text_pages = 0
    total_text_len = 0
    sample_text = {}
    
    for page_idx in range(total_pages):
        page = doc[page_idx]
        text = page.get_text()
        text_len = len(text.strip())
        if text_len == 0:
            empty_pages += 1
        else:
            text_pages += 1
            total_text_len += text_len
            
        # grab samples at beginning, middle, end
        if page_idx in [0, 4, 12, 18, 32, 48, 100, 150, 200, 284, 292, 300, total_pages - 1]:
            sample_text[page_idx + 1] = text[:300].replace("\n", " ")
            
    meta = doc.metadata
    
    return {
        "file": os.path.basename(pdf_path),
        "file_size_bytes": os.path.getsize(pdf_path),
        "total_pages": total_pages,
        "text_pages": text_pages,
        "empty_pages": empty_pages,
        "avg_chars_per_page": round(total_text_len / max(1, text_pages), 2),
        "metadata": meta,
        "sample_pages": sample_text
    }

if __name__ == "__main__":
    coal_pdf = "data/raw/sanket_coal_2016_2022.pdf"
    non_coal_pdf = "data/raw/sanket_non_coal_2016_2022.pdf"
    
    res_coal = inspect_pdf(coal_pdf)
    res_non_coal = inspect_pdf(non_coal_pdf)
    
    print("=== COAL PDF INSPECTION ===")
    print(json.dumps(res_coal, indent=2))
    
    print("\n=== NON-COAL PDF INSPECTION ===")
    print(json.dumps(res_non_coal, indent=2))
