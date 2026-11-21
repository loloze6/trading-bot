def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                rs.append(c[i+H]/c[i]-1)
        drift[coin] = np.mean(rs); usual[coin] = np.std(rs)
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; f = b["forecast"].values
            ts = pd.to_datetime(b["timestamp"])
            # realised vol 20d at bar
            lr = np.log(b["close"]).diff()
            vol = lr.rolling(20, min_periods=10).std().values
            r28 = b["close"].pct_change(28).values
            for i in range(0, len(c) - H, H):
                r = c[i+H]/c[i]-1
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, f=f[i]/10,
                                 ex=r-drift[coin], r=r, vol=vol[i], r28=r28[i],
                                 usual=usual[coin]))
    d = pd.DataFrame(rows)
    d["v"] = d.f*d.ex
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["all"] = tt(d.v).to_frame().T
    out["by_coin"] = d.groupby("coin").v.apply(tt).unstack()
    out["by_year"] = d.groupby("year").v.apply(tt).unstack()
    out["by_window"] = d.groupby("w").v.apply(tt).unstack()
    d["side"] = np.sign(d.f)
    out["by_side"] = d.groupby("side").v.apply(tt).unstack()
    # side: ex in direction
    d["exdir"] = d.side*d.ex
    out["by_side_exdir"] = d.groupby("side").exdir.apply(tt).unstack()
    d["fq"] = pd.qcut(d.f.abs().rank(method="first"), 5, labels=False)
    g = d.groupby("fq")
    out["by_absf_quint"] = pd.concat([g.f.apply(lambda x: x.abs().mean()).rename("absf"), g.exdir.apply(tt).unstack()], axis=1)
    d["fq_signed"] = pd.qcut(d.f.rank(method="first"), 10, labels=False)
    g = d.groupby("fq_signed")
    out["by_f_decile_ex"] = pd.concat([g.f.mean().rename("f"), g.ex.apply(tt).unstack()], axis=1)
    # vol regime relative per coin
    d["volq"] = d.groupby("coin").vol.transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["by_vol_tercile"] = d.groupby("volq").v.apply(tt).unstack()
    out["by_vol_tercile_side"] = d.groupby(["volq","side"]).exdir.apply(tt).unstack()
    # other horizons using r28 raw sign*ex at longer horizons computed separately
    res = []
    for Hh in [1,3,5,10,20]:
        vals=[]
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b=b.reset_index(drop=True); c=b["close"].values; f=b["forecast"].values/10
                rr=[c[i+Hh]/c[i]-1 for i in range(0,len(c)-Hh,Hh)]
                dr=None
                for k,i in enumerate(range(0,len(c)-Hh,Hh)):
                    vals.append((coin, f[i], rr[k]))
        v=pd.DataFrame(vals,columns=["coin","f","r"])
        v["ex"]=v.r-v.groupby("coin").r.transform("mean")
        x=v.f*v.ex
        res.append(dict(H=Hh,n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))),
                        corr=stats.spearmanr(v.f,v.ex).correlation))
    out["by_horizon"]=pd.DataFrame(res)
    return out
