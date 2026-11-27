def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            d=pd.DataFrame()
            d["ts"]=pd.to_datetime(b["timestamp"])
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            d["r0"]=c.pct_change()
            d["r1"]=c.shift(-1)/c-1
            d["r2"]=c.shift(-2)/c-1
            rng=(h-l)/c
            d["rr"]=rng/rng.rolling(20,min_periods=20).mean()
            d["loc"]=(c-l)/(h-l).replace(0,np.nan)
            d["tr60"]=c/c.shift(60)-1
            d["vol"]=d["r0"].rolling(30).std()
            d["inprof"]=(b["regime"]!="chop").astype(int)
            d["pos"]=b["postRebalance_current_allocation"].astype(float)
            d["coin"]=coin; d["w"]=w
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["day"]=A["ts"].dt.floor("D")
    A["mu"]=A.groupby("coin")["r1"].transform("mean")
    A["dev"]=A["r1"]-A["mu"]
    A["wd"]=A["ts"].dt.weekday
    def tt(sub,sign=1):
        sub=sub.dropna(subset=["dev"])
        if len(sub)<5: return pd.Series({"n":len(sub),"mean":np.nan,"t":np.nan,"days":0})
        g=(sign*sub["dev"]).groupby(sub["day"]).sum()
        D=len(g); m=g.sum()/len(sub)
        se=np.sqrt((g**2).sum()*D/(D-1))/len(sub)
        return pd.Series({"n":len(sub),"mean":m,"t":m/se,"days":D})
    out={}
    A["upw"]=(A.r0>0)&(A.rr>=1)&(A["loc"]>=0.75)
    A["dnw"]=(A.r0<0)&(A.rr>=1)&(A["loc"]<=0.25)
    A["trend"]=np.where(A.tr60>0.1,"rising",np.where(A.tr60<-0.1,"falling",np.where(A.tr60.notna(),"choppy","na")))
    # wide up near high by trend / inprof, long-sign dev
    res={}
    for k,s in A[A.upw].groupby(["trend","inprof"]): res[str(k)]=tt(s)
    out["upwide_nextday_by_trend_inprof"]=pd.DataFrame(res).T
    res={}
    for k,s in A[A.dnw].groupby(["trend","inprof"]): res[str(k)]=tt(s)
    out["dnwide_nextday_by_trend_inprof"]=pd.DataFrame(res).T
    # grading by rr quintile for up-wide in falling (trend) 
    res={}
    U=A[A.upw&(A.trend=="falling")].copy()
    U["q"]=pd.qcut(U.rr,3,labels=False,duplicates="drop")
    for k,s in U.groupby("q"): res["fall_q"+str(k)]=tt(s)
    U=A[A.upw&(A.trend=="rising")].copy()
    U["q"]=pd.qcut(U.rr,3,labels=False,duplicates="drop")
    for k,s in U.groupby("q"): res["rise_q"+str(k)]=tt(s)
    U=A[A.upw&(A.trend=="choppy")].copy()
    U["q"]=pd.qcut(U.rr,3,labels=False,duplicates="drop")
    for k,s in U.groupby("q"): res["chop_q"+str(k)]=tt(s)
    out["upwide_by_width_tercile"]=pd.DataFrame(res).T
    # all up days by rr tercile and trend, regardless loc
    res={}
    for tr in ["falling","choppy","rising"]:
        U=A[(A.r0>0)&(A.trend==tr)].copy()
        U["q"]=pd.qcut(U.rr,4,labels=False,duplicates="drop")
        for k,s in U.groupby("q"): res[tr+"_up_rrq"+str(k)]=tt(s)
        U=A[(A.r0<0)&(A.trend==tr)].copy()
        U["q"]=pd.qcut(U.rr,4,labels=False,duplicates="drop")
        for k,s in U.groupby("q"): res[tr+"_dn_rrq"+str(k)]=tt(s)
    out["all_days_by_trend_sign_rrquartile"]=pd.DataFrame(res).T
    res={}
    for k,s in A.groupby("wd"): res["wd"+str(k)]=tt(s)
    out["weekday"]=pd.DataFrame(res).T
    # vol tercile and big move
    A["z"]=A.r0/A.vol
    res={}
    for tr in ["falling","choppy","rising"]:
        S=A[A.trend==tr]
        res[tr+"_z>2"]=tt(S[S.z>2]); res[tr+"_z<-2"]=tt(S[S.z<-2])
    out["big_moves"]=pd.DataFrame(res).T
    # book days
    dl=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd.copy(); x["coin"]=coin; x["w"]=w; dl.append(x)
    Dd=pd.concat(dl)
    bk=Dd.groupby("day")["book_return"].mean().dropna()
    out["book_desc"]=bk.describe()
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): x=t.copy(); x["coin"]=coin; tr.append(x)
    T=pd.concat(tr)
    out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","sum"])
    out["trades_q"]=T["net_profit_loss_percent"].describe()
    return out
