import pymupdf
from parse_ch10_robust import parse_ch10_coal

coal_doc = pymupdf.open("data/raw/sanket_coal_2016_2022.pdf")
accs = parse_ch10_coal(coal_doc)
parsed_sls = set(a['sl'] for a in accs)
expected_sls = set(range(1, 285))
missing = expected_sls - parsed_sls
print("Missing Sl in Coal:", sorted(list(missing)))
