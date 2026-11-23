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
            df = pd.DataFrame({"coin":c,"wn":int(w[1:]),"pos":np.arange(len(b)),"f":f,"alloc":alloc,
                "ret20":cl/cl.shift(20)-1,"ret5":cl/cl.shift(5)-1,
                "fwd3":cl.shift(-3)/cl-1,"fwd6":cl.shift(-6)/cl-1,"fwd9":cl.shift(-9)/cl-1,
                "rn":cl.shift(-1)/cl-1})
            recs.append(df)
    X = pd.concat(recs, ignore_index=True)
    X["gain"]=X.alloc*X.rn
    def summ(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    # fall period w1-w10 held gain by trend state and forecast strength
    med = X.loc[X.f>0,"f"].median()
    H = X[(X.alloc.abs()>0)].dropna(subset=["gain"])
    tab={}
    for per,pc in [("w1-10",H.wn<=10),("w11-24",H.wn>10)]:
        for nm,cond in [("ret20>0",H.ret20>0),("ret20<=0",H.ret20<=0)]:
            for sn,sc in [("f>=med",H.f>=med),("f<med",H.f<med)]:
                s=H.loc[pc&cond&sc,"gain"]
                tab[f"{per}|{nm}|{sn}"]=pd.Series({"n":len(s),"mean":s.mean(),"sum":s.sum()})
    out["held gain fall vs rest"]=pd.DataFrame(tab).T.round(5)
    # quartile x trend state, horizons, on grids
    res={}
    for h in [3,6,9]:
        G=X[X.pos%h==0].dropna(subset=[f"fwd{h}"])
        dr=G.groupby("coin")[f"fwd{h}"].mean()
        G=G.assign(ex=G[f"fwd{h}"]-G.coin.map(dr))
        S=G[G.f>0].copy()
        qs=S.f.quantile([0.5]).values[0]
        for nm,cond in [("ret20>0",S.ret20>0),("ret20<=0",S.ret20<=0)]:
            for sn,sc in [("top",S.f>=qs),("bot",S.f<qs)]:
                res[f"h{h}|{nm}|{sn}"]=summ(S.loc[cond&sc,"ex"])
        # condition alone: ret20>0 without signal
        res[f"h{h}|ret20>0|nosig"]=summ(G.loc[(G.ret20>0)&(G.f<=0),"ex"])
        res[f"h{h}|all top"]=summ(S.loc[S.f>=qs,"ex"])
    out["excess by strength x trend x horizon"]=pd.DataFrame(res).T.round(4)
    return out
