def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); v = df["volume"].astype(float)
            up = (c.diff() > 0).astype(float)
            share = (v*up).rolling(20).sum() / v.rolling(20).sum()
            r1 = c.pct_change()
            ret20 = c / c.shift(20) - 1
            volr = v.rolling(20).mean() / v.rolling(60).mean()
            fc = (df["regime"] == "unknown")
            n = len(df)
            for h in [3, 5, 10, 20]:
                fwd = c.shift(-h) / c - 1
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, fc=bool(fc.iloc[i]),
                                     share=share.iloc[i], fwd=fwd.iloc[i], ret20=ret20.iloc[i],
                                     volr=volr.iloc[i], fcst=df["forecast"].iloc[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    R = pd.DataFrame(rows).dropna(subset=["share", "fwd"])
    # demean by coin & horizon over all windows
    R["ex"] = R["fwd"] - R.groupby(["coin", "h"])["fwd"].transform("mean")
    out = {}
    def corr_tab(sub, by):
        res = []
        for k, g in sub.groupby(by):
            if len(g) < 10: continue
            rho, p = stats.spearmanr(g["share"], g["ex"])
            sl = stats.linregress(g["share"], g["ex"])
            res.append(dict(key=str(k), n=len(g), slope=sl.slope, t=sl.slope/sl.stderr if sl.stderr>0 else np.nan, rho=rho, mean_ex=g["ex"].mean()))
        return pd.DataFrame(res)
    out["by_h_profile"] = corr_tab(R, ["h", "fc"])
    fcR = R[R.fc]
    out["fc_by_coin_h10"] = corr_tab(fcR[fcR.h == 10], "coin")
    out["fc_by_year_h10"] = corr_tab(fcR[fcR.h == 10], "year")
    # quintiles of share within falling calm, by horizon
    q = []
    for h, g in fcR.groupby("h"):
        g = g.copy(); g["q"] = pd.qcut(g["share"], 5, labels=False, duplicates="drop")
        for k, gg in g.groupby("q"):
            q.append(dict(h=h, q=k, n=len(gg), share_mean=gg["share"].mean(), mean_ex=gg["ex"].mean(), mean_fwd=gg["fwd"].mean(),
                          t=gg["ex"].mean()/(gg["ex"].std()/np.sqrt(len(gg)))))
    out["fc_quintiles"] = pd.DataFrame(q)
    # recent 20d return and volume ratio as alternatives in falling calm
    alt = []
    for h, g in fcR.groupby("h"):
        for var in ["ret20", "volr"]:
            gg = g.dropna(subset=[var])
            sl = stats.linregress(gg[var], gg["ex"])
            alt.append(dict(h=h, var=var, n=len(gg), slope=sl.slope, t=sl.slope/sl.stderr, rho=stats.spearmanr(gg[var], gg["ex"])[0]))
    out["fc_alt_vars"] = pd.DataFrame(alt)
    # interaction: share high & volume rising
    g = fcR[fcR.h == 10].dropna(subset=["volr"]).copy()
    g["sh_hi"] = g["share"] > g["share"].median(); g["v_hi"] = g["volr"] > g["volr"].median()
    out["fc_h10_share_x_volr"] = g.groupby(["sh_hi", "v_hi"])["ex"].agg(["count", "mean"])
    out["fc_share_dist"] = fcR[fcR.h==10]["share"].describe()
    return out
