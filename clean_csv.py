import pandas as pd

def load(path):
    return pd.read_csv(path)


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
    # TODO: convert order_date to one format (YYYY-MM-DD)
    return df


def clean_amount(df):
    # TODO: remove the £ sign and convert to a number
    return df


def remove_duplicates(df):
    # TODO: drop exact duplicate rows
    return df


def main():
    df = load("orders_messy.csv")
    df = clean_text(df)
    print(df)  # temporary: lets you see each change as you build


if __name__ == "__main__":
    main()