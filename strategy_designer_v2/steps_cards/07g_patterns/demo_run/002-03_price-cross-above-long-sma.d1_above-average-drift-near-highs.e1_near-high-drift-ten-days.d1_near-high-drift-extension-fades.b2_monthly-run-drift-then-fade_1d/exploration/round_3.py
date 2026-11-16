def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy().reset_index(drop=True); d["coin"] = coin; d["w"] = w
            r = d["coin_return"]
            d["prev1"] = r.shift(1)
            d["prev5"] = (1 + r).rolling(5).apply(np.prod, raw=True).shift(1) - 1
            d["vol20"] = r.rolling(20).std().shift(1)
            D.append(d)
    D = pd.concat(D)
    D["day"] = pd.to_datetime(D["day"]); D["wd"] = D["day"].dt.weekday
    D = D.dropna(subset=["coin_return"])
    S = D[D.wd == 5].copy()
    # Saturday return graded by Friday return, prior 5-day return, vol
    for col in ["prev1", "prev5", "vol20"]:
        x = S.dropna(subset=[col]).copy()
        x["q"] = pd.qcut(x[col], 5, labels=False)
        r = x.groupby("q")["coin_return"].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        out[f"sat_by_{col}_q"] = r.round(5)
        sl = stats.linregress(x[col], x["coin_return"])
        out[f"sat_slope_{col}"] = f"slope={sl.slope:.4f} t={sl.slope/sl.stderr:.2f} n={len(x)}"
    # Saturday excess return scaled by vol: is mean/vol constant?
    x = S.dropna(subset=["vol20"]).copy()
    x["z"] = x["coin_return"] / x["vol20"]
    out["sat_z_mean"] = f"mean={x.z.mean():.4f} t={x.z.mean()/(x.z.std()/np.sqrt(len(x))):.2f} n={len(x)}"
    y = D[D.wd != 5].dropna(subset=["vol20"]).copy(); y["z"] = y["coin_return"] / y["vol20"]
    out["notsat_z_mean"] = f"mean={y.z.mean():.4f} t={y.z.mean()/(y.z.std()/np.sqrt(len(y))):.2f} n={len(y)}"
    # same for all days: next-day return by prev1 quintile (reversal?)
    x = D.dropna(subset=["prev1"]).copy()
    x["q"] = pd.qcut(x["prev1"], 5, labels=False)
    r = x.groupby("q")["coin_return"].agg(["count", "mean", "std"])
    r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
    out["all_next_by_prev1_q"] = r.round(5)
    # book: largest gain/loss days, prior coin 5-day return
    B = D.dropna(subset=["book_return", "prev5"]).copy()
    B["bq"] = pd.qcut(B["book_return"], 20, labels=False, duplicates="drop")
    out["book_tail_prev5"] = B[B.bq.isin([0, 19])].groupby("bq")[["prev5", "coin_return", "book_return"]].mean().round(4)
    return out
