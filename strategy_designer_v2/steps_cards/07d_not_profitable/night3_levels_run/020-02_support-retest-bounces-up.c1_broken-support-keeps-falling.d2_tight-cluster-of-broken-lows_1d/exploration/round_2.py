def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    grid = []
    for coin, wins in data["bars"].items():
        mus = {}
        for h in [5, 10, 20]:
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr += list(c[idx + h] / c[idx] - 1)
            mus[h] = np.mean(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            cv = c.values
            raw = b["debug_info.components.support_cluster.last_history_value"].values
            r60 = (c / c.shift(60) - 1).values
            r20 = (c / c.shift(20) - 1).values
            r5 = (c / c.shift(5) - 1).values
            vol = c.pct_change().rolling(30).std().values
            for h in [5, 10, 20]:
                idx = np.arange(0, len(cv) - h, h)
                grid.append(pd.DataFrame({"h": h, "coin": coin, "win": w, "fc": b["forecast"].values[idx],
                    "raw": raw[idx], "f": cv[idx + h] / cv[idx] - 1,
                    "ex": cv[idx + h] / cv[idx] - 1 - mus[h], "r60": r60[idx], "r20": r20[idx],
                    "r5": r5[idx], "vol": vol[idx]}))
    G = pd.concat(grid)
    g5 = G[G.h == 5]
    # raw component (count x nearness) graded, all grid bars
    s = g5.dropna(subset=["raw"]).copy()
    s["has"] = s.raw > 0
    pos = s[s.has].copy()
    pos["q"] = pd.qcut(pos.raw.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["raw_quartiles_5d"] = pos.groupby("q").agg(n=("f", "size"), raw=("raw", "mean"), f=("f", "mean"), ex=("ex", "mean"))
    out["raw_zero_5d"] = pd.Series({"n": (~s.has).sum(), "f": s[~s.has].f.mean(), "ex": s[~s.has].ex.mean()})
    if len(pos) > 10:
        sl = stats.linregress(pos.raw, pos.ex)
        out["slope_raw_ex"] = pd.Series({"n": len(pos), "slope": sl.slope, "t": sl.slope / sl.stderr})
    # horizons for largest-third short forecast
    rows = []
    for h in [5, 10, 20]:
        gh = G[(G.h == h) & (G.fc < 0)].copy()
        gh["q"] = pd.qcut((-gh.fc).rank(method="first"), 3, labels=["small", "mid", "large"])
        for q, d in gh.groupby("q"):
            rows.append({"h": h, "q": q, "n": len(d), "f": d.f.mean(), "ex": d.ex.mean(),
                         "t_f": d.f.mean() / (d.f.std() / np.sqrt(len(d)))})
    out["horizon_terciles"] = pd.DataFrame(rows)
    # large-short tercile by 20-day and 60-day past return
    nz = g5[g5.fc < 0].copy()
    nz["q"] = pd.qcut((-nz.fc).rank(method="first"), 3, labels=["small", "mid", "large"])
    for k in ["r20", "r60", "r5"]:
        d = nz.dropna(subset=[k]).copy()
        d["t"] = pd.qcut(d[k], 4, labels=["q1low", "q2", "q3", "q4high"])
        out["fq_x_" + k] = d.groupby(["q", "t"]).agg(n=("f", "size"), f=("f", "mean"), k=(k, "mean")).reset_index()
    # past 60d return graded among all raw>0 cases
    d = pos.dropna(subset=["r60"]).copy()
    d["t"] = pd.qcut(d.r60, 5, labels=["a", "b", "c", "d", "e"])
    out["rawpos_by_r60"] = d.groupby("t").agg(n=("f", "size"), r60=("r60", "mean"), f=("f", "mean"), t_f=("f", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    return out
