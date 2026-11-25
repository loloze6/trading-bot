import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = (h - l) / c
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["ret0"] = c / c.shift(1) - 1
            d["fwd1"] = c.shift(-1) / c - 1
            d["fwd3"] = c.shift(-3) / c - 1
            d["pos3"] = (np.arange(len(b)) % 3 == 0)
            d["loc"] = ((c - l) / (h - l)).where(h > l)
            d["rr"] = rng.rolling(30).mean() / rng.rolling(90).mean()
            d["r30"] = c / c.shift(30) - 1
            d["newlow30"] = (l <= l.rolling(30).min()).astype(float)
            d["dd30"] = c / c.rolling(30).max() - 1
            d["vol20"] = d["ret0"].rolling(20).std()
            d["rngz"] = rng / rng.rolling(30).mean()
            d["fc"] = b["forecast"]
            d["alloc"] = b["postRebalance_current_allocation"]
            d["regime"] = b["regime"]
            d["gain"] = d["alloc"] * d["fwd1"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["fwd1"].mean()
    mu3 = D[D.pos3].groupby("coin")["fwd3"].mean()
    D["x1"] = D["fwd1"] - D["coin"].map(mu1)
    D["x3"] = D["fwd3"] - D["coin"].map(mu3)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.weekday

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        n = len(s)
        if n < 10: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan, "days": 0})
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / n
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / se, "days": g.size})

    out = {}
    D["locq"] = pd.qcut(D["loc"], 5, labels=False)
    D["reg"] = np.where(D["rr"] > 1, "wide", "narrow")
    out["x1 by loc quintile x rr regime"] = D.groupby(["reg", "locq"]).apply(lambda s: ct(s, "x1"))
    s3 = D[D.pos3]
    out["x3 by loc quintile (grid 3d)"] = s3.groupby("locq").apply(lambda s: ct(s, "x3"))
    D["fcb"] = pd.cut(D["fc"], [-21, -2, 2, 6, 10, 21])
    out["x1 by forecast band"] = D.groupby("fcb").apply(lambda s: ct(s, "x1"))
    D["r0q"] = pd.qcut(D["ret0"], 10, labels=False)
    out["x1 by same-day ret decile"] = D.groupby("r0q").apply(lambda s: ct(s, "x1"))
    out["x3 by same-day ret decile (grid)"] = D[D.pos3].groupby("r0q").apply(lambda s: ct(s, "x3"))
    D["dn"] = np.where(D["r30"] < 0, "down30", "up30")
    out["x1 newlow30 x down x wide"] = D.groupby(["reg", "dn", "newlow30"]).apply(lambda s: ct(s, "x1"))
    out["x3 newlow30 x reg (grid)"] = D[D.pos3].groupby(["reg", "newlow30"]).apply(lambda s: ct(s, "x3"))
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda v: pd.qcut(v, 4, labels=False, duplicates="drop"))
    out["x1 by vol quartile"] = D.groupby("volq").apply(lambda s: ct(s, "x1"))
    D["rngzq"] = pd.qcut(D["rngz"], 5, labels=False)
    out["x1 by day range / 30d mean range"] = D.groupby("rngzq").apply(lambda s: ct(s, "x1"))
    out["x1 by weekday"] = D.groupby("wd").apply(lambda s: ct(s, "x1"))
    D["dd30q"] = pd.qcut(D["dd30"], 5, labels=False)
    out["x3 by 30d drawdown quintile (grid)"] = D[D.pos3].groupby("dd30q").apply(lambda s: ct(s, "x3"))
    out["book gain by locq (in position)"] = D[D.alloc.abs() > 0].groupby("locq").apply(lambda s: ct(s, "gain"))
    out["book gain by weekday"] = D[D.alloc.abs() > 0].groupby("wd").apply(lambda s: ct(s, "gain"))
    out["x1 by coin"] = D.groupby("coin").apply(lambda s: ct(s, "x1"))
    out["locq x newlow wide"] = D[D.reg == "wide"].groupby(["newlow30", "locq"]).apply(lambda s: ct(s, "x1"))
    return out
