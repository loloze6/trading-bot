def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rs=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.copy().reset_index(drop=True)
            b["ret1"]=b.close.shift(-1)/b.close-1
            b["dayret"]=b.close/b.close.shift(1)-1
            b["raw"]=(b.high-b.close)/(b.high-b.low)
            b["r5"]=b.close/b.close.shift(5)-1
            b["coin"]=c; b["w"]=w; b["pos"]=np.arange(len(b))
            b["alloc"]=b.postRebalance_current_allocation.fillna(0)
            b["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            rs.append(b[["coin","w","pos","day","ret1","dayret","raw","r5","regime","alloc","forecast"]])
    X=pd.concat(rs,ignore_index=True)
    mu=X.groupby("coin").ret1.mean(); X["ex"]=X.ret1-X.coin.map(mu)
    X["inp"]=X.regime=="unknown"
    cost=0.0019/2
    def book(f, name):
        Y=X.copy()
        Y["a"]=np.where(Y.inp, Y.alloc*f(Y), 0.0)
        Y["da"]=Y.groupby(["coin","w"]).a.diff().fillna(Y.a).abs()
        Y["g"]=(Y.a*Y.ret1).fillna(0)-cost*Y.da
        D=Y.groupby(["w","day"]).g.sum().reset_index()
        n=Y.groupby(["w","day"]).coin.nunique().values
        D["br"]=D.g/n
        D["wn"]=D.w.str[1:].astype(int); D=D.sort_values(["wn","day"])
        v=(1+D.br).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(D))-1
        sh=D.br.mean()/D.br.std()*np.sqrt(365)
        return {"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":sh,"days_pos":float((Y.a.abs()>0).mean())}
    res={}
    res["orig"]=book(lambda Y: 1.0,"o")
    res["lower_half_only"]=book(lambda Y: (Y.raw>=0.5).astype(float),"h")
    res["graded_from_mid"]=book(lambda Y: (np.clip((Y.raw-0.5)/0.5,0,1)*2).fillna(0),"g")
    res["low_and_downday"]=book(lambda Y: ((Y.raw>=0.5)&(Y.dayret<0)).astype(float),"d")
    res["graded_mid_downday"]=book(lambda Y: (np.clip((Y.raw-0.5)/0.5,0,1)*2*(Y.dayret<0)).fillna(0),"gd")
    out["books"]=pd.DataFrame(res).T
    # w14 drawdown: by raw bucket, gains
    W=X[(X.w=="w14")&X.inp].copy()
    W["g"]=W.alloc*W.ret1
    W["rawq"]=pd.cut(W.raw,[-0.01,0.2,0.4,0.6,0.8,1.01])
    out["w14_by_raw"]=W.groupby("rawq").agg(n=("g","size"),gsum=("g","sum"),ex=("ex","mean"),alloc=("alloc","mean"))
    # condition check: down day without low close vs with, in profile and outside
    P=X.dropna(subset=["ret1","raw","dayret"])
    P["low"]=P.raw>=0.5; P["down"]=P.dayret<0
    out["cond_check_inprofile"]=P[P.inp].groupby(["down","low"]).ex.agg(["size","mean"])
    out["cond_check_outprofile"]=P[~P.inp].groupby(["down","low"]).ex.agg(["size","mean"])
    P["rawq"]=pd.cut(P.raw,[-0.01,0.2,0.4,0.6,0.8,1.01])
    out["out_profile_by_raw"]=P[~P.inp].groupby("rawq").ex.agg(["size","mean"])
    # t of graded slope in lower half in profile
    Q=P[P.inp&(P.raw>=0.5)]
    out["lowerhalf_raw_corr"]=float(np.corrcoef(Q.raw,Q.ex)[0,1]); out["lowerhalf_n"]=len(Q)
    return out
