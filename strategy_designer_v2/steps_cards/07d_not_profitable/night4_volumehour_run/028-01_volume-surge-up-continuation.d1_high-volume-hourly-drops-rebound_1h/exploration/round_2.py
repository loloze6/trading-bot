import numpy as np, pandas as pd

def explore(data):
    out = {}
    B=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True).copy()
            b["ret1"]=b.close.shift(-1)/b.close-1
            for h in [6,24,72]:
                b[f"r{h}"]=b.close.shift(-h)/b.close-1
            b["past30"]=b.close/b.close.shift(720)-1
            b["past7"]=b.close/b.close.shift(168)-1
            b["pos"]=np.arange(len(b)); b["cell"]=b.pos//24
            b["coin"]=c; b["w"]=int(w[1:])
            b["df"]=b.forecast.diff()
            B.append(b)
    B=pd.concat(B, ignore_index=True)
    a=B.postRebalance_current_allocation
    out["forecast state"]=f"share fc>0 {(B.forecast>0).mean():.3f}, fc>=2 {(B.forecast>=2).mean():.3f}, median fc when >0 {B.forecast[B.forecast>0].median():.2f}, share long when fc==0 {((a>0.001)&(B.forecast==0)).sum()/max((B.forecast==0).sum(),1):.3f}"
    # book bar gain by past30 state
    g=B.dropna(subset=["ret1","past30"]).copy()
    g["gain"]=a.loc[g.index]*g.ret1
    g["s30"]=pd.qcut(g.past30.rank(method="first"),5,labels=False)
    out["bar gain by past30 quintile"]=g.groupby("s30").agg(n=("gain","size"),gain_mean=("gain","mean"),coin_mean=("ret1","mean"),alloc=("postRebalance_current_allocation","mean"),med30=("past30","median")).round(6)
    g["s7"]=pd.qcut(g.past7.rank(method="first"),5,labels=False)
    out["bar gain by past7 quintile"]=g.groupby("s7").agg(gain_mean=("gain","mean"),coin_mean=("ret1","mean"),alloc=("postRebalance_current_allocation","mean"),med7=("past7","median")).round(6)
    # cases
    grid=B[B.pos%24==0]
    drift={h:grid.dropna(subset=[f"r{h}"]).groupby("coin")[f"r{h}"].mean() for h in [6,24,72]}
    sd={h:grid.dropna(subset=[f"r{h}"]).groupby("coin")[f"r{h}"].std() for h in [6,24,72]}
    cs=B[(B.forecast>=2)&(B.df>0)].groupby(["coin","w","cell"]).head(1).copy()
    rows=[]
    cs["up30"]=np.where(cs.past30.isna(),"na",np.where(cs.past30>0,"30d up","30d down"))
    for h in [6,24,72]:
        cs[f"ex{h}"]=cs[f"r{h}"]-cs.coin.map(drift[h])
        cs[f"st{h}"]=cs[f"ex{h}"]/cs.coin.map(sd[h])
        for k,gr in cs.dropna(subset=[f"ex{h}"]).groupby("up30"):
            x=gr[f"ex{h}"]
            rows.append({"h":h,"state":k,"n":len(x),"mean_ex":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"strength":gr[f"st{h}"].mean(),"total":gr[f"r{h}"].mean()})
    out["cases by horizon and 30d sign"]=pd.DataFrame(rows).round(5)
    # graded within 30d up: slope of ex24 on past30
    up=cs[(cs.past30>0)].dropna(subset=["ex24"])
    out["corr ex24~past30 (all cases)"]=f"{cs.dropna(subset=['ex24','past30'])[['ex24','past30']].corr().iloc[0,1]:.4f}, n {cs.dropna(subset=['ex24','past30']).shape[0]}"
    # deepest-fall windows 12-14 alloc and past30
    dfw=B[B.w.between(12,14)]
    out["w12-14"]=f"mean alloc {dfw.postRebalance_current_allocation.mean():.3f}, share bars past30<0 {(dfw.past30<0).mean():.3f}, coin chained per-bar mean {dfw.ret1.mean():.2e}"
    # windows: alloc by past30 sign
    g["sgn"]=np.where(g.past30>0,"up","down")
    out["alloc and gain by 30d sign"]=g.groupby("sgn").agg(n=("gain","size"),alloc=("postRebalance_current_allocation","mean"),gain=("gain","mean"),coin=("ret1","mean")).round(6)
    return out
