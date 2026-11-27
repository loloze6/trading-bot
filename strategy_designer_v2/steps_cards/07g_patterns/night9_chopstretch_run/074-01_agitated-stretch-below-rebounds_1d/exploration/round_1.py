def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True).copy()
            cl=b["close"].astype(float)
            r=cl.pct_change()
            sd=r.rolling(20).std()
            z=(cl/cl.rolling(20).mean()-1)/sd
            ag=(b["regime"]!="chop").astype(int)
            tr=cl/cl.shift(60)-1
            r5=cl/cl.shift(5)-1
            rng=(b["high"]-b["low"])/cl
            clpos=(cl-b["low"])/(b["high"]-b["low"])
            for h in (1,3,10):
                b[f"f{h}"]=cl.shift(-h)/cl-1
            df=pd.DataFrame({"coin":c,"w":w,"pos":np.arange(len(b)),"z":z,"ag":ag,"tr":tr,"r1":r,"r5":r5,
                             "sdz":r/sd,"rng":rng,"clpos":clpos,"f1":b["f1"],"f3":b["f3"],"f10":b["f10"],
                             "wd":pd.to_datetime(b["timestamp"]).dt.weekday,"fc":b["forecast"],
                             "alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
        for w,d in data["days"][c].items():
            d=d.copy(); d["coin"]=c; d["w"]=w; drows.append(d)
    A=pd.concat(rows,ignore_index=True)
    for h in (1,3,10):
        A[f"u{h}"]=A[f"f{h}"]-A.groupby("coin")[f"f{h}"].transform("mean")
    G10=A[A.pos%10==0].dropna(subset=["z","u10"])
    G3=A[A.pos%3==0].dropna(subset=["z","u3"])
    def tab(G,col,by):
        g=G.groupby(by)[col]
        return pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))}).round(4)
    out={}
    G10=G10.assign(zq=pd.cut(G10.z,[-9,-2,-1,0,1,2,9]))
    out["u10 by z bin x agitated"]=tab(G10,"u10",["ag","zq"])
    G3=G3.assign(zq=pd.cut(G3.z,[-9,-2,-1,0,1,2,9]))
    out["u3 by z bin x agitated"]=tab(G3,"u3",["ag","zq"])
    Gt=G10.dropna(subset=["tr"]).assign(tq=pd.cut(G10.tr,[-9,-0.1,0.1,99]))
    out["u10 by trend x ag x z<0"]=tab(Gt,"u10",["tr" and "tq","ag",Gt.z<0])
    G1=A.dropna(subset=["sdz","u1"]).assign(sq=lambda x:pd.cut(x.sdz,[-99,-2,-1,0,1,2,99]))
    out["u1 by today's move in sd x ag"]=tab(G1,"u1",["ag","sq"])
    out["u3 grid by today's move in sd"]=tab(G3.dropna(subset=["sdz"]).assign(sq=lambda x:pd.cut(x.sdz,[-99,-2,-1,0,1,2,99])),"u3",["sq"])
    out["u1 by weekday"]=tab(A.dropna(subset=["u1"]),"u1",["wd"])
    G1b=A.dropna(subset=["clpos","u1","rng"]).assign(cq=lambda x:pd.qcut(x.clpos,5,duplicates="drop"))
    out["u1 by close position in range"]=tab(G1b,"u1",["ag","cq"])
    D=pd.concat(drows,ignore_index=True)
    bk=D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book mean by year"]=bk.groupby(pd.to_datetime(bk.index.get_level_values("day")).year).agg(["size","mean","std"]).round(5)
    out["book by window"]=bk.groupby(level="w").agg(["size","mean"]).round(5)
    # trades
    T=pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()],ignore_index=True)
    T["fq"]=pd.qcut(T.entry_forecast,4,duplicates="drop")
    g=T.groupby("fq")["net_profit_loss_percent"]
    out["trades net pnl by entry forecast"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"med":g.median()}).round(3)
    g=T.groupby("coin")["net_profit_loss_percent"]
    out["trades by coin"]=pd.DataFrame({"n":g.size(),"mean":g.mean()}).round(3)
    return out
