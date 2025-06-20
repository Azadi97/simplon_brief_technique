# fetcher/data_fetcher.py

import pandas as pd
from pathlib import Path

# URLs of the datasets (replace with actual URLs)
urls = {
    "produits": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv",
    "magasins": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv",
    "ventes": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"
}

# Save location
DATA_DIR = Path("/mnt/c/Users/A.S.A/Desktop/sales_analysis/script_runner/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def normalize_headers(columns):
    """Lowercase headers and replace spaces with underscores."""
    return [col.strip().lower().replace(" ", "_") for col in columns]

for name, url in urls.items():
    try:
        print(f"⬇️ Downloading {name} from {url}")
        df = pd.read_csv(url)

        # Standardize headers
        df.columns = normalize_headers(df.columns)

        output_path = DATA_DIR / f"{name}.csv"
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"✅ Saved cleaned file: {output_path}")
    except Exception as e:
        print(f"❌ Failed to process {name}: {e}")