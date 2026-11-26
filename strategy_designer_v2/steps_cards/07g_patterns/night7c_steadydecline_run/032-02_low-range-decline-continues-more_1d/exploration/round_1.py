def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H):
                allr.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(allr)
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; hi=b["high"]; lo=b["low"]; v=b["volume"]
            rng=(hi-lo)/c
            r1=c.pct_change()
            f=pd.DataFrame({
              "ret28":c/c.shift(28)-1,
              "ret14":c/c.shift(14)-1,
              "ret5p":c/c.shift(5)-1,
              "ret1":r1,
              "rng28_rel":rng.rolling(28).mean()/rng.rolling(90,min_periods=40).mean(),
              "vol20":r1.rolling(20).std(),
              "vol_rel":v.rolling(5).mean()/v.rolling(60,min_periods=30).mean(),
              "dd_from_max28":c/c.rolling(28).max()-1,
              "calm":b.get("debug_info.components.calm.last_history_value"),
              "fc":b["forecast"],
              "regime":b["regime"],
              "wd":pd.to_datetime(b["timestamp"]).dt.weekday})
            f["fwd"]=c.shift(-H)/c-1-drift[coin]
            f["fwd_raw"]=c.shift(-H)/c-1
            f["coin"]=coin; f["w"]=w
            f=f.iloc[list(range(0,len(b)-H,H))]
            rows.append(f)
    d=pd.concat(rows)
    out={}
    feats=["ret28","ret14","ret5p","ret1","rng28_rel","vol20","vol_rel","dd_from_max28","calm"]
    res=[]
    for sub,name in [(d,"all"),(d[d.ret28<0],"down28"),(d[d.ret28>=0],"up28")]:
        for ft in feats:
            s=sub[[ft,"fwd"]].dropna()
            if len(s)<30: continue
            r,p=stats.spearmanr(s[ft],s["fwd"])
            sl=stats.linregress(s[ft],s["fwd"])
            res.append([name,ft,len(s),round(r,3),round(sl.slope/sl.stderr,2)])
    out["feature_vs_fwd5"]=pd.DataFrame(res,columns=["set","feat","n","spearman","ols_t"])
    q=[]
    for ft in ["ret28","rng28_rel","vol20","ret5p"]:
        s=d[[ft,"fwd"]].dropna().copy()
        s["q"]=pd.qcut(s[ft],5,labels=False)
        g=s.groupby("q")["fwd"].agg(["mean","std","count"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["feat"]=ft
        q.append(g.reset_index())
    out["quintiles"]=pd.concat(q).round(4)
    dn=d[d.ret28<0][["ret28","rng28_rel","fwd"]].dropna().copy()
    dn["calmhalf"]=dn.rng28_rel<dn.rng28_rel.median()
    dn["deep"]=dn.ret28<dn.ret28.median()
    g=dn.groupby(["calmhalf","deep"])["fwd"].agg(["mean","std","count"])
    g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["down_calm_x_deep"]=g.round(4)
    # daily: weekday, by coin, window-level
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    g=D.groupby("wd")[["coin_return","book_return"]].agg(["mean","count"])
    out["weekday"]=g.round(5)
    g=D.groupby("coin")[["coin_return","book_return"]].mean()
    out["by_coin_mean"]=g.round(5)
    g=D.groupby("w")[["coin_return","book_return"]].mean()
    out["by_window_mean"]=g.round(5)
    # trades
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr)
    T["absf"]=T["entry_forecast"].abs()
    T["fq"]=pd.qcut(T["absf"],4,labels=False,duplicates="drop")
    out["trades_by_fc"]=T.groupby(["side","fq"])["net_profit_loss_percent"].agg(["mean","count"]).round(3)
    return out
