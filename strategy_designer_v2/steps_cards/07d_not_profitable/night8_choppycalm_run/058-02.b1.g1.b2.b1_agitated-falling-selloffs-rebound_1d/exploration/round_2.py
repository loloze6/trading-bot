def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    wins = sorted({w for c in bars for w in bars[c]}, key=lambda s: int(s[1:]))
    cases=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change(); nxt=cl.shift(-1)/cl-1
            sd20=r.rolling(20).std(); z=r/sd20
            df=pd.DataFrame({"coin":c,"w":w,"i":np.arange(len(b)),"f":b["forecast"],"z":z,"nxt":nxt,"r":r,
                "r5":cl/cl.shift(5)-1,"r20":cl/cl.shift(20)-1,"prevdown":(r.shift(1)<0).astype(float),
                "closeloc":(cl-b["low"])/(b["high"]-b["low"]),"alloc":b["postRebalance_current_allocation"],
                "inprof":b["regime"]!="chop","sd20":sd20})
            df["gain"]=df.alloc*df.nxt
            cases.append(df)
    C=pd.concat(cases).dropna(subset=["nxt"])
    drift=C.groupby("coin")["nxt"].mean(); C["ex"]=C.nxt-C.coin.map(drift)
    # worst position-days
    W=C[C.alloc>0].nsmallest(15,"gain")[["coin","w","f","z","r","r5","r20","prevdown","closeloc","alloc","nxt","gain"]]
    out["worst_position_days"]=W.reset_index(drop=True)
    S=C[C.f>0].copy()
    out["alloc_by_fq"]=S.groupby(pd.qcut(S.f.rank(method="first"),4,labels=["q1","q2","q3","q4"])).agg(alloc=("alloc","mean"),nxt_sd=("nxt","std"),ex=("ex","mean"))
    # variant books: per-day mean of coin gains (approx, gross), with variant masks and alloc rules
    ncoins=C.groupby(["w","i"]).coin.count()
    def book(mask, scale=None):
        g=C.gain.where(mask,0.0)
        if scale is not None: g=g*scale
        D=pd.DataFrame({"w":C.w,"i":C.i,"g":g}).groupby(["w","i"]).g.mean()
        D=D.reindex(sorted(D.index,key=lambda k:(int(k[0][1:]),k[1])))
        v=(1+D).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(D))-1
        return pd.Series({"mean":D.mean(),"sh":D.mean()/D.std()*np.sqrt(365),"yr":yr,"maxdd":dd,"calmar":yr/abs(dd),"days_in":(g!=0).sum()})
    base=C.f>0
    res={"base":book(base)}
    res["drop_q1"]=book(base&(C.f>S.f.quantile(0.25)))
    res["prevdown_only"]=book(base&(C.prevdown==1))
    res["r5_le_0"]=book(base&(C.r5<0))
    res["closeloc_le_.5"]=book(base&(C.closeloc<=0.5))
    res["cap_alloc_1"]=book(base, scale=(1/C.alloc.abs().clip(lower=1)))
    res["equal_alloc"]=book(base, scale=(S.alloc.mean()/C.alloc.replace(0,np.nan)).fillna(0))
    out["variants"]=pd.DataFrame(res).T
    # conditions alone, in profile, no signal
    NS=C[(C.f<=0)&C.inprof]
    out["cond_alone"]=pd.DataFrame({
        "prevdown_nosig":[NS[NS.prevdown==1].ex.mean(),(NS.prevdown==1).sum()],
        "r5neg_nosig":[NS[NS.r5<0].ex.mean(),(NS.r5<0).sum()],
        "r5neg_sig":[S[S.r5<0].ex.mean(),(S.r5<0).sum()],
        "r5pos_sig":[S[S.r5>=0].ex.mean(),(S.r5>=0).sum()]},index=["mean_ex","n"]).T
    # 2-day horizon
    C["nxt2"]=C.groupby(["coin","w"]).apply(lambda g:(g.nxt+1)*(1+g.nxt.shift(-1))-1).reset_index(level=[0,1],drop=True)
    S=C[C.f>0]
    out["horizon2"]=pd.Series({"mean_nxt2":S.nxt2.mean(),"mean_nxt1":S.nxt.mean(),"day2_only":(S.nxt2-S.nxt).mean()})
    return out
