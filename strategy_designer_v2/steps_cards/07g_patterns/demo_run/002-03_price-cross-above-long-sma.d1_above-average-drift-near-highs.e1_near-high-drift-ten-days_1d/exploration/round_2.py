def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    # 10-bar grid: past10 vs rp joint, per coin
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True); cl=b["close"].astype(float); r1=cl.pct_change()
            hi=cl.rolling(20,min_periods=20).max(); lo=cl.rolling(20,min_periods=20).min()
            vol=r1.rolling(20,min_periods=15).std()
            d=pd.DataFrame({"coin":c,"w":w,"rp":(cl-lo)/(hi-lo),"past10":cl/cl.shift(10)-1,
                "past20":cl/cl.shift(20)-1,"z10":(cl/cl.shift(10)-1)/(vol*np.sqrt(10)),
                "fwd":cl.shift(-10)/cl-1,"trend":(b["regime"]=="trending").values})
            rows.append(d.iloc[np.arange(0,len(b),10)])
    g=pd.concat(rows).dropna(subset=["fwd"])
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    T=g[g.trend].dropna(subset=["rp","past10","past20","z10"])
    X=np.column_stack([np.ones(len(T)),T["rp"],T["past10"]]); y=T["ex"].values
    beta,res,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-3))
    out["joint_rp_past10_trend"]=pd.Series({"b_rp":beta[1],"t_rp":beta[1]/np.sqrt(cov[1,1]),
        "b_p10":beta[2],"t_p10":beta[2]/np.sqrt(cov[2,2]),"n":len(y)})
    pc=[]
    for c,s in T.groupby("coin"):
        for x in ["past10","past20","z10"]:
            r=stats.linregress(s[x],s["ex"]); pc.append([c,x,r.slope/r.stderr,len(s)])
    out["percoin_trend_t"]=pd.DataFrame(pc,columns=["coin","x","t","n"]).pivot(index="coin",columns="x",values="t")
    out["pooled_trend_t"]=pd.Series({x:(lambda r:r.slope/r.stderr)(stats.linregress(T[x],T["ex"])) for x in ["past10","past20","z10"]})
    # daily reversal after down days
    dd=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True); cl=b["close"].astype(float); r=cl.pct_change()
            vol=r.rolling(30,min_periods=20).std().shift(1)
            dd.append(pd.DataFrame({"coin":c,"w":w,"r":r,"z":r/vol,"next":r.shift(-1),
                "next3":cl.shift(-3)/cl-1,"trend":(b["regime"]=="trending").values,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,"pos":np.arange(len(b))}))
    D=pd.concat(dd).dropna(subset=["z","next"])
    D["nx"]=D["next"]-D.groupby("coin")["next"].transform("mean")
    D["zq"]=pd.qcut(D["z"],10,labels=False)
    out["next_by_zdecile"]=D.groupby("zq")["nx"].agg(["mean","count","std"])
    pr=[]
    for c,s in D.groupby("coin"):
        lo=s[s.z<s.z.quantile(0.1)]["nx"]; mid=s[(s.z>=s.z.quantile(0.1))]["nx"]
        dn=s[s.z<0]; r=stats.linregress(dn["z"],dn["nx"])
        pr.append([c,lo.mean(),stats.ttest_ind(lo,mid,equal_var=False).statistic,r.slope,r.slope/r.stderr,len(lo)])
    out["percoin_reversal"]=pd.DataFrame(pr,columns=["coin","mean_lowdec","welch_t","slope_neg_z","t_slope","n_low"])
    out["low_dec_by_regime"]=D[D.zq==0].groupby("trend")["nx"].agg(["mean","count"])
    # 3-day after down, non-overlapping grid of 3
    G3=D[D.pos%3==0].dropna(subset=["next3"]).copy()
    G3["n3"]=G3["next3"]-G3.groupby("coin")["next3"].transform("mean")
    G3["zq"]=pd.qcut(G3["z"],5,labels=False)
    out["next3_by_zquint"]=G3.groupby("zq")["n3"].agg(["mean","count"])
    # weekday per coin: saturday minus rest
    D["sat"]=D.wd==5
    wk=[]
    for c,s in D.groupby("coin"):
        a=s[s.sat]["next"]; b_=s[~s.sat]["next"]  # next is return of following day
    for c,s in D.groupby("coin"):
        a=s[s.wd==4]["next"]; b_=s[s.wd!=4]["next"]
        wk.append([c,a.mean(),b_.mean(),stats.ttest_ind(a,b_,equal_var=False).statistic])
    out["sat_return_percoin"]=pd.DataFrame(wk,columns=["coin","sat","other","t"])
    # by year of reversal
    D["yr"]=pd.concat([pd.to_datetime(b["timestamp"]).dt.year for ws in data["bars"].values() for b in ws.values()]).values[:0].tolist() or 0
    return out
