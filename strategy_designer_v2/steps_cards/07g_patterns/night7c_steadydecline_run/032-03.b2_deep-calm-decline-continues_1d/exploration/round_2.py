import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]
            b["r28"] = cl / cl.shift(28) - 1
            b["r1"] = cl / cl.shift(1) - 1
            b["rng"] = (b["high"] - b["low"]) / cl
            b["rng_rel"] = b["rng"].rolling(10).mean() / b["rng"].rolling(60, min_periods=30).mean()
            b["vol20"] = b["r1"].rolling(20).std()
            b["f10"] = cl.shift(-10) / cl - 1
            b["f1"] = cl.shift(-1) / cl - 1
            b["f3"] = cl.shift(-3) / cl - 1
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["win"] = w
            ts = pd.to_datetime(b["timestamp"])
            b["year"] = ts.dt.year; b["day"] = ts.dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cm10 = B[B.pos % 10 == 0].groupby("coin")["f10"].mean()
    B["ex10"] = B["f10"] - B["coin"].map(cm10)
    cm1 = B.groupby("coin")["f1"].mean(); B["ex1"] = B["f1"] - B["coin"].map(cm1)
    cm3 = B[B.pos % 3 == 0].groupby("coin")["f3"].mean(); B["ex3"] = B["f3"] - B["coin"].map(cm3)
    B["z1"] = B["r1"] / B["vol20"]
    G = B[B.pos % 10 == 0].dropna(subset=["ex10", "r28"])

    def ct(df, x, y):
        d = df.dropna(subset=[x, y])
        # clustered-by-day slope t
        X = d[x] - d[x].mean(); Y = d[y] - d[y].mean()
        beta = (X * Y).sum() / (X ** 2).sum()
        e = Y - beta * X
        s = (X * e).groupby(d["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"n": len(d), "days": d["day"].nunique(), "slope": beta, "t_cl": beta / se,
                          "corr": d[x].corr(d[y])})
    # 1-day reversal after big down day: graded slope of ex1 on z1
    out["z1 -> ex1 slope by year"] = B.groupby("year").apply(lambda d: ct(d, "z1", "ex1"))
    out["z1 -> ex1 slope by coin"] = B.groupby("coin").apply(lambda d: ct(d, "z1", "ex1"))
    neg1 = B[B.z1 < 0]
    out["z1<0 only -> ex1 slope by year"] = neg1.groupby("year").apply(lambda d: ct(d, "z1", "ex1"))
    pos1 = B[B.z1 > 0]
    out["z1>0 only -> ex1 slope by year"] = pos1.groupby("year").apply(lambda d: ct(d, "z1", "ex1"))
    # 3-day horizon on grid
    G3 = B[B.pos % 3 == 0]
    out["z1 -> ex3 slope all/neg"] = pd.DataFrame({"all": ct(G3, "z1", "ex3"), "neg": ct(G3[G3.z1 < 0], "z1", "ex3")})
    # thin-volume falls, raw r28
    T = G[(G.regime == "trending") & (G.r28 < 0)]
    out["trending r28<0: r28 -> ex10 by year"] = T.groupby("year").apply(lambda d: ct(d, "r28", "ex10"))
    out["trending r28<0: by coin"] = T.groupby("coin").apply(lambda d: ct(d, "r28", "ex10"))
    # fallen coins, range calm -> rebound?
    F = G[G.r28 < 0]
    out["fallen: rng_rel -> ex10 by year"] = F.groupby("year").apply(lambda d: ct(d, "rng_rel", "ex10"))
    out["fallen: rng_rel -> ex10 by coin"] = F.groupby("coin").apply(lambda d: ct(d, "rng_rel", "ex10"))
    out["all: rng_rel -> ex10"] = ct(G, "rng_rel", "ex10")
    return out
