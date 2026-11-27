def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    # drift per coin per horizon, non-overlapping, all windows
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            rng = h - l
            loc = np.where(rng > 0, (h - c) / np.where(rng > 0, rng, 1), np.nan)  # 1 = at low
            agit = (df["regime"] != "chop").values
            n = len(df)
            r60 = pd.Series(c).pct_change(60).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for H in (1, 3, 7, 14):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, H=H, i=i, year=yr[i],
                                     loc=loc[i], agit=agit[i], fc=df["forecast"].iloc[i],
                                     ret=c[i + H] / c[i] - 1, r60=r60[i],
                                     ts=str(df["timestamp"].iloc[i])[:10]))
    R = pd.DataFrame(rows)
    drift = R.groupby(["coin", "H"])["ret"].agg(["mean", "std"]).rename(columns={"mean": "d", "std": "s"})
    R = R.join(drift, on=["coin", "H"])
    R["unus"] = R["ret"] - R["d"]  # long direction
    def tstat(sub, col="unus"):
        g = sub.groupby("ts")[col].sum()
        m = sub[col].mean(); n = len(sub)
        se = g.std(ddof=1) * np.sqrt(len(g)) / n if len(g) > 1 else np.nan
        return pd.Series(dict(n=n, days=len(g), mean=m, t=m / se if se else np.nan))
    out = {}
    A = R[R.agit & R["loc"].notna()].copy()
    A["locq"] = pd.cut(A["loc"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["top", "upmid", "lowmid", "bottom"])
    out["agitated_by_locq_H_longdir"] = A.groupby(["H", "locq"]).apply(tstat).reset_index()
    C = R[R.agit & (R["loc"] >= 0.75)].copy()
    C7 = C[C.H == 7]
    out["low_close_H7_by_coin_shortdir"] = C7.assign(unus=-C7.unus).groupby("coin").apply(tstat)
    out["low_close_H7_by_year_shortdir"] = C7.assign(unus=-C7.unus).groupby("year").apply(tstat)
    C7 = C7.assign(tr=pd.cut(C7.r60, [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"]))
    out["low_close_H7_by_trend_shortdir"] = C7.assign(unus=-C7.unus).groupby("tr").apply(tstat)
    Cal = R[(~R.agit) & R["loc"].notna()].copy()
    Cal["locq"] = pd.cut(Cal["loc"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["top", "upmid", "lowmid", "bottom"])
    out["calm_by_locq_H7_longdir"] = Cal[Cal.H == 7].groupby("locq").apply(tstat)
    A7 = A[A.H == 7]
    out["agit_H7_corr_loc_unus"] = float(np.corrcoef(A7["loc"], A7["unus"] / A7["s"])[0, 1])
    return out
