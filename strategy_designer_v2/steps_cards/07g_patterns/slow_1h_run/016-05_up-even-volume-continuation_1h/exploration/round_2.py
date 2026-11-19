def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72; rows=[]; hrows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            c=df["close"].values.astype(float)
            lr=np.diff(np.log(c),prepend=np.nan)
            ts=pd.to_datetime(df["timestamp"])
            r1=pd.Series(c).pct_change().shift(-1).values
            hrows.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"year":ts.dt.year.values,"r":r1}))
            n=len(c)
            for t in range(H,n-H,H):
                seg=lr[t-H+1:t+1]
                if np.any(~np.isfinite(seg)): continue
                sabs=np.abs(seg).sum()
                rows.append(dict(coin=coin,w=w,year=ts.iloc[t].year,past=c[t]/c[t-H]-1,fwd=c[t+H]/c[t]-1,
                                 eff=abs(seg.sum())/sabs if sabs>0 else np.nan,vol=np.sqrt((seg**2).sum())))
    g=pd.DataFrame(rows).dropna()
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    g["side"]=np.where(g.past>0,"up","down")
    out={}
    def tb(sub,col):
        q=sub[col].rank(pct=True); a=sub.loc[q>2/3,"ex"]; b=sub.loc[q<=1/3,"ex"]
        if len(a)<10 or len(b)<10: return [len(sub),np.nan,np.nan,np.nan]
        return [len(sub),a.mean(),b.mean(),stats.ttest_ind(a,b,equal_var=False).statistic]
    # eff within size terciles of |past|, per side
    res={}
    for side,sub in g.groupby("side"):
        sub=sub.copy(); sub["sz"]=pd.qcut(sub.past.abs(),3,labels=["s1","s2","s3"])
        for sz,s2 in sub.groupby("sz",observed=True):
            # also within each coin: rank eff within coin
            res[f"{side}_{sz}"]=tb(s2,"eff")
    out["eff_within_size"]=pd.DataFrame(res,index=["n","top","bot","t"]).T.round(4)
    # eff residual on vol and |past| per coin ranking
    g["effr"]=g.groupby("coin")["eff"].rank(pct=True)
    pc={}
    for (coin,side),sub in g.groupby(["coin","side"]):
        pc[f"{coin}_{side}"]=tb(sub,"eff")
    out["eff_per_coin_side"]=pd.DataFrame(pc,index=["n","top","bot","t"]).T.round(4)
    # by year, signed eff = sign(past)*eff predicting ex? test eff on up side by year
    yr={}
    for (y,side),sub in g.groupby(["year","side"]):
        yr[f"{y}_{side}"]=tb(sub,"eff")
    out["eff_by_year_side"]=pd.DataFrame(yr,index=["n","top","bot","t"]).T.round(4)
    # down side: low eff (choppy drops) vs eff; check down_past rebound within vol terciles
    h=pd.concat(hrows).dropna(subset=["r"])
    h2=h[h.hour.isin([20,21])]
    y=h2.groupby("year")["r"].agg(["mean","std","count"]); y["t"]=y["mean"]/(y["std"]/np.sqrt(y["count"]))
    out["h20_21_by_year"]=y[["mean","count","t"]].round(6)
    cc=h2.groupby("coin")["r"].agg(["mean","std","count"]); cc["t"]=cc["mean"]/(cc["std"]/np.sqrt(cc["count"]))
    out["h20_21_by_coin"]=cc[["mean","t"]].round(6)
    h3=h[h.wd==4]; y3=h3.groupby("year")["r"].agg(["mean","std","count"]); y3["t"]=y3["mean"]/(y3["std"]/np.sqrt(y3["count"]))
    out["fri_by_year"]=y3[["mean","t"]].round(6)
    return out
