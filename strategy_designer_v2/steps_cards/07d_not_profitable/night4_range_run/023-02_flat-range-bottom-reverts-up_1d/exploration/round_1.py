import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            hh=b.high.rolling(30).max(); ll=b.low.rolling(30).min()
            mid=(hh+ll)/2
            dist=b.close/mid-1
            rng=(hh-ll)/b.close
            nmr=(b.close-b.close.shift(30)).abs()/(hh-ll)
            r5p=b.close/b.close.shift(5)-1
            r1p=b.close/b.close.shift(1)-1
            fwd=b.close.shift(-5)/b.close-1
            yr=pd.to_datetime(b.timestamp).dt.year
            d=pd.DataFrame(dict(coin=c,win=w,dist=dist,rng=rng,nmr=nmr,r5p=r5p,r1p=r1p,fwd=fwd,
                                fc=b.forecast,alloc=b.postRebalance_current_allocation,yr=yr,
                                regime=b.regime))
            d=d.iloc[::5]
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["fwd"])
    drift=D.groupby("coin").fwd.mean()
    D["ex"]=D.fwd-D.coin.map(drift)
    def agg(g):
        x=g.ex
        return pd.Series(dict(n=len(x),mean_ex=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,mean_tot=g.fwd.mean()))
    D2=D.dropna(subset=["dist","nmr"])
    D2["flat"]=np.where(D2.nmr<=0.3,"flat","trend")
    D2["dq"]=pd.qcut(D2.dist,6,labels=False)
    out={}
    out["dist_sextile_by_flat"]=D2.groupby(["flat","dq"]).apply(agg)
    fb=D2[(D2.flat=="flat")&(D2.dist<0)].copy()
    fb["r5q"]=pd.qcut(fb.r5p,3,labels=["fall5","mid5","rise5"])
    out["flat_below_by_prior5d"]=fb.groupby("r5q").apply(agg)
    fb["rngq"]=pd.qcut(fb.rng,3,labels=["narrow","midr","wide"])
    out["flat_below_by_rangewidth"]=fb.groupby("rngq").apply(agg)
    fb["nq"]=pd.qcut(fb.nmr,3,labels=["n_lo","n_mid","n_hi"])
    out["flat_below_by_nmr"]=fb.groupby("nq").apply(agg)
    out["flat_below_by_year"]=fb.groupby("yr").apply(agg)
    out["flat_below_by_coin"]=fb.groupby("coin").apply(agg)
    # book daily
    dd=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=c; x["win"]=w; x["yr"]=pd.to_datetime(x.day).dt.year; dd.append(x)
    DD=pd.concat(dd)
    bk=DD.groupby(["win","day"]).agg(book=("book_return","mean"),hold=("coin_return","mean"),yr=("yr","first")).dropna()
    out["book_by_year"]=bk.groupby("yr")[["book","hold"]].agg(["mean","count"])
    bk=bk.reset_index()
    order=sorted(bk.win.unique(),key=lambda s:int(s[1:]))
    bk["wo"]=bk.win.map({w:i for i,w in enumerate(order)})
    bk=bk.sort_values(["wo","day"])
    eq=(1+bk.book).cumprod(); dd_=eq/eq.cummax()-1
    bk["dd"]=dd_.values
    out["book_dd"]=pd.Series(dict(maxdd=dd_.min(),yrs=len(bk)/365,final=eq.iloc[-1]))
    out["book_by_window"]=bk.groupby("wo")[["book","hold"]].sum()
    return out
