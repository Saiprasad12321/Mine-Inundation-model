"""Extract Chapter 10 (Major Accidents Since 1901) and Chapter 11 (Court of Inquiry) from both PDFs."""
import pymupdf
import re
import json

def parse_major_accidents_coal(doc):
    accidents = []
    # Major Accidents Coal: pages 285 to 292 (index 284 to 291)
    for p_idx in range(284, 292):
        page_num = p_idx + 1
        text = doc[p_idx].get_text()
        lines = text.split("\n")
        for line in lines:
            line_str = line.strip()
            # Row format: e.g. "14 26-10-1910 Murulidih 6 0 Irruption of water"
            # or "271 15-06-2005 Central Sounda 14 0 Irruption of Water"
            # Regex: Sl Date Name Killed S/Injured Cause
            m = re.match(r'^(\d+)\s+([\d\/\-]+)\s+(.+?)\s+(\d+)\s+(\d+)\s+([A-Za-z0-9\s\/\(\)\-]+)$', line_str)
            if m:
                accidents.append({
                    "sl": int(m.group(1)),
                    "date": m.group(2),
                    "mine_name": m.group(3).strip(),
                    "killed": int(m.group(4)),
                    "seriously_injured": int(m.group(5)),
                    "cause": m.group(6).strip(),
                    "page": page_num,
                    "source": "Coal PDF Ch 10 (Major Accidents Since 1901)"
                })
    return accidents

def parse_major_accidents_non_coal(doc):
    accidents = []
    # Major Accidents Non-Coal: pages 331 to 334 (index 330 to 333)
    for p_idx in range(330, 334):
        page_num = p_idx + 1
        text = doc[p_idx].get_text()
        lines = text.split("\n")
        for line in lines:
            line_str = line.strip()
            m = re.match(r'^(\d+)\s+([\d\/\-]+)\s+(.+?)\s+(\d+)\s+(\d+)\s+([A-Za-z0-9\s\/\(\)\-]+)$', line_str)
            if m:
                accidents.append({
                    "sl": int(m.group(1)),
                    "date": m.group(2),
                    "mine_name": m.group(3).strip(),
                    "killed": int(m.group(4)),
                    "seriously_injured": int(m.group(5)),
                    "cause": m.group(6).strip(),
                    "page": page_num,
                    "source": "Non-Coal PDF Ch 10 (Major Accidents Since 1901)"
                })
    return accidents

def parse_court_of_inquiry_coal(doc):
    inquiries = []
    # Coal Court of Inquiry: pages 293 to 296 (index 292 to 295)
    for p_idx in range(292, 296):
        page_num = p_idx + 1
        text = doc[p_idx].get_text()
        # Court of inquiry rows often span lines because of assessors and multiline names
        # Let's inspect raw text blocks
        inquiries.append({"page": page_num, "text": text})
    return inquiries

if __name__ == "__main__":
    coal_doc = pymupdf.open("data/raw/sanket_coal_2016_2022.pdf")
    non_coal_doc = pymupdf.open("data/raw/sanket_non_coal_2016_2022.pdf")
    
    maj_coal = parse_major_accidents_coal(coal_doc)
    maj_non_coal = parse_major_accidents_non_coal(non_coal_doc)
    
    print(f"Parsed {len(maj_coal)} Major Accidents from Coal PDF.")
    print(f"Parsed {len(maj_non_coal)} Major Accidents from Non-Coal PDF.")
    
    # Check inundation/irruption in major accidents
    inund_coal = [a for a in maj_coal if any(k in a['cause'].lower() for k in ['inundation', 'irruption', 'water'])]
    inund_non_coal = [a for a in maj_non_coal if any(k in a['cause'].lower() for k in ['inundation', 'irruption', 'water'])]
    
    print(f"Inundation / Irruption Major Accidents in Coal: {len(inund_coal)}")
    for a in inund_coal:
        print(f"  {a['date']} | {a['mine_name']} | Killed: {a['killed']} | Cause: {a['cause']} | Page: {a['page']}")
        
    print(f"\nInundation / Irruption Major Accidents in Non-Coal: {len(inund_non_coal)}")
    for a in inund_non_coal:
        print(f"  {a['date']} | {a['mine_name']} | Killed: {a['killed']} | Cause: {a['cause']} | Page: {a['page']}")
