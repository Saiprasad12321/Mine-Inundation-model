import pymupdf
import re
import json

def parse_court_of_inquiry_coal(doc):
    """
    Parses Table on PDF pages 307 to 310 (index 306 to 309).
    Columns: Sl. No., Date of Accident, Name of Mine & Cause, No. of Persons Killed, Constitution of Court of Enquiry, Assessors
    """
    coi_list = []
    
    # Let's inspect the text on each page
    for p_idx in range(306, 310):
        page_num = p_idx + 1
        text = doc[p_idx].get_text()
        
        # Split by blocks or entries
        # Let's see the text structure
        lines = [l.rstrip() for l in text.split("\n") if l.strip()]
        
        # We can extract rows by matching `Sl. Date` or numbers
        # Let's do a structured parse
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # Look for number indicating Sl. No., e.g., "1 07/08/13 Jamadoba 7 Information not readily avaible."
            # Or "42 27/09/95 a) Gaslitand 64 Justice S.K.Mukherjee..."
            m = re.match(r'^(\d+)\s+([\d\/\-]+)\s+(.+)$', line)
            if m:
                sl = int(m.group(1))
                date_str = m.group(2)
                rest = m.group(3).strip()
                
                # Next lines until next Sl number or footer
                entry_lines = [rest]
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if re.match(r'^\d+\s+\d{2}[\/\-]\d{2}[\/\-]\d{2,4}', next_line) or "Statement 5.15" in next_line or next_line.isdigit() and len(next_line) == 3:
                        break
                    entry_lines.append(next_line)
                    i += 1
                    
                full_entry_text = " ".join(entry_lines)
                
                # Extract cause if in parentheses, e.g., (Inundation), (Explosion), (Irruption of Water)
                cause_m = re.findall(r'\(([^\)]+)\)', full_entry_text)
                cause = ", ".join(cause_m) if cause_m else ""
                
                # Check killed
                killed_m = re.search(r'\b(\d+)\s+(Justice|Dy\.|Commissioner|Information|Prof\.|Collector|Dr\.|T\.P\.|H\.C\.|Smt\.)', full_entry_text)
                killed = int(killed_m.group(1)) if killed_m else None
                
                coi_list.append({
                    "sl": sl,
                    "date": date_str,
                    "raw_entry": full_entry_text,
                    "cause": cause,
                    "killed": killed,
                    "page": page_num,
                    "source": "Coal PDF Ch 11 (Court of Inquiry)"
                })
                continue
            i += 1
            
    return coi_list

if __name__ == "__main__":
    coal_doc = pymupdf.open("data/raw/sanket_coal_2016_2022.pdf")
    coi_coal = parse_court_of_inquiry_coal(coal_doc)
    print(f"Parsed {len(coi_coal)} Court of Inquiry entries in Coal.")
    inund_coi = [c for c in coi_coal if any(w in c['cause'].lower() or w in c['raw_entry'].lower() for w in ['inundation', 'irruption', 'water'])]
    print(f"Inundation / Irruption Courts of Inquiry: {len(inund_coi)}")
    for c in inund_coi:
        print(f"  Sl {c['sl']}: {c['date']} | Cause: {c['cause']} | Killed: {c['killed']} | {c['raw_entry'][:80]}...")
