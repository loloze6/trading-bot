def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].astype(float)
            allr.append((c.shift(-1)/c-1).dropna())
        dr=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r=c.pct_change(); sd=r.rolling(30,min_periods=20).std()
            width=(h-l)/c/sd; loc=(h-c)/(h-l)
            fc=b["forecast"].astype(float)
            for i in range(len(b)):
                if fc.iloc[i]>0:
                    d={"coin":coin,"w":w,"width":width.iloc[i],"loc":loc.iloc[i],
                       "day":pd.Timestamp(b["timestamp"].iloc[i]).normalize()}
                    for H in (1,2,3,5):
                        d[f"r{H}"]=(c.iloc[i+H]/c.iloc[i]-1-H*dr) if i+H<len(b) else np.nan
                    rows.append(d)
    df=pd.DataFrame(rows)
    def tday(x,day):
        s=pd.DataFrame({"x":x,"d":day}).dropna()
        m=s["x"].mean(); dev=(s["x"]-m).groupby(s["d"]).sum(); G=len(dev); n=len(s)
        se=np.sqrt((dev**2).sum()*G/(G-1))/n
        return m, m/se, G
    res={}
    out={}
    for H in (1,2,3,5):
        m,t,G=tday(df[f"r{H}"],df["day"]); out[H]=(m,t,G)
    res["dayclustered_by_H"]=pd.DataFrame(out,index=["mean","t","days"]).T
    df["lb"]=pd.cut(df["loc"],[0.5,0.6,0.7,0.8,0.9,1.01])
    g={}
    for k,s in df.groupby("lb"):
        m1,t1,G=tday(s["r1"],s["day"]); m3,t3,_=tday(s["r3"],s["day"])
        g[str(k)]=(m1,t1,m3,t3,G)
    res["by_loc5"]=pd.DataFrame(g,index=["m1","t1","m3","t3","days"]).T
    x=df[["loc","width","r1","r3"]].dropna()
    X=np.column_stack([np.ones(len(x)),x["loc"],x["width"]])
    res["ols_r1_loc_width"]=pd.Series(np.linalg.lstsq(X,x["r1"],rcond=None)[0],index=["c","loc","width"])
    res["ols_r3_loc_width"]=pd.Series(np.linalg.lstsq(X,x["r3"],rcond=None)[0],index=["c","loc","width"])
    df["wh"]=df["width"]>df["width"].median()
    df["lh"]=df["loc"]>0.75
    gg={}
    for (a,bb),s in df.groupby(["wh","lh"]):
        m1,t1,G=tday(s["r1"],s["day"]); gg[f"wide{a}_low{bb}"]=(m1,t1,G)
    res["width_x_loc"]=pd.DataFrame(gg,index=["m1","t1","days"]).T
    res["loc_share_gt09"]=float((df["loc"]>0.9).mean())
    return res
