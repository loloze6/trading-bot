def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    # pooled mean daily return per coin
    mu = {}
    for c, ws in bars.items():
        rs = []
        for w, df in ws.items():
            r = df["close"].pct_change()
            rs.append(r.dropna())
        mu[c] = pd.concat(rs).mean()
    rows = []
    for H in [5, 10, 20, 40, 60]:
        for c, ws in bars.items():
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                cl = df["close"].values
                n = len(df)
                raw = df.get("debug_info.components.above_ma.last_history_value")
                for i in range(0, n - H, H):
                    ret = cl[i + H] / cl[i] - 1
                    rows.append(dict(H=H, coin=c, w=w, f=df["forecast"].iloc[i],
                                     raw=(raw.iloc[i] if raw is not None else np.nan),
                                     alloc=df["postRebalance_current_allocation"].iloc[i],
                                     ex=ret - H * mu[c], year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    g = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, hit=(x > 0).mean()))
    out = {}
    # by horizon: f>0 vs f==0
    out["by_H_side"] = g.groupby(["H", g.f > 0])["ex"].apply(tt).unstack()
    g20 = g[g.H == 20].copy()
    pos = g20[g20.f > 0].copy()
    pos["fq"] = pd.qcut(pos.f.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["20_by_fq"] = pos.groupby("fq")["ex"].apply(tt).unstack()
    out["20_by_coin_pos"] = pos.groupby("coin")["ex"].apply(tt).unstack()
    out["20_by_year_pos"] = pos.groupby("year")["ex"].apply(tt).unstack()
    g20["rawq"] = pd.qcut(g20.raw.rank(method="first"), 6, labels=False)
    out["20_by_rawdist_sext"] = g20.groupby("rawq").agg(rawmean=("raw", "mean"), n=("ex", "size"), mean=("ex", "mean"), med=("ex", "median"), hit=("ex", lambda x: (x > 0).mean()))
    g60 = g[g.H == 60].copy()
    g60["rawq"] = pd.qcut(g60.raw.rank(method="first"), 4, labels=False)
    out["60_by_rawdist_q"] = g60.groupby("rawq")["ex"].apply(tt).unstack()
    out["20_raw_corr"] = g20[["raw", "ex"]].corr(method="spearman").iloc[0, 1]
    out["20_pos_median_ex"] = pos.ex.median()
    return out
