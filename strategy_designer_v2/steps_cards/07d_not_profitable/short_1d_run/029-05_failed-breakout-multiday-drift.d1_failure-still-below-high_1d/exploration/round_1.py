def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=8
    rows=[]; drifts={}
    for c,ws in data["bars"].items():
        r=[]
        for w,b in ws.items():
            cl=b["close"].values
            for i in range(0,len(cl)-H,H): r.append(cl[i+H]/cl[i]-1)
        drifts[c]=np.mean(r)
        for w,b in ws.items():
            b=b.reset_index(drop=True); cl=b["close"]
            ret60=cl/cl.shift(60)-1; ret20=cl/cl.shift(20)-1
            ma100=cl/cl.rolling(100,min_periods=60).mean()-1
            vol=np.log(cl).diff().rolling(30,min_periods=20).std()
            f=b["forecast"].values; n=len(b)
            for s in range(0,n-H,H):
                for i in range(s,min(s+H,n-H)):
                    if f[i]<0:
                        tot=-(cl[i+H]/cl[i]-1)
                        rows.append(dict(coin=c,win=w,year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                          tot=tot,unus=tot+drifts[c],f=abs(f[i]),r60=ret60[i],r20=ret20[i],ma=ma100[i],vol=vol[i],
                          depth=b.get("debug_info.components.depth.last_history_value",pd.Series(np.nan,index=b.index)).iloc[i]))
                        break
    d=pd.DataFrame(rows)
    def g(col,q=4):
        x=d.dropna(subset=[col]).copy(); x["q"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        return x.groupby("q").agg(lo=(col,"min"),hi=(col,"max"),n=("tot","size"),tot=("tot","mean"),unus=("unus","mean"),
            t=("tot",lambda v:v.mean()/v.std()*np.sqrt(len(v))))
    out={"overall":d[["tot","unus"]].describe().T,
         "by_r60":g("r60"),"by_r20":g("r20"),"by_ma100":g("ma"),"by_vol":g("vol"),"by_depth":g("depth"),"by_f":g("f"),
         "by_coin":d.groupby("coin").agg(n=("tot","size"),tot=("tot","mean"),unus=("unus","mean")),
         "by_year":d.groupby("year").agg(n=("tot","size"),tot=("tot","mean"),unus=("unus","mean"))}
    # book: daily returns, split by held position
    br=[];
    for c,ws in data["days"].items():
        for w,dd in ws.items():
            br.append(dd.assign(coin=c,win=w))
    D=pd.concat(br)
    D=D.dropna(subset=["book_return"])
    out["book_daily"]=pd.Series({"mean":D.book_return.mean(),"share_days_nonzero":(D.book_return.abs()>1e-9).mean()})
    tr=[]
    for c,ws in data["trades"].items():
        for w,t in ws.items(): tr.append(t)
    T=pd.concat(tr)
    out["trades"]=pd.Series({"n":len(T),"gross_mean":T.profit_loss_percent.mean(),"net_mean":T.net_profit_loss_percent.mean(),
        "win":(T.net_profit_loss_percent>0).mean(),"mean_days":T.duration_minutes.mean()/1440})
    return out
