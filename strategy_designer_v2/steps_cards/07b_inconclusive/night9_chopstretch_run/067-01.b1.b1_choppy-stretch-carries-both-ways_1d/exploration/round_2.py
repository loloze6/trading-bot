def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        drift = {}; usual = {}
        for h in [5, 10]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[h] = np.mean(rs); usual[h] = np.std(rs, ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            fc = df["forecast"].values
            raw = df["debug_info.components.stretch.last_history_value"].values
            r60 = pd.Series(c).pct_change(60).values
            for h in [5, 10]:
                for i in range(0, len(c) - h, h):
                    if fc[i] == 0 or np.isnan(fc[i]):
                        continue
                    fr = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, h=h, day=pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                                     f=fc[i], raw=raw[i], fr=fr, ex=fr - drift[h],
                                     strn=(fr - drift[h]) * np.sign(fc[i]) / usual[h],
                                     r60=r60[i], year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    R = pd.DataFrame(rows)
    out = {}
    def side_stats(g):
        s = g["ex"] * np.sign(g["f"])
        d = s.groupby(g["day"]).sum()
        n = len(g)
        tday = d.mean() / (d.std(ddof=1) / np.sqrt(len(d))) * 1.0 if len(d) > 2 else np.nan
        sl = stats.linregress(g["f"].abs(), s) if n > 5 else None
        return pd.Series(dict(n=n, days=len(d), signed_ex=s.mean(), t_day=tday,
                              strength=g["strn"].mean(), raw_ex=g["fr"].mean(),
                              slope_abs_t=(sl.slope / sl.stderr) if sl is not None else np.nan))
    R["side"] = np.where(R.f > 0, "long", "short")
    out["side_h"] = R.groupby(["h", "side"]).apply(side_stats)
    r5 = R[R.h == 5]
    out["short_h5_by_year"] = r5[r5.side == "short"].groupby("year").apply(side_stats)
    out["long_h5_by_year"] = r5[r5.side == "long"].groupby("year").apply(side_stats)
    out["short_h5_by_coin"] = r5[r5.side == "short"].groupby("coin").apply(side_stats)
    out["long_h5_by_coin"] = r5[r5.side == "long"].groupby("coin").apply(side_stats)
    r5 = r5.copy()
    r5["trend_half"] = np.where(r5.r60 > 0, "r60_pos", "r60_neg")
    out["h5_side_by_r60sign"] = r5.groupby(["side", "trend_half"]).apply(side_stats)
    return out
