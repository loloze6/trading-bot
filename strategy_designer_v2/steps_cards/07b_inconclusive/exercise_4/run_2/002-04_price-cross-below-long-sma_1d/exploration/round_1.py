def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    # coin mean daily return over all windows
    mu = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            r = df["close"].pct_change().dropna()
            rs.append(r)
        mu[c] = pd.concat(rs).mean()
    rows = []
    for H in [3, 5, 10, 20, 40]:
        for c in bars:
            for w, df in bars[c].items():
                df = df.reset_index(drop=True)
                cl = df["close"].values
                al = df["postRebalance_current_allocation"].values
                dist = df["debug_info.components.below_ma.last_history_value"].values
                fc = df["forecast"].values
                for i in range(0, len(df) - H, H):
                    ex = cl[i+H]/cl[i]-1 - H*mu[c]
                    rows.append(dict(H=H, coin=c, w=w, al=al[i], dist=dist[i], fc=fc[i], ex=ex,
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    R = pd.DataFrame(rows)
    R["prod"] = R["al"]*R["ex"]
    def tstat(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out = {}
    out["by_H_below_ex"] = R[R.dist<0].groupby("H")["ex"].apply(tstat).unstack()
    out["by_H_above_ex"] = R[R.dist>=0].groupby("H")["ex"].apply(tstat).unstack()
    out["by_H_prod"] = R.groupby("H")["prod"].apply(tstat).unstack()
    R10 = R[(R.H==10)&(R.dist<0)].copy()
    R10["dbin"] = pd.qcut(R10["dist"], 5)
    out["10_below_by_distbin_ex"] = R10.groupby("dbin")["ex"].apply(tstat).unstack()
    R10["fbin"] = pd.qcut(R10["fc"].rank(method="first"), 4, labels=["deepest","q2","q3","shallow"])
    out["10_below_by_fcbin_ex"] = R10.groupby("fbin")["ex"].apply(tstat).unstack()
    out["10_below_by_coin_ex"] = R10.groupby("coin")["ex"].apply(tstat).unstack()
    out["10_below_by_year_ex"] = R10.groupby("year")["ex"].apply(tstat).unstack()
    out["10_prod_by_coin"] = R[(R.H==10)].groupby("coin")["prod"].apply(tstat).unstack()
    R20 = R[(R.H==20)&(R.dist<0)].copy()
    R20["dbin"] = pd.qcut(R20["dist"], 5)
    out["20_below_by_distbin_ex"] = R20.groupby("dbin")["ex"].apply(tstat).unstack()
    out["dist_units_desc"] = R10["dist"].describe()
    return out
