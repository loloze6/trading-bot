def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        allr=pd.concat([b["close"].pct_change().dropna() for b in wins.values()])
        mu=allr.mean()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; rng=b["high"]-b["low"]
            ratio=rng/rng.rolling(20,min_periods=20).mean()
            clv=(c-b["low"])/rng.replace(0,np.nan)
            ret=c.pct_change()
            v30=ret.rolling(30,min_periods=20).std()
            r1=c.shift(-1)/c-1
            atr_ret=ret/ret.abs().rolling(20,min_periods=10).mean()
            for i in np.where(b["regime"]=="mean_reversion")[0]:
                rows.append(dict(coin=coin,w=w,day=pd.Timestamp(b["timestamp"].iloc[i]).normalize(),
                    ratio=ratio.iloc[i],clv=clv.iloc[i],up=ret.iloc[i],upn=atr_ret.iloc[i],
                    v30=v30.iloc[i],e1=-(r1.iloc[i]-mu)))
    d=pd.DataFrame(rows).dropna(subset=["e1"])
    # coin-level median of v30 over its own recorded bars as agitation proxy
    med={}
    for coin,wins in data["bars"].items():
        s=pd.concat([b["close"].pct_change().rolling(30,min_periods=20).std() for b in wins.values()])
        med[coin]=s.median()
    d["agit"]=np.where(d["v30"]>d["coin"].map(med),"agit","calm")
    def st(g):
        x=g.groupby("day")["e1"].sum(); n=len(g)
        m=g["e1"].mean()
        se=np.sqrt((x-g.groupby("day")["e1"].count()*m).pow(2).sum())/n
        return pd.Series(dict(n=n,days=len(x),mean=m,t=m/se if se>0 else np.nan))
    out={}
    out["by_agit_proxy"]=d.groupby("agit").apply(st)
    for name,col in [("ratio","ratio"),("up","up"),("upn","upn")]:
        d[name+"_h"]=d.groupby("agit")[col].transform(lambda s: pd.qcut(s,2,labels=["lo","hi"]))
        out["agit_x_"+name]=d.groupby(["agit",name+"_h"]).apply(st)
    d["upq"]=pd.qcut(d["upn"],4,labels=False)
    out["by_upn_q_all"]=d.groupby("upq").apply(st)
    out["upn_q_bounds"]=d.groupby("upq")["upn"].agg(["min","max"])
    a=d[d.agit=="agit"]
    out["agit_by_upn_q"]=a.groupby(pd.qcut(a["upn"],3,labels=False)).apply(st)
    out["agit_by_ratio_q"]=a.groupby(pd.qcut(a["ratio"],3,labels=False)).apply(st)
    out["agit_by_window"]=a.groupby("w").apply(st)
    out["calm_by_window"]=d[d.agit=="calm"].groupby("w").apply(st)
    return out
