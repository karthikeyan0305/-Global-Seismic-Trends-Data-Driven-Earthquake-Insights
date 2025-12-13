import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import USGS_URL, STARTTIME, ENDTIME, MIN_MAGNITUDE, RAW_CSV

def fetch_simple():
    start = datetime.strptime(STARTTIME, "%Y-%m-%d")
    end = datetime.strptime(ENDTIME, "%Y-%m-%d")

    all_records = []

    print("\nFetching monthly earthquake data...\n")

    while start <= end:
        month_start = start.strftime("%Y-%m-%d")
        month_end = (start + relativedelta(months=1) - relativedelta(days=1)).strftime("%Y-%m-%d")

        print(f"Fetching {month_start} to {month_end} ...")

        params = {
            "format": "geojson",
            "starttime": month_start,
            "endtime": month_end,
            "minmagnitude": MIN_MAGNITUDE
        }

        resp = requests.get(USGS_URL, params=params)

        if resp.status_code != 200:
            print(f"❌ Failed for {month_start}: {resp.status_code}")
            start += relativedelta(months=1)
            continue

        data = resp.json()

        for feature in data.get("features", []):
            props = feature["properties"]
            geom = feature["geometry"]

            all_records.append({
                "id": feature["id"],
                "time": props.get("time"),
                "updated": props.get("updated"),
                "mag": props.get("mag"),
                "magType": props.get("magType"),
                "place": props.get("place"),
                "type": props.get("type"),
                "status": props.get("status"),
                "tsunami": props.get("tsunami"),
                "sig": props.get("sig"),
                "net": props.get("net"),
                "nst": props.get("nst"),
                "dmin": props.get("dmin"),
                "rms": props.get("rms"),
                "gap": props.get("gap"),
                "magError": props.get("magError"),
                "depthError": props.get("depthError"),
                "magNst": props.get("magNst"),
                "locationSource": props.get("locationSource"),
                "magSource": props.get("magSource"),
                "types": props.get("types"),
                "ids": props.get("ids"),
                "sources": props.get("sources"),
                "latitude": geom["coordinates"][1] if geom else None,
                "longitude": geom["coordinates"][0] if geom else None,
                "depth_km": geom["coordinates"][2] if geom else None
            })

        start += relativedelta(months=1)

    df = pd.DataFrame(all_records)
    df.to_csv(RAW_CSV, index=False)

    print(f"\n🎉 Completed fetching. Total rows = {df.shape[0]}")
    return df
