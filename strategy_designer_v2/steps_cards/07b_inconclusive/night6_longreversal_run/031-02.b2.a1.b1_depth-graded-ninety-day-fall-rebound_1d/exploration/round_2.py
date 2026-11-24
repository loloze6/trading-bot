def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            dep = df["debug_info.components.depth.last_history_value"] if "debug_info.components.depth.last_history_value" in df else pd.Series([np.nan]*n)
            for hz in [10, 20, 30]:
                for i in range(0, n - hz, hz):
                    r10 = c[i]/c[i-10]-1 if i >= 10 else np.nan
                    r20 = c[i]/c[i-20]-1 if i >= 20 else np.nan
                    lr = np.diff(np.log(c[max(0,i-30):i+1]))
                    vol = lr.std()*np.sqrt(30) if len(lr) > 10 else np.nan
                    rows.append(dict(coin=coin, w=w, hz=hz, i=i, ret=c[i+hz]/c[i]-1,
                                     regime=df["regime"].iloc[i], fc=df["forecast"].iloc[i],
                                     depth=dep.iloc[i], r10=r10, r20=r20, vol=vol,
                                     ts=df["timestamp"].iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["ret"] - g.groupby(["coin","hz"])["ret"].transform("mean")
    g["day"] = pd.to_datetime(g["ts"]).dt.floor("D")
    cases = g[(g.regime=="mean_reversion") & (g.fc > 0)].copy()

    def summ(d):
        d = d.dropna(subset=["ex"])
        if len(d) < 2: return pd.Series(dict(n=len(d), days=np.nan, mean=np.nan, t_day=np.nan))
        m = d["ex"].mean()
        dev = (d["ex"] - m).groupby(d["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev**2).sum() * G/(G-1)) / len(d) if G > 1 else np.nan
        return pd.Series(dict(n=len(d), days=G, mean=m, t_day=m/se if se else np.nan))

    out = {}
    for var in ["r10", "r20", "vol", "depth"]:
        cc = cases.dropna(subset=[var]).copy()
        cc["q"] = cc.groupby("hz")[var].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
        out["by_" + var + "_tercile"] = cc.groupby(["hz","q"]).apply(summ)
        out["mean_" + var + "_by_tercile"] = cc.groupby(["hz","q"])[var].mean().unstack()
    # sign of recent 20d return: still falling vs turned up
    cc = cases.dropna(subset=["r20"]).copy()
    cc["up20"] = cc["r20"] > 0
    out["by_r20_sign"] = cc.groupby(["hz","up20"]).apply(summ)
    # all bars in regime (any i, overlapping is avoided by grid) old coins vs new coins
    old = ["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]
    cases["old"] = cases.coin.isin(old)
    out["by_old_coins"] = cases.groupby(["hz","old"]).apply(summ)
    # corr depth vs ex
    out["spearman_depth_ex"] = cases.dropna(subset=["depth"]).groupby("hz").apply(lambda d: d["depth"].corr(d["ex"], method="spearman"))
    out["spearman_r20_ex"] = cases.dropna(subset=["r20"]).groupby("hz").apply(lambda d: d["r20"].corr(d["ex"], method="spearman"))
    return out
