def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    dc = "debug_info.components.below_ma.last_history_value"
    mdr = {}
    for c in bars:
        mdr[c] = pd.concat([df["close"].pct_change().dropna() for df in bars[c].values()]).mean()
    rows = []
    for h in [5, 10, 20]:
        for c in bars:
            for w, df in bars[c].items():
                df = df.reset_index(drop=True)
                cl = df["close"].values
                d = df[dc].values if dc in df else np.full(len(df), np.nan)
                sma = cl / (1 + d / 100.0)
                n = len(df)
                for i in range(0, n - h, h):
                    r = cl[i + h] / cl[i] - 1
                    ex = r - h * mdr[c]
                    sl = sma[i] / sma[i - 10] - 1 if i >= 10 else np.nan
                    p20 = cl[i] / cl[i - 20] - 1 if i >= 20 else np.nan
                    rows.append(dict(h=h, coin=c, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     d=d[i], f=df["forecast"].iloc[i], a=df["postRebalance_current_allocation"].iloc[i],
                                     ex=ex, sl=sl, p20=p20))
    R = pd.DataFrame(rows)
    def tt(s):
        s = s.dropna()
        return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan))
    out = {}
    out["d_range_check"] = R[R.f < 0]["d"].describe()
    act = R[R.f < 0].copy()
    act["shallow"] = np.where(act["d"] > act.groupby("h")["d"].transform("median"), "shallow", "deep")
    out["by_h_depth_ex"] = act.groupby(["h", "shallow"])["ex"].apply(tt).unstack()
    a10 = act[act.h == 10]
    out["welch_h10_shallow_minus_deep"] = pd.Series(stats.ttest_ind(a10[a10.shallow == "shallow"].ex, a10[a10.shallow == "deep"].ex, equal_var=False)._asdict())
    out["h10_shallow_by_coin"] = a10[a10.shallow == "shallow"].groupby("coin")["ex"].apply(tt).unstack()
    out["h10_shallow_by_year"] = a10[a10.shallow == "shallow"].groupby("year")["ex"].apply(tt).unstack()
    out["h10_deep_by_year"] = a10[a10.shallow == "deep"].groupby("year")["ex"].apply(tt).unstack()
    a10 = a10.copy()
    a10["slope"] = np.where(a10["sl"] < 0, "sma_falling", "sma_rising")
    out["h10_by_slope_depth"] = a10.groupby(["slope", "shallow"])["ex"].apply(tt).unstack()
    out["spearman_d_ex_h10"] = pd.Series(stats.spearmanr(a10["d"], a10["ex"], nan_policy="omit")._asdict())
    out["h10_ex_std_active"] = a10["ex"].std()
    return out
