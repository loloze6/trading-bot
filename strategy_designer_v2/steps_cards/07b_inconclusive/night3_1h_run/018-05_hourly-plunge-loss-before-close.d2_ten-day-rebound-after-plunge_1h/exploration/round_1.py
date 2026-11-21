def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        for H in [24, 72, 240, 480]:
            rr = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rr += list(c[idx + H] / c[idx] - 1)
            drift[(coin, H)] = np.mean(rr); usual[(coin, H)] = np.std(rr)
        for w, df in ws.items():
            c = df["close"].values; f = df["forecast"].fillna(0).values
            n = len(c)
            s = pd.Series(c)
            r24 = s.pct_change(24)
            mabs = r24.abs().rolling(720, min_periods=200).mean()
            depth = (-r24 / mabs).values
            r720 = s.pct_change(720).values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            for start in range(0, n, 240):
                end = min(start + 240, n)
                hit = np.where(f[start:end] >= 2)[0]
                if len(hit) == 0: continue
                t = start + hit[0]
                rec = dict(coin=coin, w=w, year=year[t], fc=f[t], depth=depth[t], prior=r720[t])
                for H in [24, 72, 240, 480]:
                    rec[f"u{H}"] = (c[t + H] / c[t] - 1 - drift[(coin, H)]) if t + H < n else np.nan
                    rec[f"s{H}"] = rec[f"u{H}"] / usual[(coin, H)] if t + H < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    out["horizons"] = pd.DataFrame({H: tt(d[f"u{H}"]) for H in [24, 72, 240, 480]}).T
    out["by_coin"] = d.groupby("coin")["u240"].apply(tt).unstack()
    out["by_year"] = d.groupby("year")["u240"].apply(tt).unstack()
    d["fcq"] = pd.qcut(d["fc"].rank(method="first"), 4, labels=False)
    out["by_fc_q"] = d.groupby("fcq")["u240"].apply(tt).unstack()
    d["dq"] = pd.qcut(d["depth"].rank(method="first"), 4, labels=False)
    out["by_depth_q"] = d.groupby("dq")["u240"].apply(tt).unstack()
    d["pq"] = pd.qcut(d["prior"].rank(method="first"), 4, labels=False)
    out["by_prior_q"] = d.groupby("pq")["u240"].apply(tt).unstack()
    slopes = {}
    for v in ["fc", "depth", "prior"]:
        for H in [72, 240, 480]:
            x = d[[v, f"s{H}"]].dropna()
            r = stats.linregress(x[v], x[f"s{H}"])
            slopes[f"{v}_{H}"] = pd.Series(dict(n=len(x), slope=r.slope, t=r.slope / r.stderr))
    out["slopes_strength"] = pd.DataFrame(slopes).T
    out["depth_prior_desc"] = d[["fc", "depth", "prior"]].describe()
    return out
