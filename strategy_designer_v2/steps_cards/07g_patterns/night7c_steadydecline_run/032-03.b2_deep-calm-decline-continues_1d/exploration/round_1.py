import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]
            b["r28"] = cl / cl.shift(28) - 1
            b["r5"] = cl / cl.shift(5) - 1
            b["r1"] = cl / cl.shift(1) - 1
            b["rng"] = (b["high"] - b["low"]) / cl
            b["rng_rel"] = b["rng"].rolling(10).mean() / b["rng"].rolling(60, min_periods=30).mean()
            b["vol_rel"] = b["volume"].rolling(10).mean() / b["volume"].rolling(60, min_periods=30).mean()
            b["vol20"] = b["r1"].rolling(20).std()
            b["f10"] = cl.shift(-10) / cl - 1
            b["f1"] = cl.shift(-1) / cl - 1
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["win"] = w
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cm10 = B[B.pos % 10 == 0].groupby("coin")["f10"].mean()
    B["ex10"] = B["f10"] - B["coin"].map(cm10)
    cm1 = B.groupby("coin")["f1"].mean()
    B["ex1"] = B["f1"] - B["coin"].map(cm1)
    G = B[(B.pos % 10 == 0)].dropna(subset=["ex10"])

    def tab(df, col, q=5, y="ex10"):
        d = df.dropna(subset=[col, y]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = d.groupby("q")[y].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g[col + "_mean"] = d.groupby("q")[col].mean()
        return g.drop(columns="std")

    out["r28 quintile, all regimes (ex10)"] = tab(G, "r28")
    out["r28 quintile, trending (ex10)"] = tab(G[G.regime == "trending"], "r28")
    out["r28 quintile, not trending (ex10)"] = tab(G[G.regime != "trending"], "r28")
    out["r5 quintile (ex10)"] = tab(G, "r5")
    out["rng_rel quintile (ex10)"] = tab(G, "rng_rel")
    out["vol_rel quintile (ex10)"] = tab(G, "vol_rel")
    out["vol20 quintile (ex10)"] = tab(G, "vol20")
    neg = G[G.r28 < 0]
    out["fallen r28<0: rng_rel quintile (ex10)"] = tab(neg, "rng_rel")
    out["fallen r28<0: vol_rel quintile (ex10)"] = tab(neg, "vol_rel")
    # daily: after large 1-day moves (all bars, 1-day horizon is non-overlapping)
    B["z1"] = B["r1"] / B["vol20"]
    out["z1 quintile -> next day ex1"] = tab(B, "z1", y="ex1")
    wd = B.groupby("wd")["ex1"].agg(["mean", "count", "std"]); wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["weekday ex1"] = wd.drop(columns="std")
    yr = G.groupby(["year"]).apply(lambda d: pd.Series({"n": len(d), "corr_r28_ex10": d["r28"].corr(d["ex10"])}))
    out["year corr r28 vs ex10"] = yr
    # book
    D = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["win"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby("day")["book_return"].mean().dropna()
    out["book by window"] = D.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out
