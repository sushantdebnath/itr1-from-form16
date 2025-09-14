# file: summarize.py
def summarize(f16, comp):
    return "\n".join([
        f"Employer: {f16.employer_name} ({f16.employer_tan})",
        f"Gross salary: {f16.salary.gross_salary}",
        f"Deductions total: {comp.deductions_total}",
        f"Taxable income: {comp.taxable_income}",
        f"TDS total: {f16.total_tds} | Net tax payable: {comp.net_tax_payable}",
    ])

