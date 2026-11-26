import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            b["fwd"] = c.shift(-H) / c - 1
            b["r1"] = c.pct_change()
            b["lvr"] = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            b["tr60"] = c / c.shift(59) - 1
            b["sd30"] = b["r1"].rolling(30).std()
            b["rng"] = (b["high"] - b["low"]) / c
            b["rngrel"] = b["rng"] / b["rng"].rolling(20).median()
            b["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["coin"] = coin; b["win"] = w
            b["pos"] = np.arange(len(b))
            rows.append(b[b["pos"] % H == 0])
    G = pd.concat(rows).dropna(subset=["fwd"])
    drift = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    G["trend"] = np.where(G["tr60"] > 0.10, "rising", np.where(G["tr60"] < -0.10, "falling", "choppy"))
    G.loc[G["tr60"].isna(), "trend"] = np.nan
    def summ(df, key):
        r = df.groupby(key)["ex"].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(4)
    def slope(df, x):
        d = df.dropna(subset=[x, "ex"])
        if len(d) < 20: return pd.Series({"n": len(d)})
        s = stats.linregress(d[x], d["ex"])
        return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})
    A = G.dropna(subset=["rngrel", "clv"]).copy()
    A["cs"] = 2 * A["clv"] - 1  # close location, -1 low to +1 high
    A["nq"] = pd.cut(A["rngrel"], [0, 0.7, 1.0, 1.4, 99], labels=["vnarrow", "narrow", "wide", "vwide"])
    out["slope ex on close-location, by relative range"] = A.groupby("nq").apply(lambda d: slope(d, "cs")).round(4)
    A["sig"] = A["cs"] / A["rngrel"].clip(lower=0.2)
    out["slope ex on close-loc/relative-range, by trend"] = A.groupby("trend").apply(lambda d: slope(d, "sig")).round(4)
    out["slope ex on close-loc/relative-range, by year"] = A.groupby("yr").apply(lambda d: slope(d, "sig")).round(4)
    out["slope ex on close-loc/relative-range, by coin"] = A.groupby("coin").apply(lambda d: slope(d, "sig")).round(4)
    out["slope ex on close-loc/relative-range, all"] = slope(A, "sig").round(4).to_frame("all")
    # day-clustered t for the close location in narrow days
    N = A[A["rngrel"] < 1.0].copy()
    N["dev"] = N["ex"] * np.sign(N["cs"])
    N["day"] = pd.to_datetime(N["timestamp"]).dt.floor("D")
    dd = N.groupby("day")["dev"].sum()
    out["narrow days: signed ex by close side, day-clustered"] = pd.Series({"cases": len(N), "mean": N["dev"].mean(), "days": len(dd), "t_day": dd.mean() / (dd.std() / np.sqrt(len(dd)))}).round(4).to_frame("v")
    # rising-volume ratio in rising markets
    R = G.dropna(subset=["lvr"]).copy()
    out["slope ex on log vol ratio, by trend"] = R.groupby("trend").apply(lambda d: slope(d, "lvr")).round(4)
    out["slope ex on log vol ratio, rising, by year"] = R[R["trend"] == "rising"].groupby("yr").apply(lambda d: slope(d, "lvr")).round(4)
    # book's biggest days: what preceded
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 20, labels=False)
    out["coin return on book's 5% worst/best days"] = D[D["bq"].isin([0, 19])].groupby("bq")[["book_return", "coin_return"]].agg(["count", "mean"]).round(4)
    return out
