def explore(data):
    import pandas as pd, numpy as np
    out={}
    coins=list(data["bars"].keys())
    cost=0.0019/2
    rows=[]
    for c in coins:
        for w,b in data["bars"][c].items():
            b=b.copy().reset_index(drop=True)
            r=b["close"].pct_change()
            b["nxt"]=b["close"].shift(-1)/b["close"]-1
            b["vol20"]=r.rolling(20,min_periods=20).std()
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["loc"]=(b["high"]-b["close"])/rng
            b["alloc"]=b["postRebalance_current_allocation"]
            b["coin"]=c;b["wn"]=int(w[1:]);b["i"]=np.arange(len(b))
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b[["coin","wn","i","day","nxt","vol20","ret20","loc","forecast","alloc"]])
    X=pd.concat(rows).reset_index(drop=True)
    X["vmed"]=X.groupby("coin")["vol20"].transform("median")
    X["vhi"]=X["vol20"]>X["vmed"]
    variants={
     "orig":np.ones(len(X),bool),
     "f>=12":X["forecast"]>=12,
     "f>=15":X["forecast"]>=15,
     "f>=17":X["forecast"]>=17,
     "vhi&low":X["vhi"]&(X["loc"]>0.5),
     "f>=15&up20":(X["forecast"]>=15)&(X["ret20"]>0),
     "f>=15 or vhi&low":(X["forecast"]>=15)|(X["vhi"]&(X["loc"]>0.5)),
    }
    res={}; fall={}
    for k,m in variants.items():
        Y=X.copy(); Y["p"]=np.where(m,Y["alloc"],0.0)
        Y["pp"]=Y.groupby(["coin","wn"])["p"].shift(1).fillna(0)
        Y["g"]=Y["p"]*Y["nxt"]-cost*(Y["p"]-Y["pp"]).abs()
        Y=Y.dropna(subset=["nxt"])
        Bk=Y.groupby(["wn","day"])["g"].mean().reset_index().sort_values(["wn","day"])
        v=(1+Bk["g"]).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(Bk))-1
        res[k]={"inpos":float((Y["p"]>0).mean()),"sharpe":Bk["g"].mean()/Bk["g"].std()*np.sqrt(365),
                "yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),
                "mean_on_pos":Bk["g"].mean()/max((Y["p"]>0).mean(),1e-9)}
        fall[k]=(1+Bk[Bk.wn.between(12,14)]["g"]).prod()-1
    out["variants"]=pd.DataFrame(res).T.round(4)
    out["fall_w12_14_ret"]=pd.Series(fall).round(4)
    # condition-alone check: high vol, close not low, vs both
    Z=X.dropna(subset=["nxt","vol20","loc"])
    def s(x): return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    Z["grp"]=np.where(Z["vhi"],"vhi","vlo")+np.where(Z["loc"]>0.5,"_low","_notlow")
    out["cond_check_nxt"]=Z.groupby("grp")["nxt"].apply(s).unstack().round(5)
    Z["fhi"]=Z["forecast"]>=15
    out["fhi_by_window_group"]=Z.groupby([pd.cut(Z["wn"],[0,6,11,14,19,24]),"fhi"])["nxt"].mean().unstack().round(5)
    return out
