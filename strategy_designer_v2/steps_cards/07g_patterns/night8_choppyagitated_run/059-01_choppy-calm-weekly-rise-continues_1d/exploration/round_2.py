import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            vol90 = r1.rolling(90, min_periods=45).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(df)),
                "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                "s7": (c / c.shift(7) - 1) / (vol30 * np.sqrt(7)),
                "s3": (c / c.shift(3) - 1) / (vol30 * np.sqrt(3)),
                "tr60": c / c.shift(60) - 1,
                "ag": vol30 / vol90,
                "f7": c.shift(-7) / c - 1, "f3": c.shift(-3) / c - 1, "f1": c.shift(-1) / c - 1,
                "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(df["timestamp"]).dt.year,
                "alloc": df["postRebalance_current_allocation"],
            })
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["trend"] = pd.cut(A["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    A["agq"] = np.where(A["ag"] > 1, "agit", "calm")
    A.loc[A["ag"].isna(), "agq"] = np.nan
    dr1 = A.groupby("coin")["f1"].mean(); A["x1"] = A["f1"] - A["coin"].map(dr1)

    def clus(df, col, by):
        out = []
        for k, g in df.dropna(subset=[col]).groupby(by):
            s = g.groupby("day")[col].sum()
            n = len(g); G = len(s)
            m = g[col].mean()
            se = np.sqrt((s - s.size and 0) .pow(0).sum()) if False else np.sqrt(((g.groupby("day")[col].apply(lambda v: (v - m).sum()))**2).sum()) / n * np.sqrt(G / max(G - 1, 1))
            out.append((k, n, G, m, m / se if se > 0 else np.nan))
        return pd.DataFrame(out, columns=["grp", "n", "days", "mean", "t_clu"]).set_index("grp").round(4)

    res = {}
    res["1d excess by weekday (clustered)"] = clus(A, "x1", "wd")
    A["late"] = A["wd"].isin([3, 4]).astype(int)
    res["late-week next-day by trend"] = clus(A, "x1", ["trend", "late"])
    res["late-week next-day by year"] = clus(A[A["late"] == 1], "x1", "yr")
    res["midweek(wd2) next-day by year"] = clus(A[A["wd"] == 2], "x1", "yr")
    # 7d grid momentum by trend x agitation proxy, graded
    g7 = A[A["pos"] % 7 == 0].copy()
    dr7 = g7.groupby("coin")["f7"].mean(); g7["x7"] = g7["f7"] - g7["coin"].map(dr7)
    out = []
    for k, g in g7.dropna(subset=["x7", "s7", "agq"]).groupby(["trend", "agq"]):
        sl = stats.linregress(g["s7"], g["x7"])
        out.append((k, len(g), sl.slope, sl.slope / sl.stderr))
    res["7d slope x7 on s7 by trend x agit"] = pd.DataFrame(out, columns=["grp", "n", "slope", "t"]).set_index("grp").round(4)
    # 3d grid: s3 -> next 3d by trend x agit
    g3 = A[A["pos"] % 3 == 0].copy()
    dr3 = g3.groupby("coin")["f3"].mean(); g3["x3"] = g3["f3"] - g3["coin"].map(dr3)
    out = []
    for k, g in g3.dropna(subset=["x3", "s3", "agq"]).groupby(["trend", "agq"]):
        sl = stats.linregress(g["s3"], g["x3"])
        out.append((k, len(g), sl.slope, sl.slope / sl.stderr))
    res["3d slope x3 on s3 by trend x agit"] = pd.DataFrame(out, columns=["grp", "n", "slope", "t"]).set_index("grp").round(4)
    # rising trend: weekly momentum by window consistency
    gr = g7[g7["trend"] == "rise"].dropna(subset=["x7", "s7"])
    out = []
    for w, g in gr.groupby("win"):
        if len(g) > 8:
            out.append((w, len(g), np.corrcoef(g["s7"], g["x7"])[0, 1]))
    res["rising: corr s7,x7 by window"] = pd.DataFrame(out, columns=["win", "n", "corr"]).set_index("win").round(3)
    # book: weekday of book daily returns
    dl = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            x = dd.copy(); x["coin"] = coin; dl.append(x)
    D = pd.concat(dl)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    res["book & coin daily return by weekday (bp)"] = D.groupby("wd")[["book_return", "coin_return"]].mean().mul(1e4).round(2)
    return res
