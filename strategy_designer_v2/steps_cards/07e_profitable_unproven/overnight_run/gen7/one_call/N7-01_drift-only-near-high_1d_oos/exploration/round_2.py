def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            b=data["bars"][c][w].copy()
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            b["vol20"]=np.log(b["close"]).diff().rolling(20).std()
            b["sma20"]=b["close"].rolling(20).mean()
            b["dist"]=b["close"]/b["sma20"]-1
            b["hi20"]=b["close"].rolling(20).max()
            b["isnewhi"]=(b["close"]>=b["hi20"]).astype(float)
            b["bsh"]=b["debug_info.components.recency.last_history_value"] if "debug_info.components.recency.last_history_value" in b else np.nan
            b["nh"]=b["debug_info.components.near_high.last_history_value"] if "debug_info.components.near_high.last_history_value" in b else np.nan
            al=b.groupby("day").agg(alloc=("postRebalance_current_allocation","last"),fc=("forecast","last"),
                ret20=("ret20","last"),vol20=("vol20","last"),dist=("dist","last"),bsh=("bsh","last"),nh=("nh","last"),newhi=("isnewhi","last"))
            dd=d.copy(); dd["day"]=pd.to_datetime(dd["day"]).dt.floor("D")
            dd=dd.merge(al,left_on="day",right_index=True,how="left")
            for k in ["alloc","fc","ret20","vol20","dist","bsh","nh","newhi"]:
                dd[k+"_p"]=dd[k].shift(1)
            dd["coin"]=c; dd["w"]=w; rows.append(dd)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["book_return"])
    D["ex"]=D.coin_return-D.groupby("coin").coin_return.transform("mean")
    D["inm"]=D["alloc_p"].fillna(0).abs()>1e-6
    out={}
    out["alloc in-market"]=D[D.inm].alloc_p.describe()
    I=D[D.inm].copy()
    def agg(g): return pd.Series({"n":len(g),"ex":g.ex.mean(),"t":g.ex.mean()/g.ex.std()*np.sqrt(len(g)),"book":g.book_return.mean()})
    I["bshb"]=pd.cut(I.bsh_p,[-1,5,10,15,20.5])
    out["in: by recency raw (20=fresh)"]=I.groupby("bshb").apply(agg)
    I["nhb"]=pd.qcut(I.nh_p.rank(method="first"),4,labels=False)
    out["in: by near_high raw quartile"]=I.groupby("nhb").apply(agg)
    out["in: newhi yesterday"]=I.groupby("newhi_p").apply(agg)
    I["r20b"]=pd.qcut(I.ret20_p.rank(method="first"),4,labels=False)
    out["in: by trailing 20d ret quartile"]=I.groupby("r20b").apply(lambda g: pd.concat([agg(g),pd.Series({"r20":g.ret20_p.mean()})]))
    I["vb"]=pd.qcut(I.vol20_p.rank(method="first"),3,labels=False)
    out["in: by vol tercile"]=I.groupby("vb").apply(agg)
    # market breadth: share of coins above SMA20 yesterday
    D["above"]=(D.dist_p>0).astype(float)
    br=D.groupby("day").above.mean().rename("breadth")
    I=I.merge(br,left_on="day",right_index=True)
    I["bb"]=pd.cut(I.breadth,[-0.01,0.34,0.67,1.01])
    out["in: by breadth"]=I.groupby("bb").apply(agg)
    # all days above SMA20 (not just gate) vs below
    D["ab"]=D.dist_p>0
    out["all: above vs below sma20"]=D.dropna(subset=["dist_p"]).groupby("ab").apply(agg)
    # out-of-market but above sma20 (gate off due to no recent high)
    O=D[(~D.inm)&(D.dist_p>0)]; out["out but above sma"]=agg(O)
    # book concentration
    bk=D.groupby("day").book_return.mean().sort_values(ascending=False)
    out["book conc"]=pd.Series({"sum":bk.sum(),"top10":bk.head(10).sum(),"top30":bk.head(30).sum(),"sum_ex_top10":bk.iloc[10:].sum(),"mean_ex_top10":bk.iloc[10:].mean()})
    out["in: by window excess"]=I.groupby("w").apply(agg)
    return out
