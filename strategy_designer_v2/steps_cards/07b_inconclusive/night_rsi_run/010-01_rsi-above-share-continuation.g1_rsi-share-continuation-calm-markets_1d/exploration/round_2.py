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
            r = c.pct_change()
            vol = r.rolling(30).std()
            vrank = vol.rolling(100, min_periods=30).rank(pct=True)
            ret30 = c/c.shift(30)-1
            for h in [7, 14, 30]:
                fwd = c.shift(-h)/c - 1
                for i in range(0, len(df), h):
                    rows.append(dict(coin=coin, w=w, h=h, reg=df["regime"].iloc[i], share=share.iloc[i],
                                     rsi=rsi.iloc[i], fwd=fwd.iloc[i], vrank=vrank.iloc[i], ret30=ret30.iloc[i]))
    R = pd.DataFrame(rows).dropna(subset=["fwd"])
    R["dm"] = R["fwd"] - R.groupby(["coin","h"])["fwd"].transform("mean")
    R["share_c"] = R["share"] - 0.5
    def slope(g, x):
        g = g.dropna(subset=[x, "dm"])
        if len(g) < 10 or g[x].std() == 0: return pd.Series(dict(n=len(g), t=np.nan, corr=np.nan))
        res = stats.linregress(g[x], g["dm"])
        return pd.Series(dict(n=len(g), t=res.slope/res.stderr, corr=res.rvalue))
    out = {}
    R["trend"] = R.reg == "trending"
    out["share_all_coins_h"] = R.groupby("h").apply(lambda g: slope(g, "share_c"))
    out["ret30_by_h_reg"] = R.groupby(["h","trend"]).apply(lambda g: slope(g, "ret30"))
    out["rsi_by_h_reg"] = R.groupby(["h","trend"]).apply(lambda g: slope(g, "rsi"))
    R["vt"] = pd.cut(R.vrank, [0, 0.33, 0.66, 1.0], labels=False)
    out["share_by_h_vtercile"] = R.groupby(["h","vt"]).apply(lambda g: slope(g, "share_c"))
    t14 = R[(R.h==14) & R.trend].dropna(subset=["share"])
    t14 = t14.assign(side=np.sign(t14.share_c))
    out["trend14_side"] = t14.groupby("side")["dm"].agg(["count","mean","std"])
    return out
