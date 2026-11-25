def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            s=r.rolling(30,min_periods=20).std()
            z=r/s
            tr=c/c.shift(60)-1
            f1=c.shift(-1)/c-1
            f2=c.shift(-2)/c-1
            f3=c.shift(-3)/c-1
            d2=c.shift(-2)/c.shift(-1)-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"r":r,"z":z,"tr":tr,
                "calm":(b["regime"]!="chop"),"f1":f1,"f2":f2,"f3":f3,"d2":d2,
                "vol":s,"wd":ts.dt.weekday,"year":ts.dt.year,
                "alloc":b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    # drift removal: coin mean over all windows on grid
    out={}
    for h,col in [(1,"f1"),(2,"f2"),(3,"f3")]:
        g=A[A.pos%h==0]
        A[col+"x"]=A[col]-A["coin"].map(g.groupby("coin")[col].mean())
    A["d2x"]=A["d2"]-A["coin"].map(A.groupby("coin")["f1"].mean())
    A["zb"]=pd.cut(A["z"],[-np.inf,-2,-1,-0.3,0.3,1,2,np.inf])
    G2=A[A.pos%2==0].dropna(subset=["z","f2x"])
    G1=A.dropna(subset=["z","f1x"])
    def tab(G,col):
        return G.groupby(["calm","zb"],observed=True)[col].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))]).rename(columns={"<lambda_0>":"t"})
    out["f2x_by_calm_z"]=tab(G2,"f2x")
    out["f1x_by_calm_z"]=tab(G1[G1.pos%1==0],"f1x")
    out["d2x_by_calm_z"]=tab(G1,"d2x")
    G3=A[A.pos%3==0].dropna(subset=["z","f3x"])
    out["f3x_by_calm_z"]=tab(G3,"f3x")
    # trend profile
    A["trd"]=pd.cut(A["tr"],[-np.inf,-0.1,0.1,np.inf],labels=["fall","chop","rise"])
    G2=A[A.pos%2==0].dropna(subset=["z","f2x","trd"])
    out["f2x_by_trend_calm_zsign"]=G2.groupby(["trd","calm",G2.z>0],observed=True)["f2x"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    # slope of f2x on z per trend x calm
    res={}
    for k,g in G2.groupby(["trd","calm"],observed=True):
        sl=stats.linregress(g["z"],g["f2x"]); res[str(k)]=[sl.slope,sl.slope/sl.stderr,len(g)]
    out["slope_f2x_on_z"]=pd.DataFrame(res,index=["slope","t","n"]).T
    G1=A.dropna(subset=["f1x"])
    out["f1x_by_weekday"]=G1.groupby("wd")["f1x"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    A["volq"]=A.groupby("coin")["vol"].transform(lambda x:pd.qcut(x,4,labels=False,duplicates="drop"))
    out["f2x_by_volq_zsign"]=G2.assign(volq=A.loc[G2.index,"volq"]).groupby(["volq",G2.z>0])["f2x"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["f2x_by_year_calm_up"]=G2[(G2.calm)&(G2.z>0)].groupby("year")["f2x"].agg(["mean","count"])
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D)
    out["book_by_window"]=D.groupby("w")[["book_return","coin_return"]].mean()
    return out
