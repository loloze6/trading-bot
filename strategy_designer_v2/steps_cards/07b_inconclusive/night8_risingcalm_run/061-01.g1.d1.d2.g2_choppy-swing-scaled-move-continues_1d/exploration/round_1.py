def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            r1 = pd.Series(c).pct_change()
            vol30 = r1.rolling(30, min_periods=20).std().values
            ret5p = pd.Series(c).pct_change(5).values
            for H in [1, 3, 5, 10, 20]:
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, H=H, i=i,
                        year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                        f=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                        fwd=c[i + H] / c[i] - 1, vol30=vol30[i], past5=ret5p[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "H"])["fwd"].transform("mean")
    d["adj"] = d["fwd"] - d["drift"]
    out = {}
    def summ(g):
        g = g[g["f"] != 0]
        if len(g) < 5:
            return pd.Series(dict(n=len(g)))
        s = np.sign(g["f"]) * g["adj"]
        dm = s.groupby(g["day"]).sum()
        t = dm.mean() / (dm.std(ddof=1) / np.sqrt(len(dm))) * 1  # per-day sum t
        sl = stats.linregress(g["f"], g["adj"])
        return pd.Series(dict(n=len(g), mean_signed=s.mean(), t_signed=t,
                              slope=sl.slope, t_slope=sl.slope / sl.stderr))
    out["by_horizon"] = d.groupby("H").apply(summ)
    d5 = d[d["H"] == 5].copy()
    out["h5_by_coin"] = d5.groupby("coin").apply(summ)
    out["h5_by_year"] = d5.groupby("year").apply(summ)
    nz = d5[d5["f"] != 0].copy()
    nz["side"] = np.where(nz["f"] > 0, "long", "short")
    out["h5_by_side"] = nz.groupby("side").apply(summ)
    nz["fq"] = pd.qcut(nz["f"].abs(), 3, labels=["low", "mid", "high"])
    out["h5_by_absf_tercile"] = nz.groupby("fq").apply(summ)
    vq = nz.groupby("coin")["vol30"].transform(lambda x: x.rank(pct=True))
    nz["agit"] = np.where(vq > 0.5, "agitated_proxy", "calm_proxy")
    out["h5_by_agit_proxy"] = nz.groupby("agit").apply(summ)
    out["h5_by_side_agit"] = nz.groupby(["side", "agit"]).apply(summ)
    out["h5_by_side_tercile"] = nz.groupby(["side", "fq"]).apply(summ)
    for H in [10, 20]:
        g = d[(d["H"] == H) & (d["f"] != 0)].copy()
        g["side"] = np.where(g["f"] > 0, "long", "short")
        out[f"h{H}_by_side"] = g.groupby("side").apply(summ)
    return out
