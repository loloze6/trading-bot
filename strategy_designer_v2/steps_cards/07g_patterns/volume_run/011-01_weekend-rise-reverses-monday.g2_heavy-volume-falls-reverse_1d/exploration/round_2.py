import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r = c.pct_change()
            sd = r.rolling(20, min_periods=10).std().shift(1)
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ret": r, "fwd1": c.shift(-1)/c - 1, "fwd2": c.shift(-2)/c - 1,
                "z": r/sd,
                "vr": b["volume"]/b["volume"].rolling(60, min_periods=20).mean(),
                "clv": ((c - l) - (h - c))/rng,
                "rngz": (rng/c)/((rng/c).rolling(20, min_periods=10).mean().shift(1)),
                "wd": ts.dt.weekday.values, "yr": ts.dt.year.values,
                "fc": b["forecast"].values,
            })
            d["z2"] = (c/c.shift(2) - 1)/(sd*np.sqrt(2))
            d["idx"] = np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["ret"].mean()
    D["ex1"] = D["fwd1"] - D["coin"].map(mu)
    D["ex2"] = D["fwd2"] - 2*D["coin"].map(mu)
    D["wnum"] = D["win"].str[1:].astype(int)
    D["half"] = np.where(D["wnum"] <= 12, "w1-12", "w13-24")

    def summ(g, col="ex1"):
        x = g[col].dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan})
    def reg(g, xcol, ycol="ex1"):
        g = g[[xcol, ycol]].replace([np.inf, -np.inf], np.nan).dropna()
        if len(g) < 20: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        res = stats.linregress(g[xcol], g[ycol])
        return pd.Series({"n": len(g), "slope": res.slope, "t": res.slope/res.stderr})
    out = {}
    # Saturday rise reversal: graded, stable?
    sat = D[(D["wd"] == 5)]
    out["sat: ex1 on z, by half"] = sat.groupby("half").apply(lambda g: reg(g, "z"))
    out["sat: ex1 on z, all + by coin"] = pd.concat([reg(sat, "z").to_frame("all").T, sat.groupby("coin").apply(lambda g: reg(g, "z"))])
    out["weekday: ex1 on z slope"] = D.groupby("wd").apply(lambda g: reg(g, "z"))
    # weekend 2-day move (Sun bar, z2 = Sat+Sun) -> Monday and Mon+Tue
    sun = D[D["wd"] == 6]
    out["sun: ex1/ex2 on 2d weekend z"] = pd.DataFrame({"ex1": reg(sun, "z2"), "ex2": reg(sun, "z2", "ex2")}).T
    # falls: graded by volume ratio, and close location
    f = D[D["z"] < -1]
    out["falls z<-1: ex1 on vr, by half"] = pd.concat([reg(f, "vr").to_frame("all").T, f.groupby("half").apply(lambda g: reg(g, "vr"))])
    out["falls z<-1: ex1 on clv, by half"] = pd.concat([reg(f, "clv").to_frame("all").T, f.groupby("half").apply(lambda g: reg(g, "clv"))])
    out["all bars: ex1 on clv, by half"] = pd.concat([reg(D, "clv").to_frame("all").T, D.groupby("half").apply(lambda g: reg(g, "clv"))])
    D["clvq"] = pd.qcut(D["clv"], 5, labels=False, duplicates="drop")
    out["all bars: ex1 by clv quintile"] = D.groupby("clvq").apply(summ)
    out["all: ex1 on range ratio, by half"] = pd.concat([reg(D, "rngz").to_frame("all").T, D.groupby("half").apply(lambda g: reg(g, "rngz"))])
    # big falls by weekday, by half (Mon/Fri no rebound?)
    out["falls z<-1 by weekday x half (t)"] = f.groupby(["wd", "half"]).apply(summ)["t"].unstack()
    # unconditional weekday by half
    out["all: ex1 by weekday x half (t)"] = D.groupby(["wd", "half"]).apply(summ)["t"].unstack()
    # active bars: by year
    out["active bars by year"] = D[D["fc"] > 0].groupby("yr").apply(summ)
    return out
