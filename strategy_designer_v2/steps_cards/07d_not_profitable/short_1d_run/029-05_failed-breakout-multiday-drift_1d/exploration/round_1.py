def explore(data):
    import numpy as np, pandas as pd
    H=8; rows=[]
    for coin,ws in data["bars"].items():
        g=[]
        for b in ws.values():
            c=b["close"].values
            g+= [c[i+H]/c[i]-1 for i in range(0,len(c)-H,H)]
        dr=np.mean(g)
        for w,b in ws.items():
            c=b["close"].values.astype(float); n=len(c)
            ph=pd.Series(c).rolling(20).max().shift(1).values
            seen=set()
            for e in range(4,n):
                ref=next((ph[k] for k in (e-1,e-2,e-3) if not np.isnan(ph[k]) and c[k]>ph[k]),None)
                if ref is None or c[e]>=ref: continue
                t=e+2
                if t+H>=n or t//H in seen: continue
                seen.add(t//H)
                r=c[t+H]/c[t]-1
                rows.append(dict(coin=coin,year=pd.Timestamp(b["timestamp"].iloc[t]).year,
                    depth=(ref-c[e])/ref,
                    r60=c[t]/c[t-60]-1 if t>=60 else np.nan,
                    bounce=c[t]/c[e]-1,
                    unus=-(r-dr),tot=-r))
    d=pd.DataFrame(rows)
    def s(gr):
        return gr["unus"].agg(n="size",mean="mean",t=lambda x:x.mean()/(x.std()/np.sqrt(len(x)))).join(gr["tot"].mean().rename("total"))
    out={"all":s(d.assign(k=1).groupby("k"))}
    for col in ["depth","r60","bounce"]:
        q=d.dropna(subset=[col]).copy()
        q["q"]=pd.qcut(q[col],3,labels=["low","mid","high"])
        x=s(q.groupby("q")); x["avg"]=q.groupby("q")[col].mean(); out["by_"+col]=x
    out["by_coin"]=s(d.groupby("coin"))
    out["by_year"]=s(d.groupby("year"))
    T=pd.concat([t for ws in data["trades"].values() for t in ws.values() if len(t)])
    out["trades"]=pd.Series({"n":len(T),"pl":T.profit_loss_percent.mean(),"net":T.net_profit_loss_percent.mean(),
        "win":(T.profit_loss_percent>0).mean(),"days":T.duration_minutes.mean()/1440})
    return out
