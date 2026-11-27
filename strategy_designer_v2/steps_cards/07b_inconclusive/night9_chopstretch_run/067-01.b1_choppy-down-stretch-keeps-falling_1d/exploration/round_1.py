import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1,3,5,10,20]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            st = (c - sma) / sma / sd
            ch = (b["regime"] == "unknown")
            for h in H:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    rows.append((coin, w, h, i, st.iloc[i], ch.iloc[i], fwd.iloc[i]))
    df = pd.DataFrame(rows, columns=["coin","w","h","i","st","chop","fwd"])
    drift = df.groupby(["coin","h"])["fwd"].mean().rename("drift")
    usual = df.groupby(["coin","h"])["fwd"].std().rename("usual")
    df = df.join(drift, on=["coin","h"]).join(usual, on=["coin","h"])
    df["ex"] = df["fwd"] - df["drift"]
    df = df.dropna(subset=["st","ex"])
    out = {}
    def reg(d):
        if len(d) < 10: return pd.Series({"n":len(d),"slope":np.nan,"t":np.nan,"mean_ex":np.nan})
        s = stats.linregress(d["st"], d["ex"])
        return pd.Series({"n":len(d),"slope":s.slope,"t":s.slope/s.stderr,"mean_ex":d["ex"].mean(),"t_mean":d["ex"].mean()/(d["ex"].std()/np.sqrt(len(d)))})
    res = []
    for h in H:
        d = df[df.h==h]
        for prof,dd in [("chop",d[d.chop]),("all",d),("notchop",d[~d.chop])]:
            for side,ds in [("below",dd[dd.st<0]),("above",dd[dd.st>0]),("both",dd)]:
                x = reg(ds); x["h"]=h; x["prof"]=prof; x["side"]=side; res.append(x)
    out["reg_by_h_prof_side"] = pd.DataFrame(res)[["h","prof","side","n","slope","t","mean_ex","t_mean"]]
    d5 = df[(df.h==5)&df.chop]
    d5 = d5.assign(q=pd.qcut(d5["st"],8,labels=False))
    out["chop5_by_stretch_octile"] = d5.groupby("q").agg(n=("ex","size"),st=("st","mean"),ex=("ex","mean"),sd=("ex","std"))
    db = d5[d5.st<0]
    out["chop5_below_by_coin"] = db.groupby("coin").apply(reg)
    out["chop5_below_by_window"] = db.groupby("w").apply(reg)
    d10 = df[(df.h==10)&df.chop]
    d10 = d10.assign(q=pd.qcut(d10["st"],8,labels=False))
    out["chop10_by_octile"] = d10.groupby("q").agg(n=("ex","size"),st=("st","mean"),ex=("ex","mean"))
    return out
