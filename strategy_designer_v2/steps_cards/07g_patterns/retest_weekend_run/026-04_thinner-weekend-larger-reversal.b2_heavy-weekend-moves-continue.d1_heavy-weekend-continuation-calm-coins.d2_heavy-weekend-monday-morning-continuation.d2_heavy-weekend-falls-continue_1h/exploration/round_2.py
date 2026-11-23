def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    drift = {}; sd = {}
    rows = []; ev = []
    for coin, wins in bars.items():
        g12 = []
        for w, df in wins.items():
            c = df["close"].values
            if len(c) > 12:
                idx = np.arange(0, len(c) - 12, 12)
                g12.extend(list(c[idx + 12] / c[idx] - 1))
        drift[coin] = np.mean(g12); sd[coin] = np.std(g12, ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            hr = ts.dt.hour.values; wd = ts.dt.weekday.values; yr = ts.dt.year.values
            c = df["close"].values; v = df["volume"].values.astype(float); n = len(c)
            vs = pd.Series(v)
            v48 = vs.rolling(48).mean().values
            v120 = vs.shift(48).rolling(120).mean().values
            def back(h):
                a = np.full(n, np.nan); a[h:] = c[h:] / c[:-h] - 1; return a
            def fwd(h):
                a = np.full(n, np.nan); a[:-h] = c[h:] / c[:-h] - 1; return a
            r48 = back(48); r720 = back(720); r19 = back(19); r24 = back(24)
            f12 = fwd(12); f24 = fwd(24); f2 = fwd(2)
            lr = np.log(c); r1b = np.r_[np.nan, np.diff(lr)]
            vol24 = pd.Series(r1b).rolling(24).std().values
            vol720 = pd.Series(r1b).rolling(720).std().values
            for i in np.where(hr == 23)[0]:
                rows.append((coin, wd[i], yr[i], r48[i], r720[i], v48[i] / v120[i] if v120[i] > 0 else np.nan, f12[i], f24[i]))
            for i in np.where(hr == 19)[0]:
                ev.append((coin, wd[i], yr[i], f2[i], r19[i], r24[i], vol24[i] / vol720[i] if vol720[i] > 0 else np.nan, vol720[i]))
    D = pd.DataFrame(rows, columns=["coin", "wd", "yr", "r48", "r720", "vr", "f12", "f24"]).dropna(subset=["r48", "f12", "vr"])
    D["sd"] = D.coin.map(sd); D["dr"] = D.coin.map(drift)
    D["x12"] = (D.f12 - D.dr) / D.sd; D["x24"] = (D.f24 - 2 * D.dr) / D.sd
    D["z48"] = D.r48 / (D.sd * 2)
    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std(ddof=1) / np.sqrt(len(s)))})
    def slope(g, y="x12", x="z48"):
        g = g.dropna(subset=[x, y])
        r = stats.linregress(g[x], g[y]); return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    # Sunday light volume: reversal (signed excess in the reversal direction)
    L = D[(D.wd == 6) & (D.vr <= 1)].copy()
    L["rev"] = -np.sign(L.z48) * L.x12
    out["sun light: slope by year"] = L.groupby("yr").apply(slope)
    out["sun light: slope x24"] = slope(L, "x24")
    L["zq"] = pd.qcut(L.z48, 5, labels=False)
    out["sun light: quintiles of z48"] = L.groupby("zq").agg(z=("z48", "mean"), x12=("x12", "mean"), n=("x12", "size"))
    L["vq"] = pd.qcut(L.vr, 3, labels=False)
    out["sun light: slope by vr tercile"] = L.groupby("vq").apply(slope)
    out["sun light: slope by coin"] = L.groupby("coin").apply(slope)
    # same light-volume reversal on weekday 23h bars (control)
    W = D[(D.wd.isin([1, 2, 3])) & (D.vr <= 1)]
    out["weekday light slope control"] = slope(W)
    # Sunday heavy fall by 30-day trend
    S = D[(D.wd == 6) & (D.r48 < 0) & (D.vr > 1)].dropna(subset=["r720"]).copy()
    S["trend"] = np.where(S.r720 < 0, "down30d", "up30d")
    out["sun heavy fall by 30d trend"] = S.groupby("trend").x12.apply(summ).unstack()
    # 19h close -> 21h close (hours 20, 21)
    E = pd.DataFrame(ev, columns=["coin", "wd", "yr", "f2", "r19", "r24", "vrel", "vol720"]).dropna()
    E["sd2"] = E.vol720 * np.sqrt(2)
    E["x2"] = E.f2 / E.sd2
    out["20-21h by year"] = E.groupby("yr").x2.apply(summ).unstack()
    out["20-21h by coin"] = E.groupby("coin").x2.apply(summ).unstack()
    out["20-21h by weekday"] = E.groupby("wd").x2.apply(summ).unstack()
    E["z19"] = E.r19 / (E.vol720 * np.sqrt(19))
    out["20-21h slope on day's 19h return"] = slope(E, "x2", "z19")
    E["vq"] = pd.qcut(E.vrel, 5, labels=False)
    out["20-21h by recent vol quintile"] = E.groupby("vq").agg(vrel=("vrel", "mean"), x2=("x2", "mean"), n=("x2", "size"),
                                                              t=("x2", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    E["zq"] = pd.qcut(E.z19, 5, labels=False)
    out["20-21h by day-return quintile"] = E.groupby("zq").agg(z=("z19", "mean"), x2=("x2", "mean"), n=("x2", "size"),
                                                              t=("x2", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    return out
