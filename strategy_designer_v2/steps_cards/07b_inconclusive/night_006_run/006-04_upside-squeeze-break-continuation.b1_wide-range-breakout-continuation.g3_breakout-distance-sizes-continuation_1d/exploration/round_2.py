def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            h = df["high"]; l = df["low"]; v = df["volume"]
            ph = h.shift(1).rolling(20).max().values
            pl = l.shift(1).rolling(20).min().values
            rng20 = (h.shift(1).rolling(20).max()/l.shift(1).rolling(20).min()-1).values
            rng60 = (h.shift(1).rolling(60, min_periods=40).max()/l.shift(1).rolling(60, min_periods=40).min()-1).values
            vr = (v/v.shift(1).rolling(20).mean()).values
            r10p = (df["close"]/df["close"].shift(10)-1).values
            n = len(df)
            for i in range(0, n-10, 10):
                rows.append(dict(coin=coin, win=w, fc=df["forecast"].iloc[i],
                                 dist=c[i]/ph[i]-1 if not np.isnan(ph[i]) else np.nan,
                                 comp=rng20[i]/rng60[i] if rng60[i] and not np.isnan(rng60[i]) else np.nan,
                                 vr=vr[i], r10p=r10p[i], r=c[i+10]/c[i]-1))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
    out = {}
    def sl(s, x):
        s = s.dropna(subset=[x,"ex"])
        if len(s) < 8: return pd.Series(dict(n=len(s)))
        r = stats.linregress(s[x], s["ex"]); sp = stats.spearmanr(s[x], s["ex"])
        return pd.Series(dict(n=len(s), slope_t=r.slope/r.stderr, rho=sp.correlation, mean_ex=s.ex.mean()))
    p = d[d.fc > 0].dropna(subset=["fc","ex"])
    out["no_ZEC"] = sl(p[p.coin!="ZECUSD"], "fc")
    ps = p.sort_values("ex")
    out["drop_top3_ex"] = sl(ps.iloc[:-3], "fc")
    out["drop_top3_fc"] = sl(p.sort_values("fc").iloc[:-3], "fc")
    top = p.sort_values("fc").tail(8)
    out["top8_fc"] = pd.Series(dict(fc_mean=top.fc.mean(), ex_mean=top.ex.mean(), ex_med=top.ex.median(), share_pos=(top.ex>0).mean()))
    out["pos_vol_ratio"] = sl(p, "vr")
    out["pos_compression"] = sl(p, "comp")
    out["pos_prior10ret"] = sl(p, "r10p")
    out["share_pos_ex_breakouts"] = pd.Series(dict(n=len(p), share=(p.ex>0).mean(), median=p.ex.median()))
    a = d.dropna(subset=["r10p","ex"])
    out["all_prior10ret"] = sl(a, "r10p")
    q = p.copy(); q["vq"] = pd.qcut(q.vr, 3, labels=False, duplicates="drop")
    out["pos_by_vol_tercile"] = q.groupby("vq").agg(n=("ex","size"), vr=("vr","mean"), mean_ex=("ex","mean"), med=("ex","median"))
    return out
