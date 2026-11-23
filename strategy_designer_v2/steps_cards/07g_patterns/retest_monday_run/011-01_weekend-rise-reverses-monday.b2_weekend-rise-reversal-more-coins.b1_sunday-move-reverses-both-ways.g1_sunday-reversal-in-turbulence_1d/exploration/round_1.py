def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float); r=cl.pct_change()
            d=pd.DataFrame({"coin":c,"win":w,"wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "year":pd.to_datetime(b["timestamp"]).dt.year,"r1":r,
                "vol20":r.rolling(20).std(),"vol60":r.rolling(60).std(),
                "vrel":b["volume"]/b["volume"].rolling(20).mean(),
                "r5":cl/cl.shift(5)-1,
                "f1":cl.shift(-1)/cl-1,"f2":cl.shift(-2)/cl-1,"f2b":cl.shift(-2)/cl.shift(-1)-1,
                "f5":cl.shift(-5)/cl-1})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["r1","vol20","vol60","f2"])
    drift=D.groupby("coin")["f2"].transform("mean")
    D["u2"]=D["f2"]-drift
    D["z"]=D["r1"]/D["vol20"]; D["ratio"]=D["vol20"]/D["vol60"]
    def reg(g,y="u2",x="z"):
        g=g.dropna(subset=[x,y])
        if len(g)<30: return pd.Series({"n":len(g)})
        s=stats.linregress(g[x],g[y]/g["vol20"])
        return pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    out={}
    out["by_weekday_u2_on_z"]=D.groupby("wd").apply(reg)
    out["by_weekday_f1_on_z"]=D.groupby("wd").apply(lambda g:reg(g,"f1"))
    out["by_weekday_day2_on_z"]=D.groupby("wd").apply(lambda g:reg(g,"f2b"))
    out["by_weekday_f5_on_z"]=D.groupby("wd").apply(lambda g:reg(g,"f5"))
    S=D[D.wd==6].copy()
    S["ratio_q"]=pd.qcut(S["ratio"],4,labels=False)
    out["sun_by_ratio_q"]=S.groupby("ratio_q").apply(reg)
    S["vrel_q"]=pd.qcut(S["vrel"],4,labels=False)
    out["sun_by_volrel_q"]=S.groupby("vrel_q").apply(reg)
    S["volq"]=pd.qcut(S["vol60"],4,labels=False)
    out["sun_by_vol60_q"]=S.groupby("volq").apply(reg)
    out["sun_by_year"]=S.groupby("year").apply(reg)
    out["sun_by_r5"]=S.groupby(pd.qcut(S["r5"],4,labels=False)).apply(lambda g:reg(g))
    out["sat_by_volrel_q"]=D[D.wd==5].groupby(pd.qcut(D[D.wd==5]["vrel"],4,labels=False)).apply(reg)
    # weekend (sat+sun) 2-day move vs next 2 days
    # book
    B=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            B.append(d.assign(coin=c,win=w))
    B=pd.concat(B); B["day"]=pd.to_datetime(B["day"])
    bk=B.groupby("day").agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
    bk["year"]=bk.index.year; bk["wd"]=bk.index.weekday
    out["book_by_year"]=bk.groupby("year").agg(mean=("br","mean"),sd=("br","std"),n=("br","size"),coin=("cr","mean"))
    out["book_by_wd"]=bk.groupby("wd")["br"].agg(["mean","std","size"])
    T=[]
    for c,ws in data["trades"].items():
        for w,t in ws.items(): T.append(t.assign(coin=c))
    T=pd.concat(T)
    out["trades_by_side"]=T.groupby("side")["net_profit_loss_percent"].agg(["mean","median","count"])
    out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["mean","count"])
    return out
