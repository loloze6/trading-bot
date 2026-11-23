def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            s = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            n = len(s)
            hv = s.pct_change().rolling(720, min_periods=240).std()
            for H in (24, 72):
                past = s / s.shift(H) - 1
                scale = past.abs().rolling(720, min_periods=240).mean()
                fwd = s.shift(-H) / s - 1
                for i in range(0, n, H):
                    if np.isnan(fwd.iloc[i]) or np.isnan(past.iloc[i]) or np.isnan(scale.iloc[i]) or np.isnan(hv.iloc[i]):
                        continue
                    rows.append((coin, w, H, past.iloc[i] / scale.iloc[i], hv.iloc[i], fwd.iloc[i], ts.iloc[i].year, ts.iloc[i].dayofweek))
    R = pd.DataFrame(rows, columns=["coin", "w", "H", "z", "hv", "fwd", "yr", "dow"])
    R["drift"] = R.groupby(["coin", "H"])["fwd"].transform("mean")
    R["usual"] = R.groupby(["coin", "H"])["fwd"].transform("std")
    R["ex"] = R["fwd"] - R["drift"]
    R["str"] = R["ex"] / R["usual"]
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(), "mean_total": g["fwd"].mean(),
                          "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))), "strength": g["str"].mean()})
    sub = R[R.H == 24].copy()
    sub["vq"] = sub.groupby("coin")["hv"].transform(lambda x: pd.qcut(x, 5, labels=False))
    sub["zc"] = sub["z"].clip(-6, 6)
    # reversal signal: -z, ex in the signal's direction
    res = []
    for vq, g in sub.groupby("vq"):
        sl = stats.linregress(g["zc"], g["str"])
        res.append((vq, len(g), sl.slope, sl.slope / sl.stderr))
    out["H24 slope of strength on z, by vol quintile"] = pd.DataFrame(res, columns=["vq", "n", "slope", "t"])
    # graded: z times hv-rank
    sub["sig"] = -sub["zc"] * sub["vq"]
    hi = sub[sub.vq >= 3].copy()
    hi["dir_ex"] = -np.sign(hi["z"]) * hi["ex"]
    hi["dir_str"] = -np.sign(hi["z"]) * hi["str"]
    hi["dir_tot"] = -np.sign(hi["z"]) * hi["fwd"]
    hi["az"] = hi.groupby("coin")["z"].transform(lambda x: pd.qcut(x.abs(), 4, labels=False))
    def s2(g):
        return pd.Series({"n": len(g), "dir_ex": g["dir_ex"].mean(), "dir_total": g["dir_tot"].mean(),
                          "t": g["dir_ex"].mean() / (g["dir_ex"].std() / np.sqrt(len(g))), "strength": g["dir_str"].mean()})
    out["H24 top-2 vol quintiles: reversal by |z| quartile"] = hi.groupby("az").apply(s2)
    big = hi[hi.az == 3]
    out["H24 hi-vol, top |z| quartile, by year"] = big.groupby("yr").apply(s2)
    out["H24 hi-vol, top |z| quartile, by side (z<0 falls)"] = big.groupby(np.sign(big["z"])).apply(s2)
    out["H24 hi-vol, top |z| quartile, by coin"] = big.groupby("coin").apply(s2)
    out["H24 hi-vol, top |z| quartile, by dow"] = big.groupby("dow").apply(s2)
    # 72h continuation in low vol
    s72 = R[R.H == 72].copy()
    s72["vq"] = s72.groupby("coin")["hv"].transform(lambda x: pd.qcut(x, 3, labels=False))
    lo = s72[s72.vq == 0].copy()
    lo["dir_ex"] = np.sign(lo["z"]) * lo["ex"]; lo["dir_str"] = np.sign(lo["z"]) * lo["str"]; lo["dir_tot"] = np.sign(lo["z"]) * lo["fwd"]
    lo["az"] = lo.groupby("coin")["z"].transform(lambda x: pd.qcut(x.abs(), 3, labels=False))
    out["H72 low vol: continuation by |z| tercile"] = lo.groupby("az").apply(s2)
    out["H72 low vol top |z|: by year"] = lo[lo.az == 2].groupby("yr").apply(s2)
    return out
