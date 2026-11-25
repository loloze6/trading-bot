def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            r7=c/c.shift(7)-1
            sd30=r.rolling(30).std()
            er=(c-c.shift(30)).abs()/(c.diff().abs().rolling(30).sum())
            s=r7/(sd30*np.sqrt(7))
            f7=c.shift(-7)/c-1
            f1=c.shift(-1)/c-1
            vol_rank=sd30.rolling(180,min_periods=60).rank(pct=True)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"r":r,"s":s,"er":er,"f7":f7,"f1":f1,
                            "sd30":sd30,"vr":vol_rank,"wd":ts.dt.weekday,"yr":ts.dt.year,
                            "fc":b["forecast"].astype(float),"alloc":b["postRebalance_current_allocation"].astype(float)})
            rows.append(d)
    D=pd.concat(rows)
    drift7=D.loc[D.pos%7==0,"f7"].mean()
    G=D[(D.pos%7==0)].dropna(subset=["s","er","f7"]).copy()
    G["ex"]=G["f7"]-drift7
    G["dir_ex"]=np.sign(G["s"])*G["ex"]
    G["erb"]=pd.cut(G["er"],[0,0.15,0.3,0.5,1.01])
    G["sb"]=pd.cut(G["s"].abs(),[0,0.5,1,1.5,2,10])
    def tt(x): 
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["dirmove_by_ER"]=G.groupby("erb")["dir_ex"].apply(tt).unstack()
    out["dirmove_by_absS"]=G.groupby("sb")["dir_ex"].apply(tt).unstack()
    out["dirmove_ERlow_by_absS"]=G[G.er<=0.3].groupby("sb")["dir_ex"].apply(tt).unstack()
    out["dirmove_ERhigh_by_absS"]=G[G.er>0.3].groupby("sb")["dir_ex"].apply(tt).unstack()
    G["sign"]=np.sign(G["s"])
    out["dirmove_by_sign_ERlow"]=G[G.er<=0.3].groupby("sign")["dir_ex"].apply(tt).unstack()
    G["vrb"]=pd.cut(G["vr"],[0,0.33,0.66,1.01])
    out["dirmove_by_volrank"]=G.groupby("vrb")["dir_ex"].apply(tt).unstack()
    out["fwd7_ex_by_volrank"]=G.groupby("vrb")["ex"].apply(tt).unstack()
    out["dirmove_by_coin"]=G.groupby("coin")["dir_ex"].apply(tt).unstack()
    out["dirmove_by_year"]=G.groupby("yr")["dir_ex"].apply(tt).unstack()
    # daily: next day after large daily move (z)
    D["z"]=D["r"]/D["sd30"]
    D1=D.dropna(subset=["z","f1"]).copy()
    D1["zb"]=pd.cut(D1["z"],[-50,-2,-1,0,1,2,50])
    out["next1d_by_dailyz"]=D1.groupby("zb")["f1"].apply(tt).unstack()
    out["ret_by_weekday"]=D1.groupby("wd")["f1"].apply(tt).unstack()
    # book: days, gain by weekday, best/worst
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    DD=pd.concat(dd)
    DD["wd"]=pd.to_datetime(DD["day"]).dt.weekday
    out["book_by_weekday"]=DD.groupby("wd")["book_return"].apply(tt).unstack()
    out["book_by_window"]=DD.groupby("w")["book_return"].apply(tt).unstack()
    out["book_by_coin"]=DD.groupby("coin")["book_return"].apply(tt).unstack()
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    T["absf"]=pd.cut(T["entry_forecast"].abs(),[0,0.5,1,1.5,2,20])
    out["trades_by_side"]=T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades_by_absforecast"]=T.groupby("absf")["net_profit_loss_percent"].agg(["count","mean"])
    out["trade_duration_days"]=T["duration_minutes"].describe()/1440
    return out
