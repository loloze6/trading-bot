import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            c = b["close"].values
            allr.append(c[1:]/c[:-1]-1)
        mu1 = np.nanmean(np.concatenate(allr))
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            o,h,l,c,v = [b[k].values.astype(float) for k in ["open","high","low","close","volume"]]
            n = len(c)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            vol20 = pd.Series(r1).rolling(20, min_periods=15).std().values
            vr = v / pd.Series(v).shift(1).rolling(30, min_periods=20).mean().values
            rng = h-l
            wick = np.where(rng>0, (np.minimum(o,c)-l)/rng, np.nan)
            z = r1/vol20
            fc = b["forecast"].fillna(0).values
            for t in range(25, n-5):
                if not (z[t] <= -1): continue
                r = dict(coin=coin, w=w, flush=fc[t]>0, vr=vr[t], wick=wick[t], z=z[t],
                         ret5=c[t]/c[t-5]-1, ret5z=(c[t]/c[t-5]-1)/(vol20[t]*np.sqrt(5)),
                         d1=c[t+1]/c[t]-1-mu1,
                         d23=c[t+3]/c[t+1]-1-2*mu1,
                         c3=c[t+3]/c[t]-1-3*mu1,
                         c5=c[t+5]/c[t]-1-5*mu1)
                rows.append(r)
    df = pd.DataFrame(rows)
    out = {}
    def tt(x):
        x = x.dropna(); return pd.Series(dict(mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))), n=len(x)))
    out["all falls<=-1sd"] = pd.DataFrame({k: tt(df[k]) for k in ["d1","d23","c3","c5"]}).T
    out["flush only"] = pd.DataFrame({k: tt(df.loc[df.flush,k]) for k in ["d1","d23","c3","c5"]}).T
    out["nonflush falls"] = pd.DataFrame({k: tt(df.loc[~df.flush,k]) for k in ["d1","d23","c3","c5"]}).T
    df["vrq"] = pd.qcut(df["vr"], 4, labels=False)
    out["falls by vol ratio quartile"] = df.groupby("vrq")[["vr","d1","d23","c3"]].mean().join(df.groupby("vrq").size().rename("n"))
    df["wq"] = pd.qcut(df["wick"], 4, labels=False)
    out["falls by wick quartile"] = df.groupby("wq")[["wick","d1","d23","c3"]].mean().join(df.groupby("wq").size().rename("n"))
    df["r5q"] = pd.qcut(df["ret5z"], 4, labels=False)
    out["falls by prior 5d ret (vol units) quartile"] = df.groupby("r5q")[["ret5z","d1","d23","c3"]].mean().join(df.groupby("r5q").size().rename("n"))
    fl = df[df.flush].copy()
    fl["r5q"] = pd.qcut(fl["ret5z"], 3, labels=False)
    g = fl.groupby("r5q")
    out["flush by prior5d tercile"] = pd.DataFrame({"ret5z": g["ret5z"].mean(),
        "c3": g["c3"].mean(), "t_c3": g["c3"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x)))), "n": g.size()})
    out["spearman falls"] = pd.Series({k: stats.spearmanr(df[k], df["c3"], nan_policy="omit")[0] for k in ["vr","wick","z","ret5z"]})
    return out
