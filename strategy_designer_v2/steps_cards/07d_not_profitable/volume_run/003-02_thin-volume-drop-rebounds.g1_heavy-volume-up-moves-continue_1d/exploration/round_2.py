def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    allb = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["coin"]=coin; b["win"]=w
            b["r1"]=b["close"].shift(-1)/b["close"]-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            b["ret5p"]=b["close"]/b["close"].shift(5)-1
            b["f5"]=b["close"].shift(-5)/b["close"]-1
            b["grid"]=(np.arange(len(b))%5==0)
            for k in range(0,6):
                b[f"rd{k}"]=b["r1"].shift(-k)
                b[f"pd{k}"]=b["pos"].shift(-k)
            allb.append(b)
    B=pd.concat(allb,ignore_index=True)
    cm=B.groupby("coin")["r1"].mean()
    ev=B[B.forecast>=10]
    rows={}
    for k in range(6):
        x=ev[f"rd{k}"]-ev["coin"].map(cm)
        rows[f"day+{k+1}"]={"excess":x.mean(),"t":x.mean()/(x.std()/np.sqrt(x.count())),"meanpos":ev[f"pd{k}"].mean(),"n":x.count()}
    out["event_path_fc10"]=pd.DataFrame(rows).T
    # grid cases forecast>=2 by ret20 tercile, excess f5
    cm5=B[B.grid].groupby("coin")["f5"].mean()
    G=B[B.grid&(B.forecast>=2)].copy()
    G["x5"]=G["f5"]-G["coin"].map(cm5)
    G["sign20"]=np.where(G.ret20>0,"up20","down20")
    out["grid_by_ret20sign"]=G.groupby("sign20")["x5"].agg(["mean","count",lambda s:s.mean()/(s.std()/np.sqrt(s.count()))])
    G["q"]=pd.qcut(G.ret20,4,labels=["q1","q2","q3","q4"])
    out["grid_by_ret20q"]=G.groupby("q")["x5"].agg(["mean","count",lambda s:s.mean()/(s.std()/np.sqrt(s.count()))])
    # book daily: which days lose, by ret20 of prior bar
    B["gain"]=B["pos"]*B["r1"]
    act=B[B.pos>0]
    act=act.assign(s=np.where(act.ret20>0,"up20","down20"))
    out["held_gain_by_ret20sign"]=act.groupby("s")["gain"].agg(["mean","sum","count"])
    # deepest falls of the book: chain days
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy();d["coin"]=coin;d["win"]=w;D.append(d)
    D=pd.concat(D,ignore_index=True)
    br=D.groupby(["win","day"])["book_return"].mean().dropna()
    order=sorted(br.index.get_level_values(0).unique(),key=lambda s:int(s[1:]))
    br=pd.concat([br.loc[w] for w in order])
    eq=(1+br).cumprod();dd=eq/eq.cummax()-1
    out["maxdd"]=dd.min()
    out["book_mean_daily"]=br.mean()
    return out
