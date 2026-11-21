def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows=[]; grid=[]; turn=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; pos=b["postRebalance_current_allocation"].fillna(0).values
            prev=b["previous_allocation"].fillna(0).values
            r1=np.r_[cl[1:]/cl[:-1]-1, np.nan]
            g=pos*r1
            n=len(b)
            turn.append({"coin":c,"win":w,"bars":n,"traded":np.abs(pos-prev).sum(),
                         "gross":np.nansum(g),"longgain":np.nansum(np.where(pos>0,g,0)),
                         "shortgain":np.nansum(np.where(pos<0,g,0)),
                         "abspos":np.abs(pos).mean(),"longshare":(pos>0).mean()})
            f=b["forecast"].values
            ts=pd.to_datetime(b["timestamp"])
            # vol-scaled 7d return raw, plus 30d context
            for h in (18,36,72):
                for i in range(0,n-h,18 if h==18 else 18):
                    pass
            for i in range(0,n-72,18):
                grid.append({"coin":c,"win":w,"f":f[i],"r18":cl[i+18]/cl[i]-1,
                             "r36":cl[i+36]/cl[i]-1,"r72":cl[i+72]/cl[i]-1,
                             "r42past":cl[i]/cl[i-42]-1 if i>=42 else np.nan,
                             "r180past":cl[i]/cl[i-180]-1 if i>=180 else np.nan,
                             "pos":pos[i],"year":ts.iloc[i].year})
    T=pd.DataFrame(turn); G=pd.DataFrame(grid)
    for h in ("r18","r36","r72"):
        G[h+"d"]=G[h]-G.groupby("coin")[h].transform("mean")
    G["sgn"]=np.sign(G["f"])
    for h in ("r18","r36","r72"):
        G[h+"s"]=G[h+"d"]*G["sgn"]; G[h+"tot"]=G[h]*G["sgn"]
    G["fb"]=pd.cut(G["f"],[-20.1,-10,-5,-2,0,2,5,10,20.1])
    byf=G.groupby("fb").agg(n=("f","size"),r18d=("r18d","mean"),r36d=("r36d","mean"),r72d=("r72d","mean"),r18=("r18","mean"))
    G["absf"]=pd.cut(G["f"].abs(),[0,2,5,10,20.1])
    bya=G.groupby("absf").agg(n=("f","size"),s18=("r18s","mean"),s36=("r36s","mean"),s72=("r72s","mean"),tot18=("r18tot","mean"))
    side=G.groupby("sgn").agg(n=("f","size"),s18=("r18s","mean"),tot18=("r18tot","mean"),s72=("r72s","mean"))
    coin=G.groupby("coin").agg(s18=("r18s","mean"),s72=("r72s","mean"),tot18=("r18tot","mean"))
    # long-term trend context: 30d past return sign vs signal side
    G["trend_agree"]=np.sign(G["r180past"])==G["sgn"]
    ctx=G.dropna(subset=["r180past"]).groupby("trend_agree").agg(n=("f","size"),s18=("r18s","mean"),tot18=("r18tot","mean"),s72=("r72s","mean"))
    agg=T.groupby("coin").agg(bars=("bars","sum"),traded=("traded","sum"),gross=("gross","sum"),longg=("longgain","sum"),shortg=("shortgain","sum"),abspos=("abspos","mean"),longshare=("longshare","mean"))
    agg["turn_per_day"]=agg["traded"]/agg["bars"]*6
    agg["gross_per_day"]=agg["gross"]/agg["bars"]*6
    agg["gross_per_unit_traded_bps"]=agg["gross"]/agg["traded"]*1e4
    # book
    D=[]
    for c in days:
        for w,d in days[c].items():
            D.append(d.assign(coin=c,win=w))
    D=pd.concat(D)
    bk=D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["wn"]=bk["win"].str[1:].astype(int); bk=bk.sort_values(["wn","day"])
    eq=(1+bk["book_return"].fillna(0)).cumprod(); dd=eq/eq.cummax()-1
    bk["dd"]=dd.values
    byw=bk.groupby("wn").agg(book=("book_return","mean"),coin=("coin_return","mean"),mindd=("dd","min"))
    return {"turnover":agg,"by_forecast":byf,"by_absf":bya,"side":side,"coin":coin,"trend_ctx":ctx,
            "by_window":byw,"maxdd":float(dd.min())}
