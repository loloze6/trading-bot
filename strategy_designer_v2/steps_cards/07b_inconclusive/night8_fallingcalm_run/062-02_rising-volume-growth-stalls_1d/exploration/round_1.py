def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].astype(float)
            m1 = v.rolling(30).mean(); m0 = v.shift(30).rolling(30).mean()
            lvr = np.log(m1 / m0)
            ret60 = df["close"] / df["close"].shift(60) - 1
            dr = df["close"].pct_change()
            vol30 = dr.rolling(30).std()
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, i=i,
                        day=str(df["timestamp"].iloc[i])[:10],
                        year=str(df["timestamp"].iloc[i])[:4],
                        fwd=c[i+h]/c[i]-1, fc=df["forecast"].iloc[i],
                        reg=df["regime"].iloc[i], lvr=lvr.iloc[i],
                        r60=ret60.iloc[i], vol30=vol30.iloc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin","h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    inp = d[(d.fc != 0) & d.fc.notna()].copy()
    out = {}
    def slope(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 15: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, corr=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope/r.stderr, corr=r.rvalue))
    out["slope_by_h"] = inp.groupby("h").apply(slope)
    i5 = inp[inp.h == 5]
    out["slope_by_coin_h5"] = i5.groupby("coin").apply(slope)
    out["slope_by_window_h5"] = i5.groupby("win").apply(slope)
    out["slope_by_year_h5"] = i5.groupby("year").apply(slope)
    out["slope_rawlvr_by_h"] = inp.groupby("h").apply(lambda g: slope(g, "lvr"))
    # quintiles of raw lvr, excess returns, by h
    q = []
    for h in H:
        g = inp[inp.h == h].dropna(subset=["lvr"]).copy()
        g["q"] = pd.qcut(g["lvr"], 5, labels=False)
        s = g.groupby("q").agg(n=("ex","size"), lvr=("lvr","mean"), ex=("ex","mean"), tot=("fwd","mean"),
                               t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
        s["h"] = h; q.append(s.reset_index())
    out["lvr_quintiles"] = pd.concat(q)
    # side: long (fc>0) vs short
    i5 = i5.copy(); i5["side"] = np.where(i5.fc > 0, "long", "short")
    out["side_h5"] = i5.groupby("side").agg(n=("ex","size"), ex=("ex","mean"),
        t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    # strength of trend: r60 tercile
    g = i5.dropna(subset=["r60"]).copy(); g["r60q"] = pd.qcut(g["r60"], 3, labels=False)
    out["slope_by_r60tercile_h5"] = g.groupby("r60q").apply(slope)
    g = i5.dropna(subset=["vol30"]).copy(); g["vq"] = pd.qcut(g["vol30"], 2, labels=False)
    out["slope_by_vol30half_h5"] = g.groupby("vq").apply(slope)
    # all bars, any profile, raw lvr
    a = d.dropna(subset=["lvr","r60"])
    a["prof"] = np.where(a.r60 > .1, "rising", np.where(a.r60 < -.1, "falling", "choppy"))
    out["rawlvr_slope_by_profile_h"] = a.groupby(["prof","h"]).apply(lambda g: slope(g, "lvr"))
    return out
