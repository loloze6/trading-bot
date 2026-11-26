def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = [1, 3, 5, 10, 20]
    rows = []
    coinmean = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            coinmean[(coin, h)] = np.mean(rs)
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values
            r = pd.Series(c).pct_change()
            sd = r.rolling(30).std().values
            raw = (pd.Series(c) / pd.Series(c).shift(14) - 1).values / (sd * np.sqrt(14))
            f = b["forecast"].values
            reg = b["regime"].values
            ts = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for h in H:
                for i in range(0, len(c) - h, h):
                    if reg[i] == "unknown" and f[i] < 0:
                        rows.append(dict(coin=coin, w=w, h=h, f=f[i], raw=raw[i], day=ts[i], yr=yr[i],
                                         ex=c[i + h] / c[i] - 1 - coinmean[(coin, h)],
                                         tot=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    def summ(g):
        n = len(g)
        m = g["ex"].mean()
        dm = g.groupby("day")["ex"].sum()
        t = m / (g["ex"].std() / np.sqrt(n)) if n > 2 else np.nan
        if n > 5 and g["f"].std() > 0:
            sl, ic, rr, p, se = stats.linregress(g["f"], g["ex"])
            tsl = sl / se
        else:
            sl = tsl = np.nan
        return pd.Series(dict(n=n, mean_ex=m, t_mean=t, slope=sl, t_slope=tsl, mean_tot=g["tot"].mean()))
    out["by_horizon"] = d.groupby("h").apply(summ)
    d5 = d[d.h == 5].copy()
    out["h5_by_coin"] = d5.groupby("coin").apply(summ)
    out["h5_by_window"] = d5.groupby("w").apply(summ)
    out["h5_by_year"] = d5.groupby("yr").apply(summ)
    d5["fq"] = pd.qcut(d5["f"], 4, labels=["q1_deepest", "q2", "q3", "q4_shallow"])
    out["h5_by_forecast_quartile"] = d5.groupby("fq").apply(summ)
    d5["rq"] = pd.qcut(d5["raw"], 4, labels=["r1_deepest", "r2", "r3", "r4_shallow"])
    out["h5_by_raw_quartile"] = d5.groupby("rq").apply(summ)
    d10 = d[d.h == 10].copy()
    d10["fq"] = pd.qcut(d10["f"], 4, labels=["q1_deepest", "q2", "q3", "q4_shallow"])
    out["h10_by_forecast_quartile"] = d10.groupby("fq").apply(summ)
    out["corr_f_raw"] = float(d5[["f", "raw"]].corr().iloc[0, 1])
    # share of bars in profile and forecast distribution
    allb = pd.concat([b for wins in data["bars"].values() for b in wins.values()])
    out["share_profile"] = float((allb["regime"] == "unknown").mean())
    out["share_short_in_profile"] = float((allb.loc[allb.regime == "unknown", "forecast"] < 0).mean())
    return out
