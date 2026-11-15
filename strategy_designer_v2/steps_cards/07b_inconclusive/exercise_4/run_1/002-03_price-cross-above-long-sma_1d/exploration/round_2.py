def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    fc = "debug_info.components.above_ma.last_history_value"
    mu = {}
    for c in bars:
        mu[c] = pd.concat([df["close"].pct_change().dropna() for df in bars[c].values()]).mean()
    rows = []
    H = 20
    for c in bars:
        for w, df in bars[c].items():
            cl = df["close"].values; f = df["forecast"].values
            raw = df[fc].values if fc in df else np.full(len(df), np.nan)
            al = df["postRebalance_current_allocation"].values
            lr = np.log(df["close"]).diff()
            vol20 = (lr.rolling(20).std()*np.sqrt(365)).values
            vol120 = (lr.rolling(120).std()*np.sqrt(365)).values
            ret60 = (df["close"]/df["close"].shift(60)-1).values
            ret20 = (df["close"]/df["close"].shift(20)-1).values
            above = (np.nan_to_num(raw, nan=-1) > 0).astype(int)
            age = np.zeros(len(df)); a = 0
            for i in range(len(df)):
                a = a+1 if above[i] else 0
                age[i] = a
            for i in range(0, len(df)-H, H):
                ex = cl[i+H]/cl[i]-1 - H*mu[c]
                rows.append((c, w, f[i], raw[i], al[i], ex, vol20[i], vol120[i], ret60[i], ret20[i], age[i]))
    R = pd.DataFrame(rows, columns=["coin","win","f","raw","al","ex","v20","v120","r60","r20","age"])
    on = R[R.f > 0].copy()
    out = {}
    def summ(d):
        return pd.Series(dict(n=len(d), mean=d.ex.mean(), med=d.ex.median(), share=(d.ex>0).mean(),
                              t=stats.ttest_1samp(d.ex,0).statistic if len(d)>2 else np.nan,
                              wmean=(d.al*d.ex).mean()))
    on["ageq"] = pd.cut(on.age, [0,20,60,150,10000], labels=["<=20d","21-60d","61-150d",">150d"])
    out["on_by_age"] = on.groupby("ageq").apply(summ)
    on["volratio"] = on.v20/on.v120
    on["vrq"] = pd.qcut(on.volratio.rank(method="first"), 3, labels=["calmer","mid","hotter"])
    out["on_by_vol_ratio"] = on.groupby("vrq").apply(summ)
    on["vq"] = pd.qcut(on.v120.rank(method="first"), 3, labels=["lowvol","mid","highvol"])
    out["on_by_vol120"] = on.groupby("vq").apply(summ)
    on["r20q"] = pd.qcut(on.r20.rank(method="first"), 3, labels=["r20_low","mid","r20_high"])
    out["on_by_r20"] = on.groupby("r20q").apply(summ)
    R2 = R.dropna(subset=["r60"]).copy()
    R2["r60q"] = pd.qcut(R2.r60.rank(method="first"), 5, labels=False)
    out["all_by_r60_quintile"] = R2.groupby("r60q").apply(summ)
    # skew: contribution of top 5% of on cases
    s = on.ex.sort_values(ascending=False)
    k = max(1,int(len(s)*0.05))
    out["skew"] = pd.Series(dict(mean_all=s.mean(), mean_without_top5pct=s.iloc[k:].mean(), skew=stats.skew(s),
                                 off_skew=stats.skew(R[R.f<=0].ex)))
    # allocation-weighted by coin and window group
    on["wi"] = on.win.str[1:].astype(int)
    out["on_wmean_by_wingroup"] = on.groupby(pd.cut(on.wi,[0,6,12,18,24])).apply(summ)
    return out
