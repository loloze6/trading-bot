def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(60,min_periods=60).std()
            z=r/sd
            nxt=c.shift(-1)/c-1
            n3=c.shift(-3)/c-1
            vr=b["volume"]/b["volume"].rolling(60,min_periods=30).mean()
            r5=c/c.shift(5)-1
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"r":r,"z":z,"sd":sd,"nxt":nxt,"n3":n3,
                            "vr":np.log(vr),"z5":r5/(sd*np.sqrt(5)),
                            "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,
                            "yr":pd.to_datetime(b["timestamp"]).dt.year,
                            "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    cm=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(cm)
    D["ex3"]=D["n3"]-3*D["coin"].map(cm)
    out={}
    E=D.dropna(subset=["z","ex"])
    E["zb"]=pd.cut(E["z"],[-99,-2.5,-1.5,-0.75,0,0.75,1.5,2.5,99])
    g=E.groupby("zb")["ex"]
    out["next1 excess by z"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    G3=E[E["pos"]%3==0].dropna(subset=["ex3"])
    g=G3.groupby("zb")["ex3"]
    out["next3 excess by z (grid3)"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # weekday of situation for falls and rises
    E["side"]=np.where(E["z"]<-1,"fall",np.where(E["z"]>1,"rise","mid"))
    g=E.groupby(["side","wd"])["ex"]
    out["next1 by side x weekday"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # vol terciles x side
    E["vq"]=E.groupby("coin")["sd"].transform(lambda s: pd.qcut(s,3,labels=False))
    g=E.groupby(["side","vq"])["ex"]
    out["next1 by side x vol tercile"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # volume ratio within falls
    F=E[E["side"]=="fall"].dropna(subset=["vr"])
    F["vb"]=pd.qcut(F["vr"],3,labels=False)
    g=F.groupby("vb")["ex"]
    out["falls: next1 by volume tercile"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # 5-day z buckets
    E5=E.dropna(subset=["z5"]); E5["b"]=pd.qcut(E5["z5"],5,labels=False)
    g=E5.groupby("b")["ex"]
    out["next1 by 5d z quintile"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # by coin & year for falls
    g=E[E["side"]=="fall"].groupby("coin")["ex"]
    out["falls next1 by coin"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    g=E[E["side"]=="fall"].groupby("yr")["ex"]
    out["falls next1 by year"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # book daily by weekday
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    DD=pd.concat(dd); DD["wd"]=pd.to_datetime(DD["day"]).dt.dayofweek
    bk=DD.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["wd"]=pd.to_datetime(bk["day"]).dt.dayofweek
    g=bk.groupby("wd")
    out["book by weekday"]=pd.DataFrame({"n":g.size(),"book":g["book_return"].mean(),"coins":g["coin_return"].mean()})
    out["book mean/std"]=f'{bk.book_return.mean():.5f} / {bk.book_return.std():.5f}; share days in pos {(D.alloc.abs()>0).mean():.3f}'
    return out
