def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            if len(b)<40: continue
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            rng=(h-l)/c
            rr=rng/rng.rolling(30,min_periods=20).mean()
            ret20=c/c.shift(20)-1
            r1=c/c.shift(1)-1
            vol20=r1.rolling(20).std()
            volrel=vol20/r1.rolling(60,min_periods=40).std()
            hi30=c/h.rolling(30).max()-1
            f5=c.shift(-5)/c-1
            idx=np.arange(0,len(b),5)
            d=pd.DataFrame({"coin":coin,"win":w,"rr":rr,"ret20":ret20,"r1":r1,"volrel":volrel,"hi30":hi30,"f5":f5,
                            "year":pd.to_datetime(b["timestamp"]).dt.year}).iloc[idx]
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["f5"])
    D["ex"]=D["f5"]-D.groupby("coin")["f5"].transform("mean")
    out={}
    def half(df,col):
        x=df.dropna(subset=[col,"ex"])
        m=x[col].median()
        a=x[x[col]>m]["ex"]; b=x[x[col]<=m]["ex"]
        t=stats.ttest_ind(a,b,equal_var=False).statistic
        cc=x.groupby("coin").apply(lambda g: stats.spearmanr(g[col],g.ex).correlation if len(g)>=15 else np.nan).dropna()
        yy=x.groupby("year").apply(lambda g: stats.spearmanr(g[col],g.ex).correlation if len(g)>=30 else np.nan).dropna()
        return pd.Series({"nA":len(a),"meanA":a.mean(),"nB":len(b),"meanB":b.mean(),"diff":a.mean()-b.mean(),"t":t,
                          "spearman":stats.spearmanr(x[col],x.ex).correlation,"coins_pos":(cc>0).mean(),"n_coins":len(cc),
                          "years_pos":(yy>0).mean(),"n_years":len(yy)})
    dn=D[D.ret20<=0]; up=D[D.ret20>0]
    res={"rr_downtrend":half(dn,"rr"),"rr_uptrend":half(up,"rr"),"rr_all":half(D,"rr"),
         "volrel_all":half(D,"volrel"),"hi30_all":half(D,"hi30"),"hi30_uptrend":half(up,"hi30")}
    out["halves"]=pd.DataFrame(res).T
    out["dn_rr_by_year"]=dn.dropna(subset=["rr"]).groupby("year").apply(lambda g: pd.Series({"n":len(g),"sp":stats.spearmanr(g.rr,g.ex).correlation}))
    return out
