def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        grid = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 3, 3)
            grid += list(c[idx + 3] / c[idx] - 1)
        g = np.array(grid)
        drift[coin] = (np.nanmean(g), np.nanstd(g, ddof=1))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values.astype(float); v = b["volume"].values.astype(float)
            n = len(c)
            r1 = np.full(n, np.nan); r1[1:] = c[1:] / c[:-1] - 1
            mad = pd.Series(np.abs(r1)).rolling(20, min_periods=20).mean().shift(1).values
            fwd = np.full(n, np.nan); fwd[:n-3] = c[3:] / c[:n-3] - 1
            vs = pd.Series(v)
            base = vs.shift(2).rolling(20, min_periods=20).mean().values
            wk = vs.rolling(2).mean().values
            fc = b["forecast"].values
            for t in range(n):
                if np.isnan(fwd[t]) or np.isnan(r1[t]) or np.isnan(mad[t]) or mad[t] == 0:
                    continue
                rows.append(dict(coin=coin, win=w, wd=ts[t].weekday(), year=ts[t].year,
                                 r1=r1[t], z=r1[t] / mad[t], fwd=fwd[t],
                                 vf=base[t] / wk[t] if wk[t] > 0 else np.nan, fc=fc[t]))
    d = pd.DataFrame(rows)
    d["mu"] = d.coin.map(lambda x: drift[x][0]); d["sd"] = d.coin.map(lambda x: drift[x][1])
    d["fade"] = -np.sign(d.r1) * (d.fwd - d.mu)
    d["str"] = d.fade / d.sd
    out = {}
    # weekday comparison: fade strength per weekday (each weekday 7 days apart -> non overlapping)
    def summ(x):
        return pd.Series(dict(n=len(x), mean_fade=x.fade.mean(), strength=x.str.mean(),
                              t=x.str.mean() / (x.str.std(ddof=1) / np.sqrt(len(x)))))
    out["by_weekday(0=Mon,6=Sun)"] = d.groupby("wd").apply(summ)
    s = d[d.wd == 6].copy()
    s["zq"] = pd.qcut(s.z.abs(), 5, labels=False)
    out["sun_by_absz_quintile"] = s.groupby("zq").apply(summ)
    s["vq"] = pd.qcut(s.vf, 5, labels=False)
    out["sun_by_volfactor_quintile"] = s.groupby("vq").apply(summ)
    s["side"] = np.where(s.r1 > 0, "rise", "fall")
    out["sun_by_side"] = s.groupby("side").apply(summ)
    out["sun_by_year"] = s.groupby("year").apply(summ)
    out["sun_by_coin"] = s.groupby("coin").apply(summ)
    # grading: corr of strength with |z| and with vf, per weekday
    g = []
    for wd, x in d.groupby("wd"):
        x = x.dropna(subset=["vf"])
        g.append(dict(wd=wd, rho_absz=stats.spearmanr(x.z.abs(), x.str)[0],
                      rho_vf=stats.spearmanr(x.vf, x.str)[0], n=len(x)))
    out["grading_by_weekday"] = pd.DataFrame(g)
    # sunday vs other days, matched |z| quintiles
    d["zq"] = pd.qcut(d.z.abs(), 5, labels=False)
    d["sun"] = d.wd == 6
    out["sun_minus_other_by_absz"] = d.groupby(["zq", "sun"]).str.mean().unstack()
    return out
