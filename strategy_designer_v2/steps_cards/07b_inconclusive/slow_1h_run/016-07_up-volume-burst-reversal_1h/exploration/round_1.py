def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 72
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            v = df["volume"].values
            n = len(df)
            ppv = df.get("debug_info.components.vol_share.post_pipeline_value")
            raw = df.get("debug_info.components.vol_share.last_history_value")
            for i in range(0, n, H):
                if i < 72: 
                    continue
                past = c[i]/c[i-72]-1
                f = {}
                for h in (24, 72, 144):
                    f[h] = c[i+h]/c[i]-1 if i+h < n else np.nan
                vv = v[i-71:i+1]
                share = np.sort(vv)[-3:].sum()/vv.sum() if vv.sum() > 0 else np.nan
                rows.append(dict(coin=coin, w=w, i=i, regime=df["regime"].iloc[i],
                                 ppv=ppv.iloc[i] if ppv is not None else np.nan,
                                 raw=raw.iloc[i] if raw is not None else np.nan,
                                 share=share, past=past, f24=f[24], f72=f[72], f144=f[144],
                                 yr=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    for h in ("f24", "f72", "f144"):
        d["x"+h] = d[h] - d.groupby("coin")[h].transform("mean")
    out = {}
    def tdiff(s, col, key):
        s = s.dropna(subset=[col, key])
        if len(s) < 30: return (len(s), np.nan, np.nan, np.nan)
        q = s[key].rank(pct=True)
        top = s.loc[q > 2/3, col]; bot = s.loc[q <= 1/3, col]
        t = stats.ttest_ind(top, bot, equal_var=False).statistic
        return (len(s), top.mean(), bot.mean(), t)
    r = d[(d.regime == "mean_reversion")]
    res = {}
    for key in ("ppv", "raw", "share"):
        for col in ("xf24", "xf72", "xf144"):
            res[f"{key}_{col}"] = tdiff(r, col, key)
    out["risen_by_key_horizon"] = pd.DataFrame(res, index=["n", "top", "bot", "t"]).T
    # falls too (other side)
    fl = d[d.past < 0]
    res = {}
    for col in ("xf24", "xf72", "xf144"):
        res[col] = tdiff(fl, col, "share")
    out["fallen_by_share"] = pd.DataFrame(res, index=["n", "top", "bot", "t"]).T
    out["by_coin"] = pd.DataFrame({c: tdiff(g, "xf72", "share") for c, g in r.groupby("coin")}, index=["n", "top", "bot", "t"]).T
    out["by_year"] = pd.DataFrame({c: tdiff(g, "xf72", "share") for c, g in r.groupby("yr")}, index=["n", "top", "bot", "t"]).T
    # by size of past rise
    r = r.copy()
    r["pq"] = pd.qcut(r.past.rank(method="first"), 3, labels=["small", "mid", "big"])
    out["by_rise_size"] = pd.DataFrame({c: tdiff(g, "xf72", "share") for c, g in r.groupby("pq")}, index=["n", "top", "bot", "t"]).T
    # does share add beyond size: corr partial
    rr = r.dropna(subset=["share", "xf72", "past"])
    X = np.column_stack([np.ones(len(rr)), rr.past, rr.share])
    b, *_ = np.linalg.lstsq(X, rr.xf72.values, rcond=None)
    e = rr.xf72.values - X @ b
    cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(rr) - 3)
    out["ols_past_share"] = pd.Series({"b_past": b[1], "t_past": b[1]/np.sqrt(cov[1,1]), "b_share": b[2], "t_share": b[2]/np.sqrt(cov[2,2]), "n": len(rr)})
    out["corr_ppv_share"] = float(r[["ppv", "share"]].corr().iloc[0, 1])
    return out
