import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r = np.full(n, np.nan); r[1:] = c[1:]/c[:-1]-1
            sd = pd.Series(r).rolling(30, min_periods=20).std().shift(1).values
            runlen = np.zeros(n, int); rungain = np.zeros(n)
            for t in range(1, n):
                if r[t] < 0:
                    k = t-1; g = 1.0; L = 0
                    while k >= 1 and r[k] > 0 and L < 30:
                        g *= (1+r[k]); L += 1; k -= 1
                    runlen[t] = L; rungain[t] = g-1
            for t in range(n):
                d = {"coin": coin, "win": w, "pos": t, "regime": b["regime"].iloc[t],
                     "day": str(pd.Timestamp(b["timestamp"].iloc[t]).date()),
                     "year": pd.Timestamp(b["timestamp"].iloc[t]).year,
                     "r0": r[t], "runlen": runlen[t], "runz": rungain[t]/sd[t] if sd[t] > 0 else np.nan,
                     "dipz": r[t]/sd[t] if sd[t] > 0 else np.nan}
                for h in (1, 3, 5, 10):
                    d[f"f{h}"] = c[t+h]/c[t]-1 if t+h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    usual = {}
    for h in (1, 3, 5, 10):
        g = df[df["pos"] % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean(); sdv = g.groupby("coin")[f"f{h}"].std()
        df[f"u{h}"] = -(df[f"f{h}"] - df["coin"].map(dr))
        df[f"s{h}"] = df[f"u{h}"] / df["coin"].map(sdv)
    inp = df[df["regime"] != "chop"].copy()
    out = {}
    def summ(g, col):
        x = g.dropna(subset=[col])
        if len(x) < 3: return pd.Series({"n": len(x)})
        dd = x.groupby("day")[col].sum()
        m = x[col].mean()
        tcl = dd.sum()/np.sqrt(((dd - m*x.groupby("day").size())**2).sum()) if len(dd) > 1 else np.nan
        return pd.Series({"n": len(x), "days": len(dd), "mean%": 100*m, "t": m/(x[col].std()/np.sqrt(len(x))), "t_day": tcl})
    ev = inp[(inp["runlen"] > 0) & (inp["r0"] < 0)].copy()
    alld = inp[inp["r0"] < 0].copy()
    # graded on dip depth, continuous
    for name, s in (("first-dip", ev), ("all down days", alld)):
        tab = {}
        for h in (1, 3, 5, 10):
            x = s.dropna(subset=["dipz", f"u{h}"])
            res = stats.linregress(-x["dipz"], x[f"u{h}"])
            tab[f"u{h}"] = pd.Series({"slope%perSD": 100*res.slope, "t": res.slope/res.stderr, "n": len(x),
                                      "strength_mean": x[f"s{h}"].mean()})
        out[f"slope of short unusual on dip depth (SD), {name}"] = pd.DataFrame(tab)
    alld["dipq"] = pd.qcut(alld["dipz"], 3, labels=["deep", "mid", "shallow"])
    out["all in-profile down days by depth"] = pd.concat({f"u{h}": alld.groupby("dipq").apply(lambda g: summ(g, f"u{h}")) for h in (3, 5, 10)}, axis=1)
    ev["dipq"] = pd.qcut(ev["dipz"], 3, labels=["deep", "mid", "shallow"])
    deep = ev[ev["dipq"] == "deep"]
    out["first-dip deep, u5 by coin"] = deep.groupby("coin").apply(lambda g: summ(g, "u5"))
    out["first-dip deep, u5 by year"] = deep.groupby("year").apply(lambda g: summ(g, "u5"))
    out["first-dip all, u5/u10 day-clustered"] = pd.concat({h: summ(ev, h) for h in ("u5", "u10")}, axis=1)
    out["deep first-dip day-clustered"] = pd.concat({h: summ(deep, h) for h in ("u1", "u3", "u5", "u10")}, axis=1)
    out["all down days deep, u5 by coin"] = alld[alld["dipq"] == "deep"].groupby("coin").apply(lambda g: summ(g, "u5"))
    # baseline: in-profile up days next 5
    up = inp[inp["r0"] > 0]
    out["in-profile up days short unusual"] = pd.concat({h: summ(up, h) for h in ("u3", "u5", "u10")}, axis=1)
    out["dip depth tercile edges (SD)"] = pd.Series(alld["dipz"].quantile([1/3, 2/3]).values, index=["q33", "q67"])
    return out
