"""
clean_csv.py - tidy up a messy CSV export.

Fixes inconsistent text, mixed date formats, currency symbols and
duplicate rows, then saves a clean copy and prints a summary.

Assumptions:
  - Dates are UK day-first (01/09/2026 means 1 September).
  - Amounts are in a single currency.
"""
import pandas as pd
from datetime import datetime
import argparse

DATE_FORMATS = [
    # Date formats we expect to see, tried in order. If a client's file has a
    # new format, add it here.
    "%Y-%m-%d",   # 2026-09-01
    "%Y/%m/%d",   # 2026/09/06
    "%d/%m/%Y",   # 01/09/2026   (UK: day first)
    "%d-%m-%Y",   # 05-09-2026
    "%b %d, %Y",  # Sep 3, 2026
    "%d %b %Y",   # 7 Sep 2026
]

def parse_args():
    #Read the input and output file names from the command line.
    parser = argparse.ArgumentParser(description="Clean a messy CSV file.")
    parser.add_argument("input_file", help="the messy CSV to clean")
    parser.add_argument("output_file", help="where to save the cleaned CSV")
    return parser.parse_args()

def load(path):
     # Read the CSV file into a pandas DataFrame.
    return pd.read_csv(path)

def clean_text(df):
    # Standardise names, cities and emails.
    for col in ["customer_name", "city"]:
        df[col] = (
            df[col]
            .str.strip()                            # remove edge white space
            .str.replace(r"\s+", " ", regex=True)   # collaspe repeated spaces
            .str.title()                            # bOB sMITH" -> "Bob Smith"
        )
    # Emails are case-insensitive, so lowercase them for consistency
    df["email"] = df["email"].str.strip().str.lower()
    return df

def parse_date(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue # wrong format, try the next one
    return None    # Better to leave a blank than to guess a date we can't trust


def clean_dates(df):
    # convert order_date to one format (YYYY-MM-DD)
    df["order_date"] = df["order_date"].apply(parse_date)
    return df


def clean_amount(df):
    # remove the £ sign and convert to a number
    df["amount"] = (
        df["amount"]
        .astype(str)                                   # make everything text first
        .str.replace(r"[^\d.\-]", "", regex=True)      # keep only digits, dots, minus signs
    )
    # errors="coerce" turns unreadable values into NaN rather than crashing,
    # so missing amounts stay flagged instead of being invented
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").round(2)
    return df


def remove_duplicates(df):
    #Drop exact duplicate rows.
    #Must run after clean_text and clean_amount, so rows that differed only
    #in spacing, case or formatting are recognised as duplicates.

    df=df.drop_duplicates()
    return df

def print_summary(line_in, line_out, df):
    # Print how many rows were processed and what is still missing.
    print("Summary:")
    print(f"Lines in: {line_in}")
    print(f"Lines out: {line_out}")
    print(f"Duplicates removed: {line_in - line_out}")
    # Blanks are reported, not filled, so the client knows what data is missing
    print(f"Blank emails: {df["email"].isna().sum()}")
    print(f"Blank amount: {df["amount"].isna().sum()}")
    print(f"Blank date: {df["order_date"].isna().sum()}")


def main():
    args = parse_args()
    df = load(args.input_file)
    line_in = len(df) # count before cleaning, to report duplicates later
    # Order matters: text and amounts first, so duplicates are caught properly
    df = clean_text(df)
    df = clean_amount(df)
    df = remove_duplicates(df)
    df = clean_dates(df)
    line_out = len(df)
    df.to_csv(args.output_file, index=False) # index=False: no row-number column
    print_summary(line_in, line_out, df)
    
# Only run main() when the file is run directly, not when imported
if __name__ == "__main__":
    main() 