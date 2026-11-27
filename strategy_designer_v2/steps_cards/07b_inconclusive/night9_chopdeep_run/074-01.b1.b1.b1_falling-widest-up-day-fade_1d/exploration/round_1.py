def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            r = df["close"].pct_change().dropna()
            allr.append(r)
        drift[coin] = pd.concat(allr).mean()
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; h = df["high"]; l = df["low"]; o = df["open"]
            rng = h - l
            rm = rng / rng.rolling(20, min_periods=20).mean()
            ret1 = c.pct_change()
            cl = (c - l) / rng.replace(0, np.nan)
            n = len(df)
            for i in range(n - 1):
                rows.append(dict(coin=coin, w=w, ts=df["timestamp"].iloc[i],
                    regime=df["regime"].iloc[i], alloc=df["postRebalance_current_allocation"].iloc[i],
                    rmr=df["debug_info.components.range_multiple.last_history_value"].iloc[i],
                    rm=rm.iloc[i], ret1=ret1.iloc[i], cl=cl.iloc[i],
                    f1=c.iloc[i+1]/c.iloc[i]-1 - drift[coin],
                    f2=(c.iloc[i+2]/c.iloc[i]-1 - 2*drift[coin]) if i+2 < n else np.nan,
                    f3=(c.iloc[i+3]/c.iloc[i]-1 - 3*drift[coin]) if i+3 < n else np.nan,
                    g1=c.iloc[i+1]/c.iloc[i]-1))
    D = pd.DataFrame(rows)
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["year"] = pd.to_datetime(D["ts"]).dt.year
    cases = D[(D.regime == "mean_reversion")].copy()
    for f in ["f1", "f2", "f3"]:
        cases["s" + f] = -cases[f]
    def tday(x, col):
        x = x.dropna(subset=[col])
        s = x.groupby("day")[col].sum()
        n = x.groupby("day")[col].count()
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev**2).sum()) / len(x) if len(x) > 1 else np.nan
        return pd.Series(dict(n=len(x), days=x["day"].nunique(), mean=m, t=m/se if se else np.nan))
    out = {}
    out["overall"] = pd.DataFrame({c: tday(cases, c) for c in ["sf1", "sf2", "sf3"]})
    out["short_share"] = float((cases.alloc < 0).mean())
    out["by_coin"] = cases.groupby("coin").apply(lambda x: tday(x, "sf1"))
    out["by_window"] = cases.groupby("w").apply(lambda x: tday(x, "sf1"))
    out["by_year"] = cases.groupby("year").apply(lambda x: tday(x, "sf1"))
    cases["rmq"] = pd.qcut(cases["rm"], 5, labels=False, duplicates="drop")
    out["by_rm_quintile"] = cases.groupby("rmq").apply(lambda x: pd.concat([tday(x, "sf1"), pd.Series(dict(rm=x.rm.mean()))]))
    cases["clq"] = pd.qcut(cases["cl"], 3, labels=False, duplicates="drop")
    out["by_close_loc_tercile"] = cases.groupby("clq").apply(lambda x: pd.concat([tday(x, "sf1"), pd.Series(dict(cl=x.cl.mean()))]))
    cases["r1q"] = pd.qcut(cases["ret1"], 3, labels=False, duplicates="drop")
    out["by_upmove_tercile"] = cases.groupby("r1q").apply(lambda x: pd.concat([tday(x, "sf1"), pd.Series(dict(r1=x.ret1.mean()))]))
    # comparison: all up days with rm>=1, outside the falling regime (non-mean_reversion bars, recomputed situation)
    other = D[(D.regime != "mean_reversion") & (D.ret1 > 0) & (D.rm >= 1)].copy()
    other["sf1"] = -other["f1"]
    out["wide_up_days_outside_regime"] = tday(other, "sf1")
    narrow = D[(D.ret1 > 0) & (D.rm < 1)].copy(); narrow["sf1"] = -narrow["f1"]
    out["narrow_up_days_all"] = tday(narrow, "sf1")
    out["spearman_rm_sf1"] = str(stats.spearmanr(cases["rm"], cases["sf1"], nan_policy="omit"))
    return out
