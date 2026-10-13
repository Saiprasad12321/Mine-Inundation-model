"""Extract, classify, and verify all inundation and water-related candidate incidents across both PDFs."""
import pymupdf
import re
import json

def inspect_all_water_mentions():
    coal_doc = pymupdf.open("data/raw/sanket_coal_2016_2022.pdf")
    non_coal_doc = pymupdf.open("data/raw/sanket_non_coal_2016_2022.pdf")
    
    # Let's inspect all Detailed Fatal Accident reports in Coal
    # We already have extract_detailed_findings in extract_all_records.py
    from extract_all_records import extract_detailed_findings
    
    coal_reports = extract_detailed_findings(coal_doc, "sanket_coal_2016_2022.pdf", "Coal")
    non_coal_reports = extract_detailed_findings(non_coal_doc, "sanket_non_coal_2016_2022.pdf", "Non-Coal")
    
    water_keywords = [
        'irruption', 'inundat', 'inrush', 'drown', 'waterlog', 'submerg', 
        'flash flood', 'water ingress', 'water barrier', 'stowing barricade', 
        'sludge', 'slurry', 'sump', 'water tank'
    ]
    
    def matches_water(r):
        text = (r.get("narrative", "") + " " + r.get("had_paras", "") + " " + (r.get("cause_name") or "")).lower()
        return any(kw in text for kw in water_keywords)
        
    coal_water = [r for r in coal_reports if matches_water(r)]
    non_coal_water = [r for r in non_coal_reports if matches_water(r)]
    
    print(f"Coal Detailed Fatal Accident reports mentioning water: {len(coal_water)}")
    for r in coal_water:
        print(f"  [{r['date']} - {r['mine_name']}] Code: {r['cause_code']} ({r['cause_name']}) | Page: {r['page_start']}")
        print(f"     Narrative excerpt: {r['narrative'][:120]}...\n")
        
    print(f"\nNon-Coal Detailed Fatal Accident reports mentioning water: {len(non_coal_water)}")
    for r in non_coal_water:
        print(f"  [{r['date']} - {r['mine_name']}] Code: {r['cause_code']} ({r['cause_name']}) | Page: {r['page_start']}")
        print(f"     Narrative excerpt: {r['narrative'][:120]}...\n")

if __name__ == "__main__":
    inspect_all_water_mentions()
