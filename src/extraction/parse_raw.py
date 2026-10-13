"""Extraction and discovery script to parse every page of both PDFs and identify:
1. All yearly detailed fatal accident findings (Summary of Findings of Fatal Accidents)
2. All Major Accidents Since 1901
3. All Courts of Inquiry
4. All decadal/yearly causewise trends (irruption of water, drowning, etc.)
"""
import pymupdf
import re
import json

def parse_coal_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    print(f"Coal PDF pages: {len(doc)}")
    
    # 1. Search for Statement X.8 (Summary of Findings)
    findings = []
    major_accidents = []
    courts_of_inquiry = []
    
    current_year = None
    current_code = None
    current_cause = None
    
    # regex for accident header in Statement X.8:
    # e.g., "1.  Date -  27.03.16             Mine -  BANGWAR U/G PROJECT"
    acc_header_pattern = re.compile(r'^\s*(\d+)\.\s+Date\s*-\s*(\d{2}[\.\-]\d{2}[\.\-]\d{2,4})\s+Mine\s*-\s*(.+)$', re.MULTILINE)
    
    full_text_by_page = {}
    for p_idx in range(len(doc)):
        text = doc[p_idx].get_text()
        full_text_by_page[p_idx + 1] = text
        
    return full_text_by_page

if __name__ == "__main__":
    coal_text = parse_coal_pdf("data/raw/sanket_coal_2016_2022.pdf")
    non_coal_text = parse_coal_pdf("data/raw/sanket_non_coal_2016_2022.pdf")
    print("PDFs loaded successfully into memory.")
