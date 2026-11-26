def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; o=b["open"]; h=b["high"]; l=b["low"]
            r=c.pct_change()
            ar=((h-l)/c).rolling(20).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret":r,"width":(h-l)/(h-l).rolling(20).mean(),
                "push":r/ar,
                "clv":((c-l)/(h-l)).where(h>l),
                "falling":(b["regime"]!="chop"),
                "tr60":c/c.shift(60)-1,
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for k in ["f1","f2","f3"]:
        D["x"+k]=D[k]-D["coin"].map(D.groupby("coin")[k].mean())
    def ct(sub,col):
        s=sub.dropna(subset=[col])
        if len(s)<10: return (len(s),np.nan,np.nan,0)
        g=s.groupby("day")[col].sum(); m=s[col].mean()
        t=g.mean()/(g.std(ddof=1)/np.sqrt(len(g))) if len(g)>2 else np.nan
        return (len(s),round(m*100,3),round(t,2),len(g))
    out={}
    D["up"]=D.ret>0
    F=D[D.falling&D.up].copy()
    F["wide"]=F.width>1
    F["cq"]=pd.qcut(F.clv,3,labels=False)
    out["falling_up_wide_x_clv"]=pd.DataFrame([[a,b_]+list(ct(g,"xf1")) for (a,b_),g in F.groupby(["wide","cq"])],columns=["wide","clvT","n","mean%","t","days"])
    F["pq"]=pd.qcut(F.push,5,labels=False)
    out["falling_up_by_push"]=pd.DataFrame([[q]+list(ct(g,"xf1")) for q,g in F.groupby("pq")],columns=["pushQ","n","mean%","t","days"])
    # half split by window parity for clv effect robustness
    F["half"]=F.w.str[1:].astype(int)<=12
    out["falling_up_clvT_by_half"]=pd.DataFrame([[hh,q]+list(ct(g,"xf1")) for (hh,q),g in F.groupby(["half","cq"])],columns=["w7_12","clvT","n","mean%","t","days"])
    # non-falling wide down days, by trend60 where known, clv, horizons nonoverlap
    N=D[(~D.falling)&(~D.up)&(D.width>1.3)].copy()
    N["trend"]=np.where(N.tr60.isna(),"na",np.where(N.tr60>0.10,"rising","choppy"))
    res=[]
    for hz in [1,2,3]:
        s=N[N.pos%hz==0]
        for k,g in s.groupby("trend"):
            res.append([hz,k]+list(ct(g,"xf%d"%hz)))
    out["nonfalling_widedown_by_trend"]=pd.DataFrame(res,columns=["h","trend","n","mean%","t","days"])
    N2=D[(~D.falling)&(~D.up)].copy(); N2["wq"]=pd.qcut(N2.width,5,labels=False)
    N2["cl"]=N2.clv<0.33
    out["nonfalling_down_wq_x_lowclose"]=pd.DataFrame([[q,cc]+list(ct(g,"xf1")) for (q,cc),g in N2.groupby(["wq","cl"])],columns=["wq","lowclose","n","mean%","t","days"])
    return out
