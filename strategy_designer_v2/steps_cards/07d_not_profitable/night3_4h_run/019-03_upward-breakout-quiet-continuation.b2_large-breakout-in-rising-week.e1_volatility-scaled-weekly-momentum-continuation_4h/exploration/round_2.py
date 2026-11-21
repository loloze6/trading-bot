def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    G=[]; P=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; f=b["forecast"].values
            pos=b["postRebalance_current_allocation"].fillna(0).values
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            lr=np.log(cl)
            n=len(b)
            for i in range(0,n-72,72):
                past180=cl[i]/cl[i-180]-1 if i>=180 else np.nan
                G.append({"coin":c,"f":f[i],"r72":cl[i+72]/cl[i]-1,"p180":past180})
            ts=pd.to_datetime(b["timestamp"]).dt.floor("D")
            P.append(pd.DataFrame({"coin":c,"win":w,"day":ts,"lg":np.where(pos>0,pos*r1,0),
                                   "sg":np.where(pos<0,pos*r1,0),"pos":pos,
                                   "fee":(b["postRebalance_total_value"]-b["total_portfolio_value"]).values/b["total_portfolio_value"].values}))
    G=pd.DataFrame(G)
    G["r72d"]=G["r72"]-G.groupby("coin")["r72"].transform("mean")
    G["sgn"]=np.sign(G["f"]); G["s72"]=G["r72d"]*G["sgn"]; G["tot72"]=G["r72"]*G["sgn"]
    G["absf"]=pd.cut(G["f"].abs(),[0,5,10,20.1])
    G["agree"]=np.sign(G["p180"])==G["sgn"]
    def tt(x): x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    g72=G.groupby(["absf","sgn"])["s72"].apply(tt).unstack()
    g72tot=G.groupby(["absf","sgn"])["tot72"].mean().unstack()
    gag=G.dropna(subset=["p180"]).groupby(["agree","sgn"])["s72"].apply(tt).unstack()
    sl=stats.linregress(G["f"],G["r72d"])
    P=pd.concat(P)
    d=P.groupby(["win","coin","day"]).agg(lg=("lg","sum"),sg=("sg","sum"),fee=("fee","sum"),pos=("pos","mean")).reset_index()
    bk=d.groupby(["win","day"]).agg(lg=("lg","mean"),sg=("sg","mean"),fee=("fee","mean"),pos=("pos","mean")).reset_index()
    D=pd.concat([dd.assign(coin=c,win=w) for c in days for w,dd in days[c].items()])
    cb=D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    cb["day"]=pd.to_datetime(cb["day"]).dt.floor("D") if not np.issubdtype(cb["day"].dtype,np.datetime64) else cb["day"]
    bk["day"]=pd.to_datetime(bk["day"]).dt.tz_localize(None) if hasattr(bk["day"].dt,"tz") and bk["day"].dt.tz is not None else bk["day"]
    cb["day"]=pd.to_datetime(cb["day"]); 
    try: cb["day"]=cb["day"].dt.tz_localize(None)
    except Exception: pass
    m=bk.merge(cb,on=["win","day"],how="inner")
    m["wn"]=m["win"].str[1:].astype(int); m=m.sort_values(["wn","day"])
    eq=(1+m["book_return"].fillna(0)).cumprod(); m["dd"]=(eq/eq.cummax()-1).values
    peak=eq.cummax(); trough=m["dd"].idxmin()
    # fall phase: windows 4..10 (deepen) vs rest
    m["phase"]=np.where(m["wn"].between(4,10),"w4-w10","other")
    ph=m.groupby("phase").agg(days=("lg","size"),longgain=("lg","mean"),shortgain=("sg","mean"),fee=("fee","mean"),
                              pos=("pos","mean"),coin=("coin_return","mean"),book=("book_return","mean"))
    tot=pd.Series({"longgain":m["lg"].mean(),"shortgain":m["sg"].mean(),"fee":m["fee"].mean(),"book":m["book_return"].mean(),"hold":m["coin_return"].mean(),
                   "slope72_t":sl.slope/sl.stderr,"n72":len(G)})
    return {"s72_by_absf_side":g72,"tot72_by_absf_side":g72tot,"s72_trend_agree":gag,"phase":ph,"totals":tot}
