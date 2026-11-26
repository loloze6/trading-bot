def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    def tt(x):
        x=pd.Series(x).dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def tday(v,day):
        df=pd.DataFrame({"v":v,"d":day}).dropna()
        m=df.v.mean(); s=(df.v-m).groupby(df.d).sum(); J=len(s)
        se=np.sqrt((s**2).sum()*J/(J-1))/len(df)
        return pd.Series({"n":len(df),"days":J,"mean":m,"t_day":m/se})
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change(); v30=r1.rolling(30).std()
            ret60=c/c.shift(60)-1
            dist=c/c.rolling(20).mean()-1
            ts=pd.to_datetime(b["timestamp"])
            for h in (2,3,5):
                pass
            f2=c.shift(-2)/c-1; f3=c.shift(-3)/c-1; f5=c.shift(-5)/c-1; f10=c.shift(-10)/c-1
            for i in range(len(b)):
                rows.append(dict(coin=coin,w=w,i=i,r1=r1[i],v30=v30[i],ret60=ret60[i],dist=dist[i],
                  f2=f2[i],f3=f3[i],f5=f5[i],f10=f10[i],day=ts[i].normalize(),yr=ts[i].year,inprof=b["regime"][i]=="unknown"))
    D=pd.DataFrame(rows)
    D["agit"]=D["v30"]/D.groupby("coin")["v30"].transform("median")>1
    D["trend"]=np.where(D["ret60"]>0.1,"rise",np.where(D["ret60"]<-0.1,"fall","chop")); D.loc[D.ret60.isna(),"trend"]=np.nan
    D["z"]=D["r1"]/D["v30"]
    res={}
    for h in (2,3,5):
        G=D[D.i%h==0].dropna(subset=["z",f"f{h}","trend"]).copy()
        G["ex"]=G[f"f{h}"]-G.groupby("coin")[f"f{h}"].transform("mean")
        FA=G[(G.trend=="fall")&G.agit&(G.z>0)].copy()
        res[f"fallag up: -z*ex h{h}"]=tday(-FA["z"]*FA["ex"],FA["day"])
        res[f"fallag up: -ex h{h}"]=tday(-FA["ex"],FA["day"])
        FC=G[(G.trend=="fall")&(~G.agit)&(G.z<0)].copy()
        res[f"fallcalm down: z*ex h{h}"]=tday(FC["z"].abs()*(-FC["ex"]),FC["day"])
        if h==3:
            FA["q"]=pd.qcut(FA["z"],4,labels=False); out["fallag up z quartile ex3"]=FA.groupby("q")["ex"].apply(tt).unstack()
            out["fallag up z>1 ex3 by year"]=FA[FA.z>1].groupby("yr")["ex"].apply(tt).unstack()
            FC["q"]=pd.qcut(FC["z"],4,labels=False); out["fallcalm down z quartile ex3"]=FC.groupby("q")["ex"].apply(tt).unstack()
            out["fallcalm down z<-1 ex3 by year"]=FC[FC.z<-1].groupby("yr")["ex"].apply(tt).unstack()
            RA=G[(G.trend=="rise")&(G.z<-1)]
            out["rise z<-1 ex3 by agit x year"]=RA.groupby(["agit","yr"])["ex"].mean().unstack()
    out["clustered tests"]=pd.DataFrame(res).T
    G=D[D.i%10==0].dropna(subset=["dist","f10","trend"]).copy()
    G["ex"]=G["f10"]-G.groupby("coin")["f10"].transform("mean")
    CB=G[(G.trend=="chop")&(G.dist<0)].copy()
    out["chop below avg: -ex10 by agit"]=CB.groupby("agit").apply(lambda g:tday(-g["ex"],g["day"]))
    CB["q"]=pd.qcut(CB["dist"],3,labels=False)
    out["chop below avg ex10 by dist tercile"]=CB.groupby("q")["ex"].apply(tt).unstack()
    out["chop below avg -ex10 by year"]=CB.groupby("yr")["ex"].apply(lambda x:-x.mean())
    return out
