def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            r=c.pct_change()
            sd30=r.rolling(30).std()
            pct=sd30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret":r,"width":(h-l)/(h-l).rolling(20).mean(),
                "clv":((c-l)/(h-l)).where(h>l),
                "falling":(b["regime"]!="chop"),
                "tr60":c/c.shift(60)-1,"agit":pct>0.5,"pctna":pct.isna(),
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
    R=D[(~D.falling)&(D.tr60>0.10)&(D.ret<0)].copy()
    R["wq"]=pd.qcut(R.width,4,labels=False)
    R["ag"]=np.where(R.pctna,"na",np.where(R.agit,"agit","calm"))
    res=[]
    for hz in [1,2,3]:
        s=R[R.pos%hz==0]
        for (a,q),g in s.groupby(["ag","wq"]):
            res.append([hz,a,q]+list(ct(g,"xf%d"%hz)))
    out["rising_down_by_agit_widthQ"]=pd.DataFrame(res,columns=["h","ag","wq","n","mean%","t","days"])
    s=R[R.pos%2==0].copy(); s["half"]=s.w.str[1:].astype(int)<=12
    out["rising_down_wq_by_half_h2"]=pd.DataFrame([[hh,q]+list(ct(g,"xf2")) for (hh,q),g in s.groupby(["half","wq"])],columns=["w7_12","wq","n","mean%","t","days"])
    s["lc"]=s.clv<0.33
    out["rising_down_wq_lowclose_h2"]=pd.DataFrame([[q,cc]+list(ct(g,"xf2")) for (q,cc),g in s.groupby(["wq","lc"])],columns=["wq","lowclose","n","mean%","t","days"])
    return out
