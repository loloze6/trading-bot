def explore(data):
    import numpy as np, pandas as pd
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
            r30=c/c.shift(30)-1
            sc10=r10/(c.pct_change(10).abs().rolling(60).mean())
            fwd=c.shift(-H)/c-1
            idx=np.arange(0,len(b),H)
            ts=pd.to_datetime(b["timestamp"])
            recs.append(pd.DataFrame({"coin":coin,"w":w,"fwd":fwd.iloc[idx].values,"flat":flat.iloc[idx].values,
                "pos":pos.iloc[idx].values,"r10":r10.iloc[idx].values,"r30":r30.iloc[idx].values,"sc10":sc10.iloc[idx].values,
                "fc":b["forecast"].iloc[idx].values,"wd":ts.iloc[idx].dt.weekday.values,
                "dt":ts.iloc[idx].dt.floor("D").values}))
        d=pd.concat(recs); g=d["fwd"].dropna()
        d["z"]=(d["fwd"]-g.mean())/g.std()
        rows.append(d)
    D=pd.concat(rows).dropna(subset=["z"])
    def clus(gr):
        m=gr.groupby("dt")["z"].mean()
        return pd.Series({"n":len(gr),"dates":len(m),"meanz":gr["z"].mean(),
            "t_naive":gr.z.mean()/(gr.z.std()/np.sqrt(len(gr))),
            "t_dates":m.mean()/(m.std()/np.sqrt(len(m))) if len(m)>2 else np.nan,
            "coins_pos":(gr.groupby("coin")["z"].mean()>0).mean()})
    out={}
    out["weekday clustered"]=D.groupby("wd").apply(clus)
    F=D.dropna(subset=["flat","pos"]).copy()
    F["trend"]=np.where(F["flat"]>F["flat"].median(),"trend","flat")
    F["posq"]=pd.qcut(F["pos"],5,labels=False)
    out["trend/flat x pos quintile clustered"]=F.groupby(["trend","posq"]).apply(clus)
    # graded: trending coins, pos signed in trend direction
    T=F[F.trend=="trend"].copy()
    T["q"]=pd.qcut(T["pos"],5,labels=False)
    X=D.dropna(subset=["sc10"]).copy(); X["q"]=pd.qcut(X["sc10"],5,labels=False)
    out["scaled 10d return quintile clustered"]=X.groupby("q").apply(clus)
    X=D.dropna(subset=["r30"]).copy(); X["q"]=pd.qcut(X["r30"].rank(pct=True),5,labels=False)
    out["30d return quintile clustered"]=X.groupby("q").apply(clus)
    A=D[D.fc<0]
    out["active clustered"]=clus(A).to_frame().T
    # book: days around largest/smallest
    br=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items(): br.append(dd.assign(coin=coin,w=w))
    B=pd.concat(br).dropna(subset=["book_return"])
    B["inpos"]=B["book_return"].abs()>1e-9
    out["book days in/out position"]=B.groupby("inpos").agg(n=("book_return","size"),book=("book_return","mean"),coin=("coin_return","mean"))
    I=B[B.inpos]
    out["in-position days: corr book vs coin"]=pd.Series({"corr":I["book_return"].corr(I["coin_return"]),
        "share coin up":(I["coin_return"]>0).mean(),"mean coin":I["coin_return"].mean(),"all-days coin mean":B["coin_return"].mean()})
    Tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): Tr.append(t.assign(coin=coin))
    Tr=pd.concat(Tr)
    Tr["fq"]=pd.qcut(Tr["entry_forecast"].abs(),4,labels=False,duplicates="drop")
    out["trades by |entry forecast| quartile"]=Tr.groupby("fq").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),med=("profit_loss_percent","median"),win=("profit_loss_percent",lambda x:(x>0).mean()))
    Tr["dq"]=pd.qcut(Tr["duration_minutes"],4,labels=False,duplicates="drop")
    out["trades by duration quartile"]=Tr.groupby("dq").agg(n=("profit_loss_percent","size"),d=("duration_minutes",lambda x:x.mean()/1440),gross=("profit_loss_percent","mean"))
    return out
