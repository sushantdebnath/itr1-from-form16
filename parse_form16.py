import re
import pdfplumber
from models import Form16Data, SalaryBreakup, DeductionBreakup, TDSItem

def safe_extract_int(value) -> int:
    try:
        if isinstance(value, (int, float)):
            return int(round(value))
        if isinstance(value, str):
            cleaned = value.replace(",", "").strip()
            return int(round(float(cleaned)))
    except Exception:
        pass
    return 0

def extract_amount_from_line(line: str) -> int:
    matches = re.findall(r'([0-9,]+\.\d{1,2}|[0-9,]+)', line)
    if matches:
        val = matches[-1].replace(",", "")
        return safe_extract_int(val)
    return 0

def parse_form16(pdf_path: str) -> Form16Data:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += "\n" + (page.extract_text() or "")

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Parse TAN
    tan_match = re.search(r"TAN\s+of\s+Employer[:\-]?\s*([A-Z0-9]{10})", text)
    tan = tan_match.group(1) if tan_match else "UNKNOWN"

    # Employer Name
    employer_name = "Employer"
    for i, line in enumerate(lines):
        if "Name and address of the Employer" in line:
            for j in range(i + 1, len(lines)):
                if lines[j] and not lines[j].isdigit():
                    employer_name = lines[j]
                    break
            break

    # Extract amounts from numbered and subitems - example for gross salary and deductions
    def extract_section_lines(section_num):
        start_idx = None
        for idx, line in enumerate(lines):
            if line.startswith(f"{section_num}."):
                start_idx = idx
                break
        if start_idx is None:
            return []
        end_idx = len(lines)
        for idx in range(start_idx + 1, len(lines)):
            if re.match(r"^\d+\.", lines[idx]):
                end_idx = idx
                break
        return lines[start_idx:end_idx]

    section1_lines = extract_section_lines(1)
    def extract_subitem(lines, letter):
        pattern = re.compile(rf"^\({letter}\)\s*(.*)")
        for line in lines:
            m = pattern.match(line)
            if m:
                return extract_amount_from_line(line)
        return 0

    gross_salary = extract_subitem(section1_lines, 'd')
    if gross_salary == 0:
        gross_salary = sum([
            extract_subitem(section1_lines, 'a'),
            extract_subitem(section1_lines, 'b'),
            extract_subitem(section1_lines, 'c')
        ])

    section4_lines = extract_section_lines(4)
    standard_deduction = extract_subitem(section4_lines, 'a')
    professional_tax = extract_subitem(section4_lines, 'c')
    perquisites = extract_subitem(section1_lines, 'b')  # for reporting

    salary = SalaryBreakup(
        gross_salary=gross_salary,
        exempt_allowances=0,
        standard_deduction=standard_deduction,
        professional_tax=professional_tax,
        perquisites=perquisites,
    )
    deductions = DeductionBreakup()

    tds_list = [TDSItem(tan=tan, employer_name=employer_name, tds_amount=0)]
    total_tds = 0

    return Form16Data(
        employer_tan=tan,
        employer_name=employer_name,
        salary=salary,
        deductions=deductions,
        tds_list=tds_list,
        total_tds=total_tds,
    )

