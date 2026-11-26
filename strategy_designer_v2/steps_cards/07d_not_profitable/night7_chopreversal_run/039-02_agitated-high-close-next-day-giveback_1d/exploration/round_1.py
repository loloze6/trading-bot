def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.copy().reset_index(drop=True)
            rng=(b["high"]-b["low"])
            cl=(b["close"]-b["low"])/rng.replace(0,np.nan)
            r1=b["close"].pct_change()
            nxt=b["close"].shift(-1)/b["close"]-1
            vol=r1.rolling(30,min_periods=20).std()
            relrng=(rng/b["close"])/vol
            mom3=b["close"]/b["close"].shift(3)-1
            ret60=b["close"]/b["close"].shift(60)-1
            pos=b["postRebalance_current_allocation"]
            gain=pos*nxt
            turn=(pos-b["previous_allocation"]).abs()
            d=pd.DataFrame({"coin":coin,"w":w,"cl":cl,"r1":r1,"nxt":nxt,"relrng":relrng,
                            "agit":b["regime"]=="unknown","pos":pos,"gain":gain,"turn":turn,
                            "mom3z":mom3/vol,"ret60":ret60,"ts":pd.to_datetime(b["timestamp"]).dt.normalize(),
                            "fc":b["forecast"]})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["cl","nxt"])
    cm=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(cm)
    A=D[D.agit].copy(); C=D[~D.agit].copy()
    def tab(X,col,q=5):
        X=X.dropna(subset=[col]).copy()
        X["b"]=pd.qcut(X[col],q,labels=False,duplicates="drop")
        g=X.groupby("b")
        return pd.DataFrame({"lo":g[col].min(),"n":g.size(),"mean_ex%":g["ex"].mean()*100,
                             "t":g["ex"].mean()/(g["ex"].std()/np.sqrt(g.size()))})
    out={}
    out["agit_cl_quintile"]=tab(A,"cl",10)
    out["calm_cl_quintile"]=tab(C,"cl",5)
    # extremes x relative range
    A["ext"]=np.where(A.cl>=0.8,"high",np.where(A.cl<=0.2,"low","mid"))
    A["rr"]=pd.qcut(A["relrng"],3,labels=["narrow","mid","wide"])
    A["sx"]=np.where(A.ext=="low",1,np.where(A.ext=="high",-1,0))*A["ex"]
    g=A.groupby(["ext","rr"])["ex"]
    out["agit_ext_by_range"]=pd.DataFrame({"n":g.size(),"mean_ex%":g.mean()*100,"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # trend split
    A["tr"]=np.where(A.ret60>0.1,"rising",np.where(A.ret60<-0.1,"falling","choppy"))
    g=A.groupby(["tr","ext"])["ex"]
    out["agit_ext_by_trend"]=pd.DataFrame({"n":g.size(),"mean_ex%":g.mean()*100})
    # book: gain by side, turnover
    P=D[D.pos.abs()>1e-9]
    P["side"]=np.sign(P.pos)
    g=P.groupby("side")
    out["book_side"]=pd.DataFrame({"n":g.size(),"mean_gain%":g["gain"].mean()*100,"mean_abs_pos":g["pos"].apply(lambda s:s.abs().mean()),
                                   "turn":g["turn"].mean(),"cost%":g["turn"].mean()*0.19})
    out["book_side_by_ext"]=P.assign(ext=np.where(P.cl>=0.8,"high",np.where(P.cl<=0.2,"low","mid"))).groupby(["side","ext"])["gain"].agg(["size","mean"]).assign(mean=lambda x:x["mean"]*100)
    out["total_turn_per_bar_all"]=float(D["turn"].mean())
    out["gross_gain_per_bar%"]=float(D["gain"].mean()*100)
    out["cost_per_bar%"]=float(D["turn"].mean()*0.19)
    out["corr_cl_r1_agit"]=float(A[["cl","r1"]].corr().iloc[0,1])
    # by window book daily
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            dd.append(x.assign(coin=coin,w=w))
    DD=pd.concat(dd)
    bk=DD.groupby(["w","day"])["book_return"].mean().reset_index()
    out["book_by_window"]=bk.groupby("w")["book_return"].agg(["mean","std","size"]).assign(mean=lambda x:x["mean"]*1e4)
    return out
