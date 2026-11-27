def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            sma = c.rolling(20).mean()
            sd = c.pct_change().rolling(20).std()
            raw = (c - sma) / sma / sd
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for h in (1, 3, 5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, i=i,
                        year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                        ret=c.iloc[i+h]/c.iloc[i]-1, f=df["forecast"].iloc[i],
                        reg=df["regime"].iloc[i], raw=raw.iloc[i]))
    r = pd.DataFrame(rows)
    r["drift"] = r.groupby(["coin","h"])["ret"].transform("mean")
    r["un"] = r["ret"] - r["drift"]
    def tday(s):
        g = s.groupby(level=0).sum(); G=len(g); m = s.mean()
        dev = (s - m).groupby(level=0).sum()
        se = np.sqrt((dev**2).sum()*G/(G-1))/len(s)
        return m, m/se if se>0 else np.nan, len(s), G
    out = {}
    def summ(sub, key):
        res = []
        for k, g in sub.groupby(key):
            s = (-g["un"]).set_axis(g["day"])
            m,t,n,G = tday(s)
            res.append(dict(group=k, mean_short_un=round(m,5), t=round(t,2), n=n, days=G))
        return pd.DataFrame(res)
    ch = r[(r.reg=="unknown")]
    sh = ch[ch.f<0]
    out["short_cases_by_horizon"] = summ(sh, "h")
    s5 = sh[sh.h==5]
    out["h5_by_coin"] = summ(s5, "coin")
    out["h5_by_window"] = summ(s5, "win")
    out["h5_by_year"] = summ(s5, "year")
    s5 = s5.copy(); s5["q"] = pd.qcut(s5["f"].rank(method="first"), 3, labels=["deep","mid","shallow"])
    out["h5_by_forecast_tercile"] = summ(s5, "q")
    # mirror: choppy, raw>0 (long side of carry): long direction unusual
    up = ch[(ch.raw>0)].copy(); up["un"] = -up["un"]  # so summ's -un gives long direction
    out["choppy_above_avg_long_dir_by_h"] = summ(up, "h")
    # raw stretch below avg outside choppy
    oc = r[(r.reg!="unknown") & (r.raw<0)]
    out["nonchoppy_below_short_by_h"] = summ(oc, "h")
    # correlation of raw stretch with fwd unusual in choppy, h5
    c5 = ch[(ch.h==5)].dropna(subset=["raw"])
    out["choppy_h5_spearman_raw_vs_un"] = str(stats.spearmanr(c5.raw, c5.un))
    return out
