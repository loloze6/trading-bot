def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    col = "debug_info.components.vol_dryup.post_pipeline_value"
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            r1 = pd.Series(c).pct_change()
            vol30 = r1.rolling(30).std()
            volpct = vol30.rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    rec = col in df.columns and pd.notna(df.loc[i, col])
                    rows.append(dict(coin=coin, w=w, h=h, year=pd.Timestamp(df.loc[i, "timestamp"]).year,
                                     inprof=rec, f=df.loc[i, "forecast"] if rec else np.nan,
                                     raw=df.loc[i, col] if rec else np.nan,
                                     ret=c[i + h] / c[i] - 1, agit=volpct.iloc[i]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["drift"]
    P = R[R.inprof].copy()
    out = {}
    def slope(g):
        g = g.dropna(subset=["f", "ex"])
        if len(g) < 10 or g["f"].std() == 0:
            return pd.Series(dict(n=len(g)))
        s = stats.linregress(g["f"], g["ex"])
        pos = g[g.f > 0]["ex"]; zer = g[g.f == 0]["ex"]
        return pd.Series(dict(n=len(g), npos=len(pos), slope=s.slope, t=s.slope / s.stderr,
                              mpos=pos.mean(), mzero=zer.mean(),
                              welch_t=stats.ttest_ind(pos, zer, equal_var=False).statistic if len(pos) > 2 and len(zer) > 2 else np.nan))
    out["by_h"] = P.groupby("h").apply(slope)
    P5 = P[P.h == 5].copy()
    out["by_coin_h5"] = P5.groupby("coin").apply(slope)
    out["by_window_h5"] = P5.groupby("w").apply(slope)
    out["by_year_h5"] = P5.groupby("year").apply(slope)
    P5["ag"] = np.where(P5.agit > 0.5, "agitated", np.where(P5.agit.notna(), "calm", "na"))
    out["by_agit_h5"] = P5.groupby("ag").apply(slope)
    P10 = P[P.h == 10].copy(); P10["ag"] = np.where(P10.agit > 0.5, "agitated", np.where(P10.agit.notna(), "calm", "na"))
    out["by_agit_h10"] = P10.groupby("ag").apply(slope)
    pos = P5[P5.f > 0].copy()
    pos["q"] = pd.qcut(pos.f, 4, labels=False, duplicates="drop")
    out["pos_quartiles_h5"] = pos.groupby("q").agg(n=("ex", "size"), fmean=("f", "mean"), ex=("ex", "mean"), sd=("ex", "std"))
    P5["rq"] = pd.qcut(P5.raw, 5, labels=False, duplicates="drop")
    out["raw_quintiles_h5"] = P5.groupby("rq").agg(n=("ex", "size"), raw=("raw", "mean"), ex=("ex", "mean"), sd=("ex", "std"))
    out["outside_profile_h5_ex_mean"] = R[(R.h == 5) & (~R.inprof)]["ex"].mean()
    return out
