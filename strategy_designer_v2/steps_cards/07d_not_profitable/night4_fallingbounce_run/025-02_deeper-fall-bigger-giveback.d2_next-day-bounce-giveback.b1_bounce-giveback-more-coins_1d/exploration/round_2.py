def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        allr=pd.concat([w["close"].pct_change() for w in ws.values()])
        mu=allr.mean()
        for wn,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":wn,"f":b["forecast"],"z":r/r.rolling(20).std(),
                "r30":c/c.shift(30)-1,"vrel":b["volume"]/b["volume"].rolling(20).mean(),
                "alloc":b["postRebalance_current_allocation"],"prev":b["previous_allocation"]})
            d["nxt"]=c.shift(-1)/c-1
            d["gain"]=d["alloc"]*d["nxt"]
            d["fee"]=(b["postRebalance_total_value"]-b["total_portfolio_value"])/b["total_portfolio_value"]
            d["turn"]=(d["alloc"]-d["prev"]).abs()
            for h in [1,3,5]:
                d[f"u{h}"]=-(c.shift(-h)/c-1-h*mu)
                d[f"t{h}"]=-(c.shift(-h)/c-1)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    D["state"]=np.where(D.alloc.abs()==0,"flat",np.where(D.f<=-2,"signal_bar",np.where(D.f<0,"weak_signal","held_f0")))
    out["by_state"]=D.groupby("state").apply(lambda x: pd.Series({"bars":len(x),"sum_gain":x.gain.sum(),
        "mean_gain":x.gain.mean(),"sum_fee":x.fee.sum(),"mean_absalloc":x.alloc.abs().mean(),"sum_turn":x.turn.sum()}))
    K=D[D.f<=-2].dropna(subset=["u1","r30","vrel"])
    K["r30q"]=pd.qcut(K.r30,3,labels=["low","mid","high"])
    K["vq"]=pd.qcut(K.vrel,3,labels=["low","mid","high"])
    def g(x):
        return pd.Series({"n":len(x),"u1":x.u1.mean(),"t":x.u1.mean()/x.u1.std()*np.sqrt(len(x)),
            "tot1":x.t1.mean(),"tot3":x.t3.mean(),"tot5":x.t5.mean()})
    out["r30_x_vrel"]=K.groupby(["r30q","vq"],observed=True).apply(g)
    # r30 continuous grading
    K["score"]=-K.r30*K.z
    out["by_r30z"]=K.groupby(pd.qcut(K.score,5),observed=True).apply(g)
    out["corr_alloc_f"]=pd.Series({"corr":D[["alloc","f"]].corr().iloc[0,1],
        "share_signal_bars_alloc_nonzero":(D[D.f<=-2].alloc.abs()>0).mean()})
    return out
