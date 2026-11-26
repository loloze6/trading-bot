import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l)
            clv = (c - l) / rng.replace(0, np.nan)  # 0 at low, 1 at high
            r0 = c.pct_change()
            r1 = c.shift(-1) / c - 1
            r2 = c.shift(-2) / c - 1
            r3 = c.shift(-3) / c - 1
            vol30 = r0.rolling(30, min_periods=20).std()
            relrng = (rng / c) / ((rng / c).rolling(30, min_periods=20).mean())
            tr60 = c / c.shift(60) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]), "clv": clv, "r0": r0,
                "z0": r0 / vol30.shift(1), "x1": r1 - mu, "x2": r2 - 2 * mu, "x3": r3 - 3 * mu,
                "relrng": relrng, "tr60": tr60,
                "ag": (b["regime"] != "chop").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["s"] = 0.5 - D["clv"]  # + when low close
    out = {}

    def tt(x):
        x = x.dropna()
        return pd.Series({"mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "n": len(x)})

    def dayt(sub, col):
        g = sub.dropna(subset=[col]).groupby("day")[col].sum()
        return pd.Series({"mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(len(g))), "days": len(g)})

    D["q"] = pd.qcut(D["clv"], 5, labels=["q1low", "q2", "q3", "q4", "q5high"])
    out["clv quintile x agitated, next-day excess"] = D.groupby(["ag", "q"])["x1"].apply(tt).unstack()
    D["sx1"] = D["s"] * D["x1"]
    D["sx2"] = D["s"] * D["x2"].where(D["pos"] % 2 == 0)
    D["sx3"] = D["s"] * D["x3"].where(D["pos"] % 3 == 0)
    out["s*excess per-day t by ag, horizons"] = pd.DataFrame({f"ag{a}_{c}": dayt(D[D.ag == a], c) for a in [0, 1] for c in ["sx1", "sx2", "sx3"]}).T
    # range width interaction in agitated
    A = D[D.ag == 1].copy()
    A["rq"] = pd.qcut(A["relrng"], 3, labels=["narrow", "mid", "wide"])
    out["agitated: s*x1 by relative range"] = A.groupby("rq").apply(lambda s: dayt(s, "sx1")).round(4)
    D["rq"] = pd.qcut(D["relrng"], 3, labels=["narrow", "mid", "wide"])
    out["all: s*x1 by relrange x ag"] = D.groupby(["ag", "rq"]).apply(lambda s: dayt(s, "sx1")).round(4)
    D["trend"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["s*x1 by trend x ag"] = D.groupby(["ag", "trend"]).apply(lambda s: dayt(s, "sx1")).round(4)
    out["s*x1 by year (ag only)"] = A.groupby("year").apply(lambda s: dayt(s, "sx1")).round(4)
    out["s*x1 by coin x ag"] = D.groupby(["coin", "ag"]).apply(lambda s: dayt(s, "sx1")).round(4)
    out["s*x1 by weekday (all)"] = D.groupby("wd").apply(lambda s: dayt(s, "sx1")).round(4)
    out["next-day excess by weekday"] = D.groupby("wd")["x1"].apply(tt).unstack().round(3)
    D["zq"] = pd.qcut(D["z0"], 5, labels=["bigdown", "down", "mid", "up", "bigup"])
    out["next-day excess by today's z-move x ag"] = D.groupby(["ag", "zq"])["x1"].apply(tt).unstack().round(3)
    D["x3g"] = D["x3"].where(D["pos"] % 3 == 0)
    out["3-day excess (grid) by today's z-move x ag"] = D.groupby(["ag", "zq"])["x3g"].apply(tt).unstack().round(3)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk["year"] = pd.to_datetime(bk.index.get_level_values("day")).year
    out["book by year"] = bk.groupby("year").agg(mean_bp=("book_return", lambda x: 1e4 * x.mean()), sd_bp=("book_return", lambda x: 1e4 * x.std()), n=("book_return", "size"), coin_bp=("coin_return", lambda x: 1e4 * x.mean()))
    bk["bq"] = pd.qcut(bk["book_return"], 10, labels=False, duplicates="drop")
    out["book decile vs coin return same day (bp)"] = bk.groupby("bq")[["book_return", "coin_return"]].mean() * 1e4
    # long vs short side
    D["side"] = np.sign(D["alloc"])
    D["pnl"] = D["alloc"] * (D["x1"])
    out["position gain by side (excess)"] = D[D.side != 0].groupby("side")["pnl"].apply(tt).unstack()
    return out
