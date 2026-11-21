def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; hrows=[]; book=[]; mv=[]
    for coin, wins in data["bars"].items():
        g_sum=0; f_sum=0; n_act=0
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].astype(float).values
            n=len(c)
            r1 = pd.Series(c).pct_change().values
            fwd1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            fwd2 = np.r_[c[2:]/c[:-2]-1, np.nan, np.nan]
            r72 = pd.Series(c).pct_change(72)
            z = (r72/ r72.rolling(73,min_periods=20).std()).values
            sd24 = pd.Series(r1).rolling(24).std().values
            hr = ts.dt.hour.values; wd = ts.dt.weekday.values
            df = pd.DataFrame({"coin":coin,"w":w,"hour":hr,"wd":wd,"fwd2":fwd2,"fwd1":fwd1,"z":z,
                               "r1":r1,"sd24":sd24,"vol":b["volume"].astype(float).values,
                               "r24":pd.Series(c).pct_change(24).values})
            rows.append(df)
            a = b["postRebalance_current_allocation"].astype(float).fillna(0).values
            gross = a*np.nan_to_num(fwd1)
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"]).astype(float)/b["total_portfolio_value"].astype(float)
            g_sum += gross.sum(); f_sum += fee.fillna(0).sum(); n_act += (a!=0).sum()
        book.append({"coin":coin,"gross_sum":g_sum,"fee_sum":f_sum,"active_bars":n_act})
    D = pd.concat(rows, ignore_index=True)
    out["book_gross_vs_fee"] = pd.DataFrame(book)
    # trend-following signed 2h excess by hour (bar stamped hour h -> cases closing h+1)
    D["m2"] = D.groupby("coin")["fwd2"].transform("mean")
    D["s"] = np.clip(D["z"],-2,2)*(D["fwd2"]-D["m2"])
    res=[]
    for h,g in D.dropna(subset=["s"]).groupby("hour"):
        x=g["s"]; res.append({"hour":h,"n":len(x),"mean_bp":x.mean()*1e4,"t":x.mean()/x.std()*np.sqrt(len(x))})
    out["trend_signed_2h_by_hour"]=pd.DataFrame(res)
    # raw 1h return by hour (fwd1 from bar stamped h-> bar h+1 return)
    res=[]
    for h,g in D.dropna(subset=["r1"]).groupby("hour"):
        x=g["r1"]; res.append({"hour":h,"mean_bp":x.mean()*1e4,"t":x.mean()/x.std()*np.sqrt(len(x)),
              "absmean_bp":x.abs().mean()*1e4,"rel_vol":g["vol"].mean()})
    R=pd.DataFrame(res); R["rel_vol"]=R["rel_vol"]/R["rel_vol"].mean()
    out["ret1h_by_bar_hour"]=R
    res=[]
    for d,g in D.dropna(subset=["r1"]).groupby("wd"):
        x=g["r1"]; res.append({"wd":d,"mean_bp":x.mean()*1e4,"t":x.mean()/x.std()*np.sqrt(len(x))})
    out["ret1h_by_weekday"]=pd.DataFrame(res)
    # reversal after large 1h moves: z of r1 by sd24, next 1h
    E=D.dropna(subset=["r1","sd24","fwd1"]).copy()
    E["zr"]=E["r1"]/E["sd24"]
    E["bin"]=pd.cut(E["zr"],[-np.inf,-3,-2,-1,0,1,2,3,np.inf])
    out["next1h_after_1h_move"]=E.groupby("bin",observed=True)["fwd1"].agg(n="count",mean_bp=lambda x:x.mean()*1e4,
            t=lambda x:x.mean()/x.std()*np.sqrt(len(x)))
    # 24h move -> next 24h, non-overlapping grid every 24
    F=[]
    for (c_,w_),g in D.groupby(["coin","w"]):
        g=g.reset_index(drop=True).iloc[::24]
        g=g.assign(f24=g["r24"].shift(-1))
        F.append(g)
    F=pd.concat(F).dropna(subset=["r24","f24"])
    F["q"]=F.groupby("coin")["r24"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["next24h_by_24h_quintile"]=F.groupby("q")["f24"].agg(n="count",mean_bp=lambda x:x.mean()*1e4,
            t=lambda x:x.mean()/x.std()*np.sqrt(len(x)))
    return out
