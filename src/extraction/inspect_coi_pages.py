import pymupdf

coal_doc = pymupdf.open("data/raw/sanket_coal_2016_2022.pdf")
print("=== COAL PDF PAGE 307 (Court of Inquiry) ===")
print(coal_doc[306].get_text()[:1500])

non_coal_doc = pymupdf.open("data/raw/sanket_non_coal_2016_2022.pdf")
print("=== NON-COAL PDF PAGE 349 (Court of Inquiry) ===")
print(non_coal_doc[348].get_text()[:1500])
