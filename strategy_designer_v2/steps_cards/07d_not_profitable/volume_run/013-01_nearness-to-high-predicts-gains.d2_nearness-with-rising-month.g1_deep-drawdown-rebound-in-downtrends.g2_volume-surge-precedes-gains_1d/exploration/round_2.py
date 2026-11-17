def explore(data):
    import pandas as pd, numpy as np
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    windows = sorted(days[coins[0]].keys(), key=lambda w: int(w[1:]))
    out = {}
    recs=[]
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].copy()
            cl = b["close"]; r1 = cl.pct_change(); fwd = cl.shift(-1)/cl-1
            pos = b["postRebalance_current_allocation"]
            hi60 = b["high"].rolling(60,min_periods=20).max()
            vr = b["volume"]/b["volume"].rolling(20,min_periods=10).mean()
            recs.append(pd.DataFrame({"coin":c,"window":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos":pos,"g":pos*fwd,"fwd":fwd,"r1":r1,"r3":cl/cl.shift(3)-1,"ret20":cl/cl.shift(20)-1,
                "near":cl/hi60-1,"vr":vr}))
    A = pd.concat(recs).dropna(subset=["g"])
    # book daily chain to locate drawdown episodes
    bk = A.groupby(["window","day"])["g"].mean().reset_index()
    bk["wn"]=bk["window"].str[1:].astype(int); bk=bk.sort_values(["wn","day"]).reset_index(drop=True)
    eq=(1+bk["g"]).cumprod(); peak=eq.cummax(); bk["dd"]=eq/peak-1
    bk["ep"]=(bk["dd"]==0).cumsum()
    eps=bk.groupby("ep").agg(depth=("dd","min"),ndays=("dd","size"),start_w=("wn","min"),end_w=("wn","max"))
    eps=eps.sort_values("depth").head(5)
    out["episodes"]=eps
    bad=set(eps.index[:3])
    bk["in_dd"]=bk["ep"].isin(bad)&(bk["dd"]<0)
    A=A.merge(bk[["window","day","in_dd"]],on=["window","day"],how="left")
    out["in_vs_out_dd"]=A.groupby("in_dd").agg(n=("g","size"),pos=("pos","mean"),vr=("vr","mean"),
        r1=("r1","mean"),ret20=("ret20","mean"),near=("near","mean"),gain=("g","mean"),fwd=("fwd","mean"))
    A["vrq"]=pd.qcut(A["vr"],5,labels=False)
    A["r1s"]=np.where(A["r1"]<0,"down","up")
    A["trend"]=np.where(A["ret20"]<0,"ret20<0","ret20>=0")
    out["vr_x_r1sign"]=A.groupby(["vrq","r1s"]).agg(n=("g","size"),pos=("pos","mean"),gain=("g","mean"),
        fwd=("fwd","mean"),sd=("g","std"),loss_sum=("g",lambda s:s[s<0].sum())).round(5)
    out["vr_x_trend"]=A.groupby(["vrq","trend"]).agg(n=("g","size"),pos=("pos","mean"),gain=("g","mean"),
        fwd=("fwd","mean"),sd=("g","std")).round(5)
    # 7-day nonoverlap forward by vr quintile and r1 sign (excess vs coin mean)
    rec7=[]
    for c in coins:
        for w in bars[c]:
            b=bars[c][w]; cl=b["close"].values; v=b["volume"]
            vr=(v/v.rolling(20,min_periods=10).mean()).values
            for i in range(0,len(cl)-7,7):
                if i<1: continue
                rec7.append((c,cl[i+7]/cl[i]-1,vr[i],cl[i]/cl[i-1]-1))
    R=pd.DataFrame(rec7,columns=["coin","f7","vr","r1"]).dropna()
    R["ex"]=R["f7"]-R.groupby("coin")["f7"].transform("mean")
    R["vrq"]=pd.qcut(R["vr"],3,labels=False); R["r1s"]=np.where(R["r1"]<0,"down","up")
    def tt(s): return s.mean()/(s.std()/np.sqrt(len(s)))
    out["f7_vr_x_r1"]=R.groupby(["vrq","r1s"])["ex"].agg(["size","mean","std",tt]).round(4)
    return out
