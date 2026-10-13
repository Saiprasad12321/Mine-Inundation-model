import pymupdf

coal_doc = pymupdf.open("data/raw/sanket_coal_2016_2022.pdf")
print("=== PAGE 285 OF COAL (Ch 10) ===")
print(coal_doc[284].get_text()[:2000])

non_coal_doc = pymupdf.open("data/raw/sanket_non_coal_2016_2022.pdf")
print("=== PAGE 331 OF NON-COAL (Ch 10) ===")
print(non_coal_doc[330].get_text()[:2000])
