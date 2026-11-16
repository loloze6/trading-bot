def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    h=5
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            n=len(cl)
            r1=pd.Series(cl).pct_change()
            vol20=r1.rolling(20).std()
            ret5p=pd.Series(cl)/pd.Series(cl).shift(5)-1
            ret20p=pd.Series(cl)/pd.Series(cl).shift(20)-1
            hi20=pd.Series(cl).rolling(20).max(); lo20=pd.Series(cl).rolling(20).min()
            pos=(pd.Series(cl)-lo20)/(hi20-lo20)
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n-h,h):
                rows.append(dict(coin=c,win=w,fwd=cl[i+h]/cl[i]-1,fc=b["forecast"].iloc[i],
                    reg=b["regime"].iloc[i],r5=ret5p.iloc[i],r20=ret20p.iloc[i],vol=vol20.iloc[i],
                    pos=pos.iloc[i],wd=ts.iloc[i].weekday(),yr=ts.iloc[i].year,
                    alloc=b["postRebalance_current_allocation"].iloc[i]))
    g=pd.DataFrame(rows)
    g["dm"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    out={}
    def summ(df,key):
        a=df.groupby(key)["dm"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a
    out["by_regime"]=summ(g,"reg")
    t=g[g.reg=="trending"].copy()
    t["fcb"]=pd.cut(t["fc"],[-0.1,0.001,5,10,15,21])
    out["trend_fc_bucket"]=summ(t,"fcb")
    for nm,col in [("r5","r5"),("r20","r20"),("vol","vol"),("pos","pos")]:
        for rg in ["trending","unknown"]:
            s=g[g.reg==rg].dropna(subset=[col]).copy()
            s["q"]=s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
            out[f"{rg}_{nm}_quint"]=summ(s,"q")
    out["trend_by_year"]=summ(t[t.fc>0],"yr")
    out["trend_by_coin_fcpos"]=summ(t[t.fc>0],"coin")
    # unknown regime: slope of fwd on r20
    u=g[g.reg=="unknown"].dropna(subset=["r20"])
    lr=stats.linregress(u["r20"],u["dm"]); out["unknown_slope_r20"]=f"slope {lr.slope:.4f} t {lr.slope/lr.stderr:.2f} n {len(u)}"
    lr=stats.linregress(t.dropna(subset=["r20"])["r20"],t.dropna(subset=["r20"])["dm"]); out["trend_slope_r20"]=f"slope {lr.slope:.4f} t {lr.slope/lr.stderr:.2f}"
    # book daily
    d=[]
    for c,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd.copy(); x["coin"]=c; x["win"]=w; d.append(x)
    d=pd.concat(d); d["wd"]=pd.to_datetime(d["day"]).dt.weekday
    out["book_by_weekday"]=d.groupby("wd")[["book_return","coin_return"]].mean()
    out["book_by_coin"]=d.groupby("coin")[["book_return","coin_return"]].mean()
    # trades
    tr=pd.concat([df.assign(coin=c) for c,ws in data["trades"].items() for w,df in ws.items()])
    tr["days"]=tr["duration_minutes"]/1440
    tr["db"]=pd.cut(tr["days"],[0,1.5,3,7,15,1000])
    out["trades_by_dur"]=tr.groupby("db")["net_profit_loss_percent"].agg(["mean","count","sum"])
    return out
