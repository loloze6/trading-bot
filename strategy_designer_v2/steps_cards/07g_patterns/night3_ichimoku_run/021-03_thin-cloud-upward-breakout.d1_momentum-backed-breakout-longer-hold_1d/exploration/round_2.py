import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    days = data["days"]
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy().reset_index(drop=True); d["coin"] = c; d["win"] = w
            d["dt"] = pd.to_datetime(d["day"])
            d["wd"] = d["dt"].dt.dayofweek; d["yr"] = d["dt"].dt.year
            sd = d["coin_return"].rolling(20, min_periods=10).std().shift(1)
            d["sd"] = sd
            d["z"] = d["coin_return"] / sd
            cl = d["close"].values; n = len(cl)
            for h in [1, 3, 5, 10]:
                d[f"f{h}"] = pd.Series(cl).shift(-h).values / cl - 1
            d["z3"] = (pd.Series(cl) / pd.Series(cl).shift(3) - 1) / (sd * np.sqrt(3))
            d["z5"] = (pd.Series(cl) / pd.Series(cl).shift(5) - 1) / (sd * np.sqrt(5))
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    for h in [1, 3, 5, 10]:
        D[f"a{h}"] = D[f"f{h}"] - D.groupby("coin")[f"f{h}"].transform("mean")
    def tt(s):
        s = s.dropna(); return pd.Series({"mean": s.mean(), "n": len(s), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    # A: reversal after a down day, by horizon, on non-overlapping grids (positions 0,h,2h,...)
    res = []
    for h in [1, 3, 5, 10]:
        for zc in ["z", "z3", "z5"]:
            sub = D[D.groupby(["coin", "win"]).cumcount() % h == 0].dropna(subset=[zc, f"a{h}"])
            r, p = stats.spearmanr(sub[zc], sub[f"a{h}"])
            # slope of unusual move normalised by sd on -z
            y = sub[f"a{h}"] / (sub["sd"] * np.sqrt(h))
            sl = stats.linregress(sub[zc], y)
            res.append(dict(h=h, sit=zc, rho=r, p=p, slope=sl.slope, t=sl.slope / sl.stderr, n=len(sub)))
    out["reversal_grid"] = pd.DataFrame(res)
    # B: day-1 after down moves, by coin, by year (deduplicated per coin)
    sub = D.dropna(subset=["z", "a1"]).copy()
    sub["down"] = sub["z"] <= -1
    out["rev1_by_coin"] = sub[sub.down].groupby("coin")["a1"].apply(tt).unstack()
    out["rev1_by_year"] = sub[sub.down].groupby("yr")["a1"].apply(tt).unstack()
    out["rev1_graded_down"] = sub[sub.z < 0].groupby(pd.cut(sub.z[sub.z < 0], [-99, -3, -2, -1.5, -1, -0.5, 0]))["a1"].apply(tt).unstack()
    # cross-coin dependence: per day, mean a1 of the down-day coins, t over days
    dd = sub[sub.down].groupby("day")["a1"].mean()
    out["rev1_by_day_dedup"] = tt(dd).to_frame().T
    # C: weekday, by coin and year, and dedup per day
    D["a1d"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    out["sat_by_coin"] = D[D.wd == 5].groupby("coin")["a1d"].apply(tt).unstack()
    out["sat_by_year"] = D[D.wd == 5].groupby("yr")["a1d"].apply(tt).unstack()
    dm = D.groupby(["day", "wd"])["a1d"].mean().reset_index()
    out["weekday_dedup"] = dm.groupby("wd")["a1d"].apply(tt).unstack()
    # weekend graded by friday? Saturday return vs prior 5-day z
    s5 = D[D.wd == 5].dropna(subset=["z5", "a1d"])
    r, p = stats.spearmanr(s5["z5"], s5["a1d"])
    out["sat_vs_prior5"] = f"rho={r:.3f} p={p:.4f} n={len(s5)}"
    # D: reversal conditional on vol level
    sub["vq"] = sub.groupby("coin")["sd"].transform(lambda s: pd.qcut(s.rank(method='first'), 3, labels=False))
    out["rev1_down_by_vol"] = sub[sub.down].groupby("vq")["a1"].apply(tt).unstack()
    # E: book days: after book's largest gains/losses
    B = D.dropna(subset=["book_return"]).copy()
    B["nb"] = B.groupby(["coin", "win"])["book_return"].shift(-1)
    B = B[B["book_return"] != 0]
    B["bq"] = B.groupby("coin")["book_return"].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
    out["book_next_by_q"] = B.groupby("bq")["nb"].apply(tt).unstack()
    return out
