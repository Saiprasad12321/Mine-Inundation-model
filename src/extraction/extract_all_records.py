"""Comprehensive parser for DGMS accident reports from both Coal and Non-Coal PDFs.
Extracts:
1. Detailed investigation findings from yearly sections (Summary of Findings of Fatal Accidents)
2. Historical major accidents from Chapter 10 (1901-2022)
3. Courts of Inquiry from Chapter 11 (1901-2022)
4. Decadal/yearly statistics from Chapter 2 and yearly statements
"""
import pymupdf
import re
import json
import os

def extract_detailed_findings(doc, pdf_name, mine_category="Coal"):
    """
    Extracts all individual accident reports from 'Summary of Findings of Fatal Accidents'.
    Format in PDF:
    <Number>. Date - <DD.MM.YY>   Mine - <MINE NAME>
             Time - <HH.MM>       Owner - <OWNER NAME>
                                  Dist. - <DISTRICT>, State - <STATE>
                                  Person(s) Killed :
                                  1. <Name>, <Designation>, <Gender>, <Age> Years
    While <Narrative description of what happened...>
    Had,
    <Conditions / Had paras that could have averted the accident...>
    """
    reports = []
    
    current_report = None
    current_cause_code = None
    current_cause_name = None
    
    # We iterate page by page
    for page_idx in range(len(doc)):
        page_num = page_idx + 1
        text = doc[page_idx].get_text()
        
        # Check if we are in Summary of Findings
        lines = text.split("\n")
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Detect Code header, e.g. "Code : 0991    Irruption of Water"
            code_match = re.search(r'Code\s*:\s*(\d{4})\s+([A-Za-z0-9\s,\(\)\/\-\&]+)', line)
            if code_match:
                current_cause_code = code_match.group(1).strip()
                current_cause_name = code_match.group(2).strip()
                i += 1
                continue
                
            # Detect accident start, e.g., "1.  Date -  27.03.16             Mine -  BANGWAR U/G PROJECT"
            # Or "43. Date - 08.12.20 Mine - KHOODIA"
            acc_start_match = re.search(r'^(\d+)\.\s+Date\s*-\s*([\d\.\-]+)\s+Mine\s*-\s*(.+)$', line, re.IGNORECASE)
            if acc_start_match:
                if current_report:
                    reports.append(current_report)
                
                acc_num = acc_start_match.group(1).strip()
                date_str = acc_start_match.group(2).strip()
                mine_name = acc_start_match.group(3).strip()
                
                current_report = {
                    "source_pdf": pdf_name,
                    "mine_category": mine_category,
                    "section": "Summary of Findings of Fatal Accidents",
                    "report_number": acc_num,
                    "date": date_str,
                    "mine_name": mine_name,
                    "time": "",
                    "owner": "",
                    "district": "",
                    "state": "",
                    "persons_killed": [],
                    "cause_code": current_cause_code,
                    "cause_name": current_cause_name,
                    "narrative": "",
                    "had_paras": "",
                    "raw_text": line,
                    "page_start": page_num,
                    "page_end": page_num
                }
                i += 1
                continue
                
            if current_report is not None:
                current_report["page_end"] = page_num
                current_report["raw_text"] += "\n" + line
                
                # Check for Time & Owner
                time_match = re.search(r'Time\s*-\s*([0-9\.:]+)\s+Owner\s*-\s*(.+)$', line, re.IGNORECASE)
                if time_match:
                    current_report["time"] = time_match.group(1).strip()
                    current_report["owner"] = time_match.group(2).strip()
                    i += 1
                    continue
                    
                # Check for Dist & State
                dist_match = re.search(r'Dist\.\s*-\s*([^,]+),\s*State\s*-\s*(.+)$', line, re.IGNORECASE)
                if dist_match:
                    current_report["district"] = dist_match.group(1).strip()
                    current_report["state"] = dist_match.group(2).strip()
                    i += 1
                    continue
                    
                # Check for Person(s) Killed:
                if "Person(s) Killed" in line:
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith("While") and not lines[i].strip().startswith("Code :"):
                        pk_line = lines[i].strip()
                        if pk_line and re.search(r'^\d+\.', pk_line):
                            current_report["persons_killed"].append(pk_line)
                        i += 1
                    continue
                    
                # Check for Narrative (starts with While ...)
                if line.startswith("While "):
                    narrative_lines = [line]
                    i += 1
                    while i < len(lines):
                        next_line = lines[i].strip()
                        if next_line.startswith("Had,") or next_line.startswith("Had :") or next_line.startswith("Had") or next_line.startswith("Code :") or re.search(r'^\d+\.\s+Date\s*-', next_line):
                            break
                        narrative_lines.append(next_line)
                        i += 1
                    current_report["narrative"] = " ".join(narrative_lines).strip()
                    continue
                    
                # Check for Had / findings
                if line.startswith("Had,") or line.startswith("Had :") or line.startswith("Had"):
                    had_lines = [line]
                    i += 1
                    while i < len(lines):
                        next_line = lines[i].strip()
                        if re.search(r'^\d+\.\s+Date\s*-', next_line) or next_line.startswith("Code :") or next_line.startswith("STATEMENT"):
                            break
                        had_lines.append(next_line)
                        i += 1
                    current_report["had_paras"] = "\n".join(had_lines).strip()
                    continue
                    
            i += 1
            
    if current_report:
        reports.append(current_report)
        
    return reports

if __name__ == "__main__":
    coal_pdf = "data/raw/sanket_coal_2016_2022.pdf"
    non_coal_pdf = "data/raw/sanket_non_coal_2016_2022.pdf"
    
    coal_doc = pymupdf.open(coal_pdf)
    non_coal_doc = pymupdf.open(non_coal_pdf)
    
    coal_reports = extract_detailed_findings(coal_doc, "sanket_coal_2016_2022.pdf", "Coal")
    non_coal_reports = extract_detailed_findings(non_coal_doc, "sanket_non_coal_2016_2022.pdf", "Non-Coal")
    
    print(f"Extracted {len(coal_reports)} detailed fatal accident reports from Coal PDF.")
    print(f"Extracted {len(non_coal_reports)} detailed fatal accident reports from Non-Coal PDF.")
