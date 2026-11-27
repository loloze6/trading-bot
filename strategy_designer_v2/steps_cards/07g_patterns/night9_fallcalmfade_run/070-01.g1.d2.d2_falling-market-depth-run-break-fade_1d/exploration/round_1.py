import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        drift[coin]=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            r=c.pct_change()
            fwd=c.shift(-1)/c-1
            f2=c.shift(-2)/c-1
            # down-run length ending at t-1
            down=(r<0).astype(int).values
            runlen=np.zeros(len(c));runloss=np.zeros(len(c))
            for i in range(1,len(c)):
                if r.iloc[i]>0:
                    k=0;j=i-1
                    while j>=1 and r.iloc[j]<0 and k<30:
                        k+=1;j-=1
                    runlen[i]=k
                    runloss[i]=(c.iloc[i-1]/c.iloc[j]-1)*100 if k>0 else 0
            tr60=c/c.shift(60)-1
            vol20=r.rolling(20).std()
            rng=(b["high"]-b["low"])/c
            clv=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            ret5=c/c.shift(5)-1
            df=pd.DataFrame({"coin":coin,"win":w,"day":ts.dt.floor("D"),"wd":ts.dt.weekday,
                "r":r,"fwd":fwd,"f2":f2,"runlen":runlen,"runloss":runloss,"tr60":tr60,
                "vol20":vol20,"rng":rng,"clv":clv,"ret5":ret5,"regime":b["regime"].values,
                "alloc":b["postRebalance_current_allocation"].astype(float).values})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["dr"]=d.coin.map(drift)
    d["ex"]=d.fwd-d.dr
    d=d.dropna(subset=["fwd","r"])
    d["fall"]=np.where(d.tr60.notna(),d.tr60<-0.10,d.regime!="chop")
    d["trend"]=pd.cut(d.tr60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    d["volq"]=d.groupby("coin").vol20.transform(lambda x:pd.qcut(x,3,labels=False,duplicates="drop"))
    def summ(g,col="ex"):
        s=g.groupby("day")[col].sum()
        n=len(g); m=g[col].mean()
        t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
        return pd.Series({"n":n,"days":len(s),"mean":m,"t_day":t})
    out={}
    brk=d[d.runlen>0].copy()
    brk["rl"]=pd.cut(brk.runlen,[0,1,2,3,30],labels=["1","2","3","4+"])
    out["break_by_trend_runlen"]=brk.groupby(["trend","rl"]).apply(summ).round(4)
    out["break_by_trend"]=brk.groupby("trend").apply(summ).round(4)
    # all days: next-day by today's return quintile and trend
    d["rq"]=d.groupby("coin").r.transform(lambda x:pd.qcut(x,5,labels=False))
    out["all_by_trend_rq"]=d.groupby(["trend","rq"]).apply(summ).round(4)
    out["all_by_trend_volq"]=d.groupby(["trend","volq"]).apply(summ).round(4)
    out["all_by_wd"]=d.groupby("wd").apply(summ).round(4)
    out["fall_by_wd"]=d[d.trend=="falling"].groupby("wd").apply(summ).round(4)
    # up-day size within falling breaks
    fb=brk[brk.trend=="falling"].copy()
    fb["upq"]=pd.qcut(fb.r,3,labels=False)
    out["fallbreak_by_upsize"]=fb.groupby("upq").apply(summ).round(4)
    fb["clvq"]=pd.qcut(fb.clv,3,labels=False,duplicates="drop")
    out["fallbreak_by_clv"]=fb.groupby("clvq").apply(summ).round(4)
    fb["vq"]=fb.volq
    out["fallbreak_by_volq"]=fb.groupby("vq").apply(summ).round(4)
    # 2-day after break
    fb["ex2"]=fb.f2-2*fb.dr
    out["fallbreak_2d"]=summ(fb.dropna(subset=["ex2"]),"ex2").round(4)
    # down days in falling: next day
    out["by_coin_fallbreak"]=fb.groupby("coin").apply(summ).round(4)
    return out
