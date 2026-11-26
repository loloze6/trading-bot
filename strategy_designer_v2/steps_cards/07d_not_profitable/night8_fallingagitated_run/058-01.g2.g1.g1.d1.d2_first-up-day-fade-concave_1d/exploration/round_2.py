def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r0=cl/cl.shift(1)-1
            sd30=r0.rolling(30,min_periods=15).std()
            x=pd.DataFrame({"coin":c,"w":w,"reg":b["regime"],"a":b["postRebalance_current_allocation"],
                "r1":cl.shift(-1)/cl-1,"r3":cl.shift(-3)/cl-1,
                "r0z":r0/sd30,"rpz":r0.shift(1)/sd30,
                "r3pz":(cl.shift(1)/cl.shift(4)-1)/sd30,
                "r10z":(cl/cl.shift(10)-1)/(sd30*np.sqrt(10)),
                "dd20":cl/cl.rolling(20,min_periods=10).max()-1,
                "rng":(b["high"]-b["low"])/cl/sd30,
                "up1":(r0>0)&(r0.shift(1)<=0),
                "pos":np.arange(len(b))})
            rows.append(x)
    X=pd.concat(rows).dropna(subset=["r1","r0z","rpz"])
    X=X[X["pos"]>=30]
    inprof=X["reg"].isin(["mean_reversion","unknown"])
    S=X[inprof & X["up1"]].copy()   # signal days in profile
    S["sr"]=-S["r1"]; S["sr3"]=-S["r3"]
    out["n_signal_inprof"]=len(S)
    # w14 worst day: features of the shorted coins
    worst=S[(S["w"]=="w14")&(S["r1"]>0.09)]
    out["w14_squeeze_cases"]=worst[["coin","r0z","rpz","r3pz","r10z","dd20","rng"]].describe().loc[["count","mean","min","max"]]
    def tab(df,col,q=4):
        d=df.dropna(subset=[col]).copy(); d["bin"]=pd.qcut(d[col],q,labels=False,duplicates="drop")
        g=d.groupby("bin")
        return pd.DataFrame({"lo":g[col].min(),"hi":g[col].max(),"n":g.size(),"short1":g["sr"].mean(),
            "t1":g["sr"].apply(lambda s:s.mean()/(s.std()/np.sqrt(len(s)))),"worst":g["sr"].min(),
            "sd":g["sr"].std(),"short3":g["sr3"].mean()})
    for col in ["r10z","dd20","r3pz"]:
        out["sig_by_"+col]=tab(S,col)
    # same conditions on in-profile bars without the signal (non-overlap not needed for 1d)
    N=X[inprof & ~X["up1"]].copy(); N["sr"]=-N["r1"]; N["sr3"]=-N["r3"]
    for col in ["r10z","dd20"]:
        out["nosig_by_"+col]=tab(N,col)
    # capitulation-type case: tiny rise after big fall
    S["cap"]=(S["rpz"]<-1)&(S["r0z"]<0.5)
    g=S.groupby("cap")["sr"]
    out["cap_split"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"sd":g.std(),"worst":g.min()})
    # rise relative to range: up move as share of range
    S["rise_share"]=S["r0z"]/S["rng"]
    out["sig_by_rise_share"]=tab(S,"rise_share")
    # number of coins signalling same day vs result
    S["day"]=S.groupby(["w"]).cumcount()
    return out
