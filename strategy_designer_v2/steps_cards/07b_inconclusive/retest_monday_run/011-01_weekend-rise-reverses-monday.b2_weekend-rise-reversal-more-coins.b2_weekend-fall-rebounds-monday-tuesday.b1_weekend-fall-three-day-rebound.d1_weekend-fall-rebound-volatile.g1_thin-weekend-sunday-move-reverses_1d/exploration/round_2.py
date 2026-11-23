def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    sdh = {}
    for coin, wins in data["bars"].items():
        for h in (1, 2, 3, 5):
            g = []
            for w, b in wins.items():
                c = b["close"].values.astype(float)
                idx = np.arange(0, len(c) - h, h)
                g += list(c[idx + h] / c[idx] - 1)
            g = np.array(g); sdh[(coin, h)] = (np.nanmean(g), np.nanstd(g, ddof=1))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values.astype(float); v = b["volume"].values.astype(float)
            n = len(c)
            r1 = np.full(n, np.nan); r1[1:] = c[1:] / c[:-1] - 1
            r2 = np.full(n, np.nan); r2[2:] = c[2:] / c[:-2] - 1
            mad = pd.Series(np.abs(r1)).rolling(20, min_periods=20).mean().shift(1).values
            vs = pd.Series(v)
            base = vs.shift(2).rolling(20, min_periods=20).mean().values
            vsun = base / v
            for t in range(n):
                if ts[t].weekday() != 6 or np.isnan(r1[t]) or np.isnan(mad[t]) or mad[t] == 0:
                    continue
                rec = dict(coin=coin, win=w, r1=r1[t], r2=r2[t], z=r1[t] / mad[t],
                           vsun=vsun[t] if v[t] > 0 else np.nan)
                for h in (1, 2, 3, 5):
                    rec[f"f{h}"] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                # day by day pieces
                for k in (1, 2, 3):
                    rec[f"d{k}"] = c[t + k] / c[t + k - 1] - 1 if t + k < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    hz = []
    for h in (1, 2, 3, 5):
        mu = d.coin.map(lambda x: sdh[(x, h)][0]); sd = d.coin.map(lambda x: sdh[(x, h)][1])
        s = (-np.sign(d.r1) * (d[f"f{h}"] - mu) / sd).dropna()
        s2 = (-np.sign(d.r2) * (d[f"f{h}"] - mu) / sd).dropna()
        hz.append(dict(h_days=h, n=len(s), strength_sun=s.mean(),
                       t_sun=s.mean() / (s.std(ddof=1) / np.sqrt(len(s))),
                       strength_weekend2d=s2.mean(),
                       t_weekend2d=s2.mean() / (s2.std(ddof=1) / np.sqrt(len(s2)))))
    out["sunday_fade_by_horizon"] = pd.DataFrame(hz)
    dd = []
    for k in (1, 2, 3):
        x = (-np.sign(d.r1) * d[f"d{k}"]).dropna()
        dd.append(dict(day_after=k, mean=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(x))), n=len(x)))
    out["fade_by_day_after_sunday"] = pd.DataFrame(dd)
    mu = d.coin.map(lambda x: sdh[(x, 3)][0]); sd = d.coin.map(lambda x: sdh[(x, 3)][1])
    d["s3"] = -np.sign(d.r1) * (d.f3 - mu) / sd
    d["g3"] = -d.z * (d.f3 - mu) / sd  # graded by z
    x = d.dropna(subset=["s3", "vsun"])
    out["grading"] = pd.DataFrame([dict(
        rho_absz_s3=stats.spearmanr(x.z.abs(), x.s3)[0], p_absz=stats.spearmanr(x.z.abs(), x.s3)[1],
        rho_vsun_s3=stats.spearmanr(x.vsun, x.s3)[0], p_vsun=stats.spearmanr(x.vsun, x.s3)[1],
        n=len(x))])
    x["vq"] = pd.qcut(x.vsun, 5, labels=False)
    out["sun_by_sunday_only_volfactor"] = x.groupby("vq").s3.agg(["count", "mean"])
    w = d.dropna(subset=["s3"]).groupby("win").s3.mean()
    out["windows_share_positive"] = pd.Series(dict(windows=len(w), positive=(w > 0).sum(), mean=w.mean()))
    return out
