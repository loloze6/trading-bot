def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            if len(b)<30: continue
            c=b["close"].astype(float)
            raw=b["debug_info.components.sma_cross_down.last_history_value"].astype(float)
            bv=b["postRebalance_total_value"].astype(float)
            df=pd.DataFrame({"coin":coin,"w":w,"f":b["forecast"].astype(float),"raw":raw,
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "r1":c.pct_change(),"fwd1":c.shift(-1)/c-1,"fwd10":c.shift(-10)/c-1,
                "dRaw10":raw-raw.shift(10),"book_fwd1":bv.shift(-1)/bv-1,
                "past30":c/c.shift(30)-1})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    out={}
    def agg(g,col="fwd10"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(max(len(x),1)/10) if len(x)>2 else np.nan,"up":(x>0).mean()})
    # book decomposition
    d["implied"]=d["alloc"]*d["fwd1"]
    s=d[d.f<0]
    out["book vs alloc*coin, short bars"]=pd.Series({"book_mean":s.book_fwd1.mean(),"implied_mean":s.implied.mean(),"corr":s[["book_fwd1","implied"]].corr().iloc[0,1],"book_std":s.book_fwd1.std(),"implied_std":s.implied.std(),"coin_fwd1_mean":s.fwd1.mean(),"alloc_mean":s.alloc.mean()}).round(5)
    out["book_fwd1 quantiles short"]=s.book_fwd1.quantile([0,0.001,0.01,0.05,0.5,0.95,0.99,0.999,1]).round(4)
    out["alloc quantiles"]=d.alloc.quantile([0,0.01,0.05,0.5,0.95,0.99,1]).round(3)
    # spread direction while short
    s=s.copy()
    s["dir"]=np.where(s.dRaw10>0,"spread rising","spread falling")
    out["fwd10 short by spread direction"]=s.groupby("dir").apply(agg).round(4)
    out["fwd10 short by past30 sign"]=s.groupby(s.past30>0).apply(agg).round(4)
    # flat bars by raw spread near zero vs positive, direction
    fl=d[d.f>=0].copy()
    fl["dir"]=np.where(fl.dRaw10>0,"rising","falling")
    fl["rb"]=pd.cut(fl.raw,[-1e9,0,50,150,1e9])
    out["fwd10 flat by raw bin x dir"]=fl.groupby(["rb","dir"]).apply(agg).round(4)
    # per-window: short-state fwd10 mean vs window coin trend
    g=d.groupby(["coin","w"]).agg(sh=("f",lambda x:(x<0).mean()),bk=("book_fwd1","sum"),cn=("fwd1","sum"))
    g["trend"]=np.where(g.cn>0,"up window","down window")
    out["book sum by window trend"]=g.groupby("trend").agg(n=("bk","size"),book=("bk","mean"),coin=("cn","mean"),short_share=("sh","mean")).round(4)
    # around biggest book losses
    d["bkz"]=d.book_fwd1
    q=d.bkz.quantile(0.01); q2=d.bkz.quantile(0.99)
    out["coin fwd1 & past30 on worst/best 1% book days"]=pd.DataFrame({"worst":d[d.bkz<=q][["fwd1","past30","alloc","f"]].mean(),"best":d[d.bkz>=q2][["fwd1","past30","alloc","f"]].mean()}).round(4)
    # trades: entry forecast and exit
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr,ignore_index=True)
    T["px"]=-(T.exit_price/T.entry_price-1)*100
    out["trade px move vs pl"]=T[["px","profit_loss_percent","net_profit_loss_percent","total_commission"]].describe().round(3)
    T["ef"]=pd.cut(T.entry_forecast,[-21,-10,-5,-2,0])
    out["trades by entry forecast"]=T.groupby("ef")[["px","net_profit_loss_percent"]].agg(["count","mean"]).round(3)
    return out
