def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,df in ws.items():
            c=df["close"].astype(float)
            allr.append(c.pct_change())
        mu=pd.concat(allr).mean()
        for w,df in ws.items():
            d=df.copy()
            c=d["close"].astype(float)
            r=c.pct_change()
            d["r"]=r
            d["nxt"]=c.shift(-1)/c-1-mu
            d["n3"]=c.shift(-3)/c-1-3*mu
            d["mabs"]=r.abs().shift(1).rolling(60,min_periods=20).mean()
            d["z"]=r/d["mabs"]
            d["vr"]=r.abs().rolling(20).std().shift(0)
            d["vol20"]=r.rolling(20).std()
            d["volratio"]=d["vol20"]/d["mabs"]
            d["vrel"]=np.log(d["volume"]/d["volume"].shift(1).rolling(20,min_periods=10).mean())
            d["r5"]=c/c.shift(5)-1
            d["r20"]=c/c.shift(20)-1
            d["wd"]=pd.to_datetime(d["timestamp"]).dt.dayofweek
            d["pos"]=d["postRebalance_current_allocation"]
            d["gain"]=d["pos"]*(c.shift(-1)/c-1)
            d["coin"]=coin; d["w"]=w
            d["pos_i"]=np.arange(len(d))
            rows.append(d[["coin","w","pos_i","r","nxt","n3","z","volratio","vrel","r5","r20","wd","pos","gain","forecast"]])
    A=pd.concat(rows).dropna(subset=["nxt","z"])
    out={}
    def tab(g,col="nxt"):
        x=g[col]
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    A["zq"]=pd.qcut(A["z"],10,labels=False)
    out["nxt by z decile"]=A.groupby("zq").apply(tab)
    out["nxt*sign(-z) by weekday, |z|top30%"]=A[A["z"].abs()>A["z"].abs().quantile(.7)].assign(f=lambda x:-np.sign(x["z"])*x["nxt"]).groupby("wd").apply(lambda g:tab(g,"f"))
    A["vq"]=pd.qcut(A["volratio"],3,labels=False)
    A["fade"]=-np.sign(A["z"])*A["nxt"]
    out["fade by volratio tercile x |z| tercile"]=A.assign(aq=pd.qcut(A["z"].abs(),3,labels=False)).groupby(["vq","aq"]).apply(lambda g:tab(g,"fade"))
    B=A.dropna(subset=["vrel"])
    B["volq"]=pd.qcut(B["vrel"],3,labels=False)
    out["fade by rel volume tercile (|z| top third)"]=B[B["z"].abs()>B["z"].abs().quantile(2/3)].groupby("volq").apply(lambda g:tab(g,"fade"))
    out["nxt by weekday"]=A.groupby("wd").apply(tab)
    out["gain by weekday"]=A.dropna(subset=["gain"]).groupby("wd").apply(lambda g:tab(g,"gain"))
    out["fade by coin"]=A.groupby("coin").apply(lambda g:tab(g,"fade"))
    C=A.dropna(subset=["r5"])
    C["q5"]=pd.qcut(C["r5"],5,labels=False)
    out["nxt by 5d ret quintile"]=C.groupby("q5").apply(tab)
    D=A.dropna(subset=["r20","n3"]); D=D[D["pos_i"]%3==0]
    D["q20"]=pd.qcut(D["r20"],5,labels=False)
    out["next3d by 20d ret quintile (nonoverlap)"]=D.groupby("q20").apply(lambda g:tab(g,"n3"))
    out["gain by window"]=A.dropna(subset=["gain"]).groupby("w")["gain"].mean()
    return out
