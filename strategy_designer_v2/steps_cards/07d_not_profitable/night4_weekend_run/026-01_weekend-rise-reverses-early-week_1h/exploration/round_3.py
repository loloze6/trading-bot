def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []; drift = {}
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
            vlong = r1.rolling(4320, min_periods=1000).std()
            alloc = b["postRebalance_current_allocation"].values.astype(float)
            for i in np.where((ts.dt.hour == 23) & (ts.dt.dayofweek == 6))[0]:
                if i - 48 < 0 or i + 48 >= n: continue
                if (ts.iloc[i + 48] - ts.iloc[i]) != pd.Timedelta(hours=48) or (ts.iloc[i] - ts.iloc[i - 48]) != pd.Timedelta(hours=48): continue
                rows.append((coin, w, ts.iloc[i].year, c[i]/c[i-48]-1, c[i+48]/c[i]-1, v30[i], vlong[i], alloc[i]))
    df = pd.DataFrame(rows, columns=["coin","w","year","past","fwd","v30","vlong","alloc"]).dropna(subset=["v30","vlong"])
    df["mu"] = df.coin.map(lambda k: drift[k][0]); df["usd"] = df.coin.map(lambda k: drift[k][1])
    df["vrel"] = df.v30 / df.vlong
    df["vr_t"] = pd.qcut(df.vrel, 3, labels=["calm","mid","hot"])
    out = {}
    def cont(s):
        sg = np.sign(s.past)
        u = sg * (s.fwd - s.mu); tot = sg * s.fwd
        return pd.Series(dict(n=len(s), cont_unusual=u.mean(), t=u.mean()/(u.std()/np.sqrt(len(s))),
                              cont_total=tot.mean(), strength=(u/s.usd).mean()))
    out["continuation_by_vol_vs_6m"] = df.groupby("vr_t").apply(cont)
    calm = df[df.vr_t == "calm"].copy()
    out["calm_continuation_by_year"] = calm.groupby("year").apply(cont)
    calm["aq"] = pd.qcut(calm.past.abs().rank(method="first"), 4, labels=False)
    out["calm_continuation_by_abs_move_quartile"] = calm.groupby("aq").apply(cont)
    out["calm_up_vs_down"] = calm.groupby(calm.past > 0).apply(cont)
    # book: drift part vs timing
    pos = []; 
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            pos.append(b["postRebalance_current_allocation"].astype(float))
    pos = pd.concat(pos)
    out["book_parts"] = pd.Series(dict(mean_position=pos.mean(), share_bars_short=(pos < 0).mean(),
                                       mean_alloc_at_case=df.alloc.mean()))
    return out
