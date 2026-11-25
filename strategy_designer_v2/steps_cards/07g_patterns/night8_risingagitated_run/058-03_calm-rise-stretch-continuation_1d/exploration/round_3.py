def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); n=len(b); r1=c.pct_change()
            sma=c.rolling(20,min_periods=20).mean()
            rngv=(b["high"]-b["low"]).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),"ts":pd.to_datetime(b["timestamp"]),
               "dist":c/sma-1,"ret1":r1,"tr30":c/c.shift(30)-1,"tr60":c/c.shift(60)-1,
               "vol30":r1.rolling(30,min_periods=30).std(),"vol10":r1.rolling(10,min_periods=10).std(),
               "fwd1":c.shift(-1)/c-1,"fwd2":c.shift(-2)/c-1,"fwd3":c.shift(-3)/c-1,
               "clpos":(c-b["low"])/rngv,"rng":rngv/c})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True); D["day"]=D["ts"].dt.floor("D"); D["year"]=D.ts.dt.year
    D["tg"]=np.where(D.tr30>0.10,"rising",np.where(D.tr30<-0.10,"falling","choppy"))
    D["ag"]=np.where(D.vol10>D.groupby("coin")["vol10"].transform("median"),"agit","calm")
    D["tg60"]=np.where(D.tr60.isna(),"na",np.where(D.tr60>0.10,"rising",np.where(D.tr60<-0.10,"falling","choppy")))
    D["ag30"]=np.where(D.vol30.isna(),"na",np.where(D.vol30>D.groupby("coin")["vol30"].transform("median"),"agit","calm"))
    D["clc"]=D.clpos-0.5
    def slope(df,x,y):
        df=df.dropna(subset=[x,y])
        if len(df)<30: return pd.Series({"n":len(df),"days":df.day.nunique(),"slope":np.nan,"t":np.nan})
        X=df[x]-df[x].mean(); Y=df[y]-df[y].mean()
        b=(X*Y).sum()/(X*X).sum(); e=Y-b*X
        sc=(X*e).groupby(df["day"]).sum(); se=np.sqrt((sc**2).sum())/(X*X).sum()
        return pd.Series({"n":len(df),"days":df.day.nunique(),"slope":b,"t":b/se})
    out={}
    for h in [1,2,3]:
        g=D[D.pos%h==0].copy(); m=g.groupby("coin")[f"fwd{h}"].mean(); g["ex"]=g[f"fwd{h}"]-g["coin"].map(m)
        g["upcl"]=g.clc*g.rng
        out[f"h{h}_clpos_slope_prof30"]=g.groupby(["tg","ag"]).apply(lambda d: slope(d,"clc","ex"))
        out[f"h{h}_clpos_slope_prof60"]=g[g.tg60!="na"].groupby(["tg60","ag30"]).apply(lambda d: slope(d,"clc","ex"))
        if h==2:
            ca=g[(g.tg=="choppy")&(g.ag=="agit")]
            out["h2_choppyagit_clpos_by_year"]=ca.groupby("year").apply(lambda d: slope(d,"clc","ex"))
            out["h2_choppyagit_clpos_by_coin"]=ca.groupby("coin").apply(lambda d: slope(d,"clc","ex"))
            out["h2_choppyagit_upcl_slope"]=slope(ca,"upcl","ex")
            fc=g[(g.tg=="falling")&(g.ag=="calm")&(g.dist>0)]
            out["h2_fallcalm_dist_by_year"]=fc.groupby("year").apply(lambda d: slope(d,"dist","ex"))
            out["h2_fallcalm_dist_by_coin"]=fc.groupby("coin").apply(lambda d: slope(d,"dist","ex"))
        if h==1:
            fc=g[(g.tg60=="falling")&(g.ag30=="calm")&(g.dist>0)]
            out["h1_fallcalm60_dist"]=slope(fc,"dist","ex")
    return out
