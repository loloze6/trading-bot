def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    drift={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H):
                allr.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(allr)
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; rng=(b["high"]-b["low"])/c
            r1=c.pct_change()
            f=pd.DataFrame({
              "ret28":c/c.shift(28)-1,
              "dd28":c/c.rolling(28).max()-1,
              "dd14":c/c.rolling(14).max()-1,
              "up28":c/c.rolling(28).min()-1,
              "rng28_rel":rng.rolling(28).mean()/rng.rolling(90,min_periods=40).mean(),
              "rng5_rel":rng.rolling(5).mean()/rng.rolling(90,min_periods=40).mean(),
              "vol20":r1.rolling(20).std(),
              "ret1":r1,
              "year":pd.to_datetime(b["timestamp"]).dt.year})
            f["fwd"]=c.shift(-H)/c-1-drift[coin]
            f["coin"]=coin; f["w"]=w
            f=f.iloc[list(range(0,len(b)-H,H))]
            rows.append(f)
    d=pd.concat(rows)
    out={}
    up=d[d.ret28>=0]
    for ft in ["dd28","rng28_rel","dd14","rng5_rel","vol20"]:
        s=up[[ft,"fwd"]].dropna().copy()
        s["q"]=pd.qcut(s[ft],5,labels=False)
        g=s.groupby("q")["fwd"].agg(["mean","std","count"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        out["up28_quint_"+ft]=g.round(4)
    def tstat(s,ft):
        s=s[[ft,"fwd"]].dropna()
        if len(s)<15: return np.nan,len(s)
        sl=stats.linregress(s[ft],s["fwd"]); return round(sl.slope/sl.stderr,2),len(s)
    res=[]
    for key in ["coin","w","year"]:
        for k,g in up.groupby(key):
            a,n=tstat(g,"dd28"); b2,_=tstat(g,"rng28_rel")
            res.append([key,k,n,a,b2])
    out["up28_split_t"]=pd.DataFrame(res,columns=["by","k","n","t_dd28","t_rng28"])
    # joint
    s=up[["dd28","rng28_rel","fwd"]].dropna()
    X=np.column_stack([np.ones(len(s)),(s.dd28-s.dd28.mean())/s.dd28.std(),(s.rng28_rel-s.rng28_rel.mean())/s.rng28_rel.std()])
    beta,res_,_,_=np.linalg.lstsq(X,s.fwd.values,rcond=None)
    e=s.fwd.values-X@beta; sig=e.var(ddof=3); cov=sig*np.linalg.inv(X.T@X)
    out["joint_up28"]=pd.DataFrame({"beta":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","dd28","rng28"]).round(4)
    # all bars dd28 grading, down set too
    for nm,sub in [("all",d),("down",d[d.ret28<0])]:
        s=sub[["dd28","fwd"]].dropna().copy()
        s["q"]=pd.qcut(s.dd28,5,labels=False)
        g=s.groupby("q")["fwd"].agg(["mean","count"]); out["dd28_quint_"+nm]=g.round(4)
    return out
