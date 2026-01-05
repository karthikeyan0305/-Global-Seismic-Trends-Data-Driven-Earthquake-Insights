# queries_app.py
import streamlit as st
import pandas as pd
import numpy as np



# ---------- CONFIG ----------
CLEAN_CSV = "../data/earthquakes_clean.csv"  # path to cleaned CSV

st.set_page_config(layout="wide", page_title="Earthquake Analyst Queries")

@st.cache_data
def load_data(path=CLEAN_CSV):
    df = pd.read_csv(path, parse_dates=["time", "updated"], low_memory=False)
    # Ensure numeric types
    for col in ["mag", "depth_km", "latitude", "longitude", "nst", "rms", "gap", "tsunami", "sig"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # safe columns
    if "country" not in df.columns:
        # try extract country from place
        if "place" in df.columns:
            df["country"] = df["place"].str.extract(r",\s*([^,]+)$", expand=False).fillna("unknown")
        else:
            df["country"] = "unknown"
    # derived
    if "year" not in df.columns:
        df["year"] = df["time"].dt.year
    if "month" not in df.columns:
        df["month"] = df["time"].dt.month
    if "depth_category" not in df.columns and "depth_km" in df.columns:
        df["depth_category"] = df["depth_km"].apply(
            lambda d: "unknown" if pd.isna(d) else ("shallow" if d < 50 else ("intermediate" if d <= 300 else "deep"))
        )
    return df

df = load_data()

st.title("Analyst Tasks – Select a Query")
st.markdown("Choose any task from the dropdown. Results are computed from the cleaned CSV (Pandas).")

TASKS = [
    "Q1 Top 10 strongest earthquakes (mag)",
    "Q2 Top 10 deepest earthquakes (depth_km)",
    "Q3 Shallow <50 km & mag > 7.5",
    "Q4 Average depth per continent (needs mapping)",
    "Q5 Average magnitude per magType",
    "Q6 Year with most earthquakes",
    "Q7 Month with highest number of earthquakes",
    "Q8 Day of week with most earthquakes",
    "Q9 Count of earthquakes per hour of day",
    "Q10 Most active reporting network (net)",
    "Q11 Top 5 places with highest casualties",
    "Q12 Total estimated economic loss per continent (needs mapping)",
    "Q13 Average economic loss by alert level",
    "Q14 Count of reviewed vs automatic earthquakes (status)",
    "Q15 Count by earthquake type (type)",
    "Q16 Number of earthquakes by data type (types)",
    "Q17 Average RMS and gap per continent (needs mapping)",
    "Q18 Events with high station coverage (nst > 100)",
    "Q19 Number of tsunamis triggered per year",
    "Q20 Count earthquakes by alert levels",
    "Q21 Top 5 countries with highest average magnitude (past 10 years)",
    "Q22 Countries with both shallow and deep quakes in same month",
    "Q23 Year-over-year growth rate in total earthquakes",
    "Q24 3 most seismically active regions (freq * avg_mag)",
    "Q25 Avg depth per country within ±5° latitude",
    "Q26 Countries highest ratio shallow:deep",
    "Q27 Avg magnitude difference tsunami vs no-tsunami",
    "Q28 Events with lowest data reliability (rms+gap)",
    "Q29 Pairs of consecutive quakes within 50 km & 1 hour (limited)",
    "Q30 Regions with highest frequency of deep-focus quakes (>300 km)"
]

choice = st.selectbox("Select an analyst task", TASKS)

# helper functions
def show_df(df_out):
    st.dataframe(df_out)
    st.download_button("Download CSV", df_out.to_csv(index=False).encode("utf-8"), file_name="query_result.csv")

def haversine_km(lat1, lon1, lat2, lon2):
    # vectorized haversine (inputs in degrees)
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

st.markdown("### Result")
# perform selected task
if choice.startswith("Q1"):
    out = df[["id","time","place","country","mag","depth_km"]].sort_values("mag", ascending=False).head(10)
    show_df(out)

elif choice.startswith("Q2"):
    out = df[["id","time","place","country","mag","depth_km"]].sort_values("depth_km", ascending=False).head(10)
    show_df(out)

elif choice.startswith("Q3"):
    out = df[(df["depth_km"] < 50) & (df["mag"] > 7.5)][["id","time","place","country","mag","depth_km"]].sort_values("mag", ascending=False)
    show_df(out)

elif choice.startswith("Q4"):
    st.info("Q4 needs a country->continent mapping table. If you don't have one, results will show grouped by country instead.")
    if "country" in df.columns:
        out = df.groupby("country", dropna=True)["depth_km"].mean().reset_index().rename(columns={"depth_km":"avg_depth_km"}).sort_values("avg_depth_km", ascending=False)
        st.write("Showing average depth per country (use country_continent mapping for continents):")
        show_df(out)
    else:
        st.warning("No country column present.")

elif choice.startswith("Q5"):
    if "magType" in df.columns:
        out = df.groupby("magType")["mag"].agg(["count","mean"]).reset_index().rename(columns={"mean":"avg_mag","count":"cnt"}).sort_values("avg_mag", ascending=False)
        show_df(out)
    else:
        st.warning("magType column not found.")

elif choice.startswith("Q6"):
    out = df.groupby(df["time"].dt.year)["id"].count().reset_index().rename(columns={"time":"year","id":"quake_count"}).sort_values("quake_count", ascending=False).head(1)
    show_df(out)

elif choice.startswith("Q7"):
    out = df.groupby(df["time"].dt.month)["id"].count().reset_index().rename(columns={"time":"month","id":"quake_count"}).sort_values("quake_count", ascending=False).head(1)
    show_df(out)

elif choice.startswith("Q8"):
    out = df.groupby(df["time"].dt.day_name())["id"].count().reset_index().rename(columns={"time":"day","id":"quake_count"}).sort_values("quake_count", ascending=False)
    show_df(out)

elif choice.startswith("Q9"):
    out = df.groupby(df["time"].dt.hour)["id"].count().reset_index().rename(columns={"time":"hour","id":"quake_count"}).sort_values("hour")
    show_df(out)

elif choice.startswith("Q10"):
    if "net" in df.columns:
        out = df["net"].value_counts().reset_index().rename(columns={"index":"net","net":"count"}).head(10)
        show_df(out)
    else:
        st.warning("net column not found.")

elif choice.startswith("Q11"):
    if "casualties" in df.columns:
        out = df.groupby(["place","country"])["casualties"].sum().reset_index().sort_values("casualties", ascending=False).head(5)
        show_df(out)
    else:
        st.warning("casualties column not present in dataset.")

elif choice.startswith("Q12"):
    st.info("Q12 needs country->continent mapping. Showing sum by country as fallback.")
    if "economic_loss" in df.columns:
        out = df.groupby("country")["economic_loss"].sum().reset_index().sort_values("economic_loss", ascending=False).head(20)
        show_df(out)
    else:
        st.warning("economic_loss column not present.")

elif choice.startswith("Q13"):
    if "alert" in df.columns and "economic_loss" in df.columns:
        out = df.groupby("alert")["economic_loss"].agg(["mean","count"]).reset_index().sort_values("mean", ascending=False)
        show_df(out)
    else:
        st.warning("alert or economic_loss column missing.")

elif choice.startswith("Q14"):
    if "status" in df.columns:
        out = df["status"].value_counts().reset_index().rename(columns={"index":"status","status":"count"})
        show_df(out)
    else:
        st.warning("status column missing.")

elif choice.startswith("Q15"):
    if "type" in df.columns:
        out = df["type"].value_counts().reset_index().rename(columns={"index":"type","type":"count"})
        show_df(out)
    else:
        st.warning("type column missing.")

elif choice.startswith("Q16"):
    if "types" in df.columns:
        # show counts for few common tokens
        tokens = ["shakemap","dyfi","origin","phase-data","finite-fault"]
        data = {}
        for t in tokens:
            data[t] = df["types"].str.contains(t, na=False).sum()
        out = pd.DataFrame(list(data.items()), columns=["type_token","count"]).sort_values("count", ascending=False)
        show_df(out)
    else:
        st.warning("types column missing.")

elif choice.startswith("Q17"):
    st.info("Q17 needs country->continent mapping. Showing avg RMS/gap by country as fallback.")
    if "rms" in df.columns and "country" in df.columns:
        out = df.groupby("country")[["rms","gap"]].mean().reset_index().sort_values("rms", ascending=False)
        show_df(out)
    else:
        st.warning("rms or country column missing.")

elif choice.startswith("Q18"):
    if "nst" in df.columns:
        threshold = st.sidebar.number_input("nst threshold", value=100, step=10)
        out = df[df["nst"] > threshold].sort_values("nst", ascending=False)[["id","time","place","country","nst"]]
        show_df(out)
    else:
        st.warning("nst column missing.")

elif choice.startswith("Q19"):
    if "tsunami" in df.columns:
        out = df.groupby(df["time"].dt.year)["tsunami"].sum().reset_index().rename(columns={"time":"year","tsunami":"tsunami_events"})
        show_df(out)
    else:
        st.warning("tsunami column missing.")

elif choice.startswith("Q20"):
    if "alert" in df.columns:
        out = df["alert"].value_counts().reset_index().rename(columns={"index":"alert","alert":"count"})
        show_df(out)
    else:
        st.warning("alert column missing.")

elif choice.startswith("Q21"):
    cutoff = (pd.Timestamp.now().year - 10)
    out = df[df["time"].dt.year >= cutoff].groupby("country")["mag"].agg(["mean","count"]).reset_index().rename(columns={"mean":"avg_mag","count":"events"})
    out = out[out["events"]>=10].sort_values("avg_mag", ascending=False).head(5)
    show_df(out)

elif choice.startswith("Q22"):
    # countries that have both shallow (<50) and deep (>300) in same month
    if "depth_km" in df.columns:
        tmp = df.dropna(subset=["country","time","depth_km"]).copy()
        tmp["year"] = tmp["time"].dt.year
        tmp["month"] = tmp["time"].dt.month
        grouped = tmp.groupby(["country","year","month"]).agg(
            shallow = ("depth_km", lambda s: (s < 50).any()),
            deep = ("depth_km", lambda s: (s > 300).any()),
            count = ("depth_km","count")
        ).reset_index()
        out = grouped[(grouped["shallow"]) & (grouped["deep"])].sort_values(["country","year","month"])
        show_df(out)
    else:
        st.warning("depth_km column missing.")

elif choice.startswith("Q23"):
    # year-over-year growth
    yearly = df.groupby(df["time"].dt.year)["id"].count().reset_index().rename(columns={"time":"year","id":"cnt"}).sort_values("year")
    yearly["prev"] = yearly["cnt"].shift(1)
    yearly["growth_pct"] = ((yearly["cnt"] - yearly["prev"]) / yearly["prev"] * 100).round(2)
    show_df(yearly.fillna(0))

elif choice.startswith("Q24"):
    # region by place score = count * avg mag
    tmp = df.groupby("place").agg(freq=("id","count"), avg_mag=("mag","mean")).reset_index()
    tmp["score"] = tmp["freq"] * tmp["avg_mag"]
    out = tmp[tmp["freq"]>=5].sort_values("score", ascending=False).head(3)
    show_df(out)

elif choice.startswith("Q25"):
    # avg depth per country within ±5° lat
    if "latitude" in df.columns and "depth_km" in df.columns:
        tmp = df[(df["latitude"].between(-5,5)) & (~df["country"].isna())]
        out = tmp.groupby("country")["depth_km"].mean().reset_index().rename(columns={"depth_km":"avg_depth_km"}).sort_values("avg_depth_km", ascending=False)
        show_df(out)
    else:
        st.warning("latitude or depth_km missing.")

elif choice.startswith("Q26"):
    # ratio shallow:deep per country
    if "depth_km" in df.columns:
        tmp = df.dropna(subset=["country","depth_km"])
        agg = tmp.groupby("country").agg(
            shallow = ("depth_km", lambda s: (s < 50).sum()),
            deep = ("depth_km", lambda s: (s > 300).sum())
        ).reset_index()
        agg["ratio"] = agg.apply(lambda r: (r["shallow"]/r["deep"]) if r["deep"]>0 else np.nan, axis=1)
        out = agg[agg["shallow"]+agg["deep"]>=5].sort_values("ratio", ascending=False).head(20)
        show_df(out)
    else:
        st.warning("depth_km missing.")

elif choice.startswith("Q27"):
    if "tsunami" in df.columns and "mag" in df.columns:
        avg_t = df[df["tsunami"]==1]["mag"].mean()
        avg_nt = df[df["tsunami"]==0]["mag"].mean()
        st.write({"avg_mag_tsunami": avg_t, "avg_mag_no_tsunami": avg_nt, "difference": (avg_t - avg_nt)})
    else:
        st.warning("tsunami or mag column missing.")

elif choice.startswith("Q28"):
    if "rms" in df.columns and "gap" in df.columns:
        df["error_score"] = df["rms"].fillna(0) + df["gap"].fillna(0)
        out = df.sort_values("error_score", ascending=False)[["id","time","place","country","rms","gap","error_score"]].head(100)
        show_df(out)
    else:
        st.warning("rms or gap missing.")

elif choice.startswith("Q29"):
    st.info("Q29 uses a time-ordered consecutive-pair approach and checks distance. For big datasets this can be slow; we limit to most recent N rows.")
    if ("latitude" in df.columns) and ("longitude" in df.columns):
        N = st.number_input("Max rows to consider (most recent). Use 10000 for large data; 2000 is faster.", min_value=500, max_value=50000, value=5000, step=500)
        tmp = df.sort_values("time", ascending=True).tail(N).reset_index(drop=True).copy()
        tmp["prev_lat"] = tmp["latitude"].shift(1)
        tmp["prev_lon"] = tmp["longitude"].shift(1)
        tmp["prev_time"] = tmp["time"].shift(1)
        # drop rows without prev
        pairs = tmp.dropna(subset=["prev_lat","prev_lon","prev_time"]).copy()
        pairs["minutes_diff"] = (pairs["time"] - pairs["prev_time"]).dt.total_seconds() / 60.0
        pairs["distance_km"] = haversine_km(pairs["prev_lat"].values, pairs["prev_lon"].values, pairs["latitude"].values, pairs["longitude"].values)
        out = pairs[(pairs["minutes_diff"] <= 60) & (pairs["distance_km"] <= 50)][["id","prev_time","time","minutes_diff","distance_km","place"]]
        show_df(out.sort_values("time", ascending=False).head(500))
    else:
        st.warning("latitude/longitude not present.")

elif choice.startswith("Q30"):
    if "depth_km" in df.columns:
        out = df[df["depth_km"] > 300].groupby("country")["id"].count().reset_index().rename(columns={"id":"deep_count"}).sort_values("deep_count", ascending=False).head(20)
        show_df(out)
    else:
        st.warning("depth_km missing.")

else:
    st.write("Task not implemented.")
