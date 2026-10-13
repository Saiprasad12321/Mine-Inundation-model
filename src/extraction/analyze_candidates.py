"""Detailed analysis of candidates found across Coal and Non-Coal PDFs."""
import pymupdf
import json
import re

def analyze_candidates():
    with open("data/extracted/candidate_scan_summary.json") as f:
        scan_data = json.load(f)
        
    coal_doc = pymupdf.open("data/raw/sanket_coal_2016_2022.pdf")
    non_coal_doc = pymupdf.open("data/raw/sanket_non_coal_2016_2022.pdf")
    
    print("=== COAL CANDIDATES BREAKDOWN ===")
    for item in scan_data["coal"]:
        p = item["page"]
        text = coal_doc[p - 1].get_text()
        first_few = text.strip().split("\n")[:4]
        print(f"Page {p} (matches {item['match_count']}, keys={item['keywords']}): {' | '.join(first_few)}")
        
    print("\n=== NON-COAL CANDIDATES BREAKDOWN ===")
    for item in scan_data["non_coal"]:
        p = item["page"]
        text = non_coal_doc[p - 1].get_text()
        first_few = text.strip().split("\n")[:4]
        print(f"Page {p} (matches {item['match_count']}, keys={item['keywords']}): {' | '.join(first_few)}")

if __name__ == "__main__":
    analyze_candidates()
