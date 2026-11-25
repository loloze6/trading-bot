import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "f3": c.shift(-3) / c - 1, "f1": c.shift(-1) / c - 1,
                               "z5": (c / c.shift(5) - 1) / (sd30 * np.sqrt(5)),
                               "z10": (c / c.shift(10) - 1) / (sd30 * np.sqrt(10)),
                               "z20": (c / c.shift(20) - 1) / (sd30 * np.sqrt(20)),
                               "z1": r1 / sd30, "sd30": sd30,
                               "rising": (b["regime"] == "unknown").values,
                               "day": ts.dt.floor("D"), "wd": ts.dt.weekday, "yr": ts.dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % 3 == 0].dropna(subset=["f3"]).copy()
    drift = g.groupby("coin")["f3"].mean()
    g["ex3"] = g["f3"] - g["coin"].map(drift)

    def slope_dayclust(x, col):
        x = x.dropna(subset=[col, "ex3"])
        X = x[col] - x[col].mean()
        b = (X * x["ex3"]).sum() / (X ** 2).sum()
        e = x["ex3"] - x["ex3"].mean() - b * X
        sc = (X * e).groupby(x["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
        return b, b / se, len(x), x["day"].nunique()
    res = {}
    for rg, x in g.groupby("rising"):
        for col in ["z1", "z5", "z10", "z20"]:
            bb, t, n, nd = slope_dayclust(x, col)
            res[f"rising={rg} {col}"] = {"slope": bb, "t_dayclust": t, "n": n, "days": nd}
    out["slope ex3 on scaled past return, day-clustered"] = pd.DataFrame(res).T

    # per-window slope sign for z5 and z10
    ws = {}
    for (rg, w), x in g.groupby(["rising", "win"]):
        x = x.dropna(subset=["z10"])
        if len(x) > 15:
            ws[f"{rg} {w}"] = {"n": len(x), "slope_z5": np.polyfit(x["z5"], x["ex3"], 1)[0], "slope_z10": np.polyfit(x["z10"], x["ex3"], 1)[0]}
    W = pd.DataFrame(ws).T
    out["per-window slopes"] = W

    # vol tercile within coin, rising: day-clustered t of mean, and slope of ex3 on sd30 rank
    g["volr"] = g.groupby("coin")["sd30"].rank(pct=True)
    r = g[g["rising"]]
    bb, t, n, nd = slope_dayclust(r, "volr")
    out["rising: slope ex3 on vol rank (dayclust)"] = pd.Series({"slope": bb, "t": t, "n": n, "days": nd})
    out["rising: low-vol tercile by window"] = r.assign(lo=r["volr"] <= 1/3).groupby(["win", "lo"])["ex3"].mean().unstack()

    # weekday next-day return by year
    d1 = d.dropna(subset=["f1"]).copy()
    d1["thfr"] = d1["wd"].isin([3, 4])
    out["f1 Thu/Fri vs other by year"] = d1.groupby(["yr", "thfr"])["f1"].mean().unstack()
    dd = d1.groupby(["day", "thfr"])["f1"].mean().reset_index()
    out["f1 day-level t Thu/Fri minus other"] = pd.Series(dict(zip(["t", "p"], stats.ttest_ind(dd[dd.thfr]["f1"], dd[~dd.thfr]["f1"], equal_var=False))))

    # book daily returns: share of gain on rising-z5-top days etc; and book largest days
    days = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            days.append(x.assign(coin=coin, win=w))
    D = pd.concat(days, ignore_index=True)
    bk = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.02, 0.98])
    out["book extreme days: mean coin return"] = pd.DataFrame({
        "worst2%": bk[bk.book_return <= q.iloc[0]].mean(), "best2%": bk[bk.book_return >= q.iloc[1]].mean(), "all": bk.mean()})
    return out
