def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.concatenate(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]
            r1 = c.shift(-1)/c-1
            r2 = c.shift(-2)/c-1
            r3 = c.shift(-3)/c-1
            ret = c/c.shift(1)-1
            vr = b["volume"]/b["volume"].shift(1).rolling(20).mean()
            rng = (b["high"]-b["low"]).replace(0,np.nan)
            cl = (c-b["low"])/rng
            df = pd.DataFrame({"coin":coin,"w":int(w[1:]),"year":ts.dt.year,"dow":ts.dt.dayofweek,
                               "fc":b["forecast"],"ex1":r1-mu,"ex2":r2-2*mu,"ex3":r3-3*mu,
                               "ret":ret,"vr":vr,"cl":cl,"pos":np.arange(len(b))})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["we"] = d["dow"].isin([5,6])
    a = d[(d.fc>0)].dropna(subset=["ex1"]).copy()
    def slope(g, y="ex1", x="fc"):
        g = g.dropna(subset=[y,x])
        if len(g) < 20: return pd.Series({"n":len(g),"b":np.nan,"t":np.nan,"mean_ex_bp":np.nan})
        r = stats.linregress(g[x], g[y])
        return pd.Series({"n":len(g),"b":r.slope*1e4,"t":r.slope/r.stderr,"mean_ex_bp":g[y].mean()*1e4})
    out = {}
    out["by_dow"] = a.groupby("dow").apply(slope)
    out["by_we_coin"] = a.groupby(["we","coin"]).apply(slope)
    out["by_we_year"] = a.groupby(["we","year"]).apply(slope)
    a["q"] = a.groupby("we")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["quint"] = a.groupby(["we","q"]).agg(n=("ex1","size"),fc=("fc","mean"),ex1_bp=("ex1",lambda s:s.mean()*1e4),
                                           t=("ex1",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    hz = []
    for h,y in [(1,"ex1"),(2,"ex2"),(3,"ex3")]:
        g = a[a.pos % h == 0]
        for we in [True, False]:
            s = slope(g[g.we==we], y=y)
            hz.append({"h":h,"we":we,**s.to_dict()})
    out["horizons"] = pd.DataFrame(hz)
    f = d[(d.ret<0)].dropna(subset=["ex1","vr"]).copy()
    f = f[f.vr>0]
    f["fall"] = -f["ret"]
    res = []
    for we in [True, False]:
        g = f[f.we==we]
        X = np.column_stack([np.ones(len(g)), g.fall, np.log(g.vr), g.fall*np.log(g.vr)])
        bta, *_ = np.linalg.lstsq(X, g.ex1.values, rcond=None)
        e = g.ex1.values - X@bta
        cov = np.linalg.inv(X.T@X)*(e@e)/(len(g)-4)
        res.append({"we":we,"n":len(g),**{k:bta[i]/np.sqrt(cov[i,i]) for i,k in enumerate(["t_c","t_fall","t_logvr","t_inter"])}})
    out["fall_vol_terms_t"] = pd.DataFrame(res)
    f["clq"] = f.groupby("we")["cl"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["fall_by_closeloc"] = f.groupby(["we","clq"]).apply(lambda g: slope(g, x="fall"))
    f["vrq"] = f.groupby("we")["vr"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["fall_by_volq"] = f.groupby(["we","vrq"]).apply(lambda g: slope(g, x="fall"))
    return out
