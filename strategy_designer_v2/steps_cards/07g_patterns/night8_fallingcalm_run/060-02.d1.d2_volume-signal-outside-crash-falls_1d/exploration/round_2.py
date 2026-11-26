def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            for i in range(0,len(b)-H,H):
                allr.append(c[i+H]/c[i]-1)
        drift=np.mean(allr); sd=np.std(allr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; v=b["volume"]
            r20=c/c.shift(20)-1; r60=c/c.shift(60)-1
            lvr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            r1=c/c.shift(1)-1
            vol30=r1.rolling(30).std()
            vrel=vol30/vol30.rolling(120,min_periods=60).median()
            yr=pd.to_datetime(b["timestamp"]).dt.year
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            for i in range(0,len(b)-H,H):
                fr=c[i+H]/c[i]-1
                rows.append(dict(coin=coin,w=w,yr=yr[i],day=day[i],fc=b["forecast"][i],
                    r20=r20[i],r60=r60[i],lvr=lvr[i],vrel=vrel[i],ex=fr-drift,z=(fr-drift)/sd))
    d=pd.DataFrame(rows)
    out={}
    def tday(x,col="ex"):
        s=x.groupby("day")[col].sum()
        return pd.Series({"n":len(x),"days":len(s),"mean":x[col].mean(),"t_day":s.mean()/(s.std()/np.sqrt(len(s)))})
    nf=d[(d.r60>=-0.10)].dropna(subset=["lvr","ex"]).copy()
    # graded slope of z on lvr outside falling
    sl=stats.linregress(nf.lvr,nf.z)
    out["nonfalling_slope_z_on_lvr"]=pd.Series({"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(nf)})
    nf["q"]=pd.qcut(nf.lvr,5,labels=False)
    out["nonfalling_lowlvr_by_coin"]=nf[nf.q==0].groupby("coin").apply(lambda x:pd.Series({"n":len(x),"mean":x.ex.mean()}))
    out["nonfalling_lowlvr_by_year"]=nf[nf.q==0].groupby("yr").apply(lambda x:pd.Series({"n":len(x),"mean":x.ex.mean()}))
    out["nonfalling_lowlvr_tday"]=tday(nf[nf.q==0])
    nf["dec"]=pd.qcut(nf.lvr,10,labels=False)
    out["nonfalling_lvr_deciles"]=nf.groupby("dec").apply(lambda x:pd.Series({"n":len(x),"lvr":x.lvr.mean(),"mean":x.ex.mean()}))
    # r20 momentum by profile trend
    d2=d.dropna(subset=["r20","r60","ex"]).copy()
    d2["tr"]=np.where(d2.r60>0.1,"rising",np.where(d2.r60<-0.1,"falling","choppy"))
    d2["r20b"]=pd.cut(d2.r20,[-1,-0.2,-0.05,0.05,0.2,10])
    g=d2.groupby(["tr","r20b"]).apply(lambda x:pd.Series({"n":len(x),"mean":x.ex.mean(),"t":x.ex.mean()/(x.ex.std()/np.sqrt(max(len(x),2)))}))
    out["r20_by_trend"]=g.reset_index().astype({"r20b":str})
    f=d2[(d2.tr=="falling")&(d2.r20<0)&(d2.r20>=-0.2)]
    out["falling_modfall_by_year"]=f.groupby("yr").ex.agg(["count","mean"])
    out["falling_modfall_tday"]=tday(f)
    # active: joint regression of z on lvr and r20
    a=d[(d.fc!=0)].dropna(subset=["lvr","r20","z","vrel"])
    X=np.column_stack([np.ones(len(a)),a.lvr,a.r20])
    beta,res,rk,sv=np.linalg.lstsq(X,a.z.values,rcond=None)
    e=a.z.values-X@beta; s2=e@e/(len(a)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["active_joint_z"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["const","lvr","r20"])
    a=a.copy(); a["sx"]=np.sign(a.fc)*a.ex
    a["ag"]=np.where(a.vrel>1,"agitated","calm")
    out["active_signed_by_agitation"]=a.groupby("ag").sx.agg(["count","mean","std"])
    a["s"]=np.sign(a.fc)
    out["active_side_by_agitation"]=a.groupby(["ag","s"]).ex.agg(["count","mean"]).reset_index()
    return out
