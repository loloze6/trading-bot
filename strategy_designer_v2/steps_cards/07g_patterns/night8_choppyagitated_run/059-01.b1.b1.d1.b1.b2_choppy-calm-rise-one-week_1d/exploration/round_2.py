def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        fr=[]
        for w,b in ws.items():
            c=b["close"].values
            for i in range(0,len(c)-7,7):
                fr.append(c[i+7]/c[i]-1)
        dr=np.mean(fr)
        tmp=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            r1=c.pct_change()
            r7=c/c.shift(7)-1
            df=pd.DataFrame({"s":r7/r7.abs().rolling(30).mean(),"tr60":c/c.shift(60)-1,
                             "vol30":r1.rolling(30).std(),"fwd":c.shift(-7)/c-1,
                             "ret1":r1,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                             "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                             "yr":pd.to_datetime(b["timestamp"]).dt.year})
            df["grid"]=(np.arange(len(df))%7==0); df["w"]=w; df["coin"]=coin
            tmp.append(df)
        d=pd.concat(tmp)
        d["calm"]=d["vol30"]<=d["vol30"].median()
        d["ex"]=d["fwd"]-dr
        rows.append(d)
    A=pd.concat(rows)
    G=A[A["grid"]&A["fwd"].notna()&A["s"].notna()&A["tr60"].notna()].copy()
    def clus(g,x="s",y="ex"):
        g=g.dropna(subset=[x,y])
        if len(g)<10: return {"n":len(g),"days":0,"slope%":np.nan,"t_cl":np.nan}
        X=np.column_stack([np.ones(len(g)),g[x].values]); Y=g[y].values
        XtX=np.linalg.inv(X.T@X); b=XtX@X.T@Y; e=Y-X@b
        meat=np.zeros((2,2))
        for _,idx in g.reset_index(drop=True).groupby("day").groups.items():
            s=(X[idx]*e[idx][:,None]).sum(0); meat+=np.outer(s,s)
        V=XtX@meat@XtX
        return {"n":len(g),"days":g["day"].nunique(),"slope%":b[1]*100,"t_cl":b[1]/np.sqrt(V[1,1])}
    out={}
    FC=G[(G["tr60"]<-0.1)&G["calm"]]
    out["falling calm slope clustered"]=pd.DataFrame({"all":clus(FC),"s>0":clus(FC[FC.s>0]),"s<0":clus(FC[FC.s<0])}).T
    out["falling calm by year"]=pd.DataFrame({str(y):clus(g) for y,g in FC.groupby("yr")}).T
    out["falling calm by coin"]=pd.DataFrame({c:clus(g) for c,g in FC.groupby("coin")}).T
    FC2=FC.copy(); FC2["side"]=np.sign(FC2["s"])
    out["falling calm mean ex by sign of s"]=FC2.groupby("side")["ex"].agg(["count","mean"]).assign(mean=lambda x:x["mean"]*100)
    # signed ex in direction of s
    FC2["dirx"]=FC2["ex"]*FC2["side"]
    dm=FC2.groupby("day")["dirx"].sum()
    out["falling calm directional ex"]=pd.Series({"mean%":FC2["dirx"].mean()*100,"t_day":dm.mean()/(dm.std()/np.sqrt(len(dm)))*np.sqrt(1)*(len(dm)/len(FC2))*(len(FC2)/len(dm)),"days":len(dm)})
    FA=G[(G["tr60"]<-0.1)&~G["calm"]]
    out["falling agit slope clustered"]=pd.DataFrame({"all":clus(FA)}).T
    # trend only falling
    out["falling (any) slope"]=pd.DataFrame({"all":clus(G[G["tr60"]<-0.1])}).T
    # weekday with day clustering: mean across coins per day
    dd=A.dropna(subset=["ret1"]).groupby(["day","wd"])["ret1"].mean().reset_index()
    out["weekday day-mean"]=dd.groupby("wd")["ret1"].agg(lambda x: x.mean()*100).to_frame("mean%").join(
        dd.groupby("wd")["ret1"].agg(lambda x: x.mean()/(x.std()/np.sqrt(len(x)))).to_frame("t")).join(dd.groupby("wd").size().to_frame("days"))
    dd["yr"]=pd.to_datetime(dd["day"]).dt.year
    out["fri+sat mean% by year"]=dd[dd.wd.isin([4,5])].groupby("yr")["ret1"].mean()*100
    out["other days mean% by year"]=dd[~dd.wd.isin([4,5])].groupby("yr")["ret1"].mean()*100
    return out
