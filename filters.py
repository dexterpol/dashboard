# filters.py
import pandas as pd

def filter_data(df, date_filter=None, obra_filter=None, categoria_filter=None):
    if df.empty:
        return df

    if date_filter and len(date_filter) == 2:
        start, end = date_filter
        df = df[(df["data"] >= pd.Timestamp(start)) & (df["data"] <= pd.Timestamp(end))]

    if obra_filter:
        df = df[df["obra"].isin(obra_filter)]

    if categoria_filter:
        df = df[df["categoria"].isin(categoria_filter)]

    return df
