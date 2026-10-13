"""Robust parser for Chapter 10 (Major Accidents Since 1901) and Chapter 11 (Court of Inquiry)."""
import pymupdf
import re
import json

def parse_ch10_coal(doc):
    """
    Parses table on pages 299 to 306 (index 284 to 291).
    Table format: Sl, Date of Accident, Name of Mine, Number of Persons (Killed, S/Injured), Cause of Accident
    """
    accidents = []
    # Collect all lines across the pages
    all_lines = []
    page_map = []
    for p_idx in range(298, 306):
        page_num = p_idx + 1
        lines = [l.strip() for l in doc[p_idx].get_text().split("\n") if l.strip()]
        for l in lines:
            all_lines.append(l)
            page_map.append(page_num)
            
    # Find start of table data
    i = 0
    while i < len(all_lines):
        line = all_lines[i]
        # Look for digit starting an entry
        if re.match(r'^\d+$', line):
            sl = int(line)
            # Look ahead for date
            if i + 1 < len(all_lines) and re.match(r'^\d{2}[\-\/]\d{2}[\-\/]\d{2,4}$', all_lines[i+1]):
                date_str = all_lines[i+1]
                # Next is mine name (could be 1 or 2 lines)
                mine_name_parts = []
                idx = i + 2
                while idx < len(all_lines) and not re.match(r'^\d+$', all_lines[idx]):
                    mine_name_parts.append(all_lines[idx])
                    idx += 1
                
                # We expect killed, injured, cause
                if idx + 2 < len(all_lines) and re.match(r'^\d+$', all_lines[idx]) and re.match(r'^\d+$', all_lines[idx+1]):
                    killed = int(all_lines[idx])
                    injured = int(all_lines[idx+1])
                    cause_parts = []
                    c_idx = idx + 2
                    while c_idx < len(all_lines) and not re.match(r'^\d+$', all_lines[c_idx]) and not all_lines[c_idx].startswith("Sl.") and not all_lines[c_idx].startswith("Date of"):
                        # Avoid page numbers like 286, 287
                        if re.match(r'^\d{3}$', all_lines[c_idx]) and int(all_lines[c_idx]) > 200:
                            c_idx += 1
                            continue
                        cause_parts.append(all_lines[c_idx])
                        c_idx += 1
                        
                    mine_name = " ".join(mine_name_parts).strip()
                    cause = " ".join(cause_parts).strip()
                    
                    accidents.append({
                        "sl": sl,
                        "date": date_str,
                        "mine_name": mine_name,
                        "killed": killed,
                        "seriously_injured": injured,
                        "cause": cause,
                        "page": page_map[i]
                    })
                    i = c_idx
                    continue
        i += 1
    return accidents

def parse_ch10_non_coal(doc):
    """
    Parses table on pages 345 to 348 (index 344 to 347).
    """
    accidents = []
    all_lines = []
    page_map = []
    for p_idx in range(344, 348):
        page_num = p_idx + 1
        lines = [l.strip() for l in doc[p_idx].get_text().split("\n") if l.strip()]
        for l in lines:
            all_lines.append(l)
            page_map.append(page_num)
            
    i = 0
    while i < len(all_lines):
        line = all_lines[i]
        if re.match(r'^\d+$', line):
            sl = int(line)
            if i + 1 < len(all_lines) and re.match(r'^\d{2}[\-\/]\d{2}[\-\/]\d{2,4}$', all_lines[i+1]):
                date_str = all_lines[i+1]
                mine_name_parts = []
                idx = i + 2
                while idx < len(all_lines) and not re.match(r'^\d+$', all_lines[idx]):
                    mine_name_parts.append(all_lines[idx])
                    idx += 1
                    
                if idx + 2 < len(all_lines) and re.match(r'^\d+$', all_lines[idx]) and re.match(r'^\d+$', all_lines[idx+1]):
                    killed = int(all_lines[idx])
                    injured = int(all_lines[idx+1])
                    cause_parts = []
                    c_idx = idx + 2
                    while c_idx < len(all_lines) and not re.match(r'^\d+$', all_lines[c_idx]) and not all_lines[c_idx].startswith("Sl.") and not all_lines[c_idx].startswith("Date of") and not "Statistical Analysis" in all_lines[c_idx] and not "SANKET" in all_lines[c_idx]:
                        if re.match(r'^\d{3}$', all_lines[c_idx]) and int(all_lines[c_idx]) > 300:
                            c_idx += 1
                            continue
                        cause_parts.append(all_lines[c_idx])
                        c_idx += 1
                        
                    mine_name = " ".join(mine_name_parts).strip()
                    cause = " ".join(cause_parts).strip()
                    
                    accidents.append({
                        "sl": sl,
                        "date": date_str,
                        "mine_name": mine_name,
                        "killed": killed,
                        "seriously_injured": injured,
                        "cause": cause,
                        "page": page_map[i]
                    })
                    i = c_idx
                    continue
        i += 1
    return accidents

if __name__ == "__main__":
    coal_doc = pymupdf.open("data/raw/sanket_coal_2016_2022.pdf")
    non_coal_doc = pymupdf.open("data/raw/sanket_non_coal_2016_2022.pdf")
    
    c_acc = parse_ch10_coal(coal_doc)
    nc_acc = parse_ch10_non_coal(non_coal_doc)
    
    print(f"Total Major Accidents parsed in Coal: {len(c_acc)} (Expected 284)")
    print(f"Total Major Accidents parsed in Non-Coal: {len(nc_acc)} (Expected 105)")
    
    inund_c = [a for a in c_acc if any(w in a['cause'].lower() for w in ['inundation', 'irruption', 'water'])]
    inund_nc = [a for a in nc_acc if any(w in a['cause'].lower() for w in ['inundation', 'irruption', 'water'])]
    
    print(f"Major Inundation / Irruption in Coal: {len(inund_c)}")
    print(f"Major Inundation / Irruption in Non-Coal: {len(inund_nc)}")
    
    for a in inund_c:
        print(f"  Coal Sl {a['sl']}: {a['date']} | {a['mine_name']} | Killed: {a['killed']} | Cause: {a['cause']} (p.{a['page']})")
    for a in inund_nc:
        print(f"  Non-Coal Sl {a['sl']}: {a['date']} | {a['mine_name']} | Killed: {a['killed']} | Cause: {a['cause']} (p.{a['page']})")
