def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    H=[1,3,5,10]
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
            ret1=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"vr":vr,"r1":ret1,
                            "inprof":(b["regime"]!="chop").values,"regime":b["regime"].values,
                            "year":pd.to_datetime(b["timestamp"]).dt.year})
            for h in H:
                d[f"f{h}"]=c.shift(-h)/c-1
                d[f"u{h}"]=d[f"f{h}"]-drift[(coin,h)][0]
                d[f"s{h}"]=d[f"u{h}"]/drift[(coin,h)][1]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    out["regime counts"]=D.groupby("regime").size()
    P=D[D.inprof & D.vr.notna() & D.r1.notna()].copy()
    P["upday"]=P.r1>0
    P["vrq"]=pd.qcut(P.vr,4,labels=["q1light","q2","q3","q4heavy"])
    def summ(g,h):
        # one case per grid cell of h
        g=g.assign(cell=g.pos//h).drop_duplicates(["coin","win","cell"])
        x=g[f"u{h}"].dropna()
        return pd.Series({"n":len(x),"unusual":x.mean(),"total":g[f"f{h}"].mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    res=[]
    for h in H:
        for (u,q),g in P.groupby(["upday","vrq"],observed=True):
            s=summ(g,h); s["h"]=h; s["up"]=u; s["vrq"]=q; res.append(s)
    out["up/down x vr quartile x horizon"]=pd.DataFrame(res)
    # corr vr vs forward on up days
    U=P[P.upday]
    cr=[]
    for h in H:
        g=U.assign(cell=U.pos//h).drop_duplicates(["coin","win","cell"]).dropna(subset=[f"u{h}"])
        r,p=stats.spearmanr(np.log(g.vr),g[f"u{h}"]); cr.append({"h":h,"n":len(g),"spearman_logvr":r,"p":p})
    out["up days spearman vr vs unusual"]=pd.DataFrame(cr)
    # by coin, heavy (vr>1) vs light, h=5
    res=[]
    for (coin,hv),g in U.groupby(["coin",U.vr>1]):
        s=summ(g,5); s["coin"]=coin; s["heavy"]=hv; res.append(s)
    out["up days by coin heavy/light h5"]=pd.DataFrame(res)
    res=[]
    for (y,hv),g in U.groupby(["year",U.vr>1]):
        s=summ(g,5); s["year"]=y; s["heavy"]=hv; res.append(s)
    out["up days by year heavy/light h5"]=pd.DataFrame(res)
    # up day size x heavy
    U2=U.copy(); U2["bigup"]=U2.r1>U2.r1.median()
    res=[]
    for (bu,hv),g in U2.groupby(["bigup",U2.vr>1]):
        for h in [3,5,10]:
            s=summ(g,h); s["bigup"]=bu; s["heavy"]=hv; s["h"]=h; res.append(s)
    out["up size x heavy"]=pd.DataFrame(res)
    # all in-profile days baseline
    out["all inprofile days"]=pd.DataFrame([dict(summ(P,h),h=h) for h in H])
    return out
