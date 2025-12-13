
from fetch_api import fetch_simple
from clean_data import basic_clean
from save_mysql import save_dataframe
from config import CLEAN_CSV
import pandas as pd

def run_all(save_to_db=False):
    print("1) Fetching raw data from USGS...")
    df_raw = fetch_simple()
    print("Raw data shape:", df_raw.shape)

    print("2) Cleaning data (basic)...")
    df_clean = basic_clean(df_raw)
    print("Cleaned data shape:", df_clean.shape)
    print("Saved cleaned CSV to", CLEAN_CSV)

    if save_to_db:
        print("3) Saving to MySQL...")
        # read cleaned to ensure consistent dtypes
        df_to_save = pd.read_csv(CLEAN_CSV)
        save_dataframe(df_to_save)
        print("Saved to MySQL")

if __name__ == "__main__":
    # Change to True if you want to push to MySQL
    run_all(save_to_db=False)
