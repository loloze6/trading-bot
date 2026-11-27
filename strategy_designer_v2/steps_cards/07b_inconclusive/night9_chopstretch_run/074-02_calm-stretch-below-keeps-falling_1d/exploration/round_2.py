def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            for h in [2, 3, 4, 5, 7, 10]:
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                        day=pd.Timestamp(df["timestamp"].iloc[i]).normalize(),
                        yr=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        fc=df["forecast"].iloc[i],
                        ret=c.iloc[i + h] / c.iloc[i] - 1))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby(["coin", "h"])["ret"].transform("mean")
    g["ex"] = g["ret"] - g["drift"]
    def reg(s):
        s = s.dropna(subset=["fc", "ex"])
        if len(s) < 8: return pd.Series(dict(n=len(s)))
        lr = stats.linregress(s["fc"], s["ex"])
        # day-clustered mean of short-side excess
        d = (-s["ex"]).groupby(s["day"]).sum()
        nd = len(d); m = (-s["ex"]).mean()
        se = np.sqrt(((d - d.mean())**2).sum()) / len(s) * np.sqrt(nd/(nd-1)) if nd > 1 else np.nan
        return pd.Series(dict(n=len(s), slope=lr.slope, t_slope=lr.slope/lr.stderr,
                              short_ex=m, t_short_clust=m/se if se else np.nan, days=nd))
    neg = g[g.fc < 0]
    out = {}
    out["fc_neg_by_h"] = neg.groupby("h").apply(reg)
    for h in [3, 5]:
        s = neg[neg.h == h]
        out[f"h{h}_by_coin"] = s.groupby("coin").apply(reg)
        out[f"h{h}_by_year"] = s.groupby("yr").apply(reg)
        s = s.copy()
        s["q"] = pd.qcut(s.fc, 4, labels=False)
        out[f"h{h}_by_fc_q"] = s.groupby("q").agg(n=("ex", "size"), fc=("fc", "mean"), ex=("ex", "mean"), ret=("ret", "mean"))
    return out
