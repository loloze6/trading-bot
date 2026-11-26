def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    hs = [1, 3, 5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=30).std()
            ret7 = c / c.shift(7) - 1
            sc = ret7 / (sd30 * np.sqrt(7))
            calm = (df["regime"] != "chop")
            year = pd.to_datetime(df["timestamp"]).dt.year
            for h in hs:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(df), h)
                for i in idx:
                    if i + h >= len(df) or np.isnan(sc.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, sc=sc.iloc[i], fc=df["forecast"].iloc[i],
                                     calm=bool(calm.iloc[i]), year=int(year.iloc[i]), fwd=fwd.iloc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["un"] = d["fwd"] - d["drift"]

    def reg(g, x="sc"):
        g = g.dropna(subset=[x, "un"])
        if len(g) < 10:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, mean_un=np.nan, t_mean=np.nan))
        res = stats.linregress(g[x], g["un"])
        return pd.Series(dict(n=len(g), slope=res.slope, t=res.slope / res.stderr,
                              mean_un=g["un"].mean(), t_mean=stats.ttest_1samp(g["un"], 0).statistic))

    out = {}
    tab = []
    for h in hs:
        for calm in [True, False]:
            for side in ["rise", "fall", "all"]:
                g = d[(d.h == h) & (d.calm == calm)]
                if side == "rise": g = g[g.sc > 0]
                if side == "fall": g = g[g.sc < 0]
                s = reg(g); s["h"] = h; s["calm"] = calm; s["side"] = side
                tab.append(s)
    out["slope_by_h_calm_side"] = pd.DataFrame(tab)
    g5 = d[(d.h == 5) & d.calm & (d.sc > 0)]
    out["calm_rise_h5_by_coin"] = g5.groupby("coin").apply(reg)
    out["calm_rise_h5_by_year"] = g5.groupby("year").apply(reg)
    out["calm_rise_h5_by_window"] = g5.groupby("w").apply(reg)
    g5a = d[(d.h == 5) & d.calm]
    g5a = g5a.assign(q=pd.qcut(g5a.sc, 6, labels=False))
    out["calm_h5_by_sextile"] = g5a.groupby("q").agg(n=("un", "size"), sc=("sc", "mean"), mean_un=("un", "mean"), mean_fwd=("fwd", "mean"))
    gf = d[(d.h == 5) & (d.fc > 0)]
    out["fc_pos_h5"] = reg(gf, "fc")
    return out
