# file: cli.py
import argparse
from datetime import date
from models import Taxpayer, AYContext
from parse_form16 import parse_form16
from compute import compute_tax_old_regime, compute_tax_new_regime
from build_json import build_itr_json
from summarize import summarize

def main():
    p = argparse.ArgumentParser(description="Generate ITR-1 JSON from Form 16")
    p.add_argument("--form16", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--pan", required=True)
    p.add_argument("--dob", required=True)      # YYYY-MM-DD
    p.add_argument("--address", required=True)
    p.add_argument("--mobile", required=True)
    p.add_argument("--email", required=True)
    p.add_argument("--ifsc", required=True)
    p.add_argument("--account", required=True)
    p.add_argument("--fy", default="2024-25")
    p.add_argument("--ay", default="2025-26")
    p.add_argument("--regime", choices=["old", "new"], default="old")
    p.add_argument("--out", default="itr1.json")
    args = p.parse_args()

    taxpayer = Taxpayer(
        name=args.name,
        pan=args.pan,
        dob=date.fromisoformat(args.dob),
        address=args.address,
        mobile=args.mobile,
        email=args.email,
        bank_ifsc=args.ifsc,
        bank_account=args.account,
    )

    ctx = AYContext(fy=args.fy, ay=args.ay, regime=args.regime)

    # Parse Form16 PDF
    f16 = parse_form16(args.form16)

    # Compute tax based on regime
    if args.regime == "old":
        comp = compute_tax_old_regime(f16)
    else:
        comp = compute_tax_new_regime(f16)

    # Build and save ITR JSON
    build_itr_json(taxpayer, ctx, f16, comp, args.form16, args.out)
    
    print(summarize(f16, comp))

    print("ITR-1 JSON generated successfully:", args.out)

if __name__ == "__main__":
    main()

