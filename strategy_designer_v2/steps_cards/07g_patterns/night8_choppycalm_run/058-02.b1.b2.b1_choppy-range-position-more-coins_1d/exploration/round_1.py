def explore(data):
    import pandas as pd, numpy as np
    rows=[]; drows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            hh=h.rolling(20).max(); ll=l.rolling(20).min()
            rp=(2*(c-ll)/(hh-ll)-1)
            r1=c.pct_change()
            r60=c/c.shift(60)-1
            v30=r1.rolling(30).std()
            v10=r1.rolling(10).std()
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            r5p=c/c.shift(5)-1
            df=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),"rp":rp,"r60":r60,"v30":v30,"v10":v10,
                             "f5":f5,"f1":f1,"r1":r1,"r5p":r5p,"fc":b["forecast"],"pos":b["postRebalance_current_allocation"],
                             "grid":(np.arange(len(b))%5==0)})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["day"]=A.ts.dt.floor("D")
    g=A[A.grid].copy()
    g["ex5"]=g.f5-g.groupby("coin").f5.transform("mean")
    A["ex1"]=A.f1-A.groupby("coin").f1.transform("mean")
    A["vrel"]=A.v30/A.groupby("coin").v30.transform("median")
    g["vrel"]=A.loc[g.index,"vrel"]
    g["trend"]=pd.cut(g.r60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    g["agit"]=np.where(g.vrel>1,"agit","calm")
    g["rpq"]=pd.cut(g.rp,[-1.01,-0.6,-0.2,0.2,0.6,1.01],labels=["q1lo","q2","q3","q4","q5hi"])
    def ct(x):
        d=x.groupby("day").ex5.sum(); n=x.groupby("day").size()
        m=x.ex5.mean(); se=np.sqrt(((d-n*m)**2).sum())/len(x)
        return pd.Series({"n":len(x),"mean%":100*m,"t":m/se if se>0 else np.nan})
    out={}
    out["rp_by_trend_agit"]=g.dropna(subset=["ex5","rpq","trend"]).groupby(["trend","agit","rpq"],observed=True).apply(ct).round(2)
    out["rp_all"]=g.dropna(subset=["ex5","rpq"]).groupby("rpq",observed=True).apply(ct).round(2)
    # prior 5d return deciles -> next 5d
    g["r5q"]=pd.qcut(g.r5p,5,labels=False)
    out["prior5_q"]=g.dropna(subset=["ex5","r5q"]).groupby("r5q").apply(ct).round(2)
    # vol level
    g["vq"]=pd.qcut(g.vrel,3,labels=["lowv","midv","hiv"])
    g["sgn"]=np.sign(g.r5p)
    out["prior5sign_by_vol"]=g.dropna(subset=["ex5","vq"]).groupby(["vq","sgn"],observed=True).apply(ct).round(2)
    # daily: after large moves
    A["z"]=A.r1/A.v30.shift(1)
    A["zq"]=pd.cut(A.z,[-99,-2,-1,0,1,2,99])
    def ct1(x):
        d=x.groupby("day").ex1.sum(); n=x.groupby("day").size(); m=x.ex1.mean()
        se=np.sqrt(((d-n*m)**2).sum())/len(x)
        return pd.Series({"n":len(x),"mean%":100*m,"t":m/se})
    out["next1_after_z"]=A.dropna(subset=["ex1","zq"]).groupby("zq",observed=True).apply(ct1).round(3)
    A["wd"]=A.ts.dt.dayofweek
    out["next1_by_weekday_of_signal"]=A.dropna(subset=["ex1"]).groupby("wd").apply(ct1).round(3)
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D); D["day"]=pd.to_datetime(D.day)
    bk=D.groupby("day").book_return.mean().dropna()
    out["book_by_year"]=bk.groupby(bk.index.year).agg(["count","mean","std"]).assign(sh=lambda x:x["mean"]/x["std"]*np.sqrt(365)).round(5)
    # position side pnl
    A["pnl"]=A.pos*A.f1
    out["pnl_by_side_rpq"]=A.assign(side=np.sign(A.pos),rpq=pd.cut(A.rp,[-1.01,-0.6,-0.2,0.2,0.6,1.01])).groupby(["side","rpq"],observed=True).pnl.agg(["count","mean"]).round(5)
    return out
