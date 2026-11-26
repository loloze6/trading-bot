def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    allb = []
    for c in coins:
        for w in wins:
            if w not in bars[c]: continue
            b = bars[c][w].copy()
            b["coin"]=c; b["w"]=w
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["pos"] = b["postRebalance_current_allocation"].fillna(0)
            b["g"] = b["pos"]*b["ret1"]
            b["r5"] = b["close"].shift(-5)/b["close"]-1
            b["r10"] = b["close"]/b["close"].shift(10)-1
            b["r3"] = b["close"]/b["close"].shift(3)-1
            b["r1"] = b["close"]/b["close"].shift(1)-1
            b["vol20"] = b["r1"].rolling(20).std()
            b["i"] = np.arange(len(b))
            # signal state carried: forecast sign at the last entry
            b["fsig"] = np.sign(b["forecast"])
            b["r10_at"] = b["r10"].where(b["forecast"]!=0).ffill()
            b["vol_at"] = b["vol20"].where(b["forecast"]!=0).ffill()
            allb.append(b)
    A = pd.concat(allb, ignore_index=True)
    # thresholds from round-1 grid terciles approx: use all signal bars
    sig = A[A["forecast"]!=0]
    q1,q2 = sig["r10"].quantile([1/3,2/3])
    v1,v2 = sig["vol20"].quantile([1/3,2/3])
    out["thresholds"] = pd.Series({"r10_q33":q1,"r10_q67":q2,"vol_q33":v1,"vol_q67":v2})
    # drawdown segment in w14: long positions, what at entry
    w14 = A[(A["w"]=="w14")]
    D = w14.groupby("timestamp")["g"].mean()
    v = (1+D).cumprod(); dd = v/v.cummax()-1
    tr = dd.idxmin(); pk = v.loc[:tr].idxmax()
    seg = w14[(w14["timestamp"]>pk)&(w14["timestamp"]<=tr)&(w14["pos"]>0)]
    out["dd_long_by_coin"] = seg.groupby("coin").agg(n=("g","size"),sum_g=("g","sum"),mean_pos=("pos","mean"),r10_at=("r10_at","mean"),vol_at=("vol_at","mean"))
    # long/short gains by state at signal (r10 tercile, vol tercile)
    A["r10t"] = np.where(A["r10_at"]<q1,0,np.where(A["r10_at"]<q2,1,2))
    A["volt"] = np.where(A["vol_at"]<v1,0,np.where(A["vol_at"]<v2,1,2))
    A["side"] = np.sign(A["pos"])
    H = A[A["pos"]!=0]
    out["gain_by_side_r10t"] = H.groupby(["side","r10t"]).agg(n=("g","size"),mean_g=("g","mean"),sum_g=("g","sum"),min_g=("g","min"))
    out["gain_by_side_volt"] = H.groupby(["side","volt"]).agg(n=("g","size"),mean_g=("g","mean"),sum_g=("g","sum"),min_g=("g","min"))
    # condition alone: grid bars in falling regime (r10<0, regime active) by r10 tercile, r5 regardless of side
    G = A[(A["i"]%5==0)&(A["forecast"]!=0)&A["r5"].notna()].copy()
    G["fside"]=np.sign(G["forecast"])
    G["r10t"]=np.where(G["r10"]<q1,0,np.where(G["r10"]<q2,1,2))
    G["volt"]=np.where(G["vol20"]<v1,0,np.where(G["vol20"]<v2,1,2))
    def s(g): 
        return pd.Series({"n":len(g),"mean_r5":g["r5"].mean(),"t":g["r5"].mean()/(g["r5"].std()/np.sqrt(len(g)))})
    out["r5_by_r10t_allsides"] = G.groupby("r10t").apply(s)
    out["r5_by_side_r10t_volt"] = G.groupby(["fside","r10t","volt"]).apply(s)
    # variants: zero positions per rule, compute Calmar-ish on daily mean gain
    def book(mask_keep):
        g = A["g"].where(mask_keep, 0.0)
        tmp = A.assign(gg=g)
        res=[]
        for w in wins:
            x = tmp[tmp["w"]==w].groupby("timestamp")["gg"].sum()/len(coins)
            res.append(x)
        r = pd.concat(res)
        vv=(1+r).cumprod(); mdd=(vv/vv.cummax()-1).min()
        yr = vv.iloc[-1]**(365/len(r))-1
        return pd.Series({"yearly":yr,"mdd":mdd,"calmar":yr/abs(mdd),"sharpe":r.mean()/r.std()*np.sqrt(365)})
    keep_all = pd.Series(True,index=A.index)
    V = {}
    V["as_is"]=book(keep_all)
    V["no_long_mild_r10"]=book(~((A["side"]>0)&(A["r10t"]==2)))
    V["long_only_deep_r10"]=book(~((A["side"]>0)&(A["r10t"]!=0)))
    V["no_short_deep_r10"]=book(~((A["side"]<0)&(A["r10t"]==0)))
    V["both_r10_fixes"]=book(~(((A["side"]>0)&(A["r10t"]==2))|((A["side"]<0)&(A["r10t"]==0))))
    V["no_long_high_vol"]=book(~((A["side"]>0)&(A["volt"]==2)))
    V["no_short_high_vol"]=book(~((A["side"]<0)&(A["volt"]==2)))
    V["short_only"]=book(~(A["side"]>0))
    V["long_only"]=book(~(A["side"]<0))
    out["variants"]=pd.DataFrame(V).T
    return out
