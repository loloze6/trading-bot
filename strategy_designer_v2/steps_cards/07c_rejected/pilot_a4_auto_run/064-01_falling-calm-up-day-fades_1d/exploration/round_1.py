import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in [1,3,5,10]:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c)-h, h)
                rr += list(c[idx+h]/c[idx]-1)
            drift[(coin,h)] = np.mean(rr) if rr else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(30).std()
            sc = r1/sd
            inprof = (df["regime"]=="unknown")
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in [1,3,5,10]:
                idx = np.arange(0, len(c)-h, h)
                for i in idx:
                    if not inprof.iloc[i] or not np.isfinite(sc.iloc[i]): continue
                    fr = c.iloc[i+h]/c.iloc[i]-1
                    rows.append(dict(coin=coin, w=w, year=yr.iloc[i], h=h, sc=sc.iloc[i],
                                     ex=fr-drift[(coin,h)], tot=fr, day=str(df["timestamp"].iloc[i])[:10]))
    d = pd.DataFrame(rows)
    out = {}
    def summ(g):
        n=len(g); m=g.ex.mean(); t=m/(g.ex.std()/np.sqrt(n)) if n>2 else np.nan
        sl = stats.linregress(g.sc, g.ex) if n>5 else None
        return pd.Series(dict(n=n, mean_ex=m, t=t, mean_tot=g.tot.mean(),
                              slope=sl.slope if sl else np.nan,
                              slope_t=(sl.slope/sl.stderr) if sl else np.nan))
    up = d[d.sc>0]
    out["up days by horizon (long dir)"] = up.groupby("h").apply(summ)
    out["all in-profile days by horizon"] = d.groupby("h").apply(summ)
    out["down days by horizon"] = d[d.sc<0].groupby("h").apply(summ)
    u3 = up.copy()
    u3["q"] = u3.groupby("h").sc.transform(lambda s: pd.qcut(s,4,labels=False))
    out["up days quartile x horizon mean_ex"] = u3.groupby(["h","q"]).ex.agg(["count","mean"]).unstack("q")
    out["up days quartile x horizon sc mean"] = u3.groupby(["h","q"]).sc.mean().unstack("q")
    out["up h3 by coin"] = up[up.h==3].groupby("coin").apply(summ)
    out["up h5 by coin"] = up[up.h==5].groupby("coin").apply(summ)
    out["up h3 by year"] = up[up.h==3].groupby("year").apply(summ)
    out["up h5 by year"] = up[up.h==5].groupby("year").apply(summ)
    return out
