import csv, os

# 👇 change these paths
CSV_PATH = "amounts.csv"
PDF_DIR = "Documents"

total_amount = 0
rows = 0

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)  # skip header
    for row in reader:
        if len(row) < 2:
            continue
        rows += 1
        try:
            amt = int(row[1].replace(",", "").replace("₹", "").replace("Rs.", "").strip("/- "))
            total_amount += amt
        except ValueError:
            pass

pdf_count = len([f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")])

print(f"Total amount: {total_amount}")
print(f"Number of entries in CSV: {rows}")
print(f"Number of PDFs in folder: {pdf_count}")
print("Match?" , "YES ✅" if rows == pdf_count else "NO ❌")
