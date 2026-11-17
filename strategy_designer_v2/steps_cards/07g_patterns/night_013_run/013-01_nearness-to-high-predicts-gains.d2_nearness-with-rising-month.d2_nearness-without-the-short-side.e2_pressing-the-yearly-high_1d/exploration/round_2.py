def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    res={}
    # weekday by coin and by year (daily coin returns)
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.reset_index(drop=True)
            day=pd.to_datetime(d["day"])
            x=pd.DataFrame({"coin":coin,"w":w,"cr":d["coin_return"],"wd":day.dt.dayofweek,"yr":day.dt.year})
            x["prev"]=d["coin_return"].shift(1)
            c=d["close"].astype(float)
            x["f3"]=c.shift(-3)/c-1
            x["r1"]=c/c.shift(1)-1
            x["sd"]=x["r1"].rolling(30).std().shift(1)
            x["z"]=x["r1"]/x["sd"]
            x["pos"]=np.arange(len(d))
            D.append(x)
    D=pd.concat(D)
    Dc=D.dropna(subset=["cr"])
    sat=Dc.assign(s=(Dc.wd==5)).groupby(["coin","s"])["cr"].mean().unstack().round(5)
    res["sat_vs_other_by_coin"]=sat
    def wt(g):
        a=g.loc[g.wd==5,"cr"];b=g.loc[g.wd!=5,"cr"]
        return pd.Series({"diff":a.mean()-b.mean(),"t":stats.ttest_ind(a,b,equal_var=False).statistic,"n":len(a)})
    res["sat_by_year"]=Dc.groupby("yr").apply(wt).round(4)
    res["sat_by_coin_t"]=Dc.groupby("coin").apply(wt).round(4)
    # reversal after big down days, non-overlapping 3-day grid, z by trailing vol
    G=D[(D.pos%3==0)].dropna(subset=["f3","z"]).copy()
    G["ex"]=G["f3"]-G.groupby("coin")["f3"].transform("mean")
    G["zb"]=pd.cut(G["z"],[-99,-2,-1,0,1,2,99])
    o=G.groupby("zb")["ex"].agg(["mean","count","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    res["z_to_next3_grid"]=o.round(4)
    o=G[G.z<-1].groupby("coin")["ex"].agg(["mean","count"]);res["z_lt_-1_by_coin"]=o.round(4)
    o=G[G.z<-1].groupby("yr")["ex"].agg(["mean","count"]);res["z_lt_-1_by_year"]=o.round(4)
    # breakout and past7 7-day: per coin, top quintile minus bottom
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float).reset_index(drop=True)
            v=b["volume"].astype(float).reset_index(drop=True)
            df=pd.DataFrame({"coin":coin,"w":w,"fwd":c.shift(-7)/c-1,
                "brk":c/c.rolling(30).max().shift(1)-1,"p7":c/c.shift(7)-1,
                "vr":v/v.rolling(20).mean(),"d364":c/c.rolling(364,min_periods=91).max()-1})
            rows.append(df.iloc[::7])
    g=pd.concat(rows).dropna(subset=["fwd"])
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    out={}
    for col in ["brk","p7","vr"]:
        x=g.dropna(subset=[col]).copy()
        x["q"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        per=x[x.q.isin([0,4])].groupby(["coin","q"])["ex"].mean().unstack()
        out[col]=(per[4]-per[0])
        sp=x.groupby("coin").apply(lambda s: stats.spearmanr(s[col],s["ex"]).correlation)
        out[col+"_rho"]=sp
    res["top_minus_bottom_by_coin"]=pd.DataFrame(out).round(4)
    x=g.dropna(subset=["brk"]).copy()
    x["q"]=x.groupby("coin")["brk"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    x["yr"]=0
    # volume interaction: breakout top quintile split by volume ratio high/low
    x2=x.dropna(subset=["vr"])
    x2["vh"]=x2.groupby("coin")["vr"].transform(lambda s: s>s.median())
    o=x2.groupby(["q","vh"])["ex"].agg(["mean","count"]);res["brk_by_vol"]=o.round(4)
    return res
