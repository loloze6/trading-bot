def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            s20=r.rolling(20).std()
            d=pd.DataFrame({"coin":c,"win":w,"r":r,"z":r/s20,
                "clv":(cl-b["low"])/(b["high"]-b["low"]),
                "volr":b["volume"]/b["volume"].rolling(20).mean(),
                "fwd1":cl.shift(-1)/cl-1,"fwd3":cl.shift(-3)/cl-1,
                "fc":b["forecast"],
                "yr":pd.to_datetime(b["timestamp"]).dt.year,"pos":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows)
    D["x1"]=D["fwd1"]-D.groupby("coin")["fwd1"].transform("mean")
    D["x3"]=D["fwd3"]-D.groupby("coin")["fwd3"].transform("mean")
    D["lv"]=np.log(D.volr)
    def summ(g,col="x1"):
        v=g[col].dropna()
        return pd.Series({"n":len(v),"mean%":100*v.mean(),"t":v.mean()/v.std()*np.sqrt(len(v)) if len(v)>2 else np.nan})
    out={}
    def ols(df,y,xs):
        df=df[[y]+xs].replace([np.inf,-np.inf],np.nan).dropna()
        X=np.column_stack([np.ones(len(df))]+[df[x].values for x in xs]); Y=df[y].values
        b,res,_,_=np.linalg.lstsq(X,Y,rcond=None); e=Y-X@b
        s2=e@e/(len(Y)-X.shape[1]); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        return pd.DataFrame({"coef":b,"t":b/se},index=["const"]+xs).assign(n=len(Y))
    F=D[D.r<0].copy()
    F["low_close"]=1-F.clv
    F["lc_x_lv"]=F.low_close*F.lv
    F["fall"]=-F.z
    out["falls: x1 ~ fall + lowclose + lv + lc*lv"]=ols(F,"x1",["fall","low_close","lv","lc_x_lv"])
    D["low_close"]=1-D.clv; D["lc_x_lv"]=D.low_close*D.lv
    out["all days: x1 ~ z + lowclose + lv + lc*lv"]=ols(D,"x1",["z","low_close","lv","lc_x_lv"])
    # graded score on all days: low close weighted by volume
    D["score"]=D.low_close*D.volr
    D["sq"]=pd.qcut(D.score,5,labels=False)
    out["all days by score quintile (x1)"]=D.groupby("sq").apply(summ)
    # non-overlapping 3 day
    D3=D[D.pos%3==0]
    out["all days by score quintile (x3, nonoverlap)"]=D3.groupby("sq").apply(summ,col="x3")
    top=D[D.sq==4]
    out["top score quintile by coin"]=top.groupby("coin").apply(summ)
    out["top score quintile by year"]=top.groupby("yr").apply(summ)
    out["top score, up days only"]=top[top.r>0].pipe(lambda g: summ(g))
    out["top score, forecast==0 (idea silent)"]=top[top.fc<=0].pipe(lambda g: summ(g))
    out["top score, forecast>0"]=top[top.fc>0].pipe(lambda g: summ(g))
    # idea's forecast residual: among fc>0, low close split
    P=D[D.fc>0].copy(); P["fq"]=pd.qcut(P.fc,3,labels=False); P["lq"]=pd.qcut(P.low_close,2,labels=["hi_close","lo_close"])
    out["fc>0: forecast tercile x close half"]=P.groupby(["fq","lq"]).apply(summ)
    return out
