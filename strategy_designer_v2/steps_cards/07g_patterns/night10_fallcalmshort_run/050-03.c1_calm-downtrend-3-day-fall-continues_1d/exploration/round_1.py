import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            b["s3"] = (c / c.shift(3) - 1) / sd30
            b["s1"] = r1 / sd30
            b["s7"] = (c / c.shift(7) - 1) / sd30
            rng = (b["high"] - b["low"])
            b["clv"] = (c - b["low"]) / rng.replace(0, np.nan)
            b["rngs"] = (rng / c.shift(1)) / sd30
            b["volr"] = b["volume"] / b["volume"].rolling(20, min_periods=10).mean()
            b["dd20"] = c / c.rolling(20, min_periods=10).max() - 1
            b["dd20s"] = b["dd20"] / sd30
            for h in (1, 3, 5):
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["pos"] = np.arange(len(b))
            b["inprof"] = (b["regime"] == "unknown")
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["coin"] = coin; b["win"] = w
            b["alloc"] = b["postRebalance_current_allocation"]
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    out = {}
    out["share_in_profile_by_coin"] = B.groupby("coin")["inprof"].mean()
    P = B[B.inprof]
    drift3 = B[B.pos % 3 == 0].groupby("coin")["f3"].mean()
    G = P[P.pos % 3 == 0].copy()
    G["u3"] = G["f3"] - G["coin"].map(drift3)
    def tab(col, q=5):
        g = G.dropna(subset=[col, "u3"]).copy()
        g["bin"] = pd.qcut(g[col], q, labels=False, duplicates="drop")
        t = g.groupby("bin").agg(lo=(col, "min"), hi=(col, "max"), n=("u3", "size"),
                                 mean_u3=("u3", "mean"),
                                 t=("u3", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
        rho = stats.spearmanr(g[col], g["u3"])
        t.loc["spearman"] = [np.nan, np.nan, len(g), rho.correlation, rho.pvalue]
        return t
    for col in ["s3", "s1", "s7", "clv", "rngs", "volr", "dd20s"]:
        out["inprof_u3_by_" + col] = tab(col)
    # 1-day horizon non-overlapping (every bar) on s1, clv
    P1 = P.dropna(subset=["f1"]).copy()
    drift1 = B.groupby("coin")["f1"].mean()
    P1["u1"] = P1["f1"] - P1["coin"].map(drift1)
    for col in ["s1", "clv", "s3"]:
        g = P1.dropna(subset=[col]).copy()
        g["bin"] = pd.qcut(g[col], 5, labels=False, duplicates="drop")
        out["inprof_u1_by_" + col] = g.groupby("bin").agg(lo=(col, "min"), n=("u1", "size"), mean_u1=("u1", "mean"),
                     t=("u1", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    out["inprof_u1_by_weekday"] = P1.groupby("wd")["u1"].agg(["size", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["inprof_u3_by_coin"] = G.groupby("coin")["u3"].agg(["size", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades"] = T.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean", "median"])
    return out
