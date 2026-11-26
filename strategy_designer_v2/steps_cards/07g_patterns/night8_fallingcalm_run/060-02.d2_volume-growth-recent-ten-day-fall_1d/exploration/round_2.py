def explore(data):
    import numpy as np, pandas as pd
    H=5
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; v=b["volume"].values
            n=len(b); r1=pd.Series(c).pct_change().values
            for i in range(0,n-H,H):
                if i<59: 
                    vr=np.nan
                else:
                    vr=np.log(v[i-29:i+1].mean()/v[i-59:i-29].mean())
                rows.append(dict(coin=coin,w=w,ts=b["timestamp"].iloc[i],fr=c[i+H]/c[i]-1,
                    fc=b["forecast"].iloc[i],reg=b["regime"].iloc[i],
                    r10=c[i]/c[i-10]-1 if i>=10 else np.nan,
                    r5p=c[i]/c[i-5]-1 if i>=5 else np.nan,
                    r30=c[i]/c[i-30]-1 if i>=30 else np.nan,
                    sd30=np.nanstd(r1[max(1,i-29):i+1]) if i>=20 else np.nan,vr=vr))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby("coin")["fr"].transform("mean"); d["ex"]=d.fr-d.drift
    d["year"]=pd.to_datetime(d.ts).dt.year
    d["day"]=pd.to_datetime(d.ts).dt.floor("D")
    d["agit"]=d.sd30>d.groupby("coin")["sd30"].transform("median")
    def ct(x,y):
        # clustered-by-day t of mean (x unused) for y series aligned with d
        s=y.groupby(d.loc[y.index,"day"]).sum()
        m=y.mean(); se=np.sqrt((s-m*y.groupby(d.loc[y.index,"day"]).size()).pow(2).sum())/len(y)
        return m/se if se>0 else np.nan
    def slope(df,col):
        df=df.dropna(subset=[col,"ex"])
        x=df[col]-df[col].mean(); b=(x*df.ex).sum()/(x*x).sum()
        e=df.ex-df.ex.mean()-b*x
        g=(x*e).groupby(df.day).sum()
        se=np.sqrt((g**2).sum())/(x*x).sum()
        return pd.Series(dict(n=len(df),days=df.day.nunique(),slope=b,t=b/se))
    out={}
    fall=d[d.reg!="chop"]; ch=d[d.reg=="chop"]
    act=d[d.fc!=0]
    out["active: slope ex on fc by agit"]=act.groupby("agit").apply(lambda g:slope(g,"fc"))
    out["active: slope by year"]=act.groupby("year").apply(lambda g:slope(g,"fc"))
    out["active: slope by coin"]=act.groupby("coin").apply(lambda g:slope(g,"fc"))
    out["falling all: slope on vr by agit"]=fall.groupby("agit").apply(lambda g:slope(g,"vr"))
    out["falling, r10>=0: slope on vr"]=slope(fall[fall.r10>=0],"vr").to_frame().T
    out["chop: slope on vr"]=slope(ch,"vr").to_frame().T
    out["chop: slope on vr by agit"]=ch.groupby("agit").apply(lambda g:slope(g,"vr"))
    out["chop: slope on vr by year"]=ch.groupby("year").apply(lambda g:slope(g,"vr"))
    out["chop: slope on r5p"]=slope(ch,"r5p").to_frame().T
    out["chop: slope on r5p by agit"]=ch.groupby("agit").apply(lambda g:slope(g,"r5p"))
    out["chop: slope on r5p by year"]=ch.groupby("year").apply(lambda g:slope(g,"r5p"))
    out["chop: slope on r30"]=slope(ch,"r30").to_frame().T
    out["all: slope on vr"]=slope(d,"vr").to_frame().T
    out["all: slope on r5p"]=slope(d,"r5p").to_frame().T
    # book worst days context
    dl=[]
    for coin,wd in data["days"].items():
        for w,x in wd.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dl.append(x)
    D=pd.concat(dl).dropna(subset=["book_return"])
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    q=bk.book_return.quantile([0.02,0.98])
    out["book extreme days: coin return"]=pd.DataFrame({
        "worst2%":[ (bk.book_return<=q.iloc[0]).sum(), bk.coin_return[bk.book_return<=q.iloc[0]].mean(), bk.book_return[bk.book_return<=q.iloc[0]].mean()],
        "best2%":[ (bk.book_return>=q.iloc[1]).sum(), bk.coin_return[bk.book_return>=q.iloc[1]].mean(), bk.book_return[bk.book_return>=q.iloc[1]].mean()]},
        index=["n","coin","book"])
    # per coin-day position side on worst days
    allb=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            x=b[["timestamp","postRebalance_current_allocation","close"]].copy()
            x["day"]=pd.to_datetime(x.timestamp).dt.floor("D").astype(str)
            x["pos"]=x.postRebalance_current_allocation.shift(1)
            x["cr"]=x.close.pct_change(); x["gain"]=x.pos*x.cr; x["coin"]=coin; x["w"]=w
            allb.append(x)
    B=pd.concat(allb).dropna(subset=["gain"])
    B["side"]=np.sign(B.pos)
    out["coin-day gain by side"]=B[B.side!=0].groupby("side").agg(n=("gain","size"),mean=("gain","mean"),
        p1=("gain",lambda s:s.quantile(0.01)),p99=("gain",lambda s:s.quantile(0.99)),
        sum_worst1pct=("gain",lambda s:s[s<=s.quantile(0.01)].sum()),total=("gain","sum"))
    return out
