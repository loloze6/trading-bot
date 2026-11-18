def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            # raw share recompute: RSI14 wilder
            d = pd.Series(c).diff()
            up = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            dn = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100/(1+up/dn)
            share = (rsi > 50).astype(float).rolling(14).mean().values - 0.5
            ret14 = pd.Series(c).pct_change(14).values
            n = len(df)
            for h in [1, 3, 7, 14, 21]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, f=f[i], share=share[i],
                                     r14=ret14[i], ts=df["timestamp"].iloc[i],
                                     fr=c[i+h]/c[i]-1))
    R = pd.DataFrame(rows)
    R["year"] = pd.to_datetime(R["ts"]).dt.year
    R["fr_dm"] = R["fr"] - R.groupby(["coin","h"])["fr"].transform("mean")
    def slope(g, x="f"):
        g = g.dropna(subset=[x, "fr_dm"])
        if len(g) < 10 or g[x].std() == 0: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["fr_dm"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope/r.stderr))
    out = {}
    out["by_h_forecast"] = R.groupby("h").apply(slope)
    out["by_h_rawshare"] = R.groupby("h").apply(lambda g: slope(g, "share"))
    out["by_h_ret14"] = R.groupby("h").apply(lambda g: slope(g, "r14"))
    R7 = R[R.h == 7].copy()
    out["h7_by_coin"] = R7.groupby("coin").apply(slope)
    out["h7_by_year"] = R7.groupby("year").apply(slope)
    out["h7_long_side"] = slope(R7[R7.f > 0])
    out["h7_short_side"] = slope(R7[R7.f < 0])
    R7["q"] = pd.qcut(R7["f"].rank(method="first"), 5, labels=False)
    out["h7_quintiles"] = R7.groupby("q").agg(n=("fr_dm","size"), f=("f","mean"),
                                              mean_fr_dm=("fr_dm","mean"),
                                              t=("fr_dm", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    # regime: coin above/below its 14d return sign
    R7["up14"] = R7["r14"] > 0
    out["h7_by_r14sign"] = R7.groupby("up14").apply(slope)
    # book long vs short days
    dd = []
    for coin in bars:
        for w, df in bars[coin].items():
            a = df["postRebalance_current_allocation"].values
            c = df["close"].values
            g = a[:-1] * (c[1:]/c[:-1]-1)
            dd.append(pd.DataFrame(dict(g=g, side=np.sign(a[:-1]))))
    D = pd.concat(dd)
    out["bar_gain_by_side"] = D.groupby("side")["g"].agg(["size","mean","sum"])
    return out
