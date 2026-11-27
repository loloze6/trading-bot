def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].astype(float)
            r1=cl.pct_change()
            nxt=cl.shift(-1)/cl-1
            hi=cl.rolling(20,min_periods=20).max()
            sd=r1.rolling(20,min_periods=20).std()
            depth=(cl/hi-1)/sd
            tr60=cl/cl.shift(60)-1
            r5=cl/cl.shift(5)-1
            r20=cl/cl.shift(20)-1
            alloc=b["postRebalance_current_allocation"].astype(float)
            df=pd.DataFrame({"coin":c,"w":w,"pos":np.arange(len(b)),"r1":r1,"nxt":nxt,"depth":depth,
                             "tr60":tr60,"r5":r5,"r20":r20,"alloc":alloc,"fc":b["forecast"].astype(float),
                             "gain":alloc*nxt,"year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    drift=d.groupby("coin")["nxt"].mean()
    d["ex"]=d["nxt"]-d["coin"].map(drift)
    d["sx"]=-d["ex"]
    up=d[(d.r1>0)&d.depth.notna()&d.nxt.notna()].copy()
    dn=d[(d.r1<=0)&d.depth.notna()&d.nxt.notna()].copy()
    def stat(g):
        x=g["sx"]; return pd.Series({"n":len(x),"mean_short_ex":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"mean_short_total":(-g["nxt"]).mean()})
    up["dq"]=pd.qcut(up.depth,5,labels=["q1deep","q2","q3","q4","q5shallow"])
    dn["dq"]=pd.qcut(dn.depth,5,labels=["q1deep","q2","q3","q4","q5shallow"])
    up["trend"]=pd.cut(up.tr60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    dn["trend"]=pd.cut(dn.tr60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    up["r1q"]=pd.qcut(up.r1,4,labels=["small","m1","m2","big"])
    deep=up[up.dq=="q1deep"]
    out={}
    out["up_by_depth"]=up.groupby("dq").apply(stat)
    out["down_by_depth"]=dn.groupby("dq").apply(stat)
    out["up_deep_by_trend"]=deep.groupby("trend").apply(stat)
    out["down_deep_by_trend"]=dn[dn.dq=="q1deep"].groupby("trend").apply(stat)
    out["up_all_by_trend"]=up.groupby("trend").apply(stat)
    out["up_deep_by_r1size"]=deep.groupby("r1q").apply(stat)
    out["up_by_r1size_all"]=up.groupby("r1q").apply(stat)
    out["deep_by_year"]=deep.groupby("year").apply(stat)
    out["deep_by_coin"]=deep.groupby("coin").apply(stat)
    # book: gain per trade by depth vs cost; book by window
    dd=data["days"]
    br=[]
    for c,ws in dd.items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=c; x["w"]=w; br.append(x)
    br=pd.concat(br)
    daily=br.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book_by_window"]=daily.groupby("w").agg(book_mean=("book_return","mean"),book_sd=("book_return","std"),hold_mean=("coin_return","mean"),n=("book_return","count"))
    # deepest falls: chain book within windows in order
    daily=daily.sort_values(["w","day"])
    v=(1+daily.book_return.fillna(0)).cumprod().values
    peak=np.maximum.accumulate(v); ddn=v/peak-1
    daily["dd"]=ddn
    out["max_dd"]=float(ddn.min())
    out["dd_by_window_min"]=daily.groupby("w")["dd"].min()
    # gain per position bar by depth and alloc size
    act=d[(d.alloc.abs()>0)&d.nxt.notna()].copy()
    act["aq"]=pd.qcut(act.alloc.abs(),5,labels=False,duplicates="drop")
    out["gain_by_alloc_q"]=act.groupby("aq").agg(n=("gain","count"),mean_gain=("gain","mean"),mean_abs_alloc=("alloc",lambda s:s.abs().mean()),mean_depth=("depth","mean"))
    # holding persistence: is position held on non-up days?
    out["alloc_nonzero_on_down_days_share"]=float(((d.r1<=0)&(d.alloc.abs()>0)).sum()/max(1,(d.alloc.abs()>0).sum()))
    out["trades_summary"]=pd.Series({"n":sum(len(t) for ws in data["trades"].values() for t in ws.values())})
    return out
