def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    ev = []   # evening 21:00-23:00 bars (start 21, 22) per day
    wk = []
    for coin, wins in bars.items():
        g48 = []
        for w, df in wins.items():
            c = df["close"].values
            a = c[::48]
            g48.extend(list(a[1:] / a[:-1] - 1))
        sd48 = np.nanstd(g48); mu48 = np.nanmean(g48)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            hr = ts.dt.hour.values; tsv = ts.values.astype("datetime64[h]").astype(np.int64)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            n = len(c)
            # bars starting at 21:00: evening return = close[t+1]/close[t-1]-1 (bars 21 and 22)
            for t in np.where(hr == 21)[0]:
                if t - 168 < 0 or t + 1 >= n: continue
                if tsv[t + 1] - tsv[t - 168] != 169: continue
                evr = c[t + 1] / c[t - 1] - 1
                rv = np.nanstd(r1[t - 167:t - 1])
                p20 = c[t - 1] / c[t - 21] - 1     # 01:00..21:00 day move
                p7d = c[t - 1] / c[t - 168] - 1
                vr = v[t - 21:t - 1].mean() / max(v[t - 168:t - 21].mean(), 1e-12)
                ev.append((coin, w, ts.iloc[t].year, ts.iloc[t].weekday(), evr, evr / (rv * np.sqrt(2)), p20 / (rv * np.sqrt(20)), p7d / (rv * np.sqrt(167)), vr, rv))
            for t in np.where(hr == 23)[0]:
                if ts.iloc[t].weekday() != 6: continue
                if t - 168 < 0 or t + 48 >= n: continue
                if tsv[t + 48] - tsv[t - 168] != 216: continue
                past = (c[t] / c[t - 48] - 1) / sd48
                vr = v[t - 47:t + 1].mean() / max(v[t - 167:t - 47].mean(), 1e-12)
                f48 = (c[t + 48] / c[t] - 1 - mu48) / sd48
                wk.append((coin, w, ts.iloc[t].year, past, vr, f48))
    E = pd.DataFrame(ev, columns=["coin", "win", "yr", "wd", "r", "z", "p20", "p7d", "vr", "rv"])
    def tm(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["evening 21-23h return by coin"] = E.groupby("coin").r.apply(tm).unstack()
    out["evening return by year"] = E.groupby("yr").r.apply(tm).unstack()
    out["evening return by weekday"] = E.groupby("wd").r.apply(tm).unstack()
    out["evening z by recent-vol tercile"] = E.groupby(pd.qcut(E.rv, 3, labels=False)).z.apply(tm).unstack()
    out["evening z by day-move (p20 z) quintile"] = E.groupby(pd.qcut(E.p20, 5, labels=False)).z.apply(tm).unstack()
    out["evening z by 7d move quintile"] = E.groupby(pd.qcut(E.p7d, 5, labels=False)).z.apply(tm).unstack()
    out["evening z by day volume ratio quintile"] = E.groupby(pd.qcut(E.vr, 5, labels=False)).z.apply(tm).unstack()
    W = pd.DataFrame(wk, columns=["coin", "win", "yr", "pz", "vr", "f48"])
    W["sig"] = np.sign(W.pz) * W.f48
    W["thin"] = W.vr < W.groupby("coin").vr.transform("median")
    rows = []
    for coin, d in W.groupby("coin"):
        for th in [True, False]:
            dd = d[d.thin == th]
            s = stats.linregress(dd.pz, dd.f48)
            rows.append({"coin": coin, "thin": th, "n": len(dd), "slope": s.slope, "t": s.slope / s.stderr})
    out["Sunday: f48 on weekend move, thin vs heavy, by coin"] = pd.DataFrame(rows)
    T = W[W.thin]
    out["thin weekends: signed cont by year"] = T.groupby("yr").sig.apply(tm).unstack()
    s = stats.linregress(T.pz, T.f48); out["thin pooled slope,t,n"] = f"{s.slope:.4f}, {s.slope/s.stderr:.2f}, {len(T)}"
    # graded: interaction pz * (1/vr) across all
    W["x"] = W.pz * (1 / W.vr)
    s2 = stats.linregress(W.x, W.f48); out["all Sunday: f48 on pz/vr slope,t,n"] = f"{s2.slope:.4f}, {s2.slope/s2.stderr:.2f}, {len(W)}"
    return out
