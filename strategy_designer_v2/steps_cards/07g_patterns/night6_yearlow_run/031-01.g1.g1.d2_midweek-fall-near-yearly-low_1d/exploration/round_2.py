import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "ts": ts, "wd": ts.dt.weekday, "year": ts.dt.year,
                              "pos": np.arange(len(b)),
                              "r1": r, "next": c.shift(-1) / c - 1,
                              "n3": c.shift(-3) / c - 1,
                              "r3": c / c.shift(3) - 1,
                              "vol20": r.rolling(20).std(),
                              "rngpos": (c - c.rolling(60).min()) / (c.rolling(60).max() - c.rolling(60).min()),
                              "regime": b["regime"]})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r1"].mean()
    D["nx"] = D["next"] - D["coin"].map(mu)
    D["nx3"] = D["n3"] - 3 * D["coin"].map(mu)
    D["z1"] = (D["r1"] / D["vol20"]).clip(-4, 4)
    D["z3"] = (D["r3"] / (D["vol20"] * np.sqrt(3))).clip(-4, 4)
    D["neg1"] = (-D["z1"]).clip(lower=0)   # size of a down day, 0 otherwise
    out = {}

    def tt(s):
        s = s.dropna()
        n = len(s)
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan, "n": n})

    def dayt(g, col):
        # cases of one day summed together
        g = g.dropna(subset=[col])
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["ts"].dt.normalize()).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(g)
        return pd.Series({"mean": m, "t_day": m / se, "days": G, "n": len(g)})

    # A. 1-day reversal: product -z1 * next excess, overall and splits
    D["rev1"] = -D["z1"] * D["nx"]
    D["dn1"] = D["neg1"] * D["nx"]
    out["A1 -z1 x next excess, all"] = pd.DataFrame({"rev1": dayt(D, "rev1"), "down-only": dayt(D, "dn1")}).T
    out["A2 down-day size x next excess by year"] = D.groupby("year").apply(lambda g: dayt(g, "dn1"))
    out["A3 down-day size x next excess by coin"] = D.groupby("coin").apply(lambda g: dayt(g, "dn1"))
    D["vq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["A4 down-day size x next excess by vol tercile"] = D.groupby("vq").apply(lambda g: dayt(g, "dn1"))
    D["rq"] = pd.cut(D["rngpos"], [-0.01, 0.2, 0.5, 0.8, 1.01], labels=False)
    out["A5 down-day size x next excess by 60d range position"] = D.groupby("rq").apply(lambda g: dayt(g, "dn1"))
    out["A6 down-day size x next excess by weekday of down day"] = D.groupby("wd").apply(lambda g: dayt(g, "dn1"))
    # 3-day horizon, non-overlapping grid pos%3==0
    G3 = D[D["pos"] % 3 == 0].copy()
    G3["dn3h"] = G3["neg1"] * G3["nx3"]
    out["A7 down-day size x next-3-day excess, grid"] = dayt(G3, "dn3h").to_frame().T
    # binned: next excess by down-day z bins
    D["zb"] = pd.cut(D["z1"], [-4.01, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, 4.01])
    out["A8 next excess by z1 bin"] = D.groupby("zb")["nx"].apply(tt).unstack()
    # B. Saturday unconditional excess
    S = D[D["wd"] == 4]
    out["B1 Friday->Saturday excess by year"] = S.groupby("year")["nx"].apply(tt).unstack()
    out["B2 Friday->Saturday excess by coin"] = S.groupby("coin")["nx"].apply(tt).unstack()
    out["B3 Saturday excess day-grouped"] = dayt(S, "nx").to_frame().T
    # C. Tuesday 3-day reversal (Sat close -> Tue close) vs Wednesday
    T = D[D["wd"] == 1].copy()
    T["revT"] = -T["z3"] * T["nx"]
    out["C1 Tue -z3 x Wed excess by year"] = T.groupby("year").apply(lambda g: dayt(g, "revT"))
    T["zb"] = pd.cut(T["z3"], [-4.01, -1.5, -0.5, 0.5, 1.5, 4.01])
    out["C2 Wed excess by Tue z3 bin"] = T.groupby("zb")["nx"].apply(tt).unstack()
    # same for other weekdays, day-grouped
    D["rev3"] = -D["z3"] * D["nx"]
    out["C3 -z3 x next excess by weekday (day t)"] = D.groupby("wd").apply(lambda g: dayt(g, "rev3"))
    return out
