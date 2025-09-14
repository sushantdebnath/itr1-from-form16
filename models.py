from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Taxpayer:
    name: str
    pan: str
    dob: str
    address: str
    mobile: str
    email: str
    bank_ifsc: str
    bank_account: str

@dataclass
class AYContext:
    fy: str
    ay: str
    regime: str

@dataclass
class SalaryBreakup:
    gross_salary: int
    exempt_allowances: int
    standard_deduction: int
    professional_tax: int
    perquisites: int

@dataclass
class DeductionBreakup:
    sec80C: int = 0
    sec80D: int = 0
    sec80CCD1B: int = 0
    sec80TTA: int = 0
    others: int = 0

@dataclass
class TDSItem:
    tan: str
    employer_name: str
    tds_amount: int

@dataclass
class Form16Data:
    employer_tan: str
    employer_name: str
    salary: SalaryBreakup
    deductions: DeductionBreakup
    tds_list: List[TDSItem]
    total_tds: int

@dataclass
class ComputedTax:
    total_income: int
    deductions_total: int
    taxable_income: int
    tax_before_cess: int
    cess: int
    rebate_87A: int
    total_tax_liability: int
    net_tax_payable: int

@dataclass
class ITRPayload:
    version: str = "1.0"
    schema_version: str = "ITR-1"
    ay: str = ""
    taxpayer: Optional[Taxpayer] = None
    context: Optional[AYContext] = None
    income: Optional[dict] = None
    deductions: Optional[dict] = None
    computed: Optional[dict] = None
    tds: Optional[List[dict]] = None

