import pymupdf

coal_doc = pymupdf.open("data/raw/sanket_coal_2016_2022.pdf")
print("=== COAL PDF PAGE 299 (Major Accidents) ===")
print(coal_doc[298].get_text()[:1500])

non_coal_doc = pymupdf.open("data/raw/sanket_non_coal_2016_2022.pdf")
print("=== NON-COAL PDF PAGE 345 (Major Accidents) ===")
print(non_coal_doc[344].get_text()[:1500])
