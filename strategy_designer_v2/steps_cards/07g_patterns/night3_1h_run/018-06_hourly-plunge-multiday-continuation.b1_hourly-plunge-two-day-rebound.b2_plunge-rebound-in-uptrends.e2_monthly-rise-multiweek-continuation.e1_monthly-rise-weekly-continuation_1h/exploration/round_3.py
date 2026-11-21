import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    # ---- A. weekday daily returns from days table (one per day, non-overlapping)
    D = []
    for c, ws in days.items():
        for w, df in ws.items():
            d = df.copy().reset_index(drop=True)
            d["day"] = pd.to_datetime(d["day"])
            d["wd"] = d["day"].dt.weekday; d["year"] = d["day"].dt.year
            d["prev5"] = d["close"].shift(1) / d["close"].shift(6) - 1
            d["coin"] = c; D.append(d)
    D = pd.concat(D).dropna(subset=["coin_return"])
    D["unusual"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    g = D.groupby("wd")["unusual"].agg(["mean", "std", "count"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    g["mean_bps"] = g["mean"] * 1e4
    out["unusual_daily_by_weekday"] = g[["mean_bps", "t", "count"]]
    sat = D[D["wd"] == 5]
    gy = sat.groupby("year")["unusual"].agg(["mean", "std", "count"]); gy["t"] = gy["mean"] / (gy["std"] / np.sqrt(gy["count"])); gy["mean"] *= 1e4
    out["saturday_by_year_bps"] = gy[["mean", "t", "count"]]
    gc = sat.groupby("coin")["unusual"].agg(["mean", "std", "count"]); gc["t"] = gc["mean"] / (gc["std"] / np.sqrt(gc["count"])); gc["mean"] *= 1e4
    out["saturday_by_coin_bps"] = gc[["mean", "t", "count"]]
    s2 = sat.dropna(subset=["prev5"]).copy()
    s2["pq"] = s2.groupby("coin")["prev5"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    gq = s2.groupby("pq")["unusual"].agg(["mean", "std", "count"]); gq["t"] = gq["mean"] / (gq["std"] / np.sqrt(gq["count"])); gq["mean"] *= 1e4
    out["saturday_by_prev5d_quintile_bps"] = gq[["mean", "t", "count"]]
    # ---- B. 21:00-23:00 two-hour move vs the day's earlier move (one case per day)
    E = []
    for c, ws in bars.items():
        for w, df in ws.items():
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            cl = df["close"].reset_index(drop=True)
            idx = np.where(ts.dt.hour.values == 20)[0]  # close of 20:00 bar = 21:00
            idx = idx[(idx + 2 < len(cl)) & (idx - 20 >= 0)]
            fwd = cl.values[idx + 2] / cl.values[idx] - 1
            prior = cl.values[idx] / cl.values[idx - 20] - 1
            E.append(pd.DataFrame({"fwd": fwd, "prior": prior, "coin": c, "year": ts.dt.year.values[idx]}))
    E = pd.concat(E)
    E["pq"] = E.groupby("coin")["prior"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    ge = E.groupby("pq")["fwd"].agg(["mean", "std", "count"]); ge["t"] = ge["mean"] / (ge["std"] / np.sqrt(ge["count"])); ge["mean"] *= 1e4
    out["evening_2h_by_prior20h_quintile_bps"] = ge[["mean", "t", "count"]]
    # ---- C. mild-decline continuation: r30 quintile 1 at 168h by year
    L = []
    for c, ws in bars.items():
        allr = []; tmp = []
        for w, df in ws.items():
            cl = df["close"].values; r30 = pd.Series(cl).pct_change(720).values
            idx = np.arange(0, len(cl) - 168, 168); fwd = cl[idx + 168] / cl[idx] - 1
            allr.append(fwd)
            tmp.append(pd.DataFrame({"r30": r30[idx], "fwd": fwd, "year": pd.to_datetime(df["timestamp"].values[idx]).year}))
        allr = np.concatenate(allr); t = pd.concat(tmp)
        t["s"] = (t["fwd"] - allr.mean()) / allr.std(); t["coin"] = c; L.append(t)
    T = pd.concat(L).dropna()
    T["q"] = T.groupby("coin")["r30"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    q1 = T[T["q"] == 1]
    out["r30_q1_by_year"] = q1.groupby("year")["s"].agg(["mean", "count"])
    return out
