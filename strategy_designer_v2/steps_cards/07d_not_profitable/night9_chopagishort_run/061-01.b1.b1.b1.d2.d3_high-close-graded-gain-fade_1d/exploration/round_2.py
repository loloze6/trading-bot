def explore(data):
    import numpy as np, pandas as pd
    out={}
    drift={}
    for coin,ws in data["bars"].items():
        for H in [2,3,5,10]:
            rets=[]
            for w,b in ws.items():
                c=b["close"].values
                for i in range(0,len(c)-H,H):
                    rets.append(c[i+H]/c[i]-1)
            drift[(coin,H)]=(np.mean(rets),np.std(rets))
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            loc=(c-l)/(h-l).replace(0,np.nan)
            r1=c.pct_change()
            g=r1/r1.abs().rolling(20,min_periods=10).mean()
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"loc":loc,"r1":r1,"g":g,
                "prof":(b["regime"]!="chop").values,"ret5p":c/c.shift(5)-1,"ret3p":c/c.shift(3)-1,
                "tr60":c/c.shift(60)-1,"ts":b["timestamp"].astype(str).str[:10],
                "alloc":b["postRebalance_current_allocation"],"year":pd.to_datetime(b["timestamp"]).dt.year})
            for H in [2,3,5,10]:
                df[f"u{H}"]=-(c.shift(-H)/c-1-drift[(coin,H)][0])
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    def meas(mask,name,H=5):
        x=D[mask & D[f"u{H}"].notna()].copy(); x["cell"]=x["pos"]//H
        s=x.sort_values("pos").groupby(["coin","w","cell"]).head(1)
        if len(s)<3: return {"name":name,"H":H,"n":len(s)}
        d=s.groupby("ts")[f"u{H}"].sum()
        # day-pooled t of mean
        dev=s[f"u{H}"]-s[f"u{H}"].mean(); dd=dev.groupby(s["ts"]).sum(); G=len(dd)
        se=np.sqrt((dd**2).sum()*G/(G-1))/len(s)
        return {"name":name,"H":H,"n":len(s),"days":G,"unus":s[f"u{H}"].mean(),"t":s[f"u{H}"].mean()/se}
    P=D["prof"]; up=D["r1"]>0; sig=P&(D["loc"]>=0.8)&up
    sg=sig&(D["g"]<1)
    choppy=D["tr60"].abs()<=0.10
    res=[]
    for H in [2,3,5,10]:
        res.append(meas(sig,"tested",H)); res.append(meas(sg,"tested g<1",H))
    res.append(meas(P&(D["ret5p"]<=0)&~sig,"prof 5d down no signal"))
    res.append(meas(P&(D["ret5p"]<=0),"prof 5d down all"))
    res.append(meas(sig&(D["ret5p"]<=0)&(D["g"]<1),"tested 5d down g<1"))
    res.append(meas(sig&(D["ret5p"]<=0)&(D["g"]>=1),"tested 5d down g>=1"))
    res.append(meas(sig&(D["ret3p"]<=0),"tested 3d down"))
    res.append(meas(P&(D["ret3p"]<=0)&~sig,"prof 3d down no sig"))
    cc=choppy&~P&D["tr60"].notna()
    res.append(meas(cc&(D["loc"]>=0.8)&up,"choppy notprof(calm) sig"))
    res.append(meas(cc&(D["loc"]>=0.8)&up&(D["g"]<1),"choppy calm sig g<1"))
    res.append(meas(cc&(D["loc"]>=0.8)&up&(D["ret5p"]<=0),"choppy calm sig 5d down"))
    res.append(meas(cc&(D["ret5p"]<=0)&~((D["loc"]>=0.8)&up),"choppy calm 5d down nosig"))
    res.append(meas(~P&(D["loc"]>=0.8)&up&(D["ret5p"]<=0)&(D["g"]<1),"outside prof sig 5ddown g<1"))
    out["cases"]=pd.DataFrame(res)
    # trades and conditions at entry
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): tr.append(t.assign(coin=coin,w=w))
    T=pd.concat(tr); T["ts"]=T["entry_time"].astype(str).str[:10]
    M=D[["coin","ts","ret5p","g","loc"]]
    T=T.merge(M,on=["coin","ts"],how="left")
    T["dur_d"]=T["duration_minutes"]/1440
    T["c5"]=np.where(T["ret5p"]<=0,"5d down","5d up")
    T["cg"]=np.where(T["g"]<1,"g<1","g>=1")
    out["trades_by_5d"]=T.groupby("c5")["net_profit_loss_percent"].agg(["count","mean","min","sum"])
    out["trades_by_g"]=T.groupby("cg")["net_profit_loss_percent"].agg(["count","mean","min","sum"])
    out["trade_dur"]=T["dur_d"].describe()
    out["worst5"]=T.nsmallest(6,"net_profit_loss_percent")[["net_profit_loss_percent","dur_d","ret5p","g","loc"]].reset_index(drop=True)
    out["mean_abs_alloc_in_pos"]=float(D.loc[D["alloc"].abs()>0,"alloc"].abs().mean())
    return out
