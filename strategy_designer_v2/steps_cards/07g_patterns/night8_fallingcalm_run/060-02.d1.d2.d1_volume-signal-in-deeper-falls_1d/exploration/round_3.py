def explore(data):
    import numpy as np, pandas as pd
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            s=pd.Series(b["close"].values); vs=pd.Series(b["volume"].values); n=len(b)
            ret20=s/s.shift(20)-1; ret60=s/s.shift(60)-1
            m30=vs.rolling(30).mean(); lv=np.log(m30/m30.shift(30))
            r1=s.pct_change(); sd30=r1.rolling(30).std()
            ag=sd30/sd30.rolling(60,min_periods=30).median()
            for i in range(0,n-H,H):
                rows.append(dict(coin=coin,w=w,fr=s[i+H]/s[i]-1,ret20=ret20[i],ret60=ret60[i],lv=lv[i],ag=ag[i],
                                 yr=pd.Timestamp(b["timestamp"].iloc[i]).year,day=str(pd.Timestamp(b["timestamp"].iloc[i]).date())))
    d=pd.DataFrame(rows)
    d["ex"]=d["fr"]-d.groupby("coin")["fr"].transform("mean")
    d["tr"]=pd.cut(d.ret60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    d["agb"]=np.where(d.ag>1,"agit","calm")
    out={}
    def clus(g,sig,wt):
        g=g.assign(sx=g.ex*sig,wt=wt).dropna(subset=["sx","wt"])
        dd=g.groupby("day").agg(sx=("sx","sum"),wt=("wt","sum"))
        m=dd.sx.sum()/dd.wt.sum(); dev=dd.sx-m*dd.wt
        se=np.sqrt((dev**2).sum()*len(dd)/(len(dd)-1))/dd.wt.sum()
        return pd.Series(dict(cases=len(g),days=len(dd),mean=m,t=m/se))
    def tab(g):
        a=g.ex.dropna(); return pd.Series(dict(n=len(a),mean=a.mean(),t=a.mean()/(a.std()/np.sqrt(len(a)))))
    for name,sub in [("rising_calm",d[(d.tr=="rising")&(d.agb=="calm")]),("rising_all",d[d.tr=="rising"]),
                     ("rising_r20gt15",d[(d.tr=="rising")&(d.ret20>0.15)])]:
        sub=sub.dropna(subset=["lv"])
        z=(sub.lv-sub.lv.mean())
        out[name+"_signed_dryup_long"]=clus(sub,-np.sign(z),np.abs(z))
        q=pd.qcut(sub.lv,4,labels=False)
        out[name+"_lv_quart"]=sub.groupby(q).apply(tab)
    RC=d[(d.tr=="rising")&(d.agb=="calm")].dropna(subset=["lv"])
    out["rising_calm_by_year"]=RC.groupby("yr").apply(lambda g:clus(g,-np.sign(g.lv-RC.lv.mean()),np.abs(g.lv-RC.lv.mean())))
    out["rising_calm_by_coin"]=RC.groupby("coin").apply(lambda g:clus(g,-np.sign(g.lv-RC.lv.mean()),np.abs(g.lv-RC.lv.mean())))
    # moderate 20-day fall continuation, all trends
    M=d.dropna(subset=["ret20"])
    out["r20_band_by_trend"]=M.assign(b=pd.cut(M.ret20,[-9,-0.25,-0.1,0,0.1,99])).groupby(["tr","b"]).apply(tab)["mean"].unstack()
    mf=M[(M.ret20<0)&(M.ret20>-0.25)]
    out["r20_neg_signed_clustered"]=clus(mf,-1,np.abs(mf.ret20))
    out["r20_neg_by_year"]=mf.groupby("yr").apply(lambda g:clus(g,-1,np.abs(g.ret20)))
    return out
