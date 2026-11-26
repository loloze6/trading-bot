def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # drift per horizon
        for h in [1,3,5,10]:
            rs=[]
            for w,df in wins.items():
                c=df["close"].values
                for i in range(0,len(c)-h,h):
                    rs.append(c[i+h]/c[i]-1)
            drift[(coin,h)]=(np.mean(rs),np.std(rs))
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            o,hi,lo,c=df["open"],df["high"],df["low"],df["close"]
            rng=hi-lo
            rr=rng/rng.rolling(20).mean()
            fl=1-(c-o).abs()/rng.replace(0,np.nan)
            pe5=c/c.shift(5)-1
            ts=pd.to_datetime(df["timestamp"])
            for i in range(len(df)):
                if np.isnan(rr[i]) or np.isnan(pe5[i]) or np.isnan(fl[i]): continue
                if rr[i]>=1.5 and fl[i]>=0.9 and pe5[i]!=0:
                    r={"coin":coin,"win":w,"pos":i,"cell":i//5,"side":"up" if pe5[i]>0 else "down",
                       "rr":rr[i],"fl":fl[i],"pe5":pe5[i],"year":ts[i].year,"day":ts[i].floor("D"),
                       "fc":df["forecast"].iloc[i]}
                    for h in [1,3,5,10]:
                        if i+h<len(df):
                            ret=c[i+h]/c[i]-1
                            d,s=drift[(coin,h)]
                            r[f"tot{h}"]=ret; r[f"unu{h}"]=ret-d; r[f"str{h}"]=(ret-d)/s
                    rows.append(r)
    X=pd.DataFrame(rows)
    X=X.groupby(["coin","win","cell","side"]).first().reset_index()
    def ct(x,days):
        x=np.asarray(x);m=x.mean();e=x-m
        S=pd.Series(e).groupby(np.asarray(days)).sum()
        se=np.sqrt((S**2).sum())/len(x)
        return m, m/se if se>0 else np.nan, len(x)
    out={}
    hz=[]
    for side in ["up","down"]:
        for h in [1,3,5,10]:
            s=X[X.side==side].dropna(subset=[f"unu{h}"])
            m,t,n=ct(s[f"unu{h}"],s["day"])
            hz.append({"side":side,"h":h,"unusual_up_dir":m,"t":t,"n":n,"tot":s[f"tot{h}"].mean(),"strength":s[f"str{h}"].mean()})
    out["by_side_horizon (coin return, + = up)"]=pd.DataFrame(hz)
    U=X[X.side=="up"].dropna(subset=["unu5"])
    def grp(key):
        g=[]
        for k,s in U.groupby(key):
            m,t,n=ct(s["unu5"],s["day"]); g.append({"k":k,"unu5":m,"t":t,"n":n})
        return pd.DataFrame(g)
    out["up_by_coin"]=grp("coin"); out["up_by_year"]=grp("year")
    U=U.copy()
    U["pe5q"]=pd.qcut(U.pe5,3,labels=False); U["rrq"]=pd.qcut(U.rr,3,labels=False); U["flq"]=pd.qcut(U.fl,3,labels=False)
    out["up_by_pe5_tercile"]=grp("pe5q"); out["up_by_rr_tercile"]=grp("rrq"); out["up_by_fl_tercile"]=grp("flq")
    out["corr_up_unu5"]=U[["unu5","rr","fl","pe5"]].corr(method="spearman")["unu5"]
    D=X[X.side=="down"].dropna(subset=["unu5"]).copy()
    D["pe5q"]=pd.qcut(D.pe5,3,labels=False)
    g=[]
    for k,s in D.groupby("pe5q"):
        m,t,n=ct(s["unu5"],s["day"]); g.append({"k":k,"unu5":m,"t":t,"n":n})
    out["down_by_pe5_tercile"]=pd.DataFrame(g)
    out["n_up_cases_recomputed"]=len(U)
    return out
