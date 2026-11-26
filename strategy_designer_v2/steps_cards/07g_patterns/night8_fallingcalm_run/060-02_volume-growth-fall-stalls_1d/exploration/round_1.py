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
            b["r5p"] = c / c.shift(5) - 1
            b["lvr"] = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            b["lvr5"] = np.log(v.rolling(5).mean() / v.shift(5).rolling(25).mean())
            b["tr60"] = c / c.shift(59) - 1
            b["sd30"] = b["r1"].rolling(30).std()
            b["rng"] = (b["high"] - b["low"]) / c
            b["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["wd"] = b["ts"].dt.weekday
            b["coin"] = coin; b["win"] = w
            b["pos"] = np.arange(len(b))
            g = b[b["pos"] % H == 0]
            rows.append(g)
    G = pd.concat(rows)
    G = G.dropna(subset=["fwd"])
    drift = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    G["sd30m"] = G.groupby("coin")["sd30"].transform("median")
    G["agit"] = np.where(G["sd30"] > G["sd30m"], "agit", "calm")
    G.loc[G["sd30"].isna(), "agit"] = np.nan
    G["fallreg"] = G["regime"] == "unknown"
    def summ(df, key):
        r = df.groupby(key)["ex"].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(4)
    act = G[G["fallreg"] & (G["forecast"] != 0)].copy()
    act["fsign"] = np.sign(act["forecast"])
    out["active by forecast sign"] = summ(act, "fsign")
    act["fq"] = pd.qcut(act["forecast"], 5, labels=False, duplicates="drop")
    out["active by forecast quintile"] = summ(act, "fq")
    out["active by agitation x sign"] = summ(act, ["agit", "fsign"])
    out["active by coin x sign"] = summ(act, ["coin", "fsign"])
    # outside falling: recomputed vol ratio
    oth = G[~G["fallreg"]].dropna(subset=["lvr", "tr60"]).copy()
    oth["trend"] = np.where(oth["tr60"] > 0.10, "rising", np.where(oth["tr60"] < -0.10, "falling", "choppy"))
    oth["lq"] = oth.groupby("trend")["lvr"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["non-active: trend x vol-ratio tercile"] = summ(oth, ["trend", "lq"])
    # all grid: prior 5d return quintile and short-term volume surge
    A = G.dropna(subset=["r5p"]).copy()
    A["q5"] = A.groupby("coin")["r5p"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["all: prior 5d return quintile"] = summ(A, "q5")
    A2 = G.dropna(subset=["lvr5"]).copy()
    A2["sq"] = A2.groupby("coin")["lvr5"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["all: 5d volume surge quintile"] = summ(A2, "sq")
    A3 = G.dropna(subset=["rng", "clv"]).copy()
    A3["rq"] = A3.groupby("coin")["rng"].transform(lambda s: pd.qcut(s, 3, labels=False))
    A3["cq"] = pd.cut(A3["clv"], [-0.01, 0.33, 0.67, 1.01], labels=["low", "mid", "high"])
    out["all: range tercile x close location"] = summ(A3, ["rq", "cq"])
    out["all: weekday"] = summ(G, "wd")
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    bk = D.dropna(subset=["book_return"])
    out["book daily by weekday"] = bk.groupby("wd")["book_return"].agg(["count", "mean"]).round(5)
    out["book daily by window"] = bk.groupby("win")[["book_return", "coin_return"]].mean().round(5)
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", "sum"]).round(3)
    return out
