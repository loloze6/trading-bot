def explore(data):
    import numpy as np, pandas as pd
    H=5
    allrows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20,min_periods=10).std()
            fwd=c.shift(-H)/c-1
            rng=(df["high"]-df["low"])/c
            ts=pd.to_datetime(df["timestamp"])
            d=pd.DataFrame({"coin":coin,"win":w,"fwd":fwd,"p1z":r1/vol,"rng":rng/vol,
                            "sgnrng":np.sign(r1)*rng/vol,"wd":ts.dt.weekday,"yr":ts.dt.year,
                            "pos":np.arange(len(df))%H})
            allrows.append(d)
    B=pd.concat(allrows)
    B=B.dropna(subset=["fwd"])
    st=B[B.pos==0].groupby("coin")["fwd"].agg(["mean","std"])
    B=B.join(st,on="coin")
    B["unus"]=(B.fwd-B["mean"])/B["std"]; B["unus_raw"]=B.fwd-B["mean"]
    def agg(x,by):
        o=x.groupby(by).agg(n=("unus","size"),strength=("unus","mean"),unus_pct=("unus_raw",lambda s:100*s.mean()),sd=("unus","std"))
        o["t"]=o.strength/(o.sd/np.sqrt(o.n)); return o.drop(columns="sd").round(3)
    res={}
    G=B[B.pos==0].dropna(subset=["p1z"]).copy()
    G["dec"]=G.groupby("coin")["p1z"].transform(lambda s: pd.qcut(s.rank(method="first"),10,labels=False))
    res["p1z_deciles"]=agg(G,"dec")
    G["q"]=G.dec//2
    res["p1z_top_fifth_by_coin"]=agg(G[G.q==4],"coin")
    res["p1z_top_fifth_by_year"]=agg(G[G.q==4],"yr")
    G["sdec"]=G.groupby("coin")["sgnrng"].transform(lambda s: pd.qcut(s.rank(method="first"),10,labels=False))
    res["signed_range_deciles"]=agg(G,"sdec")
    # robustness over grid phase
    P=B.dropna(subset=["p1z"]).copy()
    P["q"]=P.groupby(["coin","pos"])["p1z"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    res["p1z_top_minus_rest_by_phase"]=P.groupby("pos").apply(lambda x: pd.Series({
        "top":x[x.q==4].unus.mean(),"rest":x[x.q<4].unus.mean(),"n_top":(x.q==4).sum(),
        "t_top":x[x.q==4].unus.mean()/(x[x.q==4].unus.std()/np.sqrt((x.q==4).sum()))})).round(3)
    res["weekday_by_phase_MonTue_minus_rest"]=P.groupby("pos").apply(lambda x: pd.Series({
        "montue":x[x.wd<=1].unus.mean(),"rest":x[x.wd>1].unus.mean(),
        "t":(x[x.wd<=1].unus.mean())/(x[x.wd<=1].unus.std()/np.sqrt((x.wd<=1).sum()))})).round(3)
    # graded within positive days: p1z continuous corr among up days
    up=G[G.p1z>0]
    res["corr_p1z_unus_updays_by_coin"]=up.groupby("coin").apply(lambda x: pd.Series({"corr":x.p1z.corr(x.unus),"n":len(x)})).round(3)
    return res
