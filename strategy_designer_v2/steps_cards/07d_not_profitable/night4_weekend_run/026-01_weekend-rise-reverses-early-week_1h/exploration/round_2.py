def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        g48 = []
        for w, b in wins.items():
            c = b.sort_values("timestamp")["close"].values.astype(float)
            idx = np.arange(0, len(c) - 48, 48)
            g48.append(c[idx + 48] / c[idx] - 1)
        g48 = np.concatenate(g48); drift[coin] = (g48.mean(), g48.std())
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values.astype(float); n = len(c)
            r1 = pd.Series(c).pct_change()
            v30 = r1.rolling(720, min_periods=200).std()
            v7 = r1.rolling(168, min_periods=100).std()
            vlong = r1.rolling(4320, min_periods=1000).std()
            for i in np.where((ts.dt.hour == 23) & (ts.dt.dayofweek == 6))[0]:
                if i - 48 < 0 or i + 48 >= n: continue
                if (ts.iloc[i + 48] - ts.iloc[i]) != pd.Timedelta(hours=48) or (ts.iloc[i] - ts.iloc[i - 48]) != pd.Timedelta(hours=48): continue
                rows.append((coin, w, ts.iloc[i].year, c[i]/c[i-48]-1, c[i+48]/c[i]-1, v30[i], v7[i], vlong[i]))
    df = pd.DataFrame(rows, columns=["coin","w","year","past","fwd","v30","v7","vlong"]).dropna(subset=["v30"])
    df["mu"] = df.coin.map(lambda k: drift[k][0]); df["usd"] = df.coin.map(lambda k: drift[k][1])
    df["sgn_unusual"] = -np.sign(df.past) * (df.fwd - df.mu)
    df["sgn_total"] = -np.sign(df.past) * df.fwd
    df["vrel"] = df.v30 / df.vlong
    df["vt_coin"] = df.groupby("coin")["v30"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out = {}
    def summ(s):
        sl = stats.linregress(s.past / (s.v30*np.sqrt(48)), s.fwd - s.mu)
        return pd.Series(dict(n=len(s), slope_z=sl.slope, t_slope=sl.slope/sl.stderr,
            rev_unusual=s.sgn_unusual.mean(), t_rev=s.sgn_unusual.mean()/(s.sgn_unusual.std()/np.sqrt(len(s))),
            rev_total=s.sgn_total.mean(), strength=(s.sgn_unusual/s.usd).mean()))
    out["by_within_coin_vol_tercile"] = df.groupby("vt_coin").apply(summ)
    d2 = df.dropna(subset=["vrel"]).copy()
    d2["vr_t"] = pd.qcut(d2.vrel, 3, labels=["calm_vs_6m","mid","hot_vs_6m"])
    out["by_vol_vs_own_6m"] = d2.groupby("vr_t").apply(summ)
    hv = df[df.vt_coin == 2]
    out["highvol_by_year"] = hv.groupby("year").apply(summ)[["n","slope_z","t_slope","rev_total"]]
    hv = hv.copy(); hv["absq"] = pd.qcut(hv.past.abs().rank(method="first"), 4, labels=False)
    out["highvol_by_abs_weekend_move_quartile"] = hv.groupby("absq").apply(summ)[["n","rev_unusual","rev_total","strength"]]
    out["highvol_up_vs_down"] = hv.groupby(hv.past > 0).apply(summ)[["n","rev_unusual","t_rev","rev_total"]]
    lv = df[df.vt_coin == 0]
    out["lowvol_up_vs_down"] = lv.groupby(lv.past > 0).apply(summ)[["n","rev_unusual","t_rev","rev_total"]]
    return out
