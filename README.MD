# CSV Cleaner

A command-line tool that cleans messy CSV exports: it fixes inconsistent text, mixed date formats, currency symbols and duplicate rows, and tells you what data is still missing.

## The problem

For business owners, working with messy CSV exports is not just very taxing on time but has the risk to add errors to the data. Clean data allows easy and efficient use in other programs.

## What it fixes

- Extra spaces and inconsistent capitalisation in names and cities
- Emails converted to lowercase
- Dates in six different formats converted to `YYYY-MM-DD`
- Currency symbols removed so amounts become real numbers
- Duplicate rows removed
- Missing values reported (not invented)

## Before and after

Before (`orders_messy.csv`):

| order_id | customer_name | email | order_date | amount | city |
|---|---|---|---|---|---|
| 1001 | `  alice johnson ` | `ALICE@EXAMPLE.COM` | 2026-09-01 | 25.50 | london |
| 1003 | `carol   white` | carol@example.com | Sep 3, 2026 | £15.00 | `  LEEDS` |

After (`orders_clean.csv`):

| order_id | customer_name | email | order_date | amount | city |
|---|---|---|---|---|---|
| 1001 | Alice Johnson | alice@example.com | 2026-09-01 | 25.5 | London |
| 1003 | Carol White | carol@example.com | 2026-09-03 | 15.0 | Leeds |

## How to run it

Requires Python 3.

```bash
git clone git@github.com:playfu1-doubt/csv-cleaner.git
cd csv-cleaner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python clean_csv.py sample_data/orders_messy.csv sample_data/orders_clean.csv
```
#### The original file is never changed, the clean data is written to a new file

Example output:

```
Summary:
Rows in: 8
Rows out: 7
Duplicates removed: 1
Blank email: 1
Blank amount: 1
Blank order_date: 0
```

## Assumptions and limitations

- Dates are read as UK day-first (`01/09/2026` is 1 September).
- All amounts are assumed to be in one currency.
- Date columns are found by name (`date`, `joined`). Add keywords to
  `DATE_KEYWORDS` in the script for other names.
- Missing values are flagged in the summary, never filled in.
- Only CSV files are supported.

## Project structure

```
csv-cleaner/
├── clean_csv.py          # the script: loads, cleans, summarises, saves
├── requirements.txt      # Python packages needed (pandas)
├── README.md             # this file
├── .gitignore            # keeps the virtual environment and test output out of Git
└── sample_data/
    ├── orders_messy.csv      # example input: customer orders
    ├── orders_clean.csv      # the cleaned result
    ├── contacts_messy.csv    # example input with different columns
    └── contacts_clean.csv    # the cleaned result
```

## What I learned

**Hardest part:** making the cleaner work on a second file with different columns. My first version only worked on the orders file because column names like `customer_name`, `amount` and `order_date` were written directly into the code. When I ran it on a contacts file, it crashed with a `KeyError`.

**What went wrong and how I fixed it:** I read the traceback from the bottom up. It named the missing column (`customer_name`) and the function it happened in (`clean_text`). I fixed it by having each cleaning function check which columns exist in the file before touching them. Fixing one function just moved the error to the next one, so I worked through them one at a time until both files ran cleanly.

**Other things I learned:** working with files in Python using pandas, building a command-line tool with `argparse`, writing helpful error messages, and using Git from the terminal (`add`, `commit`, `push`, `mv`) to build up a clear commit history.

**What I'd add next:** a price tracker that scrapes a product page and logs price changes, to practise working with live web data instead of files.