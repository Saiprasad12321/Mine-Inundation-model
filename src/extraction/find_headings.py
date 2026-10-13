import pymupdf

def find_headings(pdf_path):
    doc = pymupdf.open(pdf_path)
    print(f"=== SEARCHING {pdf_path} ===")
    for p_idx in range(len(doc)):
        text = doc[p_idx].get_text()
        if "MAJOR ACCIDENT SINCE 1901" in text:
            print(f"  Found 'MAJOR ACCIDENT SINCE 1901' on PDF page {p_idx + 1}")
        if "COURT OF INQUIRY" in text:
            print(f"  Found 'COURT OF INQUIRY' on PDF page {p_idx + 1}")

find_headings("data/raw/sanket_coal_2016_2022.pdf")
find_headings("data/raw/sanket_non_coal_2016_2022.pdf")
