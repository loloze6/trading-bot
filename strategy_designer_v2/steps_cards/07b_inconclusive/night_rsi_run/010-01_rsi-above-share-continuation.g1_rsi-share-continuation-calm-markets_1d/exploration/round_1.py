def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            d = c.diff()
            up = d.clip(lower=0); dn = (-d).clip(lower=0)
            au = up.ewm(alpha=1/14, adjust=False, min_periods=14).mean()
            ad = dn.ewm(alpha=1/14, adjust=False, min_periods=14).mean()
            rsi = 100 - 100/(1+au/ad)
            share = (rsi > 50).astype(float).where(rsi.notna()).rolling(30, min_periods=30).mean()
            r = np.log(c).diff()
            vol = r.rolling(30).std()
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in [7, 14, 30]:
                fwd = c.shift(-h)/c - 1
                for i in range(0, len(df), h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, yr=yr[i], fc=df["forecast"].iloc[i],
                                     reg=df["regime"].iloc[i], share=share.iloc[i], fwd=fwd.iloc[i],
                                     vol=vol.iloc[i], ret30=c.iloc[i]/c.iloc[max(0,i-30)]-1 if i>=30 else np.nan))
    R = pd.DataFrame(rows).dropna(subset=["fwd"])
    R["dm"] = R["fwd"] - R.groupby(["coin","h"])["fwd"].transform("mean")
    def slope(g, x):
        g = g.dropna(subset=[x, "dm"])
        if len(g) < 10 or g[x].std() == 0: return pd.Series(dict(n=len(g), t=np.nan, corr=np.nan))
        res = stats.linregress(g[x], g["dm"])
        return pd.Series(dict(n=len(g), t=res.slope/res.stderr, corr=res.rvalue))
    out = {}
    act = R[(R.reg=="trending") & (R.fc!=0)]
    out["active_by_h"] = act.groupby("h").apply(lambda g: slope(g, "fc"))
    out["active_by_h_coin"] = act.groupby(["h","coin"]).apply(lambda g: slope(g, "fc"))
    out["active14_by_year"] = act[act.h==14].groupby("yr").apply(lambda g: slope(g, "fc"))
    R["share_c"] = R["share"] - 0.5
    out["share_all_by_h_reg"] = R.groupby(["h", R.reg=="trending"]).apply(lambda g: slope(g, "share_c"))
    a14 = act[act.h==14].copy()
    a14["side"] = np.sign(a14.fc)
    out["active14_side_mean"] = a14.groupby("side")["dm"].agg(["count","mean","std"])
    a14["q"] = pd.qcut(a14.fc.abs(), 3, labels=False, duplicates="drop")
    out["active14_signed_by_absq"] = a14.assign(sr=a14.side*a14.dm).groupby("q")["sr"].agg(["count","mean","std"])
    R14 = R[(R.h==14)].dropna(subset=["share"]).copy()
    R14["sq"] = pd.qcut(R14.share, 5, labels=False, duplicates="drop")
    out["all14_by_sharequint"] = R14.groupby(["sq", R14.reg=="trending"])["dm"].agg(["count","mean"]).unstack()
    return out
