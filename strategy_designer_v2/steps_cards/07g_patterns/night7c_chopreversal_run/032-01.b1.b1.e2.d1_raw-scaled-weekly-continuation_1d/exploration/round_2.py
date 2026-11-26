def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            r7=c/c.shift(7)-1
            sd30=r.rolling(30).std()
            er=(c-c.shift(30)).abs()/(c.diff().abs().rolling(30).sum())
            s=r7/(sd30*np.sqrt(7))
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"day":ts.dt.floor("D"),"yr":ts.dt.year,
                            "r":r,"z":r/sd30,"s":s,"er":er,"sd30":sd30,
                            "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,"f7":c.shift(-7)/c-1,
                            "vr":sd30.rolling(180,min_periods=60).rank(pct=True),
                            "alloc":b["postRebalance_current_allocation"].astype(float)})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def ct(df,col):
        x=df.dropna(subset=[col]).groupby("day")[col].mean()
        n=len(x); return pd.Series({"cases":df[col].notna().sum(),"days":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    # daily: next-day after big down days, day clustered, excess over coin mean daily return
    m1=D.groupby("coin")["f1"].transform("mean")
    D["ex1"]=D["f1"]-m1
    D["zb"]=pd.cut(D["z"],[-50,-2,-1,0,1,2,50])
    out["next1d_ex_by_z_dayclust"]=D.groupby("zb").apply(lambda g: ct(g,"ex1"))
    # non-overlapping 3-day after down day
    G3=D[D.pos%3==0].copy(); G3["ex3"]=G3["f3"]-G3.groupby("coin")["f3"].transform("mean")
    out["next3d_ex_by_z_grid_dayclust"]=G3.groupby("zb").apply(lambda g: ct(g,"ex3"))
    big=D[D.z<=-1]
    out["down_z_le_-1_by_coin"]=big.groupby("coin").apply(lambda g: ct(g,"ex1"))
    out["down_z_le_-1_by_year"]=big.groupby("yr").apply(lambda g: ct(g,"ex1"))
    D["vrb"]=pd.cut(D["vr"],[0,0.33,0.66,1.01])
    out["down_z_le_-1_by_volrank"]=D[D.z<=-1].groupby("vrb").apply(lambda g: ct(g,"ex1"))
    D["erb"]=pd.cut(D["er"],[0,0.3,1.01])
    out["down_z_le_-1_by_er"]=D[D.z<=-1].groupby("erb").apply(lambda g: ct(g,"ex1"))
    # weekly continuation in chop by vol rank, grid and day clustered
    G=D[D.pos%7==0].dropna(subset=["s","er","f7"]).copy()
    G["dir_ex"]=np.sign(G["s"])*(G["f7"]-G["f7"].mean())
    out["chop_cont_by_volrank_dayclust"]=G[G.er<=0.3].groupby("vrb").apply(lambda g: ct(g,"dir_ex"))
    out["trend_cont_by_volrank_dayclust"]=G[G.er>0.3].groupby("vrb").apply(lambda g: ct(g,"dir_ex"))
    out["chop_cont_by_er_dayclust"]=G.groupby(pd.cut(G.er,[0,0.15,0.3,0.5,1.01])).apply(lambda g: ct(g,"dir_ex"))
    # weekday, day clustered (one value per day = coin mean)
    D["wd"]=D["day"].dt.weekday
    out["next1d_by_weekday_dayclust"]=D.groupby("wd").apply(lambda g: ct(g,"ex1"))
    # book's biggest days: what preceded
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; dd.append(x)
    DD=pd.concat(dd,ignore_index=True)
    DD["day"]=pd.to_datetime(DD["day"])
    M=DD.merge(D[["coin","day","z","alloc","er","vr"]].drop_duplicates(["coin","day"]),on=["coin","day"],how="left")
    M["prev_z"]=M.groupby("coin")["z"].shift(1)
    q=M["book_return"].quantile([0.02,0.98])
    M["grp"]=np.where(M.book_return<=q.iloc[0],"worst2%",np.where(M.book_return>=q.iloc[1],"best2%","rest"))
    out["book_extremes_context"]=M.groupby("grp").agg(n=("book_return","size"),mean_ret=("book_return","mean"),
        long_share=("alloc",lambda a:(a>0).mean()),coin_ret=("coin_return","mean"),prev_z=("prev_z","mean"),er=("er","mean"),vr=("vr","mean"))
    M["side"]=np.sign(M["alloc"])
    out["book_by_side"]=M.groupby("side")["book_return"].agg(["size","mean"])
    return out
