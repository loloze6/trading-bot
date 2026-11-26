def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; book=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r1=c.pct_change(); nxt=c.shift(-1)/c-1
            h20=b["high"].rolling(20).max(); s20=r1.rolling(20).std()
            dep=(c-h20)/h20/s20
            ret60=c/c.shift(60)-1
            vol10=r1.rolling(10).std(); vol30=r1.rolling(30).std()
            ret5=c/c.shift(5)-1
            pos=b["postRebalance_current_allocation"]
            chg=b["allocation_change"].abs() if "allocation_change" in b else (pos-b["previous_allocation"]).abs()
            df=pd.DataFrame({"coin":coin,"w":w,"r1":r1,"nxt":nxt,"dep":dep,"fc":b["forecast"],
                "ret60":ret60,"ret5":ret5,"vr":vol10/vol30,"pos":pos,"chg":chg,
                "g":pos*nxt,"year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    drift=d.groupby("coin")["nxt"].mean()
    d["ex"]=d["nxt"]-d["coin"].map(drift)
    up=d[(d.r1>0)&d.nxt.notna()&d.dep.notna()].copy()
    dn=d[(d.r1<=0)&d.nxt.notna()&d.dep.notna()].copy()
    def tab(x,key):
        g=x.groupby(key)["nxt"]
        e=x.groupby(key)["ex"]
        return pd.DataFrame({"n":g.size(),"mean_next":g.mean(),"mean_ex":e.mean(),"t_ex":e.mean()/(e.std()/np.sqrt(e.size()))})
    up["dq"]=pd.qcut(up.dep,5,labels=False)
    dn["dq"]=pd.qcut(dn.dep,5,labels=False)
    up["tr"]=np.select([up.ret60>0.1,up.ret60<-0.1],["rising","falling"],"choppy"); up.loc[up.ret60.isna(),"tr"]="na"
    up["rq"]=pd.qcut(up.r1,3,labels=False)
    up["deep"]=up.dq<=1
    out={}
    out["up by depth quintile (0 deepest)"]=tab(up,"dq")
    out["down days by depth quintile"]=tab(dn,"dq")
    out["up by trend"]=tab(up,"tr")
    out["up deep(q0-1) by trend"]=tab(up[up.deep],"tr")
    out["up shallow(q3-4) by trend"]=tab(up[up.dq>=3],"tr")
    out["up deep by up-day size tercile"]=tab(up[up.deep],"rq")
    out["up all by up-day size tercile"]=tab(up,"rq")
    out["up deep by window"]=tab(up[up.deep],"w")
    out["up deep by coin"]=tab(up[up.deep],"coin")
    # book
    g=d.dropna(subset=["nxt"])
    out["position gain by window"]=pd.DataFrame({"mean_gain":g.groupby("w")["g"].mean(),"turn":g.groupby("w")["chg"].mean(),
        "share_held":g.groupby("w")["pos"].apply(lambda s:(s!=0).mean()),"coin_mean":g.groupby("w")["nxt"].mean()})
    g2=g.copy(); g2["state"]=np.where(g2.pos==0,"flat",np.where(g2.r1>0,"held_upday","held_nonup"))
    out["gain by holding state"]=pd.DataFrame({"n":g2.groupby("state").size(),"mean_gain":g2.groupby("state")["g"].mean(),"mean_pos":g2.groupby("state")["pos"].mean(),"turn":g2.groupby("state")["chg"].mean()})
    out["total mean gain, mean turnover x0.0019"]=pd.Series({"gain":g.g.mean(),"cost":g.chg.mean()*0.0019})
    return out
