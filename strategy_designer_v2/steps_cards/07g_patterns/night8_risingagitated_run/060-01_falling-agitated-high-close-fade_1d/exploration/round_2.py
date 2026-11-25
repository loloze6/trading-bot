def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for c,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            d=pd.DataFrame(index=b.index)
            d["coin"]=c; d["win"]=w
            d["loc"]=((cl-l)/(h-l)).where(h>l)
            d["ret"]=cl/cl.shift(1)-1
            d["body"]=((cl-o)/(h-l)).where(h>l)
            d["rng"]=(h-l)/cl
            d["n1"]=cl.shift(-1)/cl-1
            d["n3"]=cl.shift(-3)/cl-1
            d["n5"]=cl.shift(-5)/cl-1
            d["pos"]=np.arange(len(b))
            d["fa"]=(b["regime"].astype(str)=="unknown").astype(int)
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.dayofweek.values
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            d["r20"]=cl/cl.shift(20)-1
            d["r60"]=cl/cl.shift(60)-1
            d["vol20"]=d["ret"].rolling(20).std()
            d["rngz"]=d["rng"]/d["rng"].rolling(20).mean()
            d["gain"]=d["alloc"]*d["n1"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for k in (1,3,5):
        D["x%d"%k]=D["n%d"%k]-D.groupby("coin")["n%d"%k].transform("mean")
    def summ(G,keys,col):
        res=[]
        for key,g in G.groupby(keys):
            v=g[col].dropna()
            n=len(v)
            t=v.mean()/(v.std()/np.sqrt(n)) if n>2 and v.std()>0 else np.nan
            res.append(pd.Series({"n":n,"mean%":v.mean()*100,"t":t},name=str(key)))
        return pd.DataFrame(res)
    out={}
    def safe(name,f):
        try: out[name]=f()
        except Exception as e: out[name]="err: "+str(e)[:80]
    D["locq"]=pd.cut(D["loc"],[-.01,.2,.4,.6,.8,1.01],labels=["q1lo","q2","q3","q4","q5hi"]).astype(str)
    safe("n1_loc_fa",lambda: summ(D,["fa","locq"],"x1"))
    for k in (3,5):
        safe("n%d_loc_fa"%k,lambda k=k: summ(D[D["pos"]%k==0],["fa","locq"],"x%d"%k))
    D["trend"]=np.where(D["r60"]>0.10,"rise",np.where(D["r60"]<-0.10,"fall",np.where(D["r60"].notna(),"chop","na")))
    safe("n1_loc_trend_notfa",lambda: summ(D[(D["fa"]==0)&(D["trend"]!="na")],["trend","locq"],"x1"))
    def q5(s):
        return pd.qcut(s.rank(method="first"),5,labels=False)
    D["retq"]=D.groupby("coin")["ret"].transform(q5)
    safe("n1_dayret_q_fa",lambda: summ(D,["fa","retq"],"x1"))
    safe("n3_dayret_q_fa",lambda: summ(D[D["pos"]%3==0],["fa","retq"],"x3"))
    D["rngq"]=D.groupby("coin")["rngz"].transform(q5)
    safe("n1_relrange_q_fa",lambda: summ(D,["fa","rngq"],"x1"))
    D["hi"]=(D["loc"]>=2/3).astype(int); D["up"]=(D["ret"]>0).astype(int)
    safe("n1_fa_hi_x_up",lambda: summ(D[D["fa"]==1],["hi","up"],"x1"))
    safe("n1_fa_hi_x_widerange",lambda: summ(D[D["fa"]==1],["hi",(D.loc[D["fa"]==1,"rngq"]>=3).astype(int)],"x1"))
    safe("n1_weekday_all",lambda: summ(D,["wd"],"x1"))
    safe("n1_weekday_fa",lambda: summ(D[D["fa"]==1],["wd"],"x1"))
    D["r20q"]=D.groupby("coin")["r20"].transform(q5)
    safe("n5_r20q_all",lambda: summ(D[D["pos"]%5==0],["r20q"],"x5"))
    D["volq"]=D.groupby("coin")["vol20"].transform(q5)
    safe("n1_volq",lambda: summ(D,["volq"],"x1"))
    safe("n3_volq",lambda: summ(D[D["pos"]%3==0],["volq"],"x3"))
    safe("fa_share_by_coin",lambda: D.groupby("coin")["fa"].mean())
    safe("fa_hi_by_coin",lambda: summ(D[(D["fa"]==1)&(D["hi"]==1)],["coin"],"x1"))
    safe("fa_hi_by_win",lambda: summ(D[(D["fa"]==1)&(D["hi"]==1)],["win"],"x1"))
    P=D[D["alloc"].abs()>1e-9]
    safe("pos_gain_by_locq",lambda: summ(P,["locq"],"gain"))
    # largest gains/losses of positions: what preceded
    try:
        P2=P.dropna(subset=["gain"]).copy()
        lo=P2["gain"].quantile(0.05); hi=P2["gain"].quantile(0.95)
        P2["tail"]=np.where(P2["gain"]<=lo,"worst5",np.where(P2["gain"]>=hi,"best5","mid"))
        out["tails_context"]=P2.groupby("tail")[["loc","ret","rngz","r20","alloc"]].mean()
    except Exception as e: out["tails_context"]="err "+str(e)[:80]
    dd=[]
    for c,wins in data["days"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=c; t["win"]=w; dd.append(t)
    Y=pd.concat(dd,ignore_index=True)
    safe("book_by_win",lambda: Y.groupby("win")[["book_return","coin_return"]].mean()*100)
    safe("book_by_coin",lambda: Y.groupby("coin")[["book_return","coin_return"]].mean()*100)
    return out
