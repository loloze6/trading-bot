import pandas as pd, numpy as np
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0: return np.nan
    return x.mean() / (x.std() / np.sqrt(len(x)))

def explore(data):
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            vol = lr.rolling(20).std().shift(1)
            d = pd.DataFrame({"coin": coin, "win": w,
                              "yr": pd.to_datetime(b["timestamp"]).dt.year,
                              "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                              "r1": c / c.shift(1) - 1, "z1": (c / c.shift(1) - 1) / vol,
                              "r3": c / c.shift(3) - 1, "z3": (c / c.shift(3) - 1) / (vol * np.sqrt(3)),
                              "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f3": c.shift(-3) / c - 1,
                              "pos": np.arange(len(c))})
            recs.append(d)
    D = pd.concat(recs)
    for h in [1, 2, 3]:
        D["e%d" % h] = D["f%d" % h] - D.groupby("coin")["f%d" % h].transform(lambda v: v[D.loc[v.index, "pos"] % h == 0].mean())
    # graded reversal: next-day excess by quintile of z1 (signed), per coin quintiles
    X = D.dropna(subset=["z1", "e1"]).copy()
    X["q"] = X.groupby("coin")["z1"].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
    r = X.groupby("q").agg(n=("e1", "size"), mean_e1=("e1", "mean"), z_lo=("z1", "min"), z_hi=("z1", "max"))
    r["t"] = X.groupby("q")["e1"].apply(_t)
    out["next1d_excess_by_z1_quintile"] = r
    # correlation per coin and per year
    out["corr_z1_e1_by_coin"] = X.groupby("coin").apply(lambda z: pd.Series({"n": len(z), "pearson": z["z1"].clip(-4, 4).corr(z["e1"]), "spearman": stats.spearmanr(z["z1"], z["e1"])[0]}))
    out["corr_z1_e1_by_year"] = X.groupby("yr").apply(lambda z: pd.Series({"n": len(z), "spearman": stats.spearmanr(z["z1"], z["e1"])[0]}))
    # 3-day: z3 vs next 3 days on a 3-day grid
    Y = D[(D["pos"] % 3 == 0)].dropna(subset=["z3", "e3"]).copy()
    Y["q"] = Y.groupby("coin")["z3"].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
    r3 = Y.groupby("q").agg(n=("e3", "size"), mean_e3=("e3", "mean"))
    r3["t"] = Y.groupby("q")["e3"].apply(_t)
    out["next3d_excess_by_z3_quintile"] = r3
    out["spearman_z3_e3_by_coin"] = Y.groupby("coin").apply(lambda z: stats.spearmanr(z["z3"], z["e3"])[0])
    # weekday stability: Thu+Fri minus Mon+Wed next-day return, by coin and by year
    D2 = D.dropna(subset=["f1"]).copy()
    D2["grp"] = np.where(D2["wd"].isin([3, 4]), "thufri", np.where(D2["wd"].isin([0, 2]), "monwed", "other"))
    def wdiff(z):
        a = z.loc[z["grp"] == "thufri", "f1"]; b = z.loc[z["grp"] == "monwed", "f1"]
        return pd.Series({"diff": a.mean() - b.mean(), "t": stats.ttest_ind(a, b, equal_var=False)[0], "n": len(a) + len(b)})
    out["weekday_diff_by_coin"] = D2.groupby("coin").apply(wdiff)
    out["weekday_diff_by_year"] = D2.groupby("yr").apply(wdiff)
    return out
