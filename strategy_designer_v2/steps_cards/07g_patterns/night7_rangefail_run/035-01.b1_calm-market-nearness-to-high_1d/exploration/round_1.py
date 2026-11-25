import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi = c.shift(1).rolling(20).max()
            sd = r1.rolling(20).std()
            dist = (c - hi) / hi / sd
            ret1 = r1
            ret3 = c / c.shift(3) - 1
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            sd5 = r1.rolling(5).std()
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            n = len(b)
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(n),
                "dist": dist, "r1": ret1, "r3": ret3, "r20": ret20, "r60": ret60,
                "volratio": sd5 / sd, "sd20": sd,
                "fwd5": fwd5, "fwd1": fwd1,
                "calm": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % 5 == 0].groupby("coin")["fwd5"].mean()
    A["ex5"] = A["fwd5"] - A["coin"].map(drift)
    G = A[(A.pos % 5 == 0)].dropna(subset=["ex5", "dist"])
    out = {}
    def tab(g, key):
        t = g.groupby(key)["ex5"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.round(4)
    G = G.copy()
    G["dq"] = pd.qcut(G["dist"], 5, labels=False)
    out["dist quintile x calm"] = tab(G, ["calm", "dq"])
    G["r1q"] = pd.qcut(G["r1"], 5, labels=False)
    out["1d ret quintile x calm"] = tab(G, ["calm", "r1q"])
    G["r20q"] = pd.qcut(G["r20"], 5, labels=False)
    out["20d ret quintile"] = tab(G, ["r20q"])
    G2 = G.dropna(subset=["r60"]).copy()
    G2["trend"] = np.where(G2.r60 > .1, "rise", np.where(G2.r60 < -.1, "fall", "chop"))
    G2["dq"] = pd.qcut(G2["dist"], 3, labels=False)
    out["trend x dist tercile"] = tab(G2, ["trend", "dq"])
    G["vq"] = pd.qcut(G["volratio"], 5, labels=False)
    out["5d/20d vol ratio quintile"] = tab(G, ["vq"])
    out["window"] = tab(G, ["w"])
    # weekday on daily next-day returns
    D = A.dropna(subset=["fwd1"])
    t = D.groupby("wd")["fwd1"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["weekday next-day ret"] = t.round(5)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    Dd = pd.concat(dd)
    book = Dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    book["bq"] = pd.qcut(book["book_return"], 10, labels=False)
    out["book decile vs coin ret"] = book.groupby("bq")[["book_return", "coin_return"]].mean().round(5)
    out["book share long"] = float((A.alloc > 0).mean()); out["book share short"] = float((A.alloc < 0).mean())
    tr = []
    for coin, wins in data["trades"].items():
        for w, t_ in wins.items():
            tr.append(t_)
    T = pd.concat(tr)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean", "count", "median"]).round(3)
    return out
