def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 30
    # coin mean 30d return on grid over all windows
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            for hz in [10, 20, 30, 60]:
                for i in range(0, n - hz, hz):
                    rows.append(dict(coin=coin, w=w, hz=hz, i=i, ts=df["timestamp"].iloc[i],
                                     ret=c[i+hz]/c[i]-1, regime=df["regime"].iloc[i],
                                     fc=df["forecast"].iloc[i],
                                     depth=df.get("debug_info.components.depth.last_history_value", pd.Series([np.nan]*n)).iloc[i]))
    g = pd.DataFrame(rows)
    g["mean_coin"] = g.groupby(["coin","hz"])["ret"].transform("mean")
    g["ex"] = g["ret"] - g["mean_coin"]
    g["year"] = pd.to_datetime(g["ts"]).dt.year
    cases = g[(g.regime=="mean_reversion") & (g.fc > 0)].copy()

    def summ(s):
        s = s.dropna()
        n = len(s)
        return pd.Series(dict(n=n, mean=s.mean(), t=s.mean()/(s.std(ddof=1)/np.sqrt(n)) if n > 1 else np.nan))

    out = {}
    out["by_horizon"] = cases.groupby("hz")["ex"].apply(summ).unstack()
    c30 = cases[cases.hz==30]
    out["by_coin_30"] = c30.groupby("coin")["ex"].apply(summ).unstack()
    out["by_year_30"] = c30.groupby("year")["ex"].apply(summ).unstack()
    out["by_window_30"] = c30.groupby("w")["ex"].apply(summ).unstack()
    c30 = c30.copy()
    c30["fq"] = pd.qcut(c30["fc"].rank(method="first"), 3, labels=["low","mid","high"])
    out["by_fc_tercile_30"] = c30.groupby("fq")["ex"].apply(summ).unstack()
    out["raw_ret_30_cases"] = summ(c30["ret"])
    out["noncases_30_ex"] = summ(g[(g.hz==30) & ~((g.regime=="mean_reversion") & (g.fc>0))]["ex"])
    out["regime_counts_30"] = g[g.hz==30].groupby("regime").size()
    out["fc_zero_in_mr_30"] = int(((g.hz==30)&(g.regime=="mean_reversion")&(g.fc<=0)).sum())
    # horizon by fc tercile
    cases2 = cases.copy()
    cases2["fq"] = cases2.groupby("hz")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["hz_by_fq_mean"] = cases2.groupby(["hz","fq"])["ex"].mean().unstack()
    return out
