def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in (24, 48):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.concatenate(rs).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float)
            n = len(c)
            lr = np.diff(np.log(c), prepend=np.nan)
            s = pd.Series(c)
            r24 = s.pct_change(24).values
            z = ((s.pct_change(24) - s.pct_change(24).rolling(60, min_periods=20).mean())
                 / s.pct_change(24).rolling(60, min_periods=20).std()).values
            hrs = ts.dt.hour.values
            # every 48 bars grid, any hour, plus the 19:00 start bars
            for i in range(25, n - 48):
                hh = hrs[i]
                seg = lr[i - 23:i + 1]
                vs = v[i - 23:i + 1]
                tot = np.nansum(seg)
                if not np.isfinite(tot) or tot == 0:
                    continue
                same = seg[np.sign(seg) == np.sign(tot)]
                maxshare = np.max(np.abs(seg)) / (np.sum(np.abs(seg)) + 1e-12)
                volconc = np.max(vs) / (np.sum(vs) + 1e-12)
                stepshare = len(same) / 24
                rows.append(dict(coin=coin, w=w, i=i, hour=hh, r24=r24[i], z=z[i],
                                 maxshare=maxshare, volconc=volconc, stepshare=stepshare,
                                 x24=c[i + 24] / c[i] - 1 - drift[(coin, 24)],
                                 x48=c[i + 48] / c[i] - 1 - drift[(coin, 48)]))
    d = pd.DataFrame(rows)
    out = {}

    def reg(g, col="x48", xcol="fc"):
        g = g.dropna(subset=[col, xcol])
        if len(g) < 10:
            return pd.Series(dict(n=len(g), slope_t=np.nan, mean=np.nan))
        s = stats.linregress(g[xcol], g[col])
        return pd.Series(dict(n=len(g), slope_t=s.slope / s.stderr, mean=g[col].mean(),
                              t_mean=g[col].mean() / (g[col].std() / np.sqrt(len(g)))))

    d["fc"] = np.clip(-d.z * 10, 0, 20)
    # non-overlap: one bar per 48 per window at each hour: keep i where (i // 24) even and hour fixed
    d["day"] = d.i // 24
    g = d[(d.day % 2 == 0) & (d.fc > 0)]
    out["by_hour_48"] = g.groupby("hour").apply(reg).describe().loc[["mean", "std", "min", "max"]]
    out["hour_slope_t_list"] = g.groupby("hour").apply(reg)["slope_t"].round(2).to_frame().T
    e = g[g.hour == 19].copy()
    e["jump"] = pd.qcut(e.maxshare, 3, labels=["grind", "mid", "jump"])
    e["vconc"] = pd.qcut(e.volconc, 3, labels=["evenvol", "mid", "burstvol"])
    out["eve_by_jumpshare"] = e.groupby("jump").apply(reg)
    out["eve_by_volconc"] = e.groupby("vconc").apply(reg)
    out["eve_by_jumpshare_x24"] = e.groupby("jump").apply(lambda x: reg(x, "x24"))
    big = e[e.fc >= e.fc.quantile(2 / 3)]
    out["eve_top_third_by_jump"] = big.groupby("jump").agg(n=("x48", "size"), x24=("x24", "mean"), x48=("x48", "mean"))
    return out
