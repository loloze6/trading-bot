def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; v=b["volume"].values; o=b["open"].values; hi=b["high"].values; lo=b["low"].values
            n=len(b)
            r1=pd.Series(c).pct_change().values
            for i in range(0,n-H,H):
                fr=c[i+H]/c[i]-1
                r10=c[i]/c[i-10]-1 if i>=10 else np.nan
                r5p=c[i]/c[i-5]-1 if i>=5 else np.nan
                vr=np.log(v[max(0,i-29):i+1].mean()/v[i-59:i-29].mean()) if i>=59 else np.nan
                vs=np.log(v[max(0,i-4):i+1].mean()/v[i-29:i-4].mean()) if i>=29 else np.nan
                sd20=np.nanstd(r1[max(1,i-19):i+1]) if i>=5 else np.nan
                rows.append(dict(coin=coin,w=w,i=i,ts=b["timestamp"].iloc[i],fr=fr,
                    fc=b["forecast"].iloc[i],alloc=b["postRebalance_current_allocation"].iloc[i],
                    reg=b["regime"].iloc[i],r10=r10,r5p=r5p,vr=vr,vs=vs,r1=r1[i],sd20=sd20,
                    rng=(hi[i]-lo[i])/c[i],clo=(c[i]-lo[i])/(hi[i]-lo[i]) if hi[i]>lo[i] else np.nan,
                    wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday()))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby("coin")["fr"].transform("mean")
    d["ex"]=d["fr"]-d["drift"]
    out={}
    out["regime counts"]=d.groupby("reg")["ex"].agg(["count","mean"])
    act=d[d.fc!=0].copy()
    act["q"]=pd.qcut(act.fc,5,labels=False,duplicates="drop")
    out["active fc quintile"]=act.groupby("q").agg(n=("ex","size"),fc=("fc","mean"),ex=("ex","mean"),
        t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    act["side"]=np.sign(act.fc)
    out["active by side"]=act.groupby("side")["ex"].agg(["count","mean","std"])
    fall=d[d.reg!="chop"].copy()
    def tg(df,col,k=5):
        df=df.dropna(subset=[col]).copy()
        df["q"]=pd.qcut(df[col],k,labels=False,duplicates="drop")
        return df.groupby("q").agg(n=("ex","size"),x=(col,"mean"),ex=("ex","mean"),
            t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    out["falling: by r10"]=tg(fall,"r10")
    out["falling: by r5p"]=tg(fall,"r5p")
    out["falling: by vr30"]=tg(fall,"vr")
    out["falling: by vs5/25"]=tg(fall,"vs")
    out["falling: by sd20"]=tg(fall,"sd20")
    out["falling: by close loc"]=tg(fall,"clo")
    out["falling: by range"]=tg(fall,"rng")
    ch=d[d.reg=="chop"].copy()
    out["chop: by r5p"]=tg(ch,"r5p")
    out["chop: by vs5/25"]=tg(ch,"vs")
    out["chop: by vr30"]=tg(ch,"vr")
    out["all: by weekday"]=d.groupby("wd")["ex"].agg(["count","mean"])
    # book
    dl=[]
    for coin,wd in data["days"].items():
        for w,x in wd.items():
            x=x.copy();x["coin"]=coin;x["w"]=w;dl.append(x)
    D=pd.concat(dl)
    D["year"]=pd.to_datetime(D["day"]).dt.year
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["year"]=pd.to_datetime(bk["day"]).dt.year
    out["book by window"]=bk.groupby("w").agg(n=("book_return","size"),book=("book_return","mean"),coin=("coin_return","mean"))
    out["book by year"]=bk.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    T=pd.concat([t.assign(coin=c) for c,wd in data["trades"].items() for t in wd.values()])
    out["trades by side"]=T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median","std"])
    out["trades by coin"]=T.groupby(["coin","side"])["net_profit_loss_percent"].agg(["count","mean"])
    return out
