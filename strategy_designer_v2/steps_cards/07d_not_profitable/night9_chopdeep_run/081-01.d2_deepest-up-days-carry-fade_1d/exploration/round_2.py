def explore(data):
    import numpy as np, pandas as pd
    out={}
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
            vol30=r1.rolling(30,min_periods=20).std()
            volrank=vol30.rolling(120,min_periods=60).apply(lambda s:(s<=s[-1]).mean(),raw=True)
            r5=cl/cl.shift(5)-1
            alloc=b["postRebalance_current_allocation"].astype(float)
            df=pd.DataFrame({"coin":c,"w":w,"r1":r1,"r1sw":r1/sd,"nxt":nxt,"depth":depth,"tr60":tr60,"volrank":volrank,
                             "r5":r5,"alloc":alloc,"gain":alloc*nxt,"year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    drift=d.groupby("coin")["nxt"].mean()
    d["ex"]=d["nxt"]-d["coin"].map(drift)
    d["sx"]=-d["ex"]
    d["tn"]=-d["nxt"]
    def q(s,k,labels):
        return pd.qcut(s.rank(method="first"),k,labels=labels)
    def stat(g):
        x=g["sx"].dropna(); n=len(x)
        return pd.Series({"n":n,"short_ex":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,"short_total":g["tn"].mean()})
    base=d[d.depth.notna()&d.nxt.notna()].copy()
    base["trend"]=pd.cut(base.tr60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    base["agit"]=np.where(base.volrank>0.5,"agitated","calm")
    base.loc[base.volrank.isna(),"agit"]=np.nan
    up=base[base.r1>0].copy(); dn=base[base.r1<=0].copy()
    up["dq"]=q(up.depth,5,["q1deep","q2","q3","q4","q5shallow"])
    dn["dq"]=q(dn.depth,5,["q1deep","q2","q3","q4","q5shallow"])
    deep=up[up.dq=="q1deep"].copy()
    deep["r1q"]=q(deep.r1sw,3,["small","mid","big"])
    try: out["up_by_depth"]=up.groupby("dq").apply(stat)
    except Exception as e: out["e1"]=str(e)
    try: out["down_by_depth"]=dn.groupby("dq").apply(stat)
    except Exception as e: out["e2"]=str(e)
    try: out["deep_up_by_trend_agit"]=deep.groupby(["trend","agit"]).apply(stat)
    except Exception as e: out["e3"]=str(e)
    try: out["all_up_by_trend_agit"]=up.groupby(["trend","agit"]).apply(stat)
    except Exception as e: out["e3b"]=str(e)
    try: out["deep_down_by_trend"]=dn[dn.dq=="q1deep"].groupby("trend").apply(stat)
    except Exception as e: out["e4"]=str(e)
    try: out["deep_up_by_r1size_swings"]=deep.groupby("r1q").apply(stat)
    except Exception as e: out["e5"]=str(e)
    try: out["deep_up_by_year"]=deep.groupby("year").apply(stat)
    except Exception as e: out["e6"]=str(e)
    try: out["deep_up_by_coin"]=deep.groupby("coin").apply(stat)
    except Exception as e: out["e7"]=str(e)
    # book: position bars, gain by alloc quintile and by depth quintile
    try:
        act=base[(base.alloc.abs()>0)].copy()
        act["aq"]=q(act.alloc.abs(),5,[1,2,3,4,5])
        out["book_gain_by_alloc_q"]=act.groupby("aq").agg(n=("gain","count"),mean_gain=("gain","mean"),abs_alloc=("alloc",lambda s:s.abs().mean()),depth=("depth","mean"),up_share=("r1",lambda s:(s>0).mean()))
        out["book_gain_by_trend"]=act.groupby("trend").agg(n=("gain","count"),mean_gain=("gain","mean"),abs_alloc=("alloc",lambda s:s.abs().mean()))
        out["share_pos_bars_on_down_days"]=float((act.r1<=0).mean())
        out["mean_gain_pos_on_down_days"]=float(act[act.r1<=0].gain.mean())
        out["mean_gain_pos_on_up_days"]=float(act[act.r1>0].gain.mean())
    except Exception as e: out["e8"]=str(e)
    # daily book and drawdowns
    try:
        br=[]
        for c,ws in data["days"].items():
            for w,x in ws.items():
                x=x.copy(); x["coin"]=c; x["w"]=w; br.append(x)
        br=pd.concat(br)
        daily=br.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
        daily["wn"]=daily.w.str[1:].astype(int)
        daily=daily.sort_values(["wn","day"]).reset_index(drop=True)
        out["book_by_window"]=daily.groupby("wn").agg(book_mean=("book_return","mean"),book_sd=("book_return","std"),hold_mean=("coin_return","mean"),n=("book_return","count"),corr_hold=("book_return",lambda s:s.corr(daily.loc[s.index,"coin_return"])))
        v=(1+daily.book_return.fillna(0)).cumprod().values
        peak=np.maximum.accumulate(v); ddn=v/peak-1
        daily["dd"]=ddn
        out["max_dd"]=float(ddn.min())
        i=int(np.argmin(ddn)); p=int(np.argmax(v[:i+1]))
        seg=daily.iloc[p:i+1]
        out["deepest_fall"]=pd.Series({"days":i-p,"windows":seg.w.nunique(),"book_chain":float(v[i]/v[p]-1),"hold_chain":float((1+seg.coin_return.fillna(0)).prod()-1),"hold_mean_daily":seg.coin_return.mean()})
        out["dd_min_by_window"]=daily.groupby("wn")["dd"].min()
        daily["hq"]=q(daily.coin_return.fillna(0),5,[1,2,3,4,5])
        out["book_by_hold_day_quintile"]=daily.groupby("hq").agg(book=("book_return","mean"),hold=("coin_return","mean"))
    except Exception as e: out["e9"]=str(e)
    return out
