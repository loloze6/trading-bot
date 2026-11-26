def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
              "ret60":c/c.shift(60)-1,
              "vr":np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean()),
              "vr15":np.log(v.rolling(15).mean()/v.shift(15).rolling(15).mean()),
              "ret5p":c/c.shift(5)-1,"ret10p":c/c.shift(10)-1,"ret20p":c/c.shift(20)-1,
              "vol30":r1.rolling(30).std(),
              "fwd5":c.shift(-5)/c-1,"fwd1":c.shift(-1)/c-1,
              "day":ts.dt.floor("D"),"wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["trend"]=np.where(A.ret60>0.1,"rising",np.where(A.ret60<-0.1,"falling","choppy"))
    A.loc[A.ret60.isna(),"trend"]="na"
    med=A.groupby("coin").vol30.transform("median")
    A["agit"]=np.where(A.vol30>med,"agit","calm")
    G=A[(A.pos%5==0)&A.fwd5.notna()].copy()
    drift=G.groupby("coin").fwd5.mean(); G["ex"]=G.fwd5-G.coin.map(drift)
    sd=G.groupby("coin").fwd5.std(); G["z"]=G.ex/G.coin.map(sd)
    # standardise features per coin
    for x in ["vr","vr15","ret5p","ret10p","ret20p"]:
        G[x+"_s"]=(G[x]-G.groupby("coin")[x].transform("mean"))/G.groupby("coin")[x].transform("std")
    def cl(df,x):
        d=df[[x,"z","day"]].dropna()
        if len(d)<30: return (len(d),np.nan,np.nan,np.nan)
        X=np.c_[np.ones(len(d)),d[x].values]; y=d.z.values
        beta=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@beta
        XtXi=np.linalg.inv(X.T@X)
        S=pd.DataFrame(X*e[:,None]).groupby(d.day.values).sum().values
        V=XtXi@(S.T@S)@XtXi
        return (len(d),d.day.nunique(),beta[1],beta[1]/np.sqrt(V[1,1]))
    res=[]
    for tr in ["rising","choppy","falling"]:
        for ag in ["all","agit","calm"]:
            sub=G[G.trend==tr] if ag=="all" else G[(G.trend==tr)&(G.agit==ag)]
            for x in ["vr_s","vr15_s","ret5p_s","ret10p_s","ret20p_s"]:
                res.append((tr,ag,x)+cl(sub,x))
    out={"clustered":pd.DataFrame(res,columns=["trend","agit","feat","n","days","slope","t"])}
    # by year stability for key ones
    yy=[]
    for (tr,x) in [("rising","vr_s"),("falling","vr_s"),("choppy","ret5p_s"),("choppy","ret20p_s")]:
        for y in sorted(G.yr.unique()):
            sub=G[(G.trend==tr)&(G.yr==y)]
            yy.append((tr,x,y)+cl(sub,x))
    out["by_year"]=pd.DataFrame(yy,columns=["trend","feat","yr","n","days","slope","t"])
    # falling vr quintiles
    for tr in ["falling","rising"]:
        d=G[G.trend==tr][["vr","z","ex"]].dropna().copy(); d["q"]=pd.qcut(d.vr,4,labels=False)
        out["q4_vr_"+tr]=d.groupby("q").agg(n=("z","size"),vr=("vr","mean"),ex=("ex","mean"),t=("z",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    d=G[G.trend=="choppy"][["ret5p","z","ex"]].dropna().copy(); d["q"]=pd.qcut(d.ret5p,4,labels=False)
    out["q4_ret5p_choppy"]=d.groupby("q").agg(n=("z","size"),r=("ret5p","mean"),ex=("ex","mean"),t=("z",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    # weekday by trend and by coin count positive
    A["fwd1d"]=A.fwd1-A.groupby("coin").fwd1.transform("mean")
    out["wd_trend"]=A.pivot_table(index="wd",columns="trend",values="fwd1d",aggfunc="mean")
    out["thufri_by_year"]=A[A.wd.isin([3,4])].groupby("yr").fwd1d.agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    return out
