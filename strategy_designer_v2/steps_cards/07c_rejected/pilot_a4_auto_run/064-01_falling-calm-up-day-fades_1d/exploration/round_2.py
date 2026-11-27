import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        drift = {}
        for h in [2,3,4,5,7]:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c)-h, h)
                rr += list(c[idx+h]/c[idx]-1)
            drift[h] = np.mean(rr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(30).std()
            sc1 = r1/sd
            r3 = c/c.shift(3)-1
            sc3 = r3/(sd*np.sqrt(3))
            inprof = (df["regime"]=="unknown")
            for h in [2,3,4,5,7]:
                for i in np.arange(0, len(c)-h, h):
                    if not inprof.iloc[i] or not np.isfinite(sc1.iloc[i]): continue
                    fr = c.iloc[i+h]/c.iloc[i]-1
                    rows.append(dict(coin=coin, w=w, h=h, sc1=sc1.iloc[i], sc3=sc3.iloc[i],
                                     ex=fr-drift[h], tot=fr, usual=np.nan,
                                     day=str(df["timestamp"].iloc[i])[:10]))
    d = pd.DataFrame(rows)
    out = {}
    def summ(g, col):
        g = g.dropna(subset=[col])
        n=len(g)
        dd = g.groupby("day").ex.sum(); nd=len(dd)
        m = g.ex.mean()
        se = np.sqrt(((dd - g.groupby("day").size()*m)**2).sum())/n if n>2 else np.nan
        sl = stats.linregress(g[col], g.ex) if n>5 else None
        return pd.Series(dict(n=n, days=nd, mean_ex=m, t_dayclust=m/se if se else np.nan,
                              mean_tot=g.tot.mean(), slope=sl.slope if sl else np.nan,
                              slope_t=sl.slope/sl.stderr if sl else np.nan))
    out["1d rise >0, by horizon"] = d[d.sc1>0].groupby("h").apply(lambda g: summ(g,"sc1"))
    out["3d rise >0, by horizon"] = d[d.sc3>0].groupby("h").apply(lambda g: summ(g,"sc3"))
    out["3d fall <0, by horizon"] = d[d.sc3<0].groupby("h").apply(lambda g: summ(g,"sc3"))
    up5 = d[(d.sc1>0)&(d.h==5)].copy()
    up5["half"] = np.where(up5.sc1>up5.sc1.median(),"big","small")
    out["1d rise h5 big vs small"] = up5.groupby("half").apply(lambda g: summ(g,"sc1"))
    up5w = d[(d.sc1>0)&(d.h==5)]
    out["1d rise h5 by window: n, mean_ex"] = up5w.groupby("w").ex.agg(["count","mean"])
    return out
