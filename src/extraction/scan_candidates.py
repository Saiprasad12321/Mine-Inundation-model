"""Script to scan both PDFs for any candidate mentions of inundation, water inrush, drowning, or flooding."""
import fitz
import re
import json

def scan_pdf(pdf_path, pdf_name):
    doc = fitz.open(pdf_path)
    candidates = []
    
    # regex patterns for leads
    water_patterns = re.compile(
        r'\b(inundat\w*|irruption\w*|inrush\w*|drown\w*|waterlog\w*|submerg\w*|flooding|flash flood|water ingress)\b',
        re.IGNORECASE
    )
    
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        matches = list(water_patterns.finditer(text))
        if matches:
            # check lines or context
            lines = text.split('\n')
            matched_lines = []
            for i, line in enumerate(lines):
                if water_patterns.search(line):
                    # grab surrounding lines
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    snippet = " ".join([l.strip() for l in lines[start:end]])
                    matched_lines.append(snippet)
            
            candidates.append({
                "pdf": pdf_name,
                "page": page_num + 1,
                "match_count": len(matches),
                "keywords": list(set(m.group(0).lower() for m in matches)),
                "snippet": " | ".join(matched_lines[:4])
            })
            
    return candidates

if __name__ == "__main__":
    coal_cands = scan_pdf("data/raw/sanket_coal_2016_2022.pdf", "sanket_coal_2016_2022.pdf")
    non_coal_cands = scan_pdf("data/raw/sanket_non_coal_2016_2022.pdf", "sanket_non_coal_2016_2022.pdf")
    
    print(f"Coal PDF pages with matches: {len(coal_cands)}")
    print(f"Non-Coal PDF pages with matches: {len(non_coal_cands)}")
    
    with open("data/extracted/candidate_scan_summary.json", "w") as f:
        json.dump({"coal": coal_cands, "non_coal": non_coal_cands}, f, indent=2)
    print("Saved candidate_scan_summary.json")
