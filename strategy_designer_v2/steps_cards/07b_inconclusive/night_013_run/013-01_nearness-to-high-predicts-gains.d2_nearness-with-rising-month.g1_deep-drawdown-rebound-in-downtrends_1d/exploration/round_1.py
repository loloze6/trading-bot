import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    H = [1, 3, 7, 14, 30]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            ret30 = c / c.shift(30) - 1
            depth = c / c.rolling(60, min_periods=20).max() - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            reg = (b["regime"] == "mean_reversion")
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, year=int(yr[i]), h=h,
                                     fwd=c[i + h] / c[i] - 1, fc=float(b["forecast"].iloc[i]),
                                     reg=bool(reg[i]), r30=ret30[i], depth=depth[i]))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    out = {}

    def slope_t(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 10 or d[x].std() == 0:
            return (np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d["ex"])
        return (r.slope, r.slope / r.stderr, len(d))

    # by horizon, regime bars: forecast and raw depth (negated so positive = deeper)
    res = []
    for h in H:
        d = df[(df.h == h) & df.reg].copy()
        d["deep"] = -d["depth"]
        a = slope_t(d, "fc"); b = slope_t(d, "deep")
        dn = df[(df.h == h) & ~df.reg].copy(); dn["deep"] = -dn["depth"]
        cc = slope_t(dn, "deep")
        res.append(dict(h=h, fc_slope=a[0], fc_t=a[1], n=a[2], depth_slope=b[0], depth_t=b[1],
                        nonreg_depth_t=cc[1], nonreg_n=cc[2]))
    out["by_horizon"] = pd.DataFrame(res)

    d7 = df[(df.h == 7) & df.reg].copy()
    d7["deep"] = -d7["depth"]
    out["by_coin_h7"] = pd.DataFrame([dict(coin=k, slope=slope_t(g, "fc")[0], t=slope_t(g, "fc")[1],
                                           tdepth=slope_t(g, "deep")[1], n=len(g), meanex=g.ex.mean())
                                      for k, g in d7.groupby("coin")])
    out["by_year_h7"] = pd.DataFrame([dict(year=k, t=slope_t(g, "fc")[1], tdepth=slope_t(g, "deep")[1],
                                           n=len(g), meanex=g.ex.mean())
                                      for k, g in d7.groupby("year")])
    d7["dq"] = pd.qcut(d7["deep"], 5, labels=False, duplicates="drop")
    out["depth_quintile_h7"] = d7.groupby("dq").agg(deep_mean=("deep", "mean"), ex_mean=("ex", "mean"),
                                                   ex_std=("ex", "std"), n=("ex", "size"))
    d7["rq"] = pd.qcut(d7["r30"], 3, labels=False, duplicates="drop")
    out["r30_tercile_h7"] = pd.DataFrame([dict(rq=k, r30=g.r30.mean(), t=slope_t(g, "deep")[1],
                                               meanex=g.ex.mean(), n=len(g)) for k, g in d7.groupby("rq")])
    d30 = df[(df.h == 30) & df.reg].copy(); d30["deep"] = -d30["depth"]
    d30["dq"] = pd.qcut(d30["deep"], 5, labels=False, duplicates="drop")
    out["depth_quintile_h30"] = d30.groupby("dq").agg(deep_mean=("deep", "mean"), ex_mean=("ex", "mean"), n=("ex", "size"))
    out["corr_fc_depth"] = float(d7[["fc", "deep"]].dropna().corr().iloc[0, 1])
    return out
