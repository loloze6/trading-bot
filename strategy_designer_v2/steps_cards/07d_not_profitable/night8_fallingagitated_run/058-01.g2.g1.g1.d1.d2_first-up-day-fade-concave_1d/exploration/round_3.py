def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; out={}
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r0=cl/cl.shift(1)-1
            sd30=r0.rolling(30,min_periods=15).std()
            rngp=(b["high"]-b["low"])
            x=pd.DataFrame({"coin":c,"w":w,"day":b["timestamp"].astype(str).str[:10],"reg":b["regime"],
                "a":b["postRebalance_current_allocation"],"r1":cl.shift(-1)/cl-1,
                "r0z":r0/sd30,"rng":rngp/cl/sd30,"cpos":(cl-b["low"])/rngp,
                "up1":(r0>0)&(r0.shift(1)<=0),"pos":np.arange(len(b))})
            rows.append(x)
    X=pd.concat(rows).dropna(subset=["r1","r0z","cpos"]); X=X[X["pos"]>=30]
    inprof=X["reg"].isin(["mean_reversion","unknown"])
    X["rs"]=X["r0z"]/X["rng"]; X["sr"]=-X["r1"]
    S=X[inprof&X["up1"]]; N=X[inprof&~X["up1"]&(X["r1"].notna())]
    # condition alone check: close position on non-signal in-profile bars
    def g(df,col,edges):
        d=df.copy(); d["bin"]=pd.cut(d[col],edges)
        gg=d.groupby("bin",observed=True)["sr"]
        return pd.DataFrame({"n":gg.size(),"short1":gg.mean(),"t":gg.apply(lambda s:s.mean()/(s.std()/np.sqrt(len(s)))),"worst":gg.min()})
    out["sig_cpos"]=g(S,"cpos",[-0.01,0.6,0.75,0.86,1.01])
    out["nosig_cpos"]=g(N,"cpos",[-0.01,0.6,0.75,0.86,1.01])
    out["sig_rs"]=g(S,"rs",[0,0.21,0.45,0.69,2])
    out["nosig_up_rs"]=g(N[N["r0z"]>0],"rs",[0,0.21,0.45,0.69,2])
    # book proxy: daily mean over coins (all coins present) of a*r1 with filters
    A=X.copy(); A["g"]=A["a"].where(A["a"]<0,0)*A["r1"]
    def book(mask):
        A2=A.copy(); A2.loc[~mask,"g"]=0
        d=A2.groupby(["w","day"])["g"].mean().reset_index()
        d["wn"]=d["w"].str[1:].astype(int); d=d.sort_values(["wn","day"])
        v=(1+d["g"]).cumprod().values; dd=(v/np.maximum.accumulate(v)-1).min()
        yr=v[-1]**(365/len(v))-1
        return pd.Series({"mean":d["g"].mean(),"sharpe":d["g"].mean()/d["g"].std()*np.sqrt(365),"maxdd":dd,"yearly":yr,"calmar":yr/-dd,"worst_day":d["g"].min()})
    allm=A["a"]<0
    out["book_proxy"]=pd.DataFrame({"base":book(allm),"cpos<=0.86":book(allm&(A["cpos"]<=0.86)),
        "rs<=0.69":book(allm&(A["rs"]<=0.69)),"both":book(allm&(A["cpos"]<=0.86)&(A["rs"]<=0.69))}).T
    return out
