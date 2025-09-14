from models import Form16Data, ComputedTax

def slab_tax_old(amount: int) -> int:
    tax = 0
    slabs = [
        (250000, 0.0),
        (250000, 0.05),
        (500000, 0.20),
        (float("inf"), 0.30),
    ]
    remaining = amount
    for band, rate in slabs:
        chunk = min(remaining, band)
        tax += int(chunk * rate)
        remaining -= chunk
        if remaining <= 0:
            break
    return tax

#def slab_tax_new(amount: int) -> int:
#    tax = 0
#    slabs = [
#        (300000, 0.00),
#        (300000, 0.05),
#        (300000, 0.10),
#        (300000, 0.15),
#        (300000, 0.20),
#        (float("inf"), 0.30),
#    ]
#    remaining = amount
#    for band, rate in slabs:
#        chunk = min(remaining, band)
#        tax += int(chunk * rate)
#        remaining -= chunk
#        if remaining <= 0:
#            break
#    return tax

def slab_tax_new(amount: int) -> int:
    if amount <= 300000:
        return 0
    elif amount <= 600000:
        return int((amount - 300000) * 0.05)
    elif amount <= 700000:
        return int((amount - 300000) * 0.05)  # same rate continues (5%)
    elif amount <= 1000000:
        return 20000 + int((amount - 700000) * 0.10)
    elif amount <= 1200000:
        return 50000 + int((amount - 1000000) * 0.15)
    elif amount <= 1500000:
        return 80000 + int((amount - 1200000) * 0.20)
    else:
        return 140000 + int((amount - 1500000) * 0.30)


# --- Final old regime tax computation ---

def compute_tax_old_regime(f16: Form16Data) -> ComputedTax:
    taxable_salary = max(
        0,
        f16.salary.gross_salary
        - f16.salary.exempt_allowances
        - f16.salary.standard_deduction
        - f16.salary.professional_tax,
    )
    deductions_total = (
        f16.deductions.sec80C
        + f16.deductions.sec80D
        + f16.deductions.sec80CCD1B
        + f16.deductions.sec80TTA
        + f16.deductions.others
    )
    taxable_income = max(0, taxable_salary - deductions_total)
    tax_before_cess = slab_tax_old(taxable_income)
    rebate = min(tax_before_cess, 12500) if taxable_income <= 500000 else 0
    tax_after_rebate = max(0, tax_before_cess - rebate)
    cess = int(round(tax_after_rebate * 0.04))
    total_tax = tax_after_rebate + cess
    net_tax = max(0, total_tax - f16.total_tds)
    return ComputedTax(
        total_income=taxable_salary,
        deductions_total=deductions_total,
        taxable_income=taxable_income,
        tax_before_cess=tax_before_cess,
        cess=cess,
        rebate_87A=rebate,
        total_tax_liability=total_tax,
        net_tax_payable=net_tax,
    )

# --- Updated new regime tax computation including standard deduction of 75,000 ---

def compute_tax_new_regime(f16: Form16Data) -> ComputedTax:
    standard_deduction = 75000

    taxable_salary = max(0, f16.salary.gross_salary - f16.salary.professional_tax)
    taxable_income = max(0, taxable_salary - standard_deduction)  # Subtract deduction here

    tax_before_cess = slab_tax_new(taxable_income)
    rebate = 0  # Not applicable if taxable income > 5L
    cess = int(round(tax_before_cess * 0.04))
    total_tax = tax_before_cess + cess

    net_tax = max(0, total_tax - f16.total_tds)

    return ComputedTax(
        total_income=taxable_salary,
        deductions_total=standard_deduction,
        taxable_income=taxable_income,
        tax_before_cess=tax_before_cess,
        cess=cess,
        rebate_87A=rebate,
        total_tax_liability=total_tax,
        net_tax_payable=net_tax,
    )


# Example usage in CLI or main processing code:

# if regime == "old":
#     computed = compute_tax_old_regime(form16_data)
# else:
#     computed = compute_tax_new_regime(form16_data)


