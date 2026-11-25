def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rr = ((h - l) / c).rolling(30).mean()
            r1 = c / c.shift(1) - 1
            vol30 = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            d = {"coin": coin, "w": w, "pos": np.arange(len(b)), "s1": r1 / rr,
                 "z1": r1 / vol30, "tr60": c / c.shift(60) - 1, "vol30": vol30,
                 "year": ts.dt.year, "day": ts.dt.floor("D"),
                 "alloc": b["postRebalance_current_allocation"]}
            for hz in [1, 2, 3, 5]:
                d[f"f{hz}"] = c.shift(-hz) / c - 1
            rows.append(pd.DataFrame(d))
    A = pd.concat(rows, ignore_index=True)
    A["agit"] = A.groupby(["coin", "w"])["vol30"].transform(lambda v: v > v.expanding(30).median())
    for hz in [1, 2, 3, 5]:
        g = A[A.pos % hz == 0].dropna(subset=[f"f{hz}"])
        m = g.groupby("coin")[f"f{hz}"].mean()
        A[f"x{hz}"] = A[f"f{hz}"] - A["coin"].map(m)
    A["tr"] = pd.cut(A["tr60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    out = {}
    def summ(g, col):
        x = g[[col, "day"]].dropna()
        d = x.groupby("day")[col].sum()
        return pd.Series({"n": len(x), "days": len(d), "mean%": 100 * x[col].mean(),
                          "t_day": d.mean() / (d.std() / np.sqrt(len(d))) if len(d) > 2 else np.nan})
    FA = A[(A.tr == "fall") & (A.agit == True)]
    res = {}
    for hz in [1, 2, 3, 5]:
        g = FA[(FA.pos % hz == 0) & (FA.s1 > 0)].dropna(subset=[f"x{hz}", "s1"]).copy()
        sl = stats.linregress(g["s1"], g[f"x{hz}"])
        g["q"] = pd.qcut(g["s1"], 3, labels=False)
        top = summ(g[g.q == 2], f"x{hz}")
        res[f"h{hz}"] = pd.Series({"n_up": len(g), "slope": sl.slope, "slope_t": sl.slope / sl.stderr,
                                   "top3rd_mean%": top["mean%"], "top3rd_t_day": top["t_day"],
                                   "top3rd_days": top["days"]})
    out["fall-agit up-days: grade by horizon"] = pd.DataFrame(res).T
    g = FA[(FA.pos % 3 == 0) & (FA.s1 > 0)].dropna(subset=["x3", "s1"]).copy()
    g["q"] = pd.qcut(g["s1"], 4, labels=False)
    out["fall-agit up-days x3 by s1 quartile"] = g.groupby("q").apply(lambda z: pd.concat([summ(z, "x3"), pd.Series({"s1med": z.s1.median()})]))
    g["qz"] = pd.qcut(g["z1"], 4, labels=False)
    out["fall-agit up-days x3 by vol-scaled quartile"] = g.groupby("qz").apply(lambda z: summ(z, "x3"))
    top = g[g.q == 3]
    out["fall-agit top quartile by year"] = top.groupby("year").apply(lambda z: summ(z, "x3"))
    out["fall-agit top quartile by coin"] = top.groupby("coin").apply(lambda z: summ(z, "x3"))
    out["fall-agit up-days: book alloc mean"] = pd.Series({"alloc_top": top["alloc"].mean(), "alloc_all": g["alloc"].mean()})
    # other profiles up-days slope h3
    res2 = {}
    for (tr, ag), z in A[(A.pos % 3 == 0) & (A.s1 > 0)].dropna(subset=["x3", "s1", "tr"]).groupby(["tr", "agit"]):
        if len(z) > 20:
            sl = stats.linregress(z["s1"], z["x3"])
            res2[f"{tr}-{ag}"] = pd.Series({"n": len(z), "slope": sl.slope, "t": sl.slope / sl.stderr})
    out["up-days x3 slope on s1 by profile"] = pd.DataFrame(res2).T
    return out
