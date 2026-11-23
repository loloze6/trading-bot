def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            f = b["debug_info.components.rise5.post_pipeline_value"]
            alloc = b["postRebalance_current_allocation"]
            r_next = cl.shift(-1)/cl-1
            df = pd.DataFrame({"coin":c,"wn":int(w[1:]),"pos":np.arange(len(b)),"f":f,"alloc":alloc,
                "ret30":cl/cl.shift(30)-1,"ret60":cl/cl.shift(60)-1,"ret20":cl/cl.shift(20)-1,
                "fwd3":cl.shift(-3)/cl-1,"rn":r_next})
            recs.append(df)
    X = pd.concat(recs, ignore_index=True)
    out["share NaN"] = pd.Series({k: X[k].isna().mean() for k in ["ret20","ret30","ret60"]}).round(3)
    drift = X[X.pos%3==0].groupby("coin")["fwd3"].mean()
    X["ex3"] = X["fwd3"]-X["coin"].map(drift)
    G = X[X.pos%3==0].dropna(subset=["fwd3"])
    def summ(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    tab={}
    for k in ["ret20","ret30"]:
        for nm,cond in [(">0",G[k]>0),("<=0",G[k]<=0)]:
            for sn,sc in [("sig",G.f>0),("nosig",G.f<=0)]:
                tab[f"{k}{nm}|{sn}"]=summ(G.loc[cond&sc,"fwd3"])
    out["fwd3 total by trend state"]=pd.DataFrame(tab).T.round(4)
    # slope within states
    S=G[G.f>0]
    sl={}
    for k in ["ret20","ret30"]:
        for nm,cond in [(">0",S[k]>0),("<=0",S[k]<=0)]:
            s=S[cond].dropna(subset=["ex3"])
            bta=np.polyfit(s.f,s.ex3,1)[0]
            sl[f"{k}{nm}"]=pd.Series({"n":len(s),"slope":bta,"wmean":(s.ex3*s.f).sum()/s.f.sum()})
    out["slope within state"]=pd.DataFrame(sl).T.round(5)
    # simulated books (gross, approx with cost on alloc change)
    cost=0.0019/2
    def book(mask):
        Y=X.copy()
        a=Y["alloc"].where(mask,0.0).fillna(0)
        Y["a"]=a
        Y["chg"]=Y.groupby(["coin","wn"])["a"].diff().abs().fillna(Y["a"].abs())
        Y["g"]=Y["a"]*Y["rn"].fillna(0)-Y["chg"]*cost
        Bk=Y.groupby(["wn","pos"])["g"].mean().reset_index().sort_values(["wn","pos"])
        r=Bk["g"]; v=(1+r).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(r))-1
        return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":r.mean()/r.std()*np.sqrt(365),"inpos":(Y.a.abs()>0).mean()})
    out["books"]=pd.DataFrame({
        "as run":book(pd.Series(True,index=X.index)),
        "ret30>0":book((X.ret30>0)|X.ret30.isna()),
        "ret20>0":book((X.ret20>0)|X.ret20.isna()),
        "f>=median":book(X.f>=X.loc[X.f>0,"f"].median()),
        "ret20>0 & f>=med":book(((X.ret20>0)|X.ret20.isna())&(X.f>=X.loc[X.f>0,"f"].median())),
    }).T.round(4)
    return out
