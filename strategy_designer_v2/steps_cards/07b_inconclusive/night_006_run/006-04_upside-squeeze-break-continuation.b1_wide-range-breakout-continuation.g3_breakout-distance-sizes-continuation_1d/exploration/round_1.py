def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            h = df["high"]
            ph = h.shift(1).rolling(20).max().values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for H in (5, 10, 20, 30):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, H=H, i=i, year=yr[i],
                                     fc=df["forecast"].iloc[i],
                                     dist=c[i]/ph[i]-1 if not np.isnan(ph[i]) else np.nan,
                                     r=c[i+H]/c[i]-1))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby(["coin","H"])["r"].transform("mean")
    out = {}
    def slope(s, x="fc"):
        s = s.dropna(subset=[x,"ex"])
        if len(s) < 5 or s[x].std()==0: return pd.Series(dict(n=len(s), slope_t=np.nan, mean_ex=s["ex"].mean() if len(s) else np.nan))
        r = stats.linregress(s[x], s["ex"])
        return pd.Series(dict(n=len(s), slope_t=r.slope/r.stderr, mean_ex=s["ex"].mean(), t_mean=s["ex"].mean()/(s["ex"].std()/np.sqrt(len(s)))))
    pos = d[d.fc > 0]
    out["by_H_fc"] = pos.groupby("H").apply(slope)
    out["by_H_rawdist_pos"] = d[d.dist > 0].groupby("H").apply(lambda s: slope(s, "dist"))
    out["by_H_rawdist_all"] = d.groupby("H").apply(lambda s: slope(s, "dist"))
    p10 = pos[pos.H==10]
    out["H10_by_coin"] = p10.groupby("coin").apply(slope)
    out["H10_by_year"] = p10.groupby("year").apply(slope)
    q = p10.copy(); q["qt"] = pd.qcut(q.fc, 3, labels=False, duplicates="drop")
    out["H10_by_fc_tercile"] = q.groupby("qt").agg(n=("ex","size"), fc=("fc","mean"), mean_ex=("ex","mean"), med_ex=("ex","median"))
    nonpos = d[(d.H==10)&(d.fc<=0)]
    out["H10_fc0_mean_ex"] = pd.Series(dict(n=len(nonpos), mean_ex=nonpos.ex.mean()))
    # outlier influence
    s = p10.dropna(subset=["fc","ex"])
    lo, hi = s.ex.quantile([0.05,0.95])
    st = s[(s.ex>lo)&(s.ex<hi)]
    r = stats.linregress(st.fc, st.ex)
    out["H10_trimmed_slope_t"] = pd.Series(dict(n=len(st), t=r.slope/r.stderr))
    sp = stats.spearmanr(s.fc, s.ex)
    out["H10_spearman"] = pd.Series(dict(n=len(s), rho=sp.correlation, p=sp.pvalue))
    return out
