def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for h in (24, 72, 168, 480):
                for i in range(0, n - h, h):
                    rows.append((coin, w, int(w[1:]), yr[i], h, f[i], c[i+h]/c[i]-1))
    d = pd.DataFrame(rows, columns=["coin","w","wn","year","h","f","r"])
    d["mean_h"] = d.groupby(["coin","h"])["r"].transform("mean")
    d["ex"] = d["r"] - d["mean_h"]
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["by_h_on"] = d[d.f>0].groupby("h")["ex"].apply(tt).unstack()
    out["by_h_off"] = d[d.f<=0].groupby("h")["ex"].apply(tt).unstack()
    d72 = d[d.h==72]
    on = d72[d72.f>0]
    out["72_by_coin"] = on.groupby("coin")["ex"].apply(tt).unstack()
    out["72_by_year"] = on.groupby("year")["ex"].apply(tt).unstack()
    on = on.copy()
    on["q"] = pd.qcut(on["f"].rank(method="first"), 5, labels=False)
    out["72_by_fq"] = on.groupby("q").agg(fmean=("f","mean"), n=("ex","size"), mean=("ex","mean"), sd=("ex","std"))
    out["72_by_fq"]["t"] = out["72_by_fq"]["mean"]/(out["72_by_fq"]["sd"]/np.sqrt(out["72_by_fq"]["n"]))
    out["72_on_minus_off_welch"] = pd.Series(stats.ttest_ind(d72[d72.f>0].ex, d72[d72.f<=0].ex, equal_var=False))
    out["72_by_wn_on"] = on.groupby("wn")["ex"].apply(tt).unstack()
    out["72_coin_raw_mean"] = d72.groupby("coin")["r"].agg(["mean","std","size"])
    return out
