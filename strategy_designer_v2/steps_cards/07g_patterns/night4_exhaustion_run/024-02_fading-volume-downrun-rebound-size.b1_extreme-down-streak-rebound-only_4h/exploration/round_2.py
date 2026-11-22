def explore(data):
    import numpy as np, pandas as pd
    H = 18
    out = {}
    hr = []; grid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            absm = r1.abs().rolling(180, min_periods=45).mean()
            nxt = c.shift(-1) / c - 1
            vrel = v / v.rolling(180, min_periods=45).mean()
            p6 = (c / c.shift(6) - 1) / (absm * np.sqrt(6))
            hr.append(pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                "y": ts.dt.year, "nxt": nxt, "r1u": r1 / absm, "vrel": vrel, "p6": p6}))
            fwd = c.shift(-H) / c - 1
            f6 = c.shift(-6) / c - 1
            d = pd.DataFrame({"coin": coin, "w": w, "y": ts.dt.year, "fwd": fwd, "f6": f6, "p6": p6,
                              "vrel6": v.rolling(6).mean() / v.rolling(180, min_periods=45).mean()})
            grid.append(d[np.arange(len(b)) % H == 0])
    Hh = pd.concat(hr).dropna(subset=["nxt"])
    Hh["exc"] = Hh["nxt"] - Hh.groupby("coin")["nxt"].transform("mean")
    def summ(gr):
        x = gr["exc"].dropna(); n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    h16 = Hh[Hh.hour.isin([16, 20])]
    out["hour16/20 by coin"] = h16.groupby(["hour", "coin"]).apply(summ)
    out["hour16/20 by year"] = h16.groupby(["hour", "y"]).apply(summ)
    out["hour16/20 by weekday"] = h16.groupby(["hour", "wd"]).apply(summ)
    # graded? hour 16/20 by prior bar's signed move tercile
    h16 = h16.dropna(subset=["r1u"]).copy()
    h16["rq"] = h16.groupby("hour")["r1u"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["hour16/20 by prior 4h move quintile"] = h16.groupby(["hour", "rq"]).apply(summ)
    h16["vq"] = h16.groupby("hour")["vrel"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["hour16/20 by volume quartile"] = h16.groupby(["hour", "vq"]).apply(summ)
    fr = Hh[Hh.wd == 4]
    out["friday by hour"] = fr.groupby("hour").apply(summ)
    out["friday by year"] = fr.groupby("y").apply(summ)
    G = pd.concat(grid).dropna(subset=["fwd", "p6"])
    G["exc"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    G["side"] = np.sign(G["p6"])
    G["q"] = pd.qcut(G["p6"], 20, labels=False, duplicates="drop")
    out["fwd18 exc by p6 vigintile"] = G.groupby("q").apply(summ)
    low = G[G.q <= 1]
    out["p6 bottom 10%: by coin"] = low.groupby("coin").apply(summ)
    out["p6 bottom 10%: by year"] = low.groupby("y").apply(summ)
    low2 = low.dropna(subset=["vrel6"]).copy()
    low2["vq"] = pd.qcut(low2["vrel6"], 3, labels=False, duplicates="drop")
    out["p6 bottom 10%: by recent volume tercile"] = low2.groupby("vq").apply(summ)
    out["corr p6 vs exc, lower half"] = float(G[G.p6 < 0][["p6", "exc"]].corr().iloc[0, 1])
    out["n lower half"] = int((G.p6 < 0).sum())
    return out
