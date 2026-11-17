def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=pd.concat([b["close"].pct_change().dropna() for b in ws.values()])
        mu=allr.mean()
        for w,b in ws.items():
            pos=b["postRebalance_current_allocation"]
            ret1=b["close"].pct_change()
            nr=b["close"].shift(-1)/b["close"]-1
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            vol20=ret1.rolling(20).std()
            vlong=ret1.rolling(250,min_periods=60).std()
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"pos":pos,"nr":nr,"mu":mu,"fee":fee,"ret1":ret1,
               "vol20":vol20,"vrel":vol20/vlong,"z":ret1/vol20,"yr":ts.dt.year,
               "bv":b["postRebalance_total_value"]}))
    d=pd.concat(rows).dropna(subset=["nr","vol20"])
    d["timing"]=d.pos*(d.nr-d.mu); d["gain"]=d.pos*d.nr; d["net"]=d.gain-d.fee
    out={}
    d["vq"]=d.groupby("coin")["vol20"].transform(lambda x:pd.qcut(x.rank(method="first"),3,labels=False))
    def st(g):
        return pd.Series({"timing":g.timing.mean(),"fee":g.fee.mean(),"net":g.net.mean(),
          "t_net":g.net.mean()/(g.net.std()/np.sqrt(len(g))),"n":len(g)})
    out["vq_by_year"]=d.groupby(["yr","vq"]).apply(lambda g:pd.Series({"timing":g.timing.mean(),"net":g.net.mean(),"n":len(g)})).unstack()
    d["rq"]=pd.qcut(d.vrel.rank(method="first"),5,labels=False)
    out["by_vrel_q"]=d.dropna(subset=["vrel"]).groupby("rq").apply(st)
    # reversal coefficient: regress nr/vol20 on z within vol-rel quintile
    def slope(g):
        x=g.z; y=g.nr/g.vol20; m=x.notna()&y.notna()
        r=stats.linregress(x[m],y[m]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":m.sum()})
    out["revslope_by_vrel_q"]=d.dropna(subset=["vrel"]).groupby("rq").apply(slope)
    out["revslope_by_vq"]=d.groupby("vq").apply(slope)
    d["zq"]=pd.qcut(d.z.abs().rank(method="first"),5,labels=False)
    out["revslope_by_absz_q"]=d.groupby("zq").apply(slope)
    out["by_vq"]=d.groupby("vq").apply(st)
    # daily book sharpe by vq (bars are daily)
    out["sharpe_by_vq"]=d.groupby("vq").net.apply(lambda x:x.mean()/x.std()*np.sqrt(365))
    return out
