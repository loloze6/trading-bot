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
            alloc=b["postRebalance_current_allocation"].astype(float)
            prev=b["previous_allocation"].astype(float)
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            df=pd.DataFrame({"coin":c,"w":w,"day":day,"r1":r1,"nxt":nxt,"depth":depth,"tr60":tr60,"volrank":volrank,
                             "alloc":alloc,"turn":(alloc-prev).abs(),"gain":alloc*nxt})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    drift=d.groupby("coin")["nxt"].mean()
    d["sx"]=-(d["nxt"]-d["coin"].map(drift))
    base=d[d.depth.notna()&d.nxt.notna()].copy()
    base["trend"]=pd.cut(base.tr60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    base["agit"]=np.where(base.volrank>0.5,"agitated","calm")
    base["deep"]=np.where(base.depth<=base[base.r1>0].depth.quantile(0.4),"deep","shallow")
    base["upd"]=np.where(base.r1>0,"up","down")
    def stat(g):
        x=g["sx"]; n=len(x)
        return pd.Series({"n":n,"short_ex":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,"short_total":(-g.nxt).mean()})
    out["by_trend_agit_updown_deep"]=base.groupby(["trend","agit","upd","deep"]).apply(stat)
    # book variants: net gain per bar = gain - cost*turn ; aggregate per day mean over coins (incl zeros)
    cost=0.0011
    base["net"]=base.gain-cost*base.turn
    def book(mask,name):
        g=base.copy(); g.loc[~mask,"net"]=0.0
        dly=g.groupby(["w","day"])["net"].mean().reset_index()
        dly["wn"]=dly.w.str[1:].astype(int); dly=dly.sort_values(["wn","day"])
        r=dly.net.values; v=np.cumprod(1+r); dd=(v/np.maximum.accumulate(v)-1).min()
        yr=v[-1]**(365/len(r))-1
        return pd.Series({"sharpe":r.mean()/r.std()*np.sqrt(365),"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"pos_share":float((g.loc[mask,"alloc"].abs()>0).sum()/len(g))})
    res={}
    res["as_is"]=book(pd.Series(True,index=base.index),"a")
    res["not_rising"]=book(base.trend!="rising","b")
    res["falling_only"]=book(base.trend=="falling","c")
    res["agitated_only"]=book(base.agit=="agitated","d")
    res["falling_agit"]=book((base.trend=="falling")&(base.agit=="agitated"),"e")
    res["deep_only"]=book(base.deep=="deep","f")
    res["falling_deep"]=book((base.trend=="falling")&(base.deep=="deep"),"g")
    res["notrising_deep"]=book((base.trend!="rising")&(base.deep=="deep"),"h")
    out["book_variants"]=pd.DataFrame(res).T
    hold=base.groupby(["w","day"])["nxt"].mean()
    out["hold_sharpe"]=float(hold.mean()/hold.std()*np.sqrt(365))
    return out
