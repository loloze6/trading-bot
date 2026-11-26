def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            rng=(b.high-b.low).replace(0,np.nan)
            b["loc"]=(b.high-b.close)/rng
            b["r1"]=b.close.pct_change()
            b["nxt"]=b.close.shift(-1)/b.close-1
            b["ret60"]=b.close/b.close.shift(60)-1
            b["vol20"]=b.r1.rolling(20).std()
            b["rr"]=rng/b.close
            b["rng_rel"]=b.rr/b.rr.rolling(20).mean()
            b["coin"]=coin; b["w"]=w
            b["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            b["inprof"]=(b.regime!="chop")
            rows.append(b[["coin","w","loc","r1","nxt","ret60","vol20","rr","rng_rel","day","inprof"]])
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin").nxt.mean(); d["ex"]=d.nxt-d.coin.map(mu)
    d["volq"]=d.groupby("coin").vol20.transform(lambda x: pd.qcut(x,3,labels=["calm","mid","agit"]))
    d["rgq"]=d.groupby("coin").rng_rel.transform(lambda x: pd.qcut(x,3,labels=["narrow","mid","wide"]))
    d["tr"]=pd.cut(d.ret60,[-9,-.1,.1,99],labels=["fall","chop","rise"])
    d["r1z"]=d.r1/d.vol20
    d["sig"]=(d["loc"]-0.5)*d["ex"]
    d["rngsig"]=(d["loc"]-0.5)*d["rng_rel"]*d["ex"]
    d["r1sig"]=-d["r1z"]*d["ex"]
    def summ(g,col="sig"):
        g=g.dropna(subset=[col])
        s=g.groupby("day")[col].sum()
        t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
        return pd.Series({"n":len(g),"days":len(s),"mean_bp":g[col].mean()*1e4,"t_day":t})
    out={}
    out["slope_vol_x_range"]=d.groupby(["volq","rgq"]).apply(summ)
    out["slope_trend_x_vol"]=d.groupby(["tr","volq"]).apply(summ)
    out["rngsig_all"]=summ(d,"rngsig")
    out["r1sig_all"]=summ(d,"r1sig")
    # joint regression per day-clustered: ex on (loc-.5) and r1z
    from numpy.linalg import lstsq
    res={}
    for name,g in [("all",d),("agit",d[d.volq=="agit"]),("wide",d[d.rgq=="wide"]),("calm",d[d.volq=="calm"])]:
        g=g.dropna(subset=["loc","r1z","ex"])
        X=np.column_stack([np.ones(len(g)),g["loc"]-0.5,g.r1z.clip(-5,5)])
        y=g.ex.values
        bta=lstsq(X,y,rcond=None)[0]; e=y-X@bta
        # cluster by day
        XtXi=np.linalg.inv(X.T@X)
        sc=pd.DataFrame(X*e[:,None]).groupby(g.day.values).sum().values
        V=XtXi@(sc.T@sc)@XtXi; se=np.sqrt(np.diag(V))
        res[name]=pd.Series({"b_loc_bp":bta[1]*1e4,"t_loc":bta[1]/se[1],"b_r1z_bp":bta[2]*1e4,"t_r1z":bta[2]/se[2],"n":len(g)})
    out["joint_reg"]=pd.DataFrame(res).T
    # low close on up day vs down day
    d["up"]=np.where(d.r1>0,"up","down")
    d["locq"]=pd.cut(d["loc"],[-.01,.2,.8,1.01],labels=["hi","mid","low"])
    out["loc_x_dayside_wide"]=d[d.rgq=="wide"].groupby(["up","locq"]).apply(lambda g: summ(g,"ex"))
    # wide-range days graded: by range tercile, low close vs high close
    out["loc_x_range_ex"]=d.groupby(["rgq","locq"]).apply(lambda g: summ(g,"ex"))
    # window-level stability of rngsig
    out["rngsig_by_window"]=d.groupby("w").apply(lambda g: summ(g,"rngsig"))
    return out
