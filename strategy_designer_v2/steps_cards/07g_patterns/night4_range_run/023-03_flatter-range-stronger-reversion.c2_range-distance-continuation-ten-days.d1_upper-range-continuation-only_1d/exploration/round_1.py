def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=10
    rows=[]
    drow=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            raw=b.get("debug_info.components.range_pos.last_history_value")
            raw=pd.to_numeric(raw,errors="coerce") if raw is not None else pd.Series(np.nan,index=b.index)
            lr=np.log(c).diff()
            vol20=lr.rolling(20).std()
            r10=c/c.shift(10)-1
            r30=c/c.shift(30)-1
            hi=c.rolling(30).max(); lo=c.rolling(30).min()
            width=(hi-lo)/c
            r1=c.pct_change()
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,len(b)-H,H):
                rows.append(dict(coin=coin,w=w,fwd=c[i+H]/c[i]-1,raw=raw[i],fc=b["forecast"][i],
                    vol=vol20[i],r10=r10[i],r1=r1[i],width=width[i],r30=r30[i],
                    alloc=b["postRebalance_current_allocation"][i]))
            for i in range(1,len(b)-1):
                drow.append(dict(coin=coin,wd=ts[i].dayofweek,r=c[i+1]/c[i]-1,r1=r1[i],vol=vol20[i],raw=raw[i]))
    g=pd.DataFrame(rows); d=pd.DataFrame(drow)
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    out={}
    def summ(df,col):
        s=df.groupby(col,observed=True)["ex"].agg(["count","mean","std"])
        s["t"]=s["mean"]/(s["std"]/np.sqrt(s["count"]))
        return s.round(4)
    gg=g.dropna(subset=["raw"]).copy()
    gg["rawq"]=pd.qcut(gg["raw"],6,duplicates="drop")
    out["raw range pos sextiles -> excess fwd10"]=summ(gg,"rawq")
    out["raw describe"]=gg["raw"].describe().round(3)
    h=g.dropna(subset=["r10"]).copy(); h["q"]=pd.qcut(h["r10"],5)
    out["past10d ret quintile -> excess fwd10"]=summ(h,"q")
    h=g.dropna(subset=["r1"]).copy(); h["q"]=pd.qcut(h["r1"],5)
    out["past1d ret quintile -> excess fwd10"]=summ(h,"q")
    h=g.dropna(subset=["vol"]).copy(); h["q"]=pd.qcut(h["vol"],3)
    out["vol20 tercile -> excess fwd10"]=summ(h,"q")
    h=g.dropna(subset=["width","raw"]).copy(); h["wq"]=pd.qcut(h["width"],2,labels=["narrow","wide"]); h["side"]=np.where(h["raw"]>0,"upper","lower")
    out["width x side"]=summ(h,["wq","side"])
    out["per coin forecast>0 vs 0"]=g.assign(on=g["fc"]>0).groupby(["coin","on"])["ex"].agg(["count","mean"]).round(4)
    d["dm"]=d["r"]-d.groupby("coin")["r"].transform("mean")
    s=d.groupby("wd")["dm"].agg(["count","mean","std"]); s["t"]=s["mean"]/(s["std"]/np.sqrt(s["count"]))
    out["weekday next-day excess"]=s.round(5)
    dd=d.dropna(subset=["r1"]).copy(); dd["q"]=pd.qcut(dd["r1"],5)
    s=dd.groupby("q",observed=True)["dm"].agg(["count","mean","std"]); s["t"]=s["mean"]/(s["std"]/np.sqrt(s["count"]))
    out["daily ret quintile -> next day excess"]=s.round(5)
    # book
    br=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; br.append(x)
    B=pd.concat(br)
    bk=B.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book vs hold daily"]=pd.DataFrame({"mean":bk.mean(),"std":bk.std(),"sharpe":bk.mean()/bk.std()*np.sqrt(365)}).round(5)
    bk["wn"]=bk.index.get_level_values(0)
    out["book by window"]=bk.groupby("wn")[["book_return","coin_return"]].sum().round(3)
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr)
    T["dur_d"]=T["duration_minutes"]/1440
    T["fq"]=pd.qcut(T["entry_forecast"],4,duplicates="drop")
    out["trades by entry forecast"]=T.groupby("fq",observed=True)["net_profit_loss_percent"].agg(["count","mean","median"]).round(3)
    out["trade duration"]=T["dur_d"].describe().round(2)
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","sum"]).round(2)
    return out
