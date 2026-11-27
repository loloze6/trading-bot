import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=7
    rows=[]
    drows=[]
    for coin,wins in data["bars"].items():
        g7=[]
        for w,b in wins.items():
            c=b["close"].values.astype(float)
            n=len(c)
            for i in range(0,n-H,H):
                g7.append(c[i+H]/c[i]-1)
        drift=np.mean(g7) if g7 else np.nan
        usual=np.std(g7,ddof=1) if len(g7)>2 else np.nan
        allc=[]
        for w,b in wins.items():
            c=b["close"].astype(float).reset_index(drop=True)
            r1=c.pct_change()
            vol30=r1.rolling(30).std()
            allc.append(vol30)
        medvol=pd.concat(allc).median()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            r30=c/c.shift(30)-1
            vol30=r1.rolling(30).std()
            ts=pd.to_datetime(b["timestamp"])
            n=len(c)
            for i in range(0,n-H,H):
                f=c.iloc[i+H]/c.iloc[i]-1
                rows.append(dict(coin=coin,w=w,day=ts.iloc[i].normalize(),r30=r30.iloc[i],
                    vol=vol30.iloc[i]/medvol if medvol>0 else np.nan,
                    chop=b["regime"].iloc[i]=="unknown",fc=b["forecast"].iloc[i],
                    ex=(f-drift),exz=(f-drift)/usual,r1=r1.iloc[i],
                    r7p=c.iloc[i]/c.iloc[i-7]-1 if i>=7 else np.nan,
                    wd=ts.iloc[i].weekday()))
            for i in range(1,n-1):
                drows.append(dict(coin=coin,w=w,day=ts.iloc[i].normalize(),r1=r1.iloc[i],
                    nx=c.iloc[i+1]/c.iloc[i]-1,chop=b["regime"].iloc[i]=="unknown",wd=ts.iloc[i].weekday(),
                    vol=vol30.iloc[i]))
    G=pd.DataFrame(rows).dropna(subset=["r30"])
    D=pd.DataFrame(drows).dropna()
    def ct(df,col):
        s=df.groupby("day")[col].sum(); m=df[col].mean(); k=len(s)
        se=np.sqrt((s-m*df.groupby("day")[col].size()).pow(2).sum()*k/(k-1))/len(df)
        return pd.Series(dict(n=len(df),days=k,mean=m,t=m/se if se>0 else np.nan))
    out={}
    G["q30"]=pd.qcut(G["r30"],5,labels=False)
    out["chop_by_r30_quintile"]=G[G.chop].groupby("q30").apply(lambda d:ct(d,"ex"))
    out["nonchop_by_r30_quintile"]=G[~G.chop].groupby("q30").apply(lambda d:ct(d,"ex"))
    G["vb"]=pd.qcut(G["vol"],3,labels=["calm","mid","agit"])
    G["sgn"]=np.sign(G["r30"])
    sub=G[G.chop].copy(); sub["cont"]=sub["ex"]*sub["sgn"]
    out["chop_continuation_by_vol_side"]=sub.groupby(["vb","sgn"]).apply(lambda d:ct(d,"cont"))
    # slope of exz on r30 by chop
    for k,d in [("chop",G[G.chop]),("nonchop",G[~G.chop])]:
        s=stats.linregress(d["r30"],d["exz"]); out["slope_"+k]=f"slope {s.slope:.3f} t {s.slope/s.stderr:.2f} n {len(d)}"
    # previous week return
    G["q7"]=pd.qcut(G["r7p"],5,labels=False)
    out["all_by_prev7_quintile"]=G.dropna(subset=["q7"]).groupby("q7").apply(lambda d:ct(d,"ex"))
    # daily: next-day after large moves
    D["z"]=D["r1"]/D["vol"]
    D["zb"]=pd.cut(D["z"],[-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    out["nextday_by_dayz"]=D.groupby("zb").apply(lambda d:ct(d,"nx"))
    out["weekday_return"]=D.groupby("wd").apply(lambda d:ct(d,"nx"))
    # book
    bk=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; bk.append(d)
    B=pd.concat(bk).dropna(subset=["book_return"])
    B["yr"]=pd.to_datetime(B["day"]).dt.year
    out["book_by_window"]=B.groupby("w").agg(bm=("book_return","mean"),cm=("coin_return","mean"),n=("book_return","size"))
    out["book_by_year"]=B.groupby("yr").agg(bm=("book_return","mean"),cm=("coin_return","mean"))
    return out
