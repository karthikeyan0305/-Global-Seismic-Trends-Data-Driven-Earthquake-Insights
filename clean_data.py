import pandas as pd
import numpy as np
from config import RAW_CSV, CLEAN_CSV

def basic_clean(df=None):
    if df is None:
        df = pd.read_csv(RAW_CSV)

    # Convert timestamps
    df["time"] = pd.to_datetime(df["time"], unit="ms", errors="coerce")
    df["updated"] = pd.to_datetime(df["updated"], unit="ms", errors="coerce")

    #  Numeric columns to clean
    numeric_cols = [
        "mag", "tsunami", "sig", "nst", "dmin", "rms", "gap",
        "magError", "depthError", "magNst", "felt", "cdi", "mmi",
        "latitude", "longitude", "depth_km"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    #  Fill numeric missing values
    for col in numeric_cols:
        if col in df.columns:
            median = df[col].median(skipna=True)
            median = 0 if np.isnan(median) else median
            df[col] = df[col].fillna(median)

    # String columns → fill with "unknown"
    string_cols = [
        "place", "type", "status", "magType", "alert",
        "locationSource", "magSource", "types", "title", "sources", "ids", "net"
    ]

    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].fillna("unknown")

    # Derived columns
    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month

    df["depth_category"] = df["depth_km"].apply(
        lambda d: "unknown" if pd.isna(d)
        else "shallow" if d < 50
        else "intermediate" if d <= 300
        else "deep"
    )

    df.to_csv(CLEAN_CSV, index=False)
    return df
