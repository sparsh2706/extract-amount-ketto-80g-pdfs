import pdfplumber, re, csv, os

# Tweak patterns as needed for your PDFs
PATTERNS = [
    r"Amount\s*\(.*?\)\s*:\s*₹?\s*([0-9][0-9,]*)\s*\/?-?",  # e.g., Amount (In Rs.) : 100/-
    r"Amount\s*:\s*₹?\s*([0-9][0-9,]*)\s*\/?-?",
    r"Rs\.?\s*([0-9][0-9,]*)\s*\/?-?",
    r"₹\s*([0-9][0-9,]*)\s*\/?-?",
]

def find_amount(text: str):
    # Normalize common oddities
    t = text.replace('\xa0', ' ').replace('In Rs.', 'in Rs.')
    for pat in PATTERNS:
        m = re.search(pat, t, flags=re.IGNORECASE)
        if m:
            amt = m.group(1).replace(',', '')
            return amt
    return None

def extract_amount_from_pdf(path: str):
    try:
        with pdfplumber.open(path) as pdf:
            full_text = []
            for page in pdf.pages:
                full_text.append(page.extract_text() or "")
            text = "\n".join(full_text)
        return find_amount(text)
    except Exception as e:
        return None

def main(folder="."):
    rows = [("file", "amount")]
    for fname in os.listdir(folder):
        if fname.lower().endswith(".pdf"):
            fpath = os.path.join(folder, fname)
            amt = extract_amount_from_pdf(fpath)
            rows.append((fname, amt or "NOT_FOUND"))
    with open("amounts.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    print("Wrote amounts.csv")

if __name__ == "__main__":
    main("Documents")  # or pass a folder path
