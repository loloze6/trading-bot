def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]
            b["fwd7"]=c.shift(-7)/c-1
            b["past7"]=c/c.shift(7)-1
            b["past30"]=c/c.shift(30)-1
            r=c.pct_change()
            b["vol20"]=r.rolling(20).std()
            b["vr"]=b["volume"]/b["volume"].rolling(20).mean()
            b["dh"]=b.get("debug_info.components.dist_high.last_history_value")
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["r1"]=r.shift(-1)
            b["coin"]=coin; b["win"]=w; b["pos"]=np.arange(len(b))
            rows.append(b[["coin","win","pos","fwd7","past7","past30","vol20","vr","dh","forecast","regime","wd","r1","postRebalance_current_allocation"]])
    A=pd.concat(rows)
    cm=A[A.pos%7==0].groupby("coin")["fwd7"].mean()
    A["ex7"]=A["fwd7"]-A["coin"].map(cm)
    G=A[(A.pos%7==0)].dropna(subset=["ex7"])
    def tab(df,col,q=5):
        d=df.dropna(subset=[col]).copy()
        d["q"]=d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        g=d.groupby("q")["ex7"].agg(["mean","count","std"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        return g.drop(columns="std")
    def slope(df,col):
        d=df.dropna(subset=[col,"ex7"])
        x=d.groupby("coin")[col].transform(lambda s:(s-s.mean())/s.std())
        res=stats.linregress(x,d["ex7"]); return pd.Series({"slope":res.slope,"t":res.slope/res.stderr,"n":len(d)})
    out={}
    out["past7 quint all"]=tab(G,"past7")
    out["past30 quint all"]=tab(G,"past30")
    out["vol20 quint"]=tab(G,"vol20")
    out["volratio quint"]=tab(G,"vr")
    out["dh quint (active)"]=tab(G,"dh")
    out["slopes"]=pd.DataFrame({k:slope(G,k) for k in ["past7","past30","vol20","vr","dh"]}).T
    out["slopes falling30"]=pd.DataFrame({k:slope(G[G.past30<0],k) for k in ["past7","vol20","vr"]}).T
    out["slopes rising30"]=pd.DataFrame({k:slope(G[G.past30>0],k) for k in ["past7","vol20","vr"]}).T
    wd=A.dropna(subset=["r1"]).groupby("wd")["r1"].agg(["mean","count","std"])
    wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["next-day ret by weekday of signal bar"]=wd.drop(columns="std")
    # book
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D=pd.concat(D)
    D["yr"]=pd.to_datetime(D["day"]).dt.year
    by=D.groupby("yr")[["book_return","coin_return"]].mean()
    out["book by year"]=by
    out["book by coin"]=D.groupby("coin")[["book_return","coin_return"]].agg(["mean"])
    return out
