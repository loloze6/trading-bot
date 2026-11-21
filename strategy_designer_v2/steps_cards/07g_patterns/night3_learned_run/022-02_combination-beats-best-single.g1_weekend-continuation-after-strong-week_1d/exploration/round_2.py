def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w
            d["r1"]=c.shift(-1)/c-1
            d["r2"]=c.shift(-2)/c-1
            d["r3"]=c.shift(-3)/c-1
            d["past1"]=c/c.shift(1)-1
            d["mom7"]=c/c.shift(7)-1
            d["mom28"]=c/c.shift(28)-1
            d["near"]=c/c.rolling(28).max()-1
            lr=np.log(c).diff()
            d["vol20"]=lr.rolling(20).std()
            d["nextwd"]=(ts+pd.Timedelta(days=1)).dt.weekday.values
            d["pos"]=b["postRebalance_current_allocation"].astype(float).values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["drift"]=D.groupby("coin")["r1"].transform("mean")
    D["x1"]=D["r1"]-D["drift"]
    D["z7"]=D["mom7"]/(D["vol20"]*np.sqrt(7))
    D["z28"]=D["mom28"]/(D["vol20"]*np.sqrt(28))
    D["zp1"]=D["past1"]/D["vol20"]
    D["zn"]=D["near"]/D["vol20"]
    D["xs"]=D["x1"]/D["vol20"]
    def tc(g,col,y="xs"):
        g=g[[col,y]].replace([np.inf,-np.inf],np.nan).dropna()
        n=len(g)
        if n<30: return pd.Series({"n":n,"corr":np.nan,"t":np.nan})
        r=g[col].corr(g[y])
        return pd.Series({"n":n,"corr":r,"t":r*np.sqrt((n-2)/(1-r*r))})
    def mt(s):
        s=s.dropna(); n=len(s)
        return pd.Series({"n":n,"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    out["wd_excess"]=D.groupby("nextwd")["x1"].apply(mt).unstack()
    for col in ["z7","z28","zp1","zn"]:
        out[col+"_by_nextwd"]=D.groupby("nextwd").apply(lambda g: tc(g,col))
    sat=D[D["nextwd"]==5].copy()
    out["z7_sat_by_coin"]=sat.groupby("coin").apply(lambda g: tc(g,"z7"))
    sat["q"]=pd.qcut(sat["z7"],5,labels=False)
    out["sat_z7_quintile"]=sat.groupby("q").agg(n=("x1","count"),mean_x=("x1","mean"),mean_r2=("r2","mean"),mean_r3=("r3","mean"))
    out["sat_z7_r2_r3"]=pd.DataFrame({"r2":tc(sat,"z7","r2"),"r3":tc(sat,"z7","r3")})
    D["vq"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["volq_next"]=D.groupby("vq")["x1"].apply(mt).unstack()
    sat["vq"]=D.loc[sat.index,"vq"]
    out["z7_sat_by_volq"]=sat.groupby("vq").apply(lambda g: tc(g,"z7"))
    out["z7_sat_by_window"]=sat.groupby("win").apply(lambda g: tc(g,"z7"))
    # large past day reversal, all days
    D["pq"]=pd.qcut(D["zp1"],10,labels=False)
    out["zp1_decile_next"]=D.groupby("pq")["x1"].apply(mt).unstack()
    dd=[]
    for coin,wins in data["days"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=coin; t["wd"]=pd.to_datetime(t["day"]).dt.weekday; dd.append(t)
    Dy=pd.concat(dd)
    out["book_by_wd"]=Dy.groupby("wd").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","count"))
    out["book_by_coin"]=Dy.groupby("coin").agg(book=("book_return","mean"),sd=("book_return","std"))
    return out
