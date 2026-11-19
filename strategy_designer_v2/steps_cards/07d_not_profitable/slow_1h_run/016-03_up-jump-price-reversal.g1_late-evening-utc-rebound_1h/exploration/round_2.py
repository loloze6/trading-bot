def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            ts=pd.to_datetime(b["timestamp"],utc=True)
            cl=b["close"]
            d=pd.DataFrame({"hour":ts.dt.hour.values,"f24":(cl/cl.shift(24)-1).values,
                            "vol":np.log(cl).diff().rolling(240).std().values,
                            "pos":b["postRebalance_current_allocation"].values})
            for h in [2,4,8,12,24,48]:
                d[f"r{h}"]=(cl.shift(-h)/cl-1).values
            d["coin"]=c; d["win"]=w
            rows.append(d[d.hour==19])
    D=pd.concat(rows).dropna(subset=["f24","vol","r2"])
    D["fz"]=D.f24/(D.vol*np.sqrt(24))
    out={}
    mu={h:D[f"r{h}"].mean() for h in [2,4,8,12,24,48]}
    D["q"]=pd.qcut(D.fz.rank(method="first"),10,labels=False)
    agg={}
    for h in [2,4,8,12,24,48]:
        agg[f"r{h}_bps"]=(f"r{h}",lambda x:x.mean()*1e4)
    out["fwd_by_fz_decile_bps"]=D.groupby("q").agg(n=("r2","size"),fz=("fz","mean"),**agg)
    def tt(x): x=x.dropna(); return x.mean()/x.std()*np.sqrt(len(x))
    out["t_by_fz_decile"]=D.groupby("q").agg(**{f"t{h}":(f"r{h}",tt) for h in [2,4,8,12,24,48]})
    out["coin_mean_bps"]=pd.Series({h:v*1e4 for h,v in mu.items()})
    D["vq"]=pd.qcut(D.vol.rank(method="first"),3,labels=False)
    out["deep_fall_by_vol"]=D[D.q<=1].groupby("vq").agg(n=("r2","size"),r2=("r2",lambda x:x.mean()*1e4),r12=("r12",lambda x:x.mean()*1e4),r24=("r24",lambda x:x.mean()*1e4),pos=("pos","mean"))
    # book daily
    dd=[]
    for c in data["days"]:
        for w,x in data["days"][c].items():
            dd.append(x[["book_return","coin_return"]].assign(win=w))
    DD=pd.concat(dd).dropna()
    out["book_by_win_bps"]=DD.groupby("win").book_return.mean().mul(1e4).describe()
    return out
