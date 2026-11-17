def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    res={}
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float).reset_index(drop=True)
            v=b["volume"].astype(float).reset_index(drop=True)
            r1=c.pct_change()
            df=pd.DataFrame({"coin":coin,"w":w,"fwd":c.shift(-7)/c-1,
                "brk":c/c.rolling(30).max().shift(1)-1,
                "vr":v/v.rolling(20).mean(),
                "z":r1/r1.rolling(30).std().shift(1),
                "f3":c.shift(-3)/c-1})
            rows.append(df.iloc[::7])
    g=pd.concat(rows).dropna(subset=["fwd","brk","vr"]).copy()
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    g["qb"]=g.groupby("coin")["brk"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    g["vh"]=g.groupby("coin")["vr"].transform(lambda s: s>s.median())
    top=g[g.qb==4]
    a=top.loc[top.vh,"ex"];b=top.loc[~top.vh,"ex"]
    res["top_brk_hiV_vs_loV"]=pd.Series({"hi_mean":a.mean(),"hi_t":a.mean()/(a.std()/np.sqrt(len(a))),"hi_n":len(a),
        "lo_mean":b.mean(),"lo_n":len(b),"welch_t":stats.ttest_ind(a,b,equal_var=False).statistic}).round(4)
    res["top_brk_hiV_by_coin"]=top.groupby(["coin","vh"])["ex"].mean().unstack().round(4)
    # graded within top breakout quintile: vr quartiles
    top=top.copy();top["vq"]=pd.qcut(top["vr"].rank(method="first"),4,labels=False)
    o=top.groupby("vq")["ex"].agg(["mean","count","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    res["top_brk_by_vr_quartile"]=o.round(4)
    # whole-sample: vr quintile among bars at/above 30d high (brk>=-0.02)
    near=g[g.brk>=-0.03].copy()
    near["vq"]=pd.qcut(near["vr"].rank(method="first"),4,labels=False)
    o=near.groupby("vq")["ex"].agg(["mean","count","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    res["near30high_by_vr_quartile"]=o.round(4)
    res["near_rho_vr_ex"]=round(stats.spearmanr(near["vr"],near["ex"]).correlation,4)
    res["near_n"]=len(near)
    # by window half
    g["wn"]=g["w"].str[1:].astype(int)
    t2=g[(g.qb==4)]
    res["top_brk_hiV_minus_loV_by_windowgroup"]=t2.assign(h=(t2.wn>12)).groupby(["h","vh"])["ex"].mean().unstack().round(4)
    return res
