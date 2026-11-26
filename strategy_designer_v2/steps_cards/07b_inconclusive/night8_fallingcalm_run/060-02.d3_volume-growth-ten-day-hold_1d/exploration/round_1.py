def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            r = pd.Series(c).pct_change()
            vol30 = r.rolling(30).std()
            volmed = vol30.rolling(365, min_periods=60).median()
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                                     ts=df["timestamp"].iloc[i],
                                     f=df["forecast"].iloc[i],
                                     raw=df.get("debug_info.components.vol_shift.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                                     ret=c[i+h]/c[i]-1,
                                     agit=(vol30.iloc[i] > volmed.iloc[i]) if not np.isnan(volmed.iloc[i]) else np.nan))
    R = pd.DataFrame(rows)
    R["mean_h"] = R.groupby(["coin","h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mean_h"]
    A = R[R.f != 0].copy()
    A["val"] = A.f/10*A.ex
    A["side"] = np.where(A.f > 0, "long", "short")
    A["dex"] = np.sign(A.f)*A.ex
    def summ(g):
        d = g.groupby("ts")["val"].sum()
        t = d.mean()/(d.std(ddof=1)/np.sqrt(len(d))) if len(d) > 2 else np.nan
        return pd.Series(dict(cells=len(g), days=len(d), mean=d.mean(), t=t,
                              dir_ex=g.dex.mean(),
                              rho=stats.spearmanr(g.f, g.ex)[0] if len(g) > 5 else np.nan))
    out = {}
    out["by_h"] = A.groupby("h").apply(summ)
    A10 = A[A.h == 10].copy()
    out["by_coin"] = A10.groupby("coin").apply(summ)
    out["by_side"] = A10.groupby("side").apply(summ)
    out["by_window"] = A10.groupby("w").apply(summ)
    out["by_agit"] = A10.groupby("agit").apply(summ)
    A10["q"] = pd.qcut(A10.f.abs(), 4, labels=False, duplicates="drop")
    out["by_absf_q"] = A10.groupby(["side","q"]).apply(summ)
    A10["yr"] = pd.to_datetime(A10.ts).dt.year
    out["by_year"] = A10.groupby("yr").apply(summ)
    out["by_side_h"] = A.groupby(["h","side"]).apply(summ)
    return out
