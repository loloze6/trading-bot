import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    def build(h):
        rows = []
        for coin, ws in bars.items():
            allret = []
            per = []
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values; hi = df["high"].values; lo = df["low"].values
                n = len(df)
                yrs = pd.to_datetime(df["timestamp"]).dt.year.values
                for i in range(0, n - h, h):
                    r = c[i + h] / c[i] - 1
                    allret.append(r)
                    if i == 0:
                        continue
                    r1 = c[i] / c[i - 1] - 1
                    rng = hi[i] - lo[i]
                    cl = (c[i] - lo[i]) / rng if rng > 0 else np.nan
                    # prior 20-day return inside window
                    p20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                    per.append((coin, w, yrs[i], r, r1, cl, p20, rng / c[i]))
            mu = np.mean(allret)
            for p in per:
                rows.append(p + (p[3] - mu,))
        return pd.DataFrame(rows, columns=["coin", "win", "year", "r", "r1", "cl", "p20", "rngpct", "ex"])

    def slope_t(d):
        d = d.dropna(subset=["cl", "ex"])
        if len(d) < 20:
            return (np.nan, np.nan, len(d))
        res = stats.linregress(d["cl"], d["ex"])
        return (res.slope, res.slope / res.stderr, len(d))

    out = {}
    hz = {}
    for h in [1, 2, 3, 5, 7, 10]:
        D = build(h)
        dn = D[D.r1 < 0]; up = D[D.r1 > 0]
        s, t, n = slope_t(dn); s2, t2, n2 = slope_t(up)
        hz[h] = {"down_slope": s, "down_t": t, "down_n": n, "up_slope": s2, "up_t": t2, "up_n": n2,
                 "down_mean_ex": dn.ex.mean(), "down_mean_t": dn.ex.mean() / (dn.ex.std() / np.sqrt(len(dn)))}
    out["by_horizon"] = pd.DataFrame(hz).T

    D = build(3); dn = D[D.r1 < 0].dropna(subset=["cl"]).copy()
    dn["q"] = pd.qcut(dn.cl, 5, labels=False)
    g = dn.groupby("q").ex.agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["down_cl_quintiles_3d"] = g
    out["by_coin"] = pd.DataFrame({c: slope_t(x) for c, x in dn.groupby("coin")}, index=["slope", "t", "n"]).T
    out["by_year"] = pd.DataFrame({y: slope_t(x) for y, x in dn.groupby("year")}, index=["slope", "t", "n"]).T
    dn["r1q"] = dn.groupby("coin").r1.transform(lambda s: pd.qcut(s, 3, labels=False))
    out["by_downsize_tercile(0=largest fall)"] = pd.DataFrame({c: slope_t(x) for c, x in dn.groupby("r1q")}, index=["slope", "t", "n"]).T
    dn["trend"] = np.where(dn.p20 > 0, "p20_up", np.where(dn.p20 <= 0, "p20_down", "na"))
    out["by_trend20"] = pd.DataFrame({c: slope_t(x) for c, x in dn.groupby("trend")}, index=["slope", "t", "n"]).T
    dn["rq"] = dn.groupby("coin").rngpct.transform(lambda s: pd.qcut(s, 3, labels=False))
    out["by_range_tercile(2=widest)"] = pd.DataFrame({c: slope_t(x) for c, x in dn.groupby("rq")}, index=["slope", "t", "n"]).T

    # book: position share and timing
    pos = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            a = df["postRebalance_current_allocation"]
            pos.append(((a.abs() > 1e-9).mean(), a.mean(), (df["regime"] == "mean_reversion").mean()))
    out["book_pos_share_meanalloc_downshare"] = pd.Series(np.mean(pos, axis=0), index=["in_pos_share", "mean_alloc", "down_bar_share"])
    return out
