def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        recs=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float)
            r1=c.pct_change()
            hh=hi.rolling(30).max(); ll=lo.rolling(30).min()
            flat=(c-c.shift(30)).abs()/(hh-ll)
            pos=(c-(hh+ll)/2)/(hh-ll)
            r10=c/c.shift(10)-1
            r5p=c/c.shift(5)-1
            r1abs=r1.abs().rolling(20).mean()
            vol20=r1.rolling(20).std()
            vol60=r1.rolling(60).std()
            fwd=c.shift(-H)/c-1
            idx=np.arange(0,len(b),H)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"fwd":fwd.iloc[idx].values,"flat":flat.iloc[idx].values,
                "pos":pos.iloc[idx].values,"r10":r10.iloc[idx].values,"r5p":r5p.iloc[idx].values,
                "r1":r1.iloc[idx].values,"r1z":(r1/vol20.shift(1)).iloc[idx].values,
                "vr":(vol20/vol60).iloc[idx].values,"vol20":vol20.iloc[idx].values,
                "fc":b["forecast"].iloc[idx].values,"al":b["postRebalance_current_allocation"].iloc[idx].values,
                "wd":ts.iloc[idx].dt.weekday.values,"yr":ts.iloc[idx].dt.year.values})
            recs.append(d)
        d=pd.concat(recs)
        g=d["fwd"].dropna()
        d["z"]=(d["fwd"]-g.mean())/g.std()
        d["r10z"]=d["r10"]/d.groupby("w")["r10"].transform("std")
        rows.append(d)
    D=pd.concat(rows).dropna(subset=["z"])
    def summ(gr):
        return pd.Series({"n":len(gr),"meanz":gr["z"].mean(),"t":gr["z"].mean()/(gr["z"].std()/np.sqrt(len(gr))) if len(gr)>2 else np.nan})
    out={}
    out["all"]=summ(D).to_frame().T
    F=D.dropna(subset=["flat","pos"])
    F["flatq"]=pd.qcut(F["flat"],4,labels=False)
    F["posq"]=pd.qcut(F["pos"],5,labels=False)
    out["flatq x posq meanz"]=F.groupby(["flatq","posq"])["z"].mean().unstack()
    out["flatq x posq t"]=F.groupby(["flatq","posq"]).apply(lambda g:g.z.mean()/(g.z.std()/np.sqrt(len(g)))).unstack()
    out["flatq x posq n"]=F.groupby(["flatq","posq"]).size().unstack()
    X=D.dropna(subset=["r1z"]); X["r1q"]=pd.qcut(X["r1z"],5,labels=False)
    out["by last-day move z quintile"]=X.groupby("r1q").apply(summ)
    X=D.dropna(subset=["r5p"]); X["q"]=pd.qcut(X["r5p"].rank(pct=True),5,labels=False)
    out["by past5d ret quintile"]=X.groupby("q").apply(summ)
    X=D.dropna(subset=["r10"]); X["q"]=pd.qcut(X["r10"].rank(pct=True),5,labels=False)
    out["by past10d ret quintile"]=X.groupby("q").apply(summ)
    X=D.dropna(subset=["vr"]); X["q"]=pd.qcut(X["vr"],5,labels=False)
    out["by vol20/vol60 quintile"]=X.groupby("q").apply(summ)
    out["by weekday"]=D.groupby("wd").apply(summ)
    out["by year"]=D.groupby("yr").apply(summ)
    A=D[D["fc"]<0]
    out["active by year"]=A.groupby("yr").apply(summ)
    # book
    br=[];
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            br.append(dd.assign(coin=coin,w=w))
    B=pd.concat(br)
    out["book daily mean/sd by coin"]=B.groupby("coin").agg(m=("book_return","mean"),s=("book_return","std"),cm=("coin_return","mean")).round(5)
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): T.append(t.assign(coin=coin))
    T=pd.concat(T)
    out["trades"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean()),dur_d=("duration_minutes",lambda x:x.mean()/1440))
    return out
