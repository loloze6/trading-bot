def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    rows = []; hr_rows = []; drift = {}; sd = {}
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
            c = df["close"].values; v = df["volume"].values.astype(float); n = len(c)
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            hr_rows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday, "r1": r1}))
            vs = pd.Series(v)
            v48 = vs.rolling(48).mean().values
            v120 = vs.shift(48).rolling(120).mean().values
            r48 = np.full(n, np.nan); r48[48:] = c[48:] / c[:-48] - 1
            r24 = np.full(n, np.nan); r24[24:] = c[24:] / c[:-24] - 1
            f12 = np.full(n, np.nan); f12[:-12] = c[12:] / c[:-12] - 1
            f24 = np.full(n, np.nan); f24[:-24] = c[24:] / c[:-24] - 1
            f48 = np.full(n, np.nan); f48[:-48] = c[48:] / c[:-48] - 1
            sel = np.where(ts.dt.hour.values == 23)[0]
            for i in sel:
                rows.append((coin, w, ts.dt.weekday.values[i], ts.dt.year.values[i], r48[i], r24[i],
                             v48[i] / v120[i] if v120[i] > 0 else np.nan, f12[i], f24[i], f48[i]))
    D = pd.DataFrame(rows, columns=["coin", "w", "wd", "yr", "r48", "r24", "vr", "f12", "f24", "f48"])
    D["sd"] = D.coin.map(sd); D["dr"] = D.coin.map(drift)
    D["x12"] = (D.f12 - D.dr) / D.sd
    D["z48"] = D.r48 / (D.sd * 2)
    D = D.dropna(subset=["r48", "f12", "vr"])
    # by weekday of the 23:00 bar: 48h fall/rise x heavy/light volume -> next 12h excess (in usual moves)
    def summ(s):
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std(ddof=1) / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    D["dir"] = np.where(D.r48 < 0, "fall", "rise")
    D["vol"] = np.where(D.vr > 1, "heavy", "light")
    out["x12 by weekday(23h bar) dir vol"] = D.groupby(["wd", "dir", "vol"]).x12.apply(summ).unstack()
    # slope of x12 on z48 by weekday and vol
    sl = []
    for (wd, vol), g in D.groupby(["wd", "vol"]):
        r = stats.linregress(g.z48, g.x12)
        sl.append((wd, vol, len(g), r.slope, r.slope / r.stderr))
    out["slope x12 on z48"] = pd.DataFrame(sl, columns=["wd", "vol", "n", "slope", "t"])
    # Sunday heavy falls: 24h and 48h follow-on, and by year, and quintiles of size
    S = D[(D.wd == 6) & (D.r48 < 0) & (D.vr > 1)].copy()
    S["x24"] = (S.f24 - 2 * S.dr) / S.sd; S["x48"] = (S.f48 - 4 * S.dr) / S.sd
    out["sun heavy fall horizons"] = pd.DataFrame({k: summ(S[k].dropna()) for k in ["x12", "x24", "x48"]})
    out["sun heavy fall by year"] = S.groupby("yr").x12.apply(summ).unstack()
    S["vq"] = pd.qcut(S.vr, 3, labels=False); S["zq"] = pd.qcut(S.z48, 3, labels=False)
    out["sun heavy fall terciles vr"] = S.groupby("vq").agg(vr=("vr", "mean"), x12=("x12", "mean"), n=("x12", "size"))
    out["sun heavy fall terciles z"] = S.groupby("zq").agg(z=("z48", "mean"), x12=("x12", "mean"), n=("x12", "size"))
    out["sun heavy fall by coin"] = S.groupby("coin").x12.apply(summ).unstack()
    # hour of day / weekday
    H = pd.concat(hr_rows).dropna()
    H["sdh"] = H.coin.map(lambda c: 1)
    out["hour mean r1 bp"] = H.groupby("hour").r1.apply(lambda s: pd.Series({"bp": s.mean() * 1e4, "t": s.mean() / (s.std() / np.sqrt(len(s)))})).unstack()
    out["weekday mean r1 bp"] = H.groupby("wd").r1.apply(lambda s: pd.Series({"bp": s.mean() * 1e4, "t": s.mean() / (s.std() / np.sqrt(len(s)))})).unstack()
    return out
