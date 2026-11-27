def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    drifts={}
    for coin,ws in data["bars"].items():
        d={1:[],2:[],3:[],5:[]}
        for w,b in ws.items():
            c=b["close"].values
            for h in d:
                idx=np.arange(0,len(c)-h,h)
                d[h]+=list(c[idx+h]/c[idx]-1)
        drifts[coin]={h:np.mean(v) for h,v in d.items()}
        for w,b in ws.items():
            c=b["close"].values; n=len(c)
            ts=pd.to_datetime(b["timestamp"]).values
            r=np.r_[np.nan,c[1:]/c[:-1]-1]
            run=np.zeros(n,int)
            for i in range(1,n):
                if r[i]<0: run[i]=run[i-1]+1 if i>1 and r[i-1]<0 else 1
            # down-run length broken at up day i = run[i-1]
            tr60=np.full(n,np.nan)
            tr60[60:]=c[60:]/c[:-60]-1
            sd=pd.Series(r).rolling(30).std().values
            med=pd.Series(sd).rolling(365,min_periods=200).median().values
            seen=set()
            for i in range(2,n-5):
                if r[i]>0 and run[i-1]>=1:
                    cell=i//3
                    if cell in seen: continue
                    seen.add(cell)
                    rows.append(dict(coin=coin,w=w,day=str(ts[i])[:10],k=run[i-1],up=r[i],
                        r1=c[i+1]/c[i]-1,r23=c[i+3]/c[i+1]-1,r13=c[i+3]/c[i]-1,r15=c[i+5]/c[i]-1,
                        tr=tr60[i],agit=(sd[i]>med[i]) if not np.isnan(med[i]) else np.nan,
                        year=str(ts[i])[:4]))
    df=pd.DataFrame(rows)
    for col,h in [("r1",1),("r23",2),("r13",3),("r15",5)]:
        df["x"+col]=-(df[col]-df.coin.map(lambda c:drifts[c][h]))
        df["t"+col]=-df[col]
    def summ(g):
        out={"n":len(g)}
        for col in ["xr1","xr23","xr13","xr15","tr13"]:
            dd=g.groupby("day")[col].apply(lambda s:(s-g[col].mean()).sum())
            D=len(dd); se=np.sqrt((dd**2).sum()*D/(D-1))/len(g) if D>1 else np.nan
            out[col]=round(g[col].mean()*100,3); out["t_"+col]=round(g[col].mean()/se,2)
        return pd.Series(out)
    df["kb"]=df.k.clip(upper=5)
    df["trend"]=np.where(df.tr>0.10,"rising",np.where(df.tr<-0.10,"falling",np.where(df.tr.isna(),"na","choppy")))
    df["upq"]=pd.qcut(df.up,4,labels=["q1","q2","q3","q4"])
    res={"all":summ(df).to_frame().T,
         "by_runlen":df.groupby("kb").apply(summ),
         "by_coin":df.groupby("coin").apply(summ),
         "by_window":df.groupby("w").apply(summ),
         "by_trend":df.groupby("trend").apply(summ),
         "by_agit":df.groupby(df.agit.astype(str)).apply(summ),
         "by_upsize":df.groupby("upq").apply(summ)}
    from scipy import stats
    for col in ["xr23","xr13","xr15","xr1"]:
        s=stats.linregress(df.k.clip(upper=10),df[col])
        res["slope_"+col]=f"{s.slope*100:.4f}% per day, t {s.slope/s.stderr:.2f}"
    res["drift3_mean"]=np.mean([drifts[c][3] for c in drifts])
    return res
