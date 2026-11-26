def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            r28 = pd.Series(c).pct_change(28).values
            rng = ((df["high"]-df["low"])/df["close"]).astype(float).rolling(20).mean().values
            for H in (5, 10, 20):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, H=H, f=f[i], ret=c[i+H]/c[i]-1,
                                     day=ts.iloc[i].floor("D"), year=ts.iloc[i].year,
                                     r28=r28[i], rng=rng[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin","H"])["ret"].transform("mean")
    d["g"] = d["f"]/10*d["ex"]
    def tday(s):
        x = s.groupby(level=0).sum() if False else s
        return x
    def stat(sub):
        per = sub.groupby("day")["g"].sum()
        m = sub["g"].mean()
        sd = per.std(ddof=1)
        t = per.mean()/(sd/np.sqrt(len(per))) if len(per)>1 and sd>0 else np.nan
        return pd.Series({"n": len(sub), "days": len(per), "mean_g": m, "t": t})
    out = {}
    out["by_H"] = d.groupby("H").apply(stat)
    d10 = d[d.H==10].copy()
    out["by_coin"] = d10.groupby("coin").apply(stat)
    out["by_window"] = d10.groupby("win").apply(stat)
    out["by_year"] = d10.groupby("year").apply(stat)
    d10["side"] = np.sign(d10["f"])
    out["by_side"] = d10.groupby("side").apply(lambda s: pd.Series({"n":len(s),"mean_ex":s["ex"].mean(),"t":stats.ttest_1samp(s["ex"],0).statistic}))
    d10["fb"] = pd.cut(d10["f"], [-21,-4,-2,0,2,4,21])
    out["by_fbucket"] = d10.groupby("fb").agg(n=("ex","size"), mean_ex=("ex","mean"), mean_ret=("ret","mean"))
    d10["r28s"] = np.where(d10["r28"]<0, "r28<0", "r28>=0")
    out["by_r28sign"] = d10.groupby("r28s").apply(stat)
    d10["rngq"] = pd.qcut(d10["rng"], 3, labels=["lowrng","midrng","hirng"])
    out["by_range"] = d10.groupby("rngq").apply(stat)
    out["by_r28_side"] = d10.groupby(["r28s","side"]).agg(n=("ex","size"), mean_ex=("ex","mean"))
    return out
