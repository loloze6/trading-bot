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
            v10=vs.rolling(10).mean(); lv10=np.log(v10/vs.rolling(60).mean())
            r1=s.pct_change(); sd30=r1.rolling(30).std()
            ag=sd30/sd30.rolling(60,min_periods=30).median()
            for i in range(0,n-H,H):
                rows.append(dict(coin=coin,w=w,fr=s[i+H]/s[i]-1,ret20=ret20[i],ret60=ret60[i],lv=lv[i],lv10=lv10[i],ag=ag[i],
                                 yr=pd.Timestamp(b["timestamp"].iloc[i]).year,day=str(pd.Timestamp(b["timestamp"].iloc[i]).date())))
    d=pd.DataFrame(rows)
    d["ex"]=d["fr"]-d.groupby("coin")["fr"].transform("mean")
    d["tr"]=pd.cut(d.ret60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    d["agb"]=np.where(d.ag>1,"agit","calm")
    out={}
    def cor(g,x="lv"):
        g=g[[x,"ex"]].dropna()
        if len(g)<10: return pd.Series(dict(n=len(g),r=np.nan,t=np.nan))
        r=g.corr().iloc[0,1]; return pd.Series(dict(n=len(g),r=r,t=r*np.sqrt((len(g)-2)/(1-r*r))))
    def tab(g,col="ex"):
        a=g[col].dropna(); return pd.Series(dict(n=len(a),mean=a.mean(),t=a.mean()/(a.std()/np.sqrt(len(a)))))
    R=d[d.tr=="rising"].copy()
    R["lvq"]=pd.qcut(R.lv,5,labels=False)
    out["rising_lv_quint"]=R.groupby("lvq").apply(tab)
    out["rising_lv_quint_by_ag"]=R.groupby(["agb","lvq"]).apply(tab)["mean"].unstack()
    out["rising_corr_by_coin"]=R.groupby("coin").apply(cor)
    out["rising_corr_by_year"]=R.groupby("yr").apply(cor)
    out["rising_corr_lv10"]=R.groupby("agb").apply(lambda g:cor(g,"lv10"))
    # signed: short when volume grew, scaled by lv, day-clustered t
    R2=R.dropna(subset=["lv"]).copy(); R2["sx"]=-R2.ex*np.sign(R2.lv)*np.abs(R2.lv)
    dd=R2.groupby("day").agg(sx=("sx","sum"),wt=("lv",lambda x:np.abs(x).sum()))
    m=dd.sx.sum()/dd.wt.sum(); dev=dd.sx-m*dd.wt
    out["rising_weighted_signed"]=pd.Series(dict(days=len(dd),mean=m,t=m/(np.sqrt((dev**2).sum()*len(dd)/(len(dd)-1))/dd.wt.sum())))
    # volume growth x ret20 inside rising
    R["r20b"]=pd.cut(R.ret20,[-9,0,0.15,99])
    out["rising_corr_by_ret20"]=R.groupby("r20b").apply(cor)
    C=d[(d.tr=="choppy")&(d.agb=="agit")]
    out["choppy_agit_by_coin"]=C.groupby("coin").apply(cor)
    out["choppy_agit_by_year"]=C.groupby("yr").apply(cor)
    return out
