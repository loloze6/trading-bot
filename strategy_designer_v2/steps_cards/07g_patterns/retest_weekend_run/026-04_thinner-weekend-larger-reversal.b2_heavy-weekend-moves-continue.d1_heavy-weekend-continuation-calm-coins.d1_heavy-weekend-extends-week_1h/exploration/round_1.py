def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    hour_rows = []
    day_rows = []
    for coin, wins in bars.items():
        # usual 48h move per coin
        g48 = []
        for w, df in wins.items():
            c = df["close"].values
            g48.extend(list(c[48::48] / c[:-48:48][:len(c[48::48])] - 1))
        g48 = np.array(g48); sd48 = np.nanstd(g48); mu48 = np.nanmean(g48)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            hour_rows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values, "r": r1}))
            tsv = ts.values.astype("datetime64[h]").astype(np.int64)
            n = len(c)
            # anchors: bar starting at 23:00 (close at 00:00) on any day
            idx = np.where((ts.dt.hour.values == 23))[0]
            for t in idx:
                if t - 168 < 0 or t + 48 >= n: continue
                if tsv[t + 48] - tsv[t - 168] != 216: continue
                past = c[t] / c[t - 48] - 1
                prior = c[t - 48] / c[t - 168] - 1
                vr = v[t - 47:t + 1].mean() / max(v[t - 167:t - 47].mean(), 1e-12)
                f24 = c[t + 24] / c[t] - 1
                f48 = c[t + 48] / c[t] - 1
                # recent vol: 7d hourly std
                rv = np.nanstd(r1[t - 167:t + 1])
                rows.append((coin, w, ts.iloc[t].weekday(), past / sd48, prior / sd48, vr, (f48 - mu48) / sd48, f24 / sd48, rv))
    R = pd.DataFrame(rows, columns=["coin", "win", "wd", "pz", "prz", "vr", "f48", "f24", "rv"])
    # wd is weekday of bar start at 23:00; Sunday=6 -> Monday 00:00 close
    out = {}
    def slope(d, x="pz", y="f48"):
        d = d.dropna(subset=[x, y])
        if len(d) < 20: return (np.nan, np.nan, len(d))
        s = stats.linregress(d[x], d[y]); return (s.slope, s.slope / s.stderr, len(d))
    t1 = []
    for wd in range(7):
        d = R[R.wd == wd]
        s = slope(d); t1.append({"anchor_wd(23h start)": wd, "slope_f48_on_past48": s[0], "t": s[1], "n(overlap 2d)": s[2]})
    out["48h past vs 48h next, by anchor weekday (z units)"] = pd.DataFrame(t1)
    # Sunday anchor splits
    S = R[R.wd == 6].copy()
    S["agree"] = np.sign(S.pz) == np.sign(S.prz)
    S["heavy"] = S.vr > 1
    t2 = []
    for a in [True, False]:
        for h in [True, False]:
            d = S[(S.agree == a) & (S.heavy == h)]
            s = slope(d)
            sig = (np.sign(d.pz) * d.f48)
            t2.append({"agree_week": a, "heavy_vol": h, "n": len(d), "slope": s[0], "t_slope": s[1],
                       "mean signed cont": sig.mean(), "t_mean": sig.mean() / (sig.std() / np.sqrt(len(d)))})
    out["Sunday anchor: continuation by agree x heavy"] = pd.DataFrame(t2)
    # same for weekday anchors pooled (Tue..Fri anchors wd 1..4)
    W = R[R.wd.isin([1, 2, 3])].copy()
    W["agree"] = np.sign(W.pz) == np.sign(W.prz); W["heavy"] = W.vr > 1
    t3 = []
    for a in [True, False]:
        for h in [True, False]:
            d = W[(W.agree == a) & (W.heavy == h)]
            sig = (np.sign(d.pz) * d.f48)
            t3.append({"agree": a, "heavy": h, "n": len(d), "mean signed cont": sig.mean(), "t": sig.mean() / (sig.std() / np.sqrt(len(d)))})
    out["Tue-Thu 23h anchors: same split (overlapping across days)"] = pd.DataFrame(t3)
    # Sunday anchor by vr quintile, signed by past
    S["sig"] = np.sign(S.pz) * S.f48
    S["vrq"] = pd.qcut(S.vr, 5, labels=False)
    out["Sunday: signed cont by vol-ratio quintile"] = S.groupby("vrq").agg(n=("sig", "size"), vr=("vr", "mean"), m=("sig", "mean"), sd=("sig", "std")).assign(t=lambda x: x.m / (x.sd / np.sqrt(x.n)))
    S["pq"] = pd.qcut(S.pz.abs(), 5, labels=False)
    out["Sunday: signed cont by |weekend move| quintile"] = S.groupby("pq").agg(n=("sig", "size"), apz=("pz", lambda x: x.abs().mean()), m=("sig", "mean"), sd=("sig", "std")).assign(t=lambda x: x.m / (x.sd / np.sqrt(x.n)))
    S["sigp"] = np.sign(S.prz) * S.f48
    S["prq"] = pd.qcut(S.prz.abs(), 5, labels=False)
    out["Sunday: next48 signed by PRIOR week, by |prior| quintile"] = S.groupby("prq").agg(n=("sigp", "size"), m=("sigp", "mean"), sd=("sigp", "std")).assign(t=lambda x: x.m / (x.sd / np.sqrt(x.n)))
    S["rvq"] = pd.qcut(S.rv, 3, labels=False)
    out["Sunday: slope by recent-vol tercile"] = pd.DataFrame([dict(zip(["slope", "t", "n"], slope(S[S.rvq == q]))) for q in range(3)])
    H = pd.concat(hour_rows).dropna()
    hh = H.groupby("hour").r.agg(["mean", "std", "size"]); hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["size"]))
    out["hourly return by hour (all coins)"] = hh[["mean", "t", "size"]]
    ww = H.groupby("wd").r.agg(["mean", "std", "size"]); ww["t"] = ww["mean"] / (ww["std"] / np.sqrt(ww["size"]))
    out["hourly return by weekday"] = ww[["mean", "t"]]
    return out
