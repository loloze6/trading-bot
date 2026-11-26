import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    drift = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 10, 10):
                g.append(c[i+10]/c[i]-1)
        drift[coin] = np.mean(g)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            s = df["close"]; c = s.values; n = len(c)
            ph = df["high"].shift(1).rolling(60).max().values
            ch = s.diff().abs().rolling(60).sum()
            er = ((s - s.shift(60)).abs() / ch).rolling(5).mean().values
            last = -999
            for i in range(1, n):
                if np.isnan(ph[i]) or np.isnan(er[i]) or np.isnan(ph[i-1]): continue
                if c[i] > ph[i] and c[i-1] <= ph[i-1]:
                    if i - last < 10: continue
                    last = i
                    r = {}
                    for h in (3, 5, 10, 20):
                        r[f"r{h}"] = (c[i+h]/c[i]-1 - drift[coin]*h/10) if i+h < n else np.nan
                    rows.append(dict(coin=coin, w=w, ts=str(df["timestamp"].iloc[i])[:10], er=er[i],
                                     os=c[i]/ph[i]-1, **r))
    ab = pd.DataFrame(rows)
    def tday(x, col):
        x = x.dropna(subset=[col])
        d = x.groupby("ts")[col].sum()
        return pd.Series(dict(n=len(x), days=len(d), mean=x[col].mean(), med=x[col].median(),
                              t=d.mean()/(d.std(ddof=1)/np.sqrt(len(d))) if len(d) > 2 else np.nan))
    out = {}
    lo = ab[ab["er"] <= 0.3]
    out["fresh breakouts ER<=0.3, up-move minus drift by horizon"] = pd.DataFrame({h: tday(lo, h) for h in ["r3","r5","r10","r20"]}).T
    out["fresh breakouts ER>0.3 by horizon"] = pd.DataFrame({h: tday(ab[ab["er"] > 0.3], h) for h in ["r3","r5","r10","r20"]}).T
    ab["erq"] = pd.qcut(ab["er"].rank(method="first"), 4, labels=["q1 flattest","q2","q3","q4 trendiest"])
    out["all fresh breakouts by ER quartile r10"] = ab.groupby("erq").apply(lambda g: pd.concat([tday(g, "r10"), pd.Series({"er": g["er"].mean()})]))
    x = ab.dropna(subset=["r10"])
    sl = stats.linregress(x["er"], x["r10"])
    out["slope r10 on ER, all fresh breakouts"] = pd.Series(dict(slope=sl.slope, t=sl.slope/sl.stderr, n=len(x)))
    out["ER<=0.3 by coin r10"] = lo.groupby("coin").apply(lambda g: tday(g, "r10"))
    out["ER<=0.3 by year-ish window r10"] = lo.groupby("w").apply(lambda g: tday(g, "r10"))
    out["ER<=0.3 share rising 10d"] = float((lo["r10"].dropna() > 0).mean())
    return out
