def explore(data):
    import numpy as np, pandas as pd
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values.astype(float); n=len(b)
            r1=np.full(n,np.nan); r1[1:]=c[1:]/c[:-1]-1
            f1=np.full(n,np.nan); f1[:-1]=c[1:]/c[:-1]-1
            fwd=np.full(n,np.nan); fwd[:n-H]=c[H:]/c[:n-H]-1
            vol20=pd.Series(r1).rolling(20).std().values
            ts=pd.to_datetime(b["timestamp"])
            for i in range(n):
                rows.append(dict(coin=coin,w=w,i=i,r1=r1[i],f1=f1[i],fwd=fwd[i],vol20=vol20[i],
                    reg=b["regime"].iloc[i],wd=ts.iloc[i].dayofweek,yr=ts.iloc[i].year,
                    alloc=b["postRebalance_current_allocation"].iloc[i]))
    d=pd.DataFrame(rows)
    d["z1"]=d["r1"]/d["vol20"]
    d["ex5"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d["ex1"]=d["f1"]-d.groupby("coin")["f1"].transform("mean")
    def tab(g,key,col):
        o=g.groupby(key)[col].agg(["mean","count","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"])); return o.drop(columns="std")
    res={}
    # r1 quintile effect on 5-day, each grid offset separately
    out={}
    dd=d.dropna(subset=["z1","ex5"]).copy()
    dd["q"]=pd.qcut(dd["z1"],5,labels=False)
    for off in range(5):
        g=dd[(dd.i%5)==off]
        m=g.groupby("q")["ex5"].mean(); out[f"off{off}"]=m
    res["z1_quintile_ex5_by_offset"]=pd.DataFrame(out)
    # next-day (non-overlapping daily) by z1 decile
    d1=d.dropna(subset=["z1","ex1"]).copy()
    d1["q"]=pd.qcut(d1["z1"],10,labels=False)
    res["z1_decile_next_day"]=tab(d1,"q","ex1")
    d1["fc"]=d1.reg=="unknown"
    res["z1_quint_next_day_fallcalm"]=tab(d1[d1.fc].assign(q5=lambda x:pd.qcut(x.z1,5,labels=False)),"q5","ex1")
    # weekday next-day return, non-overlapping
    res["wd_next_day"]=tab(d1,"wd","ex1")
    res["wd_next_day_by_year"]=d1.groupby(["yr","wd"])["ex1"].mean().unstack()
    # Q2 z1 5-day effect by year and by coin
    q1=dd[(dd.q==1)&(dd.i%5==0)]
    res["z1q1_by_year"]=tab(q1,"yr","ex5")
    res["z1q1_by_coin"]=tab(q1,"coin","ex5")
    # book: short positions, next-day return by z1 quintile while short
    sh=d1[d1.alloc<0].copy()
    sh["q5"]=pd.qcut(sh.z1,5,labels=False,duplicates="drop")
    res["short_next_day_by_z1"]=tab(sh,"q5","ex1")
    return res
