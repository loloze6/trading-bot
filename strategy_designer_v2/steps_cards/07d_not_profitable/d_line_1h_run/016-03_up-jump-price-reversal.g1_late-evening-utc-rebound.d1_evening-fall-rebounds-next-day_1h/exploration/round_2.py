def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        allr24 = []
        for w, b in ws.items():
            cl = b["close"].values
            if len(cl) > 24:
                a = cl[0::24]; allr24.extend(list(a[1:] / a[:-1] - 1))
        m24 = np.nanmean(allr24)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(b)
            hi = b["high"].values; lo = b["low"].values
            lr = np.full(n, np.nan); lr[1:] = np.log(cl[1:] / cl[:-1])
            idx = np.where(b["regime"].values == "mean_reversion")[0]
            for i in idx:
                if i + 24 >= n or i < 168:
                    continue
                r24p = cl[i] / cl[i - 24] - 1
                r7d = cl[i - 24] / cl[i - 168] - 1
                h = lr[i - 23:i + 1]
                vol = np.nanstd(lr[i - 167:i + 1])
                # path: share of the 24h move made by the largest hour
                big = np.nanmax(np.abs(h)) / (np.nansum(np.abs(h)) + 1e-12)
                rows.append(dict(coin=c, w=w, f=b["forecast"].iloc[i], alloc=b["postRebalance_current_allocation"].iloc[i],
                                 r24=cl[i + 24] / cl[i] - 1, ex24=cl[i + 24] / cl[i] - 1 - m24,
                                 r7d=r7d, r24p=r24p, vol=vol, big=big))
    r = pd.DataFrame(rows)
    p = r[r.f > 0].copy()
    # hypothetical 24h hold, same allocation, 0.1% each side? use 0.2% round trip as observed fee per trade ~0.1% total
    p["net24_01"] = p.alloc * p.r24 - p.alloc.abs() * 0.001
    out["hold24_hyp"] = pd.Series({"n": len(p), "mean_alloc_r24": (p.alloc * p.r24).mean(),
                                   "mean_net24": p.net24_01.mean(),
                                   "t_net24": stats.ttest_1samp(p.net24_01, 0).statistic,
                                   "sharpe_daily_ann_approx": p.net24_01.mean() / p.net24_01.std() * np.sqrt(365)})
    p["trend7"] = np.where(p.r7d < 0, "prior7d_down", "prior7d_up")
    out["by_prior_week"] = p.groupby("trend7").agg(n=("f", "size"), ex24=("ex24", "mean"),
                                                   t=("ex24", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    p["bigq"] = pd.qcut(p.big, 3, labels=["grind", "mid", "jump"])
    out["by_path_shape"] = p.groupby("bigq").agg(n=("f", "size"), ex24=("ex24", "mean"),
                                                t=("ex24", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    p["volq"] = pd.qcut(p.vol, 3, labels=["lowvol", "midvol", "highvol"])
    out["by_vol"] = p.groupby("volq").agg(n=("f", "size"), ex24=("ex24", "mean"),
                                          t=("ex24", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # slope of ex24 on forecast inside each path tercile
    sl = {}
    for k, g in p.groupby("bigq"):
        s = stats.linregress(g.f, g.ex24); sl[k] = s.slope / s.stderr
    out["slope_t_by_path"] = pd.Series(sl)
    p["year"] = None
    return out
