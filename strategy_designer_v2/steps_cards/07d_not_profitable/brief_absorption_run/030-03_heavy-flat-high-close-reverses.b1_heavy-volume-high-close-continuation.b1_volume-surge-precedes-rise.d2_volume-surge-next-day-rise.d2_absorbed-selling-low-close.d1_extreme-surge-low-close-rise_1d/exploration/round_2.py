import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    wins = sorted(bars[coins[0]].keys(), key=lambda w: int(w[1:]))
    rows=[]
    for c in coins:
        for w in wins:
            if w not in bars[c]: continue
            b = bars[c][w].copy().reset_index(drop=True)
            b["pos"]=np.arange(len(b))
            for h in (1,2,3,5):
                b[f"r{h}"]=b["close"].shift(-h)/b["close"]-1
            b["vs"]=b["volume"]/b["volume"].shift(1).rolling(20).mean()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["lc"]=(b["high"]-b["close"])/rng
            b["ma50"]=b["close"]/b["close"].rolling(50,min_periods=20).mean()-1
            b["alloc"]=b["postRebalance_current_allocation"]
            b["turn"]=(b["alloc"]-b["previous_allocation"]).abs()
            b["coin"]=c; b["w"]=w
            rows.append(b[["pos","r1","r2","r3","r5","vs","lc","ma50","forecast","alloc","turn","coin","w","timestamp"]])
    X=pd.concat(rows,ignore_index=True)
    cost=0.0019/2
    X["pnl"]=X["alloc"]*X["r1"]-X["turn"]*cost
    X["fb"]=pd.cut(X["forecast"],[-0.1,5,10,20.1],labels=["<=5","5-10",">10"])
    out["pnl net by forecast band"]=X.groupby("fb",observed=True).agg(n=("pnl","size"),pnl_sum=("pnl","sum"),gross=("r1",lambda s: (X.loc[s.index,"alloc"]*s).sum()),fees=("turn",lambda s:(s*cost).sum()),alloc=("alloc","mean"))
    # simulated book variants: daily mean over coins per window, compute dd & calmar
    def book(mask_fn,name):
        Y=X.copy(); m=mask_fn(Y)
        Y["p"]=np.where(m,Y["alloc"]*Y["r1"],0.0)
        # turnover approx: changes in masked alloc
        Y["a2"]=np.where(m,Y["alloc"],0.0)
        Y["t2"]=Y.groupby(["coin","w"])["a2"].diff().abs().fillna(Y["a2"])
        Y["p"]=Y["p"]-Y["t2"]*cost
        Y=Y.dropna(subset=["r1"])
        D=Y.groupby(["w","pos"])["p"].mean().reset_index()
        D["wi"]=D["w"].str[1:].astype(int); D=D.sort_values(["wi","pos"])
        v=(1+D["p"]).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(D))-1
        return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":D["p"].mean()/D["p"].std()*np.sqrt(365),"share_in":m.mean()})
    out["variants"]=pd.DataFrame({
        "all":book(lambda Y: Y["forecast"]>=0,"all"),
        "fc>5":book(lambda Y: Y["forecast"]>5,""),
        "fc>10":book(lambda Y: Y["forecast"]>10,""),
        "fc>15":book(lambda Y: Y["forecast"]>15,""),
    }).T
    # horizon of the effect on strong signals, non-overlapping per h grid
    mu={h:X.groupby("coin")[f"r{h}"].mean() for h in (1,2,3,5)}
    res=[]
    for h in (1,2,3,5):
        G=X[X["pos"]%h==0].dropna(subset=[f"r{h}"]).copy()
        G["ex"]=G[f"r{h}"]-G["coin"].map(mu[h])
        for nm,m in [("fc>10",G["forecast"]>10),("fc<=5",G["forecast"]<=5)]:
            s=G.loc[m,"ex"]; res.append({"h":h,"grp":nm,"n":len(s),"ex":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    out["horizon"]=pd.DataFrame(res)
    # stronger case: surge x lowclose grid
    X["vsq"]=pd.cut(X["vs"],[0,1,1.5,2.5,100]); X["lcq"]=pd.cut(X["lc"],[-0.01,0.5,0.8,1.01])
    mu1=X.groupby("coin")["r1"].mean(); X["ex1"]=X["r1"]-X["coin"].map(mu1)
    g=X.dropna(subset=["ex1","vsq","lcq"]).groupby(["vsq","lcq"],observed=True)["ex1"].agg(["size","mean","std"])
    g["t"]=g["mean"]/(g["std"]/np.sqrt(g["size"])); out["surge x lowclose ex1"]=g
    # deepest fall period: holdings in w1-w3 by band
    F=X[X["w"].isin(["w1","w2","w3"])]
    out["w1-w3 pnl by band"]=F.groupby("fb",observed=True).agg(n=("pnl","size"),pnl_sum=("pnl","sum"),r1=("r1","mean"),alloc=("alloc","mean"))
    return out
