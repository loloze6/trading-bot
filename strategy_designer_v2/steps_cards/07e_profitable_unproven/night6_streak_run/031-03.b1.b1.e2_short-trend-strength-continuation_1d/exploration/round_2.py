import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"].astype(float)
            r = cl.pct_change()
            alloc = b["postRebalance_current_allocation"].astype(float)
            vol = r.rolling(60, min_periods=30).std()
            s10 = (cl / cl.shift(10) - 1) / vol
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": c, "win": w, "pos": np.arange(len(b)), "ts": ts,
                               "year": ts.dt.year, "r": r, "alloc_prev": alloc.shift(1),
                               "s10_prev": s10.shift(1), "s10": s10, "vol": vol,
                               "fc": b["forecast"].astype(float)})
            for h in (5, 10):
                df[f"f{h}"] = cl.shift(-h) / cl - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r"].mean()
    D["mu"] = D["coin"].map(mu)
    D["timing"] = D["alloc_prev"] * (D["r"] - D["mu"])
    D["gain"] = D["alloc_prev"] * D["r"]
    # where the book earns: by s10 quintile of the bar before
    q = D.dropna(subset=["s10_prev", "gain"]).copy()
    q["bin"] = pd.qcut(q["s10_prev"], 5, labels=False)
    out["book gain by prior s10 quintile"] = q.groupby("bin").agg(
        s10=("s10_prev", "median"), alloc=("alloc_prev", "mean"), gain_sum=("gain", "sum"),
        timing_sum=("timing", "sum"), n=("gain", "size")).round(4)
    # alloc vs vol: does sizing load low-vol periods
    q["vbin"] = q.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["gain by own-vol tercile"] = q.groupby("vbin").agg(alloc=("alloc_prev", "mean"), r=("r", "mean"),
        gain_sum=("gain", "sum"), timing_sum=("timing", "sum"), n=("r", "size")).round(5)
    res, yr, cn = [], [], []
    for h in (5, 10):
        g = D[(D.pos % h == 0)].dropna(subset=["s10", f"f{h}"]).copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g["coin"].map(drift)
        g["dec"] = pd.qcut(g["s10"], 10, labels=False)
        for d, gg in g.groupby("dec"):
            dd = gg.groupby("ts")["ex"].sum()
            tday = gg.ex.mean() / (np.sqrt((dd**2).sum()) / len(gg))
            res.append({"h": h, "dec": d, "s10": gg.s10.median(), "ex": gg.ex.mean(),
                        "t_day": tday, "n": len(gg), "days": len(dd)})
        top = g[g.dec >= 8]
        for y, gg in top.groupby("year"):
            yr.append({"h": h, "year": y, "ex": gg.ex.mean(), "n": len(gg)})
        for c, gg in top.groupby("coin"):
            cn.append({"h": h, "coin": c, "ex": gg.ex.mean(), "n": len(gg)})
        # graded inside positive s10
        pos = g[g.s10 > 0]
        sl = stats.linregress(pos.s10, pos.ex)
        res.append({"h": h, "dec": "slope s10>0", "s10": sl.slope, "ex": np.nan,
                    "t_day": sl.slope / sl.stderr, "n": len(pos), "days": np.nan})
    out["fwd excess by s10 decile"] = pd.DataFrame(res).round(5)
    out["top 20% s10 by year"] = pd.DataFrame(yr).pivot(index="year", columns="h", values="ex").round(4)
    cdf = pd.DataFrame(cn)
    out["top 20% s10 by coin"] = cdf.pivot(index="coin", columns="h", values="ex").round(4)
    out["top 20% coins positive share"] = cdf.groupby("h")["ex"].apply(lambda x: (x > 0).mean())
    return out
