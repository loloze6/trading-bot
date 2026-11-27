def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values
            rng=h-l
            clv=np.where(rng>0,(c-l)/np.where(rng>0,rng,1),np.nan)
            r1=pd.Series(c).pct_change().values
            n=len(b)
            vol20=pd.Series(r1).rolling(20).std().values
            fc=b["forecast"].values
            alloc=b["postRebalance_current_allocation"].values
            for i in range(n):
                d=dict(coin=coin,w=w,pos=i,day=pd.Timestamp(b["timestamp"].iloc[i]).normalize(),
                       clv=clv[i],ret1=r1[i],agit=(b["regime"].iloc[i]!="chop"),fc=fc[i],alloc=alloc[i],
                       rngrel=rng[i]/c[i]/vol20[i] if vol20[i]==vol20[i] and vol20[i]>0 else np.nan,
                       ret20=c[i]/c[i-20]-1 if i>=20 else np.nan,
                       clv3=np.nanmean(clv[max(0,i-2):i+1]))
                for hh in (1,3,7):
                    d[f"f{hh}"]=c[i+hh]/c[i]-1 if i+hh<n else np.nan
                    d[f"g{hh}"]=(i%hh==0)
                d["f2_7"]=c[i+7]/c[i+1]-1 if i+7<n else np.nan
                rows.append(d)
    df=pd.DataFrame(rows)
    for hh in (1,3,7):
        g=df[df[f"g{hh}"]]
        df[f"x{hh}"]=df[f"f{hh}"]-df.coin.map(g.groupby("coin")[f"f{hh}"].mean())
    g=df[df.g7]; df["x2_7"]=df["f2_7"]-df.coin.map(g.groupby("coin")["f2_7"].mean())
    def ct(s,col):
        s=s.dropna(subset=[col])
        dd=(s[col]).groupby(s.day).sum()
        n=len(s); m=s[col].mean()
        se=np.sqrt(((s[col]-m).groupby(s.day).sum()**2).sum())/n
        return pd.Series(dict(mean=round(m,4),n=n,days=len(dd),t_day=round(m/se,2) if se>0 else np.nan))
    out={}
    A=df[df.agit & df.g7].dropna(subset=["clv","x7"]).copy()
    A["q"]=pd.qcut(A.clv,5,labels=False)
    out["agit clv q x7 day-clustered"]=A.groupby("q").apply(lambda z: ct(z,"x7"))
    out["agit clv q x2_7 (skip day1)"]=A.groupby("q").apply(lambda z: ct(z,"x2_7"))
    A["tr"]=np.where(A.ret20>0.05,"up",np.where(A.ret20<-0.05,"down","flat"))
    A["top"]=np.where(A.q==4,"top",np.where(A.q==0,"bot","mid"))
    out["agit x7 by trend20 x clv top/bot"]=A.groupby(["tr","top"]).apply(lambda z: ct(z,"x7"))
    out["agit x7 clv top/bot by coin"]=A[A.top!="mid"].groupby(["coin","top"]).x7.mean().unstack().round(4)
    out["agit x7 clv top/bot by year"]=A[A.top!="mid"].assign(y=A.day.dt.year).groupby(["y","top"]).x7.mean().unstack().round(4)
    A["rq"]=pd.qcut(A.rngrel,3,labels=False)
    out["agit x7 by range-size tercile x clv top/bot"]=A.groupby(["rq","top"]).apply(lambda z: ct(z,"x7"))
    A["c3q"]=pd.qcut(A.clv3,5,labels=False)
    out["agit 3-day mean clv q x7"]=A.groupby("c3q").apply(lambda z: ct(z,"x7"))
    # forecast vs raw clv
    P=df[df.agit & df.g7 & (df.fc>0)].dropna(subset=["x7"])
    out["fc>0 corr fc,clv"]=round(P[["fc","clv"]].corr().iloc[0,1],3)
    out["fc>0 by clv>0.5"]=P.groupby(P.clv>0.5).apply(lambda z: ct(z,"x7"))
    C=df[(~df.agit)&df.g7].dropna(subset=["clv","x7"]).copy()
    C["q"]=pd.qcut(C.clv,5,labels=False)
    out["calm clv q x7 day-clustered"]=C.groupby("q").apply(lambda z: ct(z,"x7"))
    # book largest days
    dl=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dl.append(d.assign(coin=coin,w=w))
    D=pd.concat(dl).dropna(subset=["book_return"])
    bk=D.groupby("day").agg(b=("book_return","mean"),c=("coin_return","mean"))
    out["book: corr with coin mean"]=round(bk.corr().iloc[0,1],3)
    q=bk.b.quantile([0.02,0.98])
    out["book worst2% coin mean"]=round(bk[bk.b<=q.iloc[0]].c.mean(),4)
    out["book best2% coin mean"]=round(bk[bk.b>=q.iloc[1]].c.mean(),4)
    return out
