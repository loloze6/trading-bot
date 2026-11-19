def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[]; hr=[]; bk=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            ar=r1.abs()
            past=c/c.shift(H)-1
            er=(c-c.shift(H)).abs()/(c.diff().abs().rolling(H).sum())
            maxshare=ar.rolling(H).max()/ar.rolling(H).sum()
            vshare=v.rolling(H).max()/v.rolling(H).sum()
            vol=r1.rolling(H).std()
            vol30=r1.rolling(720).std()
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"past":past,"er":er,"ms":maxshare,"vs":vshare,
                             "volr":vol/vol30,"fwd":fwd,"fc":b["forecast"],
                             "alloc":b["postRebalance_current_allocation"]})
            g=df.iloc[::H]
            rows.append(g)
            nx=c.shift(-1)/c-1
            hr.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour,"wd":ts.dt.weekday,"r":nx,
                                    "pos":b["postRebalance_current_allocation"],"prev_r":r1,"vz":r1/vol30}))
    G=pd.concat(rows).dropna(subset=["fwd","past"])
    G["ex"]=G["fwd"]-G.groupby("coin")["fwd"].transform("mean")
    out={}
    out["n_grid"]=len(G)
    def tq(df,col,q=5):
        d=df.dropna(subset=[col]).copy()
        d["q"]=d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),q,labels=False))
        a=d.groupby("q")["ex"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a
    out["ex by past72 ret quintile"]=tq(G,"past")
    out["ex by ER quintile (all)"]=tq(G,"er")
    up=G[G.past>0]; dn=G[G.past<0]
    out["ex by ER quintile (up)"]=tq(up,"er")
    out["ex by ER quintile (down)"]=tq(dn,"er")
    out["ex by maxhour share (up)"]=tq(up,"ms")
    out["ex by maxhour share (down)"]=tq(dn,"ms")
    out["ex by vol ratio quintile"]=tq(G,"volr")
    out["ex by volume burst share"]=tq(G,"vs")
    H1=pd.concat(hr).dropna()
    a=H1.groupby("hour")["r"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["next-hour ret by hour"]=a
    a=H1.groupby("wd")["r"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["next-hour ret by weekday"]=a
    H1["zb"]=pd.cut(H1["vz"],[-99,-4,-2,-1,1,2,4,99])
    a=H1.groupby("zb")["r"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["next-hour ret after hourly z move"]=a
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D)
    out["book by coin"]=D.groupby("coin")[["book_return","coin_return"]].mean()
    out["book by window"]=D.groupby("w")[["book_return","coin_return"]].mean()
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items(): tr.append(t.assign(coin=coin))
    T=pd.concat(tr)
    out["trades"]=T.groupby("coin")[["profit_loss_percent","net_profit_loss_percent","total_commission","duration_minutes"]].mean()
    out["trade count"]=T.groupby("coin").size()
    return out
