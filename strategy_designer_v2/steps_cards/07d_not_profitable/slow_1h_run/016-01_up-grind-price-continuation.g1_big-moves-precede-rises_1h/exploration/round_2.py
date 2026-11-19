import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    samp = []; R = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            vol = pd.Series(r1).rolling(1440, min_periods=300).std().values*np.sqrt(72)
            past = np.r_[np.full(72,np.nan), c[72:]/c[:-72]-1]
            fwd = np.r_[c[72:]/c[:-72]-1, np.full(72,np.nan)]
            z = past/vol
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            ch = np.abs(b["allocation_change"].fillna(0).values) if "allocation_change" in b else np.abs(np.diff(np.r_[0,alloc]))
            pv = b["total_portfolio_value"].values; pr = b["postRebalance_total_value"].values
            fee = (pv-pr)/pv
            fc = b["forecast"].values
            dfc = np.abs(np.r_[0, np.diff(fc)])
            R.append(pd.DataFrame({"fee":fee,"dfc":dfc,"fc":fc,"alloc":alloc}))
            idx = np.arange(0,len(b),72)
            year = pd.to_datetime(b["timestamp"]).dt.year.values[idx]
            samp.append(pd.DataFrame({"coin":coin,"w":w,"year":year,"z":z[idx],"past":past[idx],"fwd":fwd[idx],"fc":fc[idx]}))
    S = pd.concat(samp).dropna(subset=["fwd","z"]); R = pd.concat(R)
    cm = S.groupby("coin")["fwd"].mean(); S["ex"]=S["fwd"]-S["coin"].map(cm)
    S["az"]=S["z"].abs()
    S["d"]=pd.qcut(S["az"].rank(method="first"),10,labels=False)
    g=S.groupby("d").agg(n=("ex","size"),az=("az","mean"),ex=("ex","mean"),sd=("ex","std"))
    g["t"]=g["ex"]/(g["sd"]/np.sqrt(g["n"])); out["excess by |past/longvol| decile"]=g
    s1=stats.linregress(S["az"],S["ex"]); s2=stats.linregress(S["fc"],S["ex"])
    out["slopes"]=pd.Series({"az_slope_t":s1.slope/s1.stderr,"fc_slope_t":s2.slope/s2.stderr,"corr_fc_az":np.corrcoef(S["fc"],S["az"])[0,1]})
    S["top"]=S["d"]>=8
    out["top-20% |z| excess by year"]=S[S["top"]].groupby("year").agg(n=("ex","size"),ex=("ex","mean"),up=("z",lambda x:(x>0).mean()))
    out["top-20% by sign"]=S[S["top"]].assign(sg=np.sign(S["z"])).groupby("sg").agg(n=("ex","size"),ex=("ex","mean"),sd=("ex","std"))
    R["dq"]=pd.qcut(R["dfc"].rank(method="first"),5,labels=False)
    out["fee by |forecast change| quintile"]=R.groupby("dq").agg(dfc=("dfc","mean"),fee=("fee",lambda x:x.mean()*1e4),share_fee=("fee","sum"))
    out["fee share check"]=pd.Series({"total_fee":R["fee"].sum(),"bars":len(R),"mean_abs_fc_change":R["dfc"].mean(),"mean_fc":R["fc"].mean()})
    return out
