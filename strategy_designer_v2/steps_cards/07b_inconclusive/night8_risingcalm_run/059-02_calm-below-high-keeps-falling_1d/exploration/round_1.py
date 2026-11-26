def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            ret60 = pd.Series(c).pct_change(60).values
            dr = pd.Series(c).pct_change()
            vol10 = dr.rolling(10).std().values
            for h in [1, 3, 5, 10, 20]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                        year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        fwd=c[i+h]/c[i]-1, f=df["forecast"].iloc[i],
                        reg=df["regime"].iloc[i],
                        raw=df.get("debug_info.components.depth.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                        r60=ret60[i], past14=(c[i]/c[i-14]-1) if i>=14 else np.nan))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin","h"])["fwd"].transform("mean")
    R["ex"] = R["fwd"] - R["drift"]
    P = R[R.reg == "unknown"].copy()
    def slope(g):
        g = g.dropna(subset=["f","ex"])
        if len(g) < 15 or g.f.std() == 0: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        s = stats.linregress(g.f, g.ex)
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope/s.stderr))
    out = {}
    out["by_h"] = P.groupby("h").apply(slope)
    P5 = P[P.h == 5].copy()
    out["by_coin_h5"] = P5.groupby("coin").apply(slope)
    out["by_year_h5"] = P5.groupby("year").apply(slope)
    out["by_window_h5"] = P5.groupby("w").apply(slope)
    P5["trend"] = pd.cut(P5.r60, [-np.inf, -0.10, 0.10, np.inf], labels=["falling","choppy","rising"])
    out["by_trend_h5"] = P5.groupby("trend").apply(slope)
    P5["fbin"] = pd.cut(P5.f, [-21, -15, -10, -5, -0.01, 0.01, 21])
    out["fbin_h5_meanex"] = P5.groupby("fbin")["ex"].agg(["count","mean","std"])
    P10 = P[P.h == 10].copy(); P10["fbin"] = pd.cut(P10.f, [-21,-15,-10,-5,-0.01,0.01,21])
    out["fbin_h10_meanex"] = P10.groupby("fbin")["ex"].agg(["count","mean"])
    # raw depth slope
    def slope_raw(g):
        g = g.dropna(subset=["raw","ex"])
        if len(g) < 15: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        s = stats.linregress(g.raw, g.ex); return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope/s.stderr))
    out["raw_by_h"] = P.groupby("h").apply(slope_raw)
    # outside profile (agitated), recomputed forecast not recorded -> use past14 as proxy
    A = R[(R.reg != "unknown") & (R.h == 5)].dropna(subset=["past14"])
    s = stats.linregress(A.past14, A.ex); out["agitated_h5_past14_slope_t"] = s.slope/s.stderr
    s = stats.linregress(P5.dropna(subset=["past14"]).past14, P5.dropna(subset=["past14"]).ex); out["calm_h5_past14_slope_t"] = s.slope/s.stderr
    return out
