def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 7, 14]
    # coin mean returns per horizon over all visible windows (non-overlapping grid)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            f = df["forecast"].fillna(0).values
            reg = df["regime"].astype(str).values
            # scaled week return recomputed
            r1 = pd.Series(c).pct_change()
            sd30 = r1.rolling(30).std()
            r7 = pd.Series(c).pct_change(7)
            sc = (r7 / (sd30 * np.sqrt(7))).values
            for h in H:
                for i in range(0, n - h, 7):
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     day=pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                                     h=h, f=f[i], inprof=(reg[i] == "unknown"), sc=sc[i],
                                     ret=c[i + h] / c[i] - 1))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["drift"]
    out = {}

    def summ(g):
        if len(g) < 3:
            return pd.Series(dict(n=len(g), mean_ex=np.nan, t_day=np.nan, mean_tot=np.nan))
        d = g.groupby("day")["ex"].sum()
        nd = g.groupby("day").size()
        m = g["ex"].mean()
        dev = (g["ex"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(g) * np.sqrt(len(dev) / max(len(dev) - 1, 1))
        return pd.Series(dict(n=len(g), days=len(dev), mean_ex=m, t_day=m / se if se > 0 else np.nan,
                              mean_tot=g["ret"].mean()))

    S = R[R.f > 0]
    out["signal_by_horizon"] = S.groupby("h").apply(summ)
    P = R[R.inprof & (R.f == 0)]
    out["inprofile_noSignal_by_horizon"] = P.groupby("h").apply(summ)
    S7 = S[S.h == 7].copy()
    out["sig7_by_coin"] = S7.groupby("coin").apply(summ)
    out["sig7_by_year"] = S7.groupby("year").apply(summ)
    out["sig7_by_window"] = S7.groupby("w").apply(summ)
    S7["fq"] = pd.qcut(S7["f"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["sig7_by_forecast_tercile"] = S7.groupby("fq").apply(summ)
    # in-profile, all bars, by scaled return sign/quintile (both sides)
    P7 = R[R.inprof & (R.h == 7)].dropna(subset=["sc"]).copy()
    P7["scq"] = pd.qcut(P7["sc"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out["inprof7_by_scaled_quintile"] = P7.groupby("scq").apply(summ)
    out["inprof7_corr_sc_ex"] = float(stats.spearmanr(P7["sc"], P7["ex"]).correlation)
    # whole market (all profiles) scaled return quintile
    A7 = R[R.h == 7].dropna(subset=["sc"]).copy()
    A7["scq"] = pd.qcut(A7["sc"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out["all7_by_scaled_quintile"] = A7.groupby("scq").apply(summ)
    return out
