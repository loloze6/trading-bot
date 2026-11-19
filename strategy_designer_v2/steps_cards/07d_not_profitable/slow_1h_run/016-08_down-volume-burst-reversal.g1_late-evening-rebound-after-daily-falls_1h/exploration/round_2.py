def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            ts=pd.to_datetime(b["timestamp"]); cl=pd.Series(b["close"].values)
            d=pd.DataFrame({"hour":ts.dt.hour.values})
            for h in [1,2,4,8,12,24,48,72]:
                d[f"r{h}"]=(cl.shift(-h)/cl-1).values
            d["p24"]=(cl/cl.shift(24)-1).values
            d["p72"]=(cl/cl.shift(72)-1).values
            lr=np.log(cl).diff()
            d["vol24"]=lr.rolling(24).std().values
            d["maxbar24"]=lr.abs().rolling(24).max().values/ (lr.abs().rolling(24).sum().values)
            d["pos"]=b["postRebalance_current_allocation"].values
            d["fee"]=(b["postRebalance_total_value"]/b["total_portfolio_value"]-1).values
            d["coin"]=c; d["win"]=w
            rows.append(d)
    B=pd.concat(rows)
    out={}
    # coin mean per horizon (all bars approx)
    cm={h:B[f"r{h}"].mean() for h in [1,2,4,8,12,24,48,72]}
    h=B[(B.hour==19)&(B.p24<0)].copy()
    h["q"]=pd.qcut(h.p24.rank(method="first"),3,labels=["deep","mid","shallow"])
    res={}
    for hh in [1,2,4,8,12,24,48,72]:
        x=h[f"r{hh}"]-cm[hh]
        g=x.groupby(h.q).mean()
        # slope t of excess on -p24
        m=x.notna()
        s=stats.linregress(-h.p24[m],x[m])
        res[f"{hh}h"]={"deep":g["deep"],"mid":g["mid"],"shallow":g["shallow"],"slope_t":s.slope/s.stderr,"n":int(m.sum())}
    out["horizon_excess_by_fall"]=pd.DataFrame(res).T
    # fee per trade relative to position size
    tr=B[B.fee.abs()>0]
    out["fee_stats"]=pd.Series({"n_fee_bars":len(tr),"mean_fee":tr.fee.mean(),"fee_per_unit_turnover":(tr.fee/ (B.loc[B.fee.abs()>0,"pos"].abs()+1e-9)).median()})
    # shape of fall: jump vs grind among deep falls, r24 excess
    dd=h[h.q=="deep"].copy()
    dd["shape"]=pd.qcut(dd.maxbar24.rank(method="first"),2,labels=["grind","jump"])
    out["deep_by_shape"]=dd.groupby("shape").agg(n=("r24","size"),p24=("p24","mean"),r2=("r2","mean"),r24=("r24","mean"),r48=("r48","mean"))
    # by year of deep falls r24
    return out
