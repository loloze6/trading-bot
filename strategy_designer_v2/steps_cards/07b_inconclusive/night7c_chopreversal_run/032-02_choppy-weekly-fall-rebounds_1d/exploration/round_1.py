def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            if n < 60: continue
            r1 = pd.Series(c).pct_change()
            sd30 = r1.rolling(30).std()
            r7 = pd.Series(c) / pd.Series(c).shift(7) - 1
            net = (pd.Series(c) - pd.Series(c).shift(30)).abs()
            path = pd.Series(c).diff().abs().rolling(30).sum()
            er = net / path
            z = r7 / (sd30 * np.sqrt(7))
            reg = df["regime"].values
            fc = df["forecast"].astype(float).values
            for h in (3, 7, 14):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, i=i, ts=df["timestamp"].iloc[i],
                                     fwd=c[i+h]/c[i]-1, z=z.iloc[i], er=er.iloc[i], sd=sd30.iloc[i],
                                     reg=reg[i], fc=fc[i], year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows).dropna(subset=["z", "er"])
    mu = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - mu
    d["exn"] = d["ex"] / d.groupby(["coin","h"])["fwd"].transform("std")
    out = {}
    def summ(g):
        x = g["ex"]; 
        sl = stats.linregress(g["z"], g["ex"]) if len(g) > 5 else None
        return pd.Series(dict(n=len(g), mean_ex=x.mean(), t_mean=x.mean()/(x.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,
                              slope_z=sl.slope if sl else np.nan, t_slope=(sl.slope/sl.stderr) if sl else np.nan))
    d7 = d[d.h == 7]
    d7 = d7.assign(mr=(d7.reg == "mean_reversion"), side=np.where(d7.z < 0, "fall", "rise"))
    out["h7 by regime x side"] = d7.groupby(["mr", "side"]).apply(summ)
    dmf = d7[d7.mr & (d7.z < 0)]
    out["mr falls by z bin"] = dmf.groupby(pd.cut(dmf.z, [-10, -2, -1.5, -1, -0.5, 0])).apply(summ)
    out["mr falls by coin"] = dmf.groupby("coin").apply(summ)
    out["mr falls by window"] = dmf.groupby("win").apply(summ)
    out["mr falls by year"] = dmf.groupby("year").apply(summ)
    out["mr falls by er tercile"] = dmf.groupby(pd.qcut(dmf.er, 3)).apply(summ)
    allf = d[(d.z < 0)].assign(mr=lambda x: x.reg == "mean_reversion")
    out["falls by h x regime"] = allf.groupby(["h", "mr"]).apply(summ)
    # all bars: slope on z across all regimes, by er tercile
    out["h7 all bars by er tercile slope"] = d7.groupby(pd.qcut(d7.er, 3)).apply(summ)
    out["mr falls forecast>0 share"] = float((dmf.fc > 0).mean())
    return out
