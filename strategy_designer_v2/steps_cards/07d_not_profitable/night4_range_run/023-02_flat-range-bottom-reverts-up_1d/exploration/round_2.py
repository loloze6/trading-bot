import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            hh=b.high.rolling(30).max(); ll=b.low.rolling(30).min()
            mid=(hh+ll)/2
            dist=b.close/mid-1
            nmr=(b.close-b.close.shift(30)).abs()/(hh-ll)
            r5p=b.close/b.close.shift(5)-1
            r3p=b.close/b.close.shift(3)-1
            r10p=b.close/b.close.shift(10)-1
            fwd=b.close.shift(-5)/b.close-1
            d=pd.DataFrame(dict(coin=c,win=w,dist=dist,nmr=nmr,r5p=r5p,r3p=r3p,r10p=r10p,fwd=fwd,
                                fc=b.forecast,alloc=b.postRebalance_current_allocation))
            rows.append(d.iloc[::5])
    D=pd.concat(rows).dropna(subset=["fwd","dist","nmr","r5p","r10p"])
    drift=D.groupby("coin").fwd.mean()
    D["ex"]=D.fwd-D.coin.map(drift)
    def agg(g):
        x=g.ex
        return pd.Series(dict(n=len(x),mean_ex=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))),mean_tot=g.fwd.mean()))
    out={}
    fb=D[(D.nmr<=0.3)&(D.dist<0)].copy()
    fb["r5q"]=pd.qcut(fb.r5p,5,labels=False)
    out["flat_below_r5_quint"]=fb.groupby("r5q").apply(agg)
    fb["r3q"]=pd.qcut(fb.r3p,3,labels=False)
    out["flat_below_r3_terc"]=fb.groupby("r3q").apply(agg)
    fb["r10q"]=pd.qcut(fb.r10p,3,labels=False)
    out["flat_below_r10_terc"]=fb.groupby("r10q").apply(agg)
    fb["dq"]=pd.qcut(fb.dist,2,labels=["deep","shallow"])
    fb["up"]=np.where(fb.r5p>0,"r5up","r5down")
    out["flat_below_dist_x_r5sign"]=fb.groupby(["up","dq"]).apply(agg)
    # all cases where r5p>0 vs dist (any regime) graded
    tr=D[(D.nmr>0.3)&(D.dist<0)].copy()
    tr["up"]=np.where(tr.r5p>0,"r5up","r5down")
    out["trend_below_by_r5sign"]=tr.groupby("up").apply(agg)
    # book falls: daily book, deepest drawdown episodes, allocation and coin move
    dd=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=c; x["win"]=w; dd.append(x)
    DD=pd.concat(dd)
    bk=DD.groupby(["win","day"]).agg(book=("book_return","mean"),hold=("coin_return","mean")).dropna().reset_index()
    bk["wo"]=bk.win.str[1:].astype(int); bk=bk.sort_values(["wo","day"])
    eq=(1+bk.book).cumprod(); bk["dd"]=(eq/eq.cummax()-1).values
    bk["indd"]=bk.dd<-0.15
    out["book_in_deep_dd_vs_not"]=bk.groupby("indd")[["book","hold"]].agg(["mean","count"])
    # share of book loss on days where coins fell
    bk["holddown"]=bk.hold<0
    out["book_by_hold_sign"]=bk.groupby("holddown").book.agg(["mean","count"])
    # bar-level: position held vs coin's prior 5d return
    B=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            r5p=b.close/b.close.shift(5)-1; g=b.close.shift(-1)/b.close-1
            B.append(pd.DataFrame(dict(alloc=b.postRebalance_current_allocation,r5p=r5p,gain=b.postRebalance_current_allocation*g)))
    B=pd.concat(B).dropna(); B=B[B.alloc>0]
    B["r5s"]=np.where(B.r5p>0,"r5up","r5down")
    out["held_gain_by_prior5"]=B.groupby("r5s").agg(n=("gain","size"),mean_gain=("gain","mean"),mean_alloc=("alloc","mean"))
    return out
