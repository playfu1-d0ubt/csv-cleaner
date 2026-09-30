import pandas as pd
from datetime import datetime

DATE_FORMATS = [
    "%Y-%m-%d",   # 2026-09-01
    "%Y/%m/%d",   # 2026/09/06
    "%d/%m/%Y",   # 01/09/2026   (UK: day first)
    "%d-%m-%Y",   # 05-09-2026
    "%b %d, %Y",  # Sep 3, 2026
    "%d %b %Y",   # 7 Sep 2026
]

def load(path):
    return pd.read_csv(path)

def parse_date(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None   # no format matched


def clean_text(df):
    # strip spaces, collapse repeated spaces,
    # title-case customer_name and city, lowercase email
    for col in ["customer_name", "city"]:
        df[col] = (
            df[col]
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.title()
        )
    df["email"] = df["email"].str.strip().str.lower()
    return df


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
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").round(2)
    return df


def remove_duplicates(df):
    # drop exact duplicate rows
    df=df.drop_duplicates()
    return df


def main():
    df = load("orders_messy.csv")
    df = clean_text(df) 
    df = clean_amount(df)
    df = remove_duplicates(df)
    df = clean_dates(df)
    print(df)  # temporary: lets you see each change as you build


if __name__ == "__main__":
    main()