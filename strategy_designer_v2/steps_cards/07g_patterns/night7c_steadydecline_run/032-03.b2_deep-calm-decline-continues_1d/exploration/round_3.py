import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]
            b["r28"] = cl / cl.shift(28) - 1
            b["r14"] = cl / cl.shift(14) - 1
            b["r1"] = cl / cl.shift(1) - 1
            b["vol20"] = b["r1"].rolling(20).std()
            b["r28z"] = b["r28"] / (b["vol20"] * np.sqrt(28))
            b["fc"] = b["forecast"]
            for h in (5, 10):
                b["f%d" % h] = cl.shift(-h) / cl - 1
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["win"] = w
            ts = pd.to_datetime(b["timestamp"])
            b["year"] = ts.dt.year; b["day"] = ts.dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    for h in (5, 10):
        cm = B[B.pos % h == 0].groupby("coin")["f%d" % h].mean()
        B["ex%d" % h] = B["f%d" % h] - B["coin"].map(cm)

    def ct(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 10:
            return pd.Series({"n": len(d)})
        X = d[x] - d[x].mean(); Y = d[y] - d[y].mean()
        beta = (X * Y).sum() / (X ** 2).sum()
        e = Y - beta * X
        s = (X * e).groupby(d["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"n": len(d), "days": d["day"].nunique(), "slope": beta, "t_cl": beta / se})
    G10 = B[B.pos % 10 == 0]; G5 = B[B.pos % 5 == 0]
    T10 = G10[G10.regime == "trending"]; N10 = G10[G10.regime != "trending"]
    res = {}
    for nm, d in [("thin all r28", (T10, "r28", "ex10")), ("thin r28<0", (T10[T10.r28 < 0], "r28", "ex10")),
                  ("thin r28>0", (T10[T10.r28 > 0], "r28", "ex10")), ("thin r28z", (T10, "r28z", "ex10")),
                  ("thin forecast", (T10[T10.fc < 0], "fc", "ex10")), ("thin r14", (T10, "r14", "ex10")),
                  ("notthin r28", (N10, "r28", "ex10")), ("all r28", (G10, "r28", "ex10")),
                  ("thin r28 h5", (G5[G5.regime == "trending"], "r28", "ex5"))]:
        res[nm] = ct(*d)
    out["pooled slopes"] = pd.DataFrame(res).T
    out["thin all r28 by year"] = T10.groupby("year").apply(lambda d: ct(d, "r28", "ex10"))
    out["thin all r28 by coin"] = T10.groupby("coin").apply(lambda d: ct(d, "r28", "ex10"))
    out["notthin r28 by year"] = N10.groupby("year").apply(lambda d: ct(d, "r28", "ex10"))
    out["corr r28 vs forecast on thin fallen"] = T10[T10.fc < 0][["r28", "r28z", "fc"]].corr()
    return out
