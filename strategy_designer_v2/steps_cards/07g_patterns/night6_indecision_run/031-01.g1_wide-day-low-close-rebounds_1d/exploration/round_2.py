import numpy as np
import pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            allr.append((b["close"].shift(-1) / b["close"] - 1).dropna())
        mu1 = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, o, h, l = b["close"], b["open"], b["high"], b["low"]
            rng = (h - l)
            rr = rng / rng.rolling(20, min_periods=20).mean()
            cl = (c - l) / rng.replace(0, np.nan)
            r1 = c.shift(-1) / c - 1
            r3 = c.shift(-3) / c - 1
            past1 = c / c.shift(1) - 1
            past5 = c.shift(1) / c.shift(6) - 1
            vol = past1.rolling(20, min_periods=10).std()
            pos = np.arange(len(b))
            d = pd.DataFrame({
                "coin": coin, "win": w, "day": b["timestamp"].astype(str).str[:10],
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "rr": rr, "cl": cl, "r1x": r1 - mu1, "r3": r3, "g3": pos % 3 == 0,
                "past1": past1, "past5": past5, "vol": vol, "relrng": rng / c,
                "p5z": past5 / (vol * np.sqrt(5)),
                "alloc": b["postRebalance_current_allocation"],
                "br": b["postRebalance_total_value"].shift(-1) / b["postRebalance_total_value"] - 1,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def ct(df, col):
        x = df[[col, "day"]].dropna()
        if len(x) < 5:
            return pd.Series({"mean": np.nan, "t": np.nan, "n": len(x), "days": 0})
        m = x[col].mean()
        s = (x[col] - m).groupby(x["day"]).sum()
        D_ = len(s)
        se = np.sqrt((s ** 2).sum() * D_ / max(D_ - 1, 1)) / len(x)
        return pd.Series({"mean": m, "t": m / se if se > 0 else np.nan, "n": len(x), "days": D_})

    out = {}
    # wide-high-close after prior 5d fall (prior run excludes the day)
    wh = D[(D["rr"] >= 1.5) & (D["cl"] >= 0.75)].copy()
    wh["p5zb"] = pd.cut(wh["p5z"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["wide-high by prior 5d z"] = wh.groupby("p5zb", observed=True).apply(lambda x: ct(x, "r1x"))
    whd = wh[wh["p5z"] < -0.5]
    out["wide-high after fall by coin"] = whd.groupby("coin").apply(lambda x: ct(x, "r1x"))
    out["wide-high after fall by year"] = whd.groupby("year").apply(lambda x: ct(x, "r1x"))
    s3 = whd[whd["g3"]].copy(); s3["x"] = s3["r3"]
    out["wide-high after fall r3 raw grid"] = ct(s3, "x").to_frame().T
    # control: high close, normal range, after fall
    hc = D[(D["cl"] >= 0.75) & (D["p5z"] < -0.5)].copy()
    hc["rrb"] = pd.cut(hc["rr"], [0, 1, 1.5, 2, 99])
    out["high-close after fall by range"] = hc.groupby("rrb", observed=True).apply(lambda x: ct(x, "r1x"))
    # wide-low: relative range (range / close) grading
    wl = D[(D["rr"] >= 1.5) & (D["cl"] <= 0.25)].copy()
    wl["relb"] = pd.qcut(wl["relrng"], 4, labels=["q1", "q2", "q3", "q4"])
    out["wide-low by range/close quartile"] = wl.groupby("relb", observed=True).apply(lambda x: ct(x, "r1x"))
    # low-close any range, by relative range: is it absolute size?
    lc = D[D["cl"] <= 0.25].copy()
    lc["relb"] = lc.groupby("coin")["relrng"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["low-close by coin-relrange quintile"] = lc.groupby("relb").apply(lambda x: ct(x, "r1x"))
    lc["pb"] = lc.groupby("coin")["past1"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["low-close by coin past1 quintile"] = lc.groupby("pb").apply(lambda x: ct(x, "r1x"))
    # book largest gains/losses: share in position with wide-low
    B = D.dropna(subset=["br"])
    inpos = B[B["alloc"].abs() > 0]
    q = inpos["br"].quantile([0.05, 0.95])
    out["book bar returns in pos"] = pd.Series({"n": len(inpos), "mean": inpos["br"].mean(),
        "p05": q.iloc[0], "p95": q.iloc[1],
        "share of gain from top 10%": inpos["br"].nlargest(int(len(inpos)*0.1)).sum() / inpos["br"].sum()})
    inpos = inpos.copy()
    inpos["volb"] = inpos.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False, duplicates="drop"))
    out["book in pos by vol tercile"] = inpos.groupby("volb")["br"].agg(["mean", "std", "count"])
    return out
