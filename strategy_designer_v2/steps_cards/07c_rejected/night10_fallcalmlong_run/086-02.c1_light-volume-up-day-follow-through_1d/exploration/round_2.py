def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    H=[3,5,10]
    drift={}
    for coin,wins in data["bars"].items():
        for h in H:
            rr=[]
            for w,b in wins.items():
                c=b["close"].values
                for i in range(0,len(c)-h,h):
                    rr.append(c[i+h]/c[i]-1)
            drift[(coin,h)]=(np.mean(rr),np.std(rr))
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; v=b["volume"]
            vr=v/v.shift(1).rolling(20,min_periods=20).mean()
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"vr":vr,"r1":c.pct_change(),
                            "r10":c/c.shift(10)-1,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                            "inprof":(b["regime"]!="chop").values,
                            "year":pd.to_datetime(b["timestamp"]).dt.year})
            for h in H:
                d[f"f{h}"]=c.shift(-h)/c-1
                d[f"u{h}"]=d[f"f{h}"]-drift[(coin,h)][0]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    P=D[D.inprof & D.vr.notna() & D.r1.notna()].copy()
    q=P.vr.quantile([.25,.5,.75]).values
    P["vrq"]=np.where(P.vr<=q[0],"q1light",np.where(P.vr<=q[1],"q2",np.where(P.vr<=q[2],"q3","q4heavy")))
    def summ(g,h):
        g=g.assign(cell=g.pos//h).drop_duplicates(["coin","win","cell"]).dropna(subset=[f"u{h}"])
        dd=g.groupby("day")[f"u{h}"].sum()
        n=len(g); m=g[f"u{h}"].mean()
        se=np.sqrt((dd-dd.index.map(g.groupby("day").size())*m).pow(2).sum())/n if n>2 else np.nan
        return pd.Series({"n":n,"days":len(dd),"unusual":m,"total":g[f"f{h}"].mean(),"tday":m/se if se else np.nan})
    out={}
    out["vr quartile edges"]=pd.Series(q,index=["q25","q50","q75"])
    U=P[P.r1>0]
    res=[]
    for (y,k),g in U.groupby(["year","vrq"]):
        s=summ(g,5); s["year"]=y; s["vrq"]=k; res.append(s)
    out["up days year x vrq h5"]=pd.DataFrame(res)
    res=[]
    for (c,k),g in U.groupby(["coin",U.vrq=="q1light"]):
        s=summ(g,5); s["coin"]=c; s["q1"]=k; res.append(s)
    out["up days coin x lightest h5"]=pd.DataFrame(res)
    # prior 10-day fall depth x light
    U2=U.copy(); U2["deep"]=U2.r10<U2.r10.median()
    res=[]
    for (dp,k),g in U2.groupby(["deep",U2.vrq=="q1light"]):
        for h in H:
            s=summ(g,h); s["deep10dfall"]=dp; s["q1"]=k; s["h"]=h; res.append(s)
    out["up days prior10d fall x lightest"]=pd.DataFrame(res)
    # all up vs down days in profile, day-clustered
    res=[]
    for up,g in P.groupby(P.r1>0):
        for h in H:
            s=summ(g,h); s["up"]=up; s["h"]=h; res.append(s)
    out["up vs down in profile"]=pd.DataFrame(res)
    # deep prior fall, any day
    P2=P.copy(); P2["r10q"]=pd.qcut(P2.r10,3,labels=["deepfall","mid","shallow"])
    res=[]
    for k,g in P2.groupby("r10q",observed=True):
        for h in H:
            s=summ(g,h); s["r10q"]=k; s["h"]=h; res.append(s)
    out["in profile by prior 10d return tercile"]=pd.DataFrame(res)
    return out
