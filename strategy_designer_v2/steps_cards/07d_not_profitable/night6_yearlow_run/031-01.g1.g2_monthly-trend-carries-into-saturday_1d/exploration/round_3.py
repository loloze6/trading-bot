def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy().reset_index(drop=True)
            b["ts"]=pd.to_datetime(b["timestamp"])
            b["r1"]=b["close"].shift(-1)/b["close"]-1
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            lr=np.log(b["close"]).diff()
            b["vol20"]=lr.rolling(20).std()
            b["coin"]=c; b["wn"]=int(w[1:]); b["wd"]=b["ts"].dt.weekday; b["year"]=b["ts"].dt.year
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    mu=B.groupby("coin")["r1"].mean()
    B["ex"]=B["r1"]-B["coin"].map(mu)
    F=B[(B.wd==4)&B.r1.notna()].copy()
    F["a"]=F["postRebalance_current_allocation"].fillna(0)
    F["f"]=F["forecast"].fillna(0)
    cost=0.0019
    ndays=7.94*365
    out={}
    def book(alloc,name):
        g=alloc*F["r1"]-cost*alloc.abs()
        d=pd.DataFrame({"wn":F.wn,"ts":F.ts.dt.normalize(),"g":g}).groupby(["wn","ts"])["g"].sum()/6
        d=d.reset_index().sort_values(["wn","ts"])
        v=(1+d["g"]).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/ndays)-1
        d["year"]=d.ts.dt.year
        by=d.groupby("year")["g"].sum()
        return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"days_in":(alloc!=0).mean(),"worst_year_sum":by.min(),"years_neg":(by<0).sum()},name=name)
    res=[]
    res.append(book(F["a"],"as tested"))
    res.append(book(F["a"].clip(lower=0),"long side only"))
    fl=F["f"].clip(lower=0)/10
    sc=F.loc[F.a>0,"a"].mean()/fl[fl>0].mean()
    res.append(book(fl*sc,"long only, size by forecast, no vol target"))
    res.append(book(F["a"].clip(lower=0).clip(upper=0.6),"long only, alloc capped 0.6"))
    al=pd.Series(np.where(F.f!=-999,F.loc[F.a>0,"a"].mean(),0),index=F.index)
    res.append(book(al,"condition alone: long every Friday, flat size"))
    res.append(book(F["a"].where(F.f>=5,0).clip(lower=0),"long only, forecast>=5"))
    out["variant books (approx)"]=pd.DataFrame(res)
    # condition alone vs with signal, by ret20 tercile on Fridays
    F["rt"]=F.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["Friday ex by ret20 tercile"]=F.groupby("rt").agg(n=("ex","size"),ret20=("ret20","mean"),ex=("ex","mean"),exsd=("ex","std"))
    # other weekdays, ret20 tercile
    O=B[(B.wd!=4)&B.r1.notna()&B.ret20.notna()].copy()
    O["rt"]=O.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["other weekdays ex by ret20 tercile"]=O.groupby("rt").agg(n=("ex","size"),ex=("ex","mean"))
    # long cases by year
    L=F[F.a>0]
    out["long cases by year"]=L.groupby("year").agg(n=("ex","size"),ex=("ex","mean"),gain=("r1",lambda s:(s*L.loc[s.index,"a"]).mean()))
    return out
