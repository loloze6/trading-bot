def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            rs.extend(list(c[idx + 48] / c[idx] - 1))
        drift[coin] = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sel = np.where((ts.dt.dayofweek == 6) & (ts.dt.hour == 23))[0]
            for t in sel:
                if t < 216 or t + 48 >= len(c): continue
                wk = c[t] / c[t - 48] - 1
                v1 = np.nanstd(r1[t - 47:t + 1]); v0 = np.nanstd(r1[t - 215:t - 47])
                rows.append(dict(coin=coin, year=ts.iloc[t].year, wk=wk, vr=v1 / v0 if v0 > 0 else np.nan,
                                 wkz=wk / (v0 * np.sqrt(48)) if v0 > 0 else np.nan,
                                 x=c[t + 48] / c[t] - 1 - drift[coin]))
    d = pd.DataFrame(rows).dropna()
    out = {}
    def summ(g, sign=-1):
        v = sign * g["x"]
        return pd.Series(dict(n=len(v), mean_pct=100 * v.mean(), t=v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan))
    f = d[d.wk < 0].copy(); r = d[d.wk > 0].copy()
    f["vrq"] = pd.qcut(f.vr, 4, labels=False); r["vrq"] = pd.qcut(r.vr, 4, labels=False)
    f["half"] = np.where(f.year <= 2021, "2018-2021", "2022-2025")
    out["falls_vr_spearman_short"] = pd.Series(dict(rho=stats.spearmanr(f.vr, -f.x)[0], p=stats.spearmanr(f.vr, -f.x)[1], n=len(f)))
    out["falls_wkz_spearman_short"] = pd.Series(dict(rho=stats.spearmanr(-f.wkz, -f.x)[0], p=stats.spearmanr(-f.wkz, -f.x)[1]))
    out["falls_vrq_by_half"] = f.groupby(["half", "vrq"]).apply(summ).unstack(0)
    f["top"] = f.vrq == 3
    out["falls_topvr_by_coin"] = f[f.top].groupby("coin").apply(summ)
    out["falls_topvr_by_year"] = f[f.top].groupby("year").apply(summ)
    out["rises_vrq_long"] = r.groupby("vrq").apply(lambda g: summ(g, 1))
    a = d.copy(); a["vrq"] = pd.qcut(a.vr, 4, labels=False)
    a["signed"] = -np.sign(a.wk) * a.x  # continuation-direction excess
    out["all_vrq_continuation"] = a.groupby("vrq")["signed"].apply(lambda s: pd.Series(dict(n=len(s), mean_pct=100*s.mean(), t=s.mean()/(s.std()/np.sqrt(len(s)))))).unstack()
    return out
