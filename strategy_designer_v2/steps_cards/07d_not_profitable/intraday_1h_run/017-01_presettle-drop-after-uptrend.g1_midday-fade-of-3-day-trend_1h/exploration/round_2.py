def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]
    H=[]; F=[]
    for c in bars:
        for w,b in bars[c].items():
            ts=pd.to_datetime(b["timestamp"]); cl=b["close"].astype(float)
            a=b["postRebalance_current_allocation"].astype(float)
            pa=b["previous_allocation"].astype(float)
            fee=1-b["postRebalance_total_value"].astype(float)/b["total_portfolio_value"].astype(float)
            ch=(a-pa).abs()
            F.append(pd.DataFrame({"fee":fee,"ch":ch}))
            r72=cl/cl.shift(72)-1
            vol=np.log(cl).diff().rolling(72,min_periods=20).std()*np.sqrt(72)
            d=pd.DataFrame({"h":ts.dt.hour,"yr":ts.dt.year,"coin":c,"z":r72/vol})
            for k in [1,2,3,4,6,8,12]:
                d[f"n{k}"]=cl.shift(-k)/cl-1
            H.append(d[d.h==11])
    F=pd.concat(F); F=F[F.ch>0]
    fee_rate=pd.Series({"fee_per_unit_change_bp":F.fee.sum()/F.ch.sum()*1e4,"n_trades":len(F)})
    H=pd.concat(H).dropna(subset=["z"])
    hz=[]
    for k in [1,2,3,4,6,8,12]:
        g=H.dropna(subset=[f"n{k}"]); s=-np.sign(g.z)*g[f"n{k}"]
        q=pd.qcut(g.z,5,labels=False)
        hz.append(dict(k=k,n=len(g),fade_bp=s.mean()*1e4,t=s.mean()/s.std()*np.sqrt(len(s)),
                       q0_bp=g[f"n{k}"][q==0].mean()*1e4,q2_bp=g[f"n{k}"][q==2].mean()*1e4,q4_bp=g[f"n{k}"][q==4].mean()*1e4))
    H["q"]=pd.qcut(H.z,5,labels=False)
    H["f4"]=-np.sign(H.z)*H.n4
    byyr=H.groupby("yr").f4.agg(["count","mean"]); byyr["mean"]*=1e4
    bycoin=H.groupby("coin").f4.agg(["count","mean"]); bycoin["mean"]*=1e4
    # graded: absolute z quintile, fade over 4h
    H["aq"]=pd.qcut(H.z.abs(),5,labels=False)
    byabs=H.groupby("aq").agg(absz=("z",lambda x:x.abs().mean()),n=("f4","count"),fade4_bp=("f4",lambda x:x.mean()*1e4),
                             t=("f4",lambda x:x.mean()/x.std()*np.sqrt(x.count())))
    return {"fee":fee_rate,"h11_horizons":pd.DataFrame(hz),"fade4_by_year":byyr,"fade4_by_coin":bycoin,"fade4_by_absz":byabs}
