import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    rows = []
    for c, ws in bars.items():
        allr20 = []
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(cl)
            prox = b.get("debug_info.components.low_prox.last_history_value")
            prox = prox.values if prox is not None else np.full(n, np.nan)
            r1 = pd.Series(cl).pct_change().values
            ret20p = pd.Series(cl).pct_change(20).values
            vol20 = pd.Series(r1).rolling(20).std().values
            for h in (5, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=c, win=w, h=h, prox=prox[i], fc=b["forecast"].iloc[i],
                                     fwd=cl[i+h]/cl[i]-1, past20=ret20p[i], r1=r1[i], vol20=vol20[i],
                                     alloc=b["postRebalance_current_allocation"].iloc[i],
                                     wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                                     year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows)
    drift = df.groupby(["coin","h"])["fwd"].transform("mean")
    df["ab"] = df["fwd"] - drift
    d20 = df[df.h==20].copy(); d5 = df[df.h==5].copy()
    out["prox describe"] = d20["prox"].describe()
    def bucket(d, col, q=5):
        d = d.dropna(subset=[col, "ab"]).copy()
        d["b"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        g = d.groupby("b")
        return pd.DataFrame({"lo": g[col].min(), "hi": g[col].max(), "n": g.size(),
                             "mean_ab": g["ab"].mean(), "mean_fwd": g["fwd"].mean(),
                             "t": g["ab"].apply(lambda x: x.mean()/(x.std(ddof=1)/np.sqrt(len(x))))})
    out["20d: by proximity quintile"] = bucket(d20, "prox")
    out["5d: by proximity quintile"] = bucket(d5, "prox")
    out["20d: by past 20d return quintile"] = bucket(d20, "past20")
    out["5d: by past 20d return quintile"] = bucket(d5, "past20")
    out["20d: by 20d vol quintile"] = bucket(d20, "vol20")
    out["5d: by 1d return quintile"] = bucket(d5, "r1")
    # interaction: near low (top prox quintile) and past20
    d = d20.dropna(subset=["prox","past20"]).copy()
    d["nearlow"] = d["prox"] >= d["prox"].quantile(0.8)
    d["down20"] = d["past20"] < 0
    out["20d: nearlow x down20"] = d.groupby(["nearlow","down20"])["ab"].agg(["count","mean"])
    out["20d: by year"] = d20.groupby("year")["ab"].agg(["count","mean"])
    out["20d by coin, top prox quintile"] = d.groupby(["coin","nearlow"])["ab"].agg(["count","mean"]).unstack()
    # book daily
    dd = []
    for c, ws in days.items():
        for w, t in ws.items():
            t = t.copy(); t["coin"]=c; t["win"]=w; dd.append(t)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["coin daily ret by weekday"] = dd.groupby("wd")["coin_return"].agg(["count","mean",
        lambda x: x.mean()/(x.std()/np.sqrt(x.count()))])
    out["book daily ret by weekday"] = dd.groupby("wd")["book_return"].agg(["count","mean"])
    return out
