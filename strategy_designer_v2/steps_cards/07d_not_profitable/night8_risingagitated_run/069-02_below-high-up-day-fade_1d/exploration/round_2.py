def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r1=c.pct_change(); nxt=c.shift(-1)/c-1; nxt2=c.shift(-2)/c-1; nxt3=c.shift(-3)/c-1
            h20=b["high"].rolling(20).max(); s20=r1.rolling(20).std()
            dep=(c-h20)/h20/s20
            ret60=c/c.shift(60)-1
            vol30=r1.rolling(30).std()
            pos=b["postRebalance_current_allocation"]
            chg=(pos-b["previous_allocation"]).abs()
            idx=np.arange(len(b))
            rows.append(pd.DataFrame({"coin":coin,"w":w,"r1":r1,"nxt":nxt,"nxt2":nxt2,"nxt3":nxt3,"dep":dep,
                "ret60":ret60,"vrel":vol30/vol30.expanding(30).median(),"pos":pos,"chg":chg,"g":pos*nxt,
                "g2":(idx%2==0),"g3":(idx%3==0)}))
    d=pd.concat(rows,ignore_index=True)
    for k in ["nxt","nxt2","nxt3"]:
        d["ex"+k[3:] if k!="nxt" else "ex"]=d[k]-d["coin"].map(d.groupby("coin")[k].mean())
    d["tr"]=np.select([d.ret60>0.1,d.ret60<-0.1],["rising","falling"],"choppy"); d.loc[d.ret60.isna(),"tr"]="na"
    v=d.dropna(subset=["nxt","dep"]).copy()
    v["dq"]=pd.qcut(v.dep,5,labels=False)
    v["up"]=v.r1>0
    def tab(x,key,col="ex"):
        e=x.groupby(key)[col]
        return pd.DataFrame({"n":e.size(),"mean_ex":e.mean(),"t":e.mean()/(e.std()/np.sqrt(e.size()))})
    out={}
    out["next-day ex by up x depth quintile (all days pooled)"]=tab(v,["up","dq"])
    out["next-day ex by trend x up (condition alone vs with signal)"]=tab(v,["tr","up"])
    nr=v[v.tr!="rising"]
    out["not-rising: ex by up x dq"]=tab(nr,["up","dq"])
    v["ag"]=np.where(v.vrel>1,"agitated","calm")
    out["up days: ex by agitation x deep(q0)"]=tab(v[v.up],["ag",v[v.up].dq==0])
    out["down days: ex by agitation"]=tab(v[~v.up],"ag")
    u=v[v.up]
    out["horizon2 grid, up, by dq"]=tab(u[u.g2 & u.nxt2.notna()],"dq","ex2")
    out["horizon3 grid, up, by dq"]=tab(u[u.g3 & u.nxt3.notna()],"dq","ex3")
    out["horizon2 grid, up not-rising, by dq"]=tab(u[u.g2 & u.nxt2.notna()&(u.tr!="rising")],"dq","ex2")
    # book by trend state
    g=d.dropna(subset=["nxt"])
    out["book gain and cost by trend"]=pd.DataFrame({"n":g.groupby("tr").size(),"gain":g.groupby("tr")["g"].mean(),
        "cost":g.groupby("tr")["chg"].mean()*0.0019,"held":g.groupby("tr")["pos"].apply(lambda s:(s!=0).mean())})
    # book restricted: only deepest quintile, not rising
    vv=v.copy(); vv["keep"]=(vv.up)&(vv.dq==0)&(vv.tr!="rising")
    out["deep q0 not-rising up-days: n, mean next, mean ex"]=pd.Series({"n":vv.keep.sum(),"next":vv.loc[vv.keep,"nxt"].mean(),"ex":vv.loc[vv.keep,"ex"].mean()})
    out["deep q0 not-rising by window"]=tab(vv[vv.keep],"w")
    return out
