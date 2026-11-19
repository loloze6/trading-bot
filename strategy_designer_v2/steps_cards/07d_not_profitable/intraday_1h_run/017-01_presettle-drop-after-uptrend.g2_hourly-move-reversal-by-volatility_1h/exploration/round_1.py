import numpy as np, pandas as pd
def explore(data):
    rows=[]; days=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            nr=b["close"].shift(-1)/b["close"]-1
            a=b["postRebalance_current_allocation"]
            g=a*nr
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            to=(b["postRebalance_current_allocation"]-b["previous_allocation"]).abs()
            hr=pd.to_datetime(b["timestamp"]).dt.hour
            f=b["forecast"]
            r4=b["close"].shift(-4)/b["close"]-1
            r24=b["close"].shift(-24)/b["close"]-1
            pos=np.arange(len(b))
            rows.append(pd.DataFrame({"coin":c,"w":w,"nr":nr,"g":g,"fee":fee,"to":to,"hr":hr,"f":f,"a":a,"r4":r4,"r24":r24,"g4":pos%4==0,"g24":pos%24==0}))
    d=pd.concat(rows)
    out={}
    out["per bar"]=pd.Series({"gross_mean_bps":d.g.mean()*1e4,"fee_mean_bps":d.fee.mean()*1e4,"turnover_mean":d.to.mean(),"abs_alloc_mean":d.a.abs().mean(),"fee_per_turnover_bps":d.fee.sum()/d.to.sum()*1e4})
    d["fb"]=pd.qcut(d.f.abs(),5,labels=False,duplicates="drop")
    d["sr"]=np.sign(d.f)*d.nr*1e4
    out["by |f| quintile"]=d.groupby("fb").agg(n=("sr","size"),signed_next1h_bps=("sr","mean"),absf=("f",lambda x:x.abs().mean()))
    d["sr4"]=np.sign(d.f)*d.r4*1e4; d["sr24"]=np.sign(d.f)*d.r24*1e4
    e=d[d.g4]; out["signed next4h bps by quintile"]=e.groupby("fb").sr4.agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    e=d[d.g24]; out["signed next24h bps by quintile"]=e.groupby("fb").sr24.agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["by coin"]=d.groupby("coin").agg(gross_bps=("g",lambda x:x.mean()*1e4),fee_bps=("fee",lambda x:x.mean()*1e4),signed1h=("sr","mean"))
    out["by hour"]=d.groupby("hr").agg(signed1h=("sr","mean"),gross_bps=("g",lambda x:x.mean()*1e4))
    return out
