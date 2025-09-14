ITR from Form16
This project generates Income Tax Return (ITR) JSON files (ITR-1 for AY 2025-26) by parsing Form 16 PDFs and computing tax liability under both old and new Indian tax regimes (FY 2024-25).

Features
Parses Form 16 PDF to extract salary details, deductions, and TDS data

Computes tax liability supporting:

Old regime tax slabs (with exemptions and deductions)

New regime tax slabs with updated FY 24-25 slab rates

Generates JSON output suitable for digital filing or further processing

Maintains audit logs with input/output file hash verification

Modular structure with separate parsing, calculation, and JSON building modules

Technologies Used
Python 3.10+

pdfplumber for PDF text extraction

dataclasses for clean data models

Standard libraries: argparse, json, hashlib, etc.

Project Structure
text
perplexity/
├── cli.py                # CLI entry point for running the tool
├── compute.py            # Tax computation logic, old & new regimes
├── parse_form16.py       # Logic for parsing Form 16 PDFs
├── build_json.py         # Converts computed data to ITR JSON format
├── models.py             # Data classes for structured data handling
├── form16.pdf            # Sample Form 16 for testing (not checked in)
└── README.md             # This documentation file
Installation
Clone the repository:

bash
git clone <repo-url>
cd perplexity
(Optional) Create and activate a Python virtual environment:

bash
python3 -m venv .venv
source .venv/bin/activate
Install required packages:

bash
pip install -r requirements.txt
(If requirements.txt is not provided, manually install pdfplumber)

Usage
Run the CLI with required arguments:

bash
python cli.py --form16 form16.pdf \
              --name "Full Name" \
              --pan "ABCDE1234F" \
              --dob 1980-01-01 \
              --address "City, State" \
              --mobile "9999999999" \
              --email "email@example.com" \
              --ifsc "HDFC0000001" \
              --account "123456789012" \
              --regime new \
              --out itr1.json
Arguments
Argument	Description	Required	Default
--form16	Path to input Form 16 PDF	Yes	—
--name	Taxpayer full name	Yes	—
--pan	Taxpayer PAN	Yes	—
--dob	Date of birth (YYYY-MM-DD)	Yes	—
--address	Residential address	Yes	—
--mobile	Mobile phone number	Yes	—
--email	Email address	Yes	—
--ifsc	Bank IFSC code	Yes	—
--account	Bank account number	Yes	—
--fy	Financial year	No	2024-25
--ay	Assessment year	No	2025-26
--regime	Tax regime (old	new)	No
--out	Output JSON filename	No	itr1.json
How It Works
Parsing:
Uses pdfplumber to extract text from the Form 16 PDF and regex to parse salary, deductions, and TDS details into structured Form16Data.

Computation:
Applies appropriate tax slab rates based on the selected regime.
Correctly applies standard deductions and other claimable deductions.
Calculates tax before cess, rebate, cess, and net tax payable after accounting for TDS.

Output:
Builds a clean JSON structure conforming to simplified ITR-1 schema with all relevant taxpayer and income details.
Writes JSON to specified output file and logs file hash for audit trail.

Notes & Limitations
Current TDS extraction is basic; may need improvement for complex Form 16s with multiple heads of income.

Only supports ITR-1 form (individuals with salary income).

New tax regime slabs are hardcoded for FY 2024-25; update slabs each year as required.

No GUI; intended for CLI/script use.

Assumes well-formed and readable Form 16 PDFs.

Contributing
Contributions are welcome! Please fork the repo and submit PRs for bug fixes, improvements, or feature additions.
