def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            allr.append(df["close"].pct_change().dropna())
        drift[coin] = pd.concat(allr).mean()
    col_rm = "debug_info.components.range_multiple.last_history_value"
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); h = df["high"].values.astype(float); l = df["low"].values.astype(float)
            rng = pd.Series(h - l)
            rm = (rng / rng.rolling(20, min_periods=20).mean()).values
            ret1 = pd.Series(c).pct_change().values
            tr60 = (pd.Series(c) / pd.Series(c).shift(60) - 1).values
            cl = ((c - l) / np.where(h - l == 0, np.nan, h - l))
            rmr = df[col_rm].values if col_rm in df.columns else np.full(len(df), np.nan)
            reg = df["regime"].values
            al = df["postRebalance_current_allocation"].values
            ts = pd.to_datetime(df["timestamp"]).values
            n = len(df); d = drift[coin]
            for i in range(n - 1):
                rows.append(dict(coin=coin, w=w, ts=ts[i], regime=reg[i], alloc=al[i], rmr=rmr[i],
                    rm=rm[i], ret1=ret1[i], cl=cl[i], tr60=tr60[i],
                    f1=c[i+1]/c[i]-1-d,
                    f2=(c[i+2]/c[i]-1-2*d) if i+2 < n else np.nan,
                    f3=(c[i+3]/c[i]-1-3*d) if i+3 < n else np.nan,
                    f1b=(c[i+2]/c[i+1]-1-d) if i+2 < n else np.nan))
    D = pd.DataFrame(rows)
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["year"] = pd.to_datetime(D["ts"]).dt.year
    for f in ["f1", "f2", "f3", "f1b"]:
        D["s" + f] = -D[f]
    def tday(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 2:
            return pd.Series(dict(n=len(x), days=0, mean=np.nan, t=np.nan))
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev**2).sum()) / len(x)
        return pd.Series(dict(n=len(x), days=x["day"].nunique(), mean=m, t=m/se if se > 0 else np.nan))
    cases = D[D.regime == "mean_reversion"].copy()
    out = {}
    out["overall"] = pd.DataFrame({c: tday(cases, c) for c in ["sf1", "sf2", "sf3", "sf1b"]})
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
    cases["trq"] = pd.qcut(cases["tr60"], 3, labels=False, duplicates="drop")
    out["by_trend_tercile"] = cases.groupby("trq").apply(lambda x: pd.concat([tday(x, "sf1"), pd.Series(dict(tr=x.tr60.mean()))]))
    up = D[(D.ret1 > 0) & D.rm.notna() & D.tr60.notna()].copy()
    up["prof"] = np.where(up.tr60 < -0.10, "falling", np.where(up.tr60 > 0.10, "rising", "choppy"))
    up["wide"] = np.where(up.rm >= 1, "wide", "narrow")
    out["up_days_by_profile_width"] = up.groupby(["prof", "wide"]).apply(lambda x: tday(x, "sf1"))
    fw = up[up.prof == "falling"].copy()
    out["falling_up_wide_minus_narrow_welch"] = str(stats.ttest_ind(fw[fw.wide=="wide"].sf1.dropna(), fw[fw.wide=="narrow"].sf1.dropna(), equal_var=False))
    out["spearman_rm_sf1_cases"] = str(stats.spearmanr(cases["rm"], cases["sf1"], nan_policy="omit"))
    out["case_sf1_median_std"] = pd.Series(dict(median=cases.sf1.median(), std=cases.sf1.std(), pos_share=(cases.sf1 > 0).mean()))
    return out
