import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    # coin mean h-return over all its windows (non-overlapping grid)
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            ret28 = pd.Series(c).pct_change(28).values
            raw = df.get("debug_info.components.thin_volume.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            fc = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, year=yr[i],
                                     day=str(pd.to_datetime(df["timestamp"].iloc[i]).date()),
                                     fr=c[i+h]/c[i]-1, regime=df["regime"].iloc[i],
                                     ret28=ret28[i], raw=raw[i], fc=fc[i]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin","h"])["fr"].transform("mean")
    R["ex"] = R["fr"] - R["drift"]
    T = R[(R.regime=="trending") & R.raw.notna()].copy()
    out = {}
    def reg(d, x):
        d = d.dropna(subset=[x,"ex"])
        if len(d) < 10: return (len(d), np.nan, np.nan)
        s = stats.linregress(d[x], d["ex"])
        return (len(d), s.slope, s.slope/s.stderr)
    res = []
    for h in (5,10,20):
        d = T[T.h==h]
        for x in ("raw","fc","ret28"):
            n,sl,t = reg(d,x); res.append(dict(h=h,x=x,n=n,slope=sl,t=t))
    out["slopes_by_h_var (pos slope on raw = thin vol falls more)"] = pd.DataFrame(res)
    d5 = T[T.h==5].copy()
    d5["volq"] = pd.qcut(d5.raw, 4, labels=False)
    out["5d ex by vol quartile (0=thinnest)"] = d5.groupby("volq")["ex"].agg(["count","mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    d5["depq"] = pd.qcut(d5.ret28, 4, labels=False)
    out["5d ex by depth quartile (0=deepest)"] = d5.groupby("depq")["ex"].agg(["count","mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["5d ex depth x vol halves"] = d5.assign(thin=d5.raw<d5.raw.median(), deep=d5.ret28<d5.ret28.median()).groupby(["deep","thin"])["ex"].agg(["count","mean"])
    bc = []
    for k, g in d5.groupby("coin"):
        n,sl,t = reg(g,"raw"); bc.append(dict(coin=k,n=n,slope=sl,t=t,meanex=g.ex.mean()))
    out["by coin raw slope 5d"] = pd.DataFrame(bc)
    by = []
    for k, g in d5.groupby("year"):
        n,sl,t = reg(g,"raw"); by.append(dict(year=k,n=n,slope=sl,t=t,meanex=g.ex.mean()))
    out["by year raw slope 5d"] = pd.DataFrame(by)
    # non-regime vs regime mean ex
    out["regime vs not mean ex"] = R[R.h.isin([5,10,20])].assign(dec=R.ret28<0).groupby(["h","dec"])["ex"].agg(["count","mean"])
    return out
