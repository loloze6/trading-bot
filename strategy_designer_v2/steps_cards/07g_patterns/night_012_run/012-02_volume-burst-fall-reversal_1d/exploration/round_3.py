def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(20,min_periods=20).std()
            vr=b["volume"]/b["volume"].rolling(30,min_periods=30).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"z":r/sd,"vr":vr,"sd":sd,
                            "yr":pd.to_datetime(b["timestamp"]).dt.year})
            d["m5"]=(c/c.shift(5)-1)/(sd*np.sqrt(5))
            d["vr5"]=b["volume"].rolling(5).mean()/b["volume"].rolling(30,min_periods=30).mean()
            for h in [1,2,3,5,7,14]:
                d[f"f{h}"]=c.shift(-h)/c-1
            rows.append(d)
    A=pd.concat(rows)
    def grid(h):
        G=[]
        for (coin,w),g in A.groupby(["coin","w"]):
            G.append(g.iloc[::h])
        G=pd.concat(G).dropna(subset=[f"f{h}"]).copy()
        G["ex"]=G[f"f{h}"]-G.groupby("coin")[f"f{h}"].transform("mean")
        return G
    def slope(g,col):
        g=g.dropna(subset=[col,"ex"]); x=g[col]; y=g["ex"]
        if len(g)<10: return pd.Series({"n":len(g),"b":np.nan,"t":np.nan})
        X=np.c_[np.ones(len(x)),x]; bb=np.linalg.lstsq(X,y,rcond=None)[0]
        e=y-X@bb; s2=(e**2).sum()/(len(y)-2); se=np.sqrt(s2*np.linalg.inv(X.T@X)[1,1])
        return pd.Series({"n":len(g),"b":bb[1],"t":bb[1]/se})
    out={}
    Gs={h:grid(h) for h in [1,2,3,5,7,14]}
    out["fall_vr_slope_by_h"]=pd.DataFrame({h:slope(Gs[h][Gs[h]["z"]<-1],"vr") for h in Gs}).T
    out["m5_slope_by_h"]=pd.DataFrame({h:slope(Gs[h],"m5") for h in Gs}).T
    G7=Gs[7]
    out["m5_7d_by_coin"]=G7.groupby("coin").apply(lambda g: slope(g,"m5"))
    out["m5_7d_by_year"]=G7.groupby("yr").apply(lambda g: slope(g,"m5"))
    G7["sdq"]=G7.groupby("coin")["sd"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["m5_7d_by_vol_tercile"]=G7.groupby("sdq").apply(lambda g: slope(g,"m5"))
    G7["vq"]=pd.qcut(G7["vr5"],3,labels=False)
    out["m5_7d_by_vr5_tercile"]=G7.groupby("vq").apply(lambda g: slope(g,"m5"))
    G7["m5x"]=G7["m5"]*G7["vr5"]
    out["m5xvr5_7d"]=slope(G7,"m5x").to_frame().T
    return out
