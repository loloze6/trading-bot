def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            ts=pd.to_datetime(b["timestamp"])
            vr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
              "ret60":c/c.shift(60)-1,"vr":vr,
              "vrz60":(vr-vr.rolling(60,min_periods=20).mean())/vr.rolling(60,min_periods=20).std(),
              "fc":b["forecast"].astype(float),
              "ret5p":c/c.shift(5)-1,"vol30":r1.rolling(30).std(),
              "fwd5":c.shift(-5)/c-1,"fwd1":c.shift(-1)/c-1,
              "day":ts.dt.floor("D"),"wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["trend"]=np.where(A.ret60>0.1,"rising",np.where(A.ret60<-0.1,"falling","choppy"))
    A.loc[A.ret60.isna(),"trend"]="na"
    A["agit"]=np.where(A.vol30>A.groupby("coin").vol30.transform("median"),"agit","calm")
    G=A[(A.pos%5==0)&A.fwd5.notna()].copy()
    drift=G.groupby("coin").fwd5.mean(); G["ex"]=G.fwd5-G.coin.map(drift)
    sd=G.groupby("coin").fwd5.std(); G["z"]=G.ex/G.coin.map(sd)
    G["vr_s"]=(G.vr-G.groupby("coin").vr.transform("mean"))/G.groupby("coin").vr.transform("std")
    def cl(df,x,y="z"):
        d=df[[x,y,"day"]].dropna()
        if len(d)<30: return (len(d),np.nan,np.nan,np.nan)
        X=np.c_[np.ones(len(d)),d[x].values]; yy=d[y].values
        beta=np.linalg.lstsq(X,yy,rcond=None)[0]; e=yy-X@beta
        XtXi=np.linalg.inv(X.T@X)
        S=pd.DataFrame(X*e[:,None]).groupby(d.day.values).sum().values
        V=XtXi@(S.T@S)@XtXi
        return (len(d),d.day.nunique(),beta[1],beta[1]/np.sqrt(V[1,1]))
    R=G[G.trend=="rising"]
    res=[]
    for x in ["vr_s","vrz60","fc"]:
        res.append(("rising",x)+cl(R,x))
    res.append(("rising_corr_vr_vrz60",str(round(R[["vr","vrz60"]].corr().iloc[0,1],3)),0,0,0,0))
    out={"rising_measures":pd.DataFrame(res,columns=["set","feat","n","days","slope","t"])}
    cc=[]
    for coin in sorted(G.coin.unique()):
        cc.append(("rising_vr",coin)+cl(R[R.coin==coin],"vr_s"))
        cc.append(("choppycalm_ret5p",coin)+cl(G[(G.trend=="choppy")&(G.agit=="calm")&(G.coin==coin)],"ret5p"))
    out["by_coin"]=pd.DataFrame(cc,columns=["set","coin","n","days","slope","t"])
    # Thursday/Friday next-day return, demeaned, by trend x agit, by coin, clustered by day
    A["fwd1d"]=A.fwd1-A.groupby("coin").fwd1.transform("mean")
    A["tf"]=A.wd.isin([3,4]).astype(float)
    tt=[]
    for tr in ["rising","choppy","falling","na"]:
        for ag in ["agit","calm"]:
            sub=A[(A.trend==tr)&(A.agit==ag)]
            tt.append((tr,ag)+cl(sub,"tf","fwd1d"))
    out["thufri_minus_rest_profile"]=pd.DataFrame(tt,columns=["trend","agit","n","days","diff","t"])
    out["thufri_by_coin"]=pd.DataFrame([(c,)+cl(A[A.coin==c],"tf","fwd1d") for c in sorted(A.coin.unique())],
        columns=["coin","n","days","diff","t"])
    # daily-level: market mean across coins thursday+friday by window
    out["thufri_by_window"]=A.groupby("w").apply(lambda s: pd.Series(cl(s,"tf","fwd1d"),index=["n","days","diff","t"]))
    return out
