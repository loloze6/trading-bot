import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z=r/sd
            nxt=c.shift(-1)/c-1
            ret60=c/c.shift(60)-1
            ret30=c/c.shift(30)-1
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                            "r":r,"z":z,"nxt":nxt,"ret60":ret60,"ret30":ret30,
                            "agit":(b["regime"]!="chop"),"fc":b["forecast"].astype(float),
                            "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(mu)
    D=D.dropna(subset=["z","ex"])
    def st(g):
        dd=g.groupby("day")["ex"].mean()
        return pd.Series({"n":len(g),"days":len(dd),"mean_ex%":g["ex"].mean()*100,
                          "t_day":dd.mean()/(dd.std()/np.sqrt(len(dd))) if len(dd)>2 else np.nan})
    def wst(g):
        f=g["fc"]; e=g["ex"]
        m=(f*e).sum()/f.sum()
        res=(f*(e-m)); dd=res.groupby(g["day"]).sum(); fd=f.groupby(g["day"]).sum()
        se=np.sqrt((dd**2).sum())/fd.sum()
        return pd.Series({"n":len(g),"wmean%":m*100,"t":m/se})
    out={}
    A=D[D.agit&(D.z>0)&(D.fc>0)].copy()
    A["tr"]=np.where(A.ret60>0.1,"rising",np.where(A.ret60<-0.1,"falling",np.where(A.ret60.notna(),"choppy","na")))
    A["tr30"]=np.where(A.ret30>0.1,"rising",np.where(A.ret30<-0.1,"falling",np.where(A.ret30.notna(),"choppy","na")))
    out["agit_up_weighted_by_trend60"]=A.groupby("tr").apply(wst)
    out["agit_up_by_trend30"]=A.groupby("tr30").apply(st)
    R=A[A.tr=="rising"]
    out["rising_by_z"]=R.groupby(pd.cut(R.z,[0,0.5,1,2,99]),observed=True).apply(st)
    out["rising_by_coin"]=R.groupby("coin").apply(st)
    out["rising_by_year"]=R.groupby("year").apply(st)
    out["rising_corr_z_ex"]=float(np.corrcoef(R.z,R.ex)[0,1])
    F=A[A.tr=="falling"]
    out["falling_by_z"]=F.groupby(pd.cut(F.z,[0,0.5,1,2,99]),observed=True).apply(st)
    C=D[(~D.agit)&(D.z>0)].copy()
    C["tr"]=np.where(C.ret60>0.1,"rising",np.where(C.ret60<-0.1,"falling",np.where(C.ret60.notna(),"choppy","na")))
    out["calm_up_by_trend60"]=C.groupby("tr").apply(st)
    return out
