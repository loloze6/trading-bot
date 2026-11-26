def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        allret=[]
        for w,b in wins.items():
            c=b["close"].values; allret.append(pd.Series(c).pct_change().dropna())
        drift=pd.concat(allret).mean()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            rng=(b["high"]-b["low"])
            cl=(b["close"]-b["low"])/rng.replace(0,np.nan)
            rr=rng/rng.rolling(20,min_periods=20).mean()
            nxt=b["close"].shift(-1)/b["close"]-1
            r1=b["close"].pct_change()
            r5=b["close"]/b["close"].shift(5)-1
            inprof=b["regime"]!="chop"
            d=pd.DataFrame({"coin":coin,"w":w,"cl":cl,"rr":rr,"nxt":nxt,"r1":r1,"r5":r5,
                            "inprof":inprof,"fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                            "ts":b["timestamp"].astype(str).str[:10]})
            d["short_unusual"]=-(d["nxt"]-drift)
            d["short_total"]=-d["nxt"]
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["nxt","rr","cl"])
    def stat(m):
        x=D[m]
        if len(x)<3: return pd.Series({"n":len(x),"days":0,"mean":np.nan,"t_day":np.nan,"total":np.nan})
        g=x.groupby("ts")["short_unusual"].sum()
        n=len(g); t=g.mean()/(g.std(ddof=1)/np.sqrt(n))*1 if n>2 else np.nan
        return pd.Series({"n":len(x),"days":n,"mean":x["short_unusual"].mean(),"t_day":t,"total":x["short_total"].mean()})
    out={}
    grid={}
    for prof in ["in","all"]:
        for clt in [0.0,0.5,0.6,0.75,0.9]:
            for rrt in [0.0,1.0,1.2,1.5,2.0]:
                m=(D["cl"]>=clt)&(D["rr"]>=rrt)
                if prof=="in": m&=D["inprof"]
                grid[f"{prof} cl>={clt} rr>={rrt}"]=stat(m)
    out["grid"]=pd.DataFrame(grid).T.round(4)
    # condition alone: wide day without high close, in profile
    alt={}
    alt["in rr>=1.5 cl<0.5"]=stat(D["inprof"]&(D["rr"]>=1.5)&(D["cl"]<0.5))
    alt["in rr<1.0 cl>=0.75"]=stat(D["inprof"]&(D["rr"]<1.0)&(D["cl"]>=0.75))
    alt["in all"]=stat(D["inprof"])
    alt["in r1>0 rr>=1.5"]=stat(D["inprof"]&(D["r1"]>0)&(D["rr"]>=1.5))
    alt["in r1>0 cl>=0.75"]=stat(D["inprof"]&(D["r1"]>0)&(D["cl"]>=0.75))
    alt["in r1<=0 cl>=0.75 rr>=1.2"]=stat(D["inprof"]&(D["r1"]<=0)&(D["cl"]>=0.75)&(D["rr"]>=1.2))
    alt["in r1>0 cl>=0.75 rr>=1.2"]=stat(D["inprof"]&(D["r1"]>0)&(D["cl"]>=0.75)&(D["rr"]>=1.2))
    out["alt"]=pd.DataFrame(alt).T.round(4)
    # grading by cl within in-profile rr>=1.2
    m=D["inprof"]&(D["rr"]>=1.0)
    q=pd.cut(D.loc[m,"cl"],[0,0.25,0.5,0.75,0.9,1.01],include_lowest=True)
    out["by_cl_inprof_rr1"]=D[m].groupby(q)["short_unusual"].agg(["count","mean"]).round(4)
    q2=pd.cut(D.loc[m&(D["cl"]>=0.6),"rr"],[1,1.2,1.5,2,10])
    out["by_rr_inprof_cl06"]=D[m&(D["cl"]>=0.6)].groupby(q2)["short_unusual"].agg(["count","mean"]).round(4)
    out["share_inprof"]=float(D["inprof"].mean())
    # held days
    h=D[D["alloc"]<0]
    out["held"]=pd.Series({"n":len(h),"mean_short_total":h["short_total"].mean(),"mean_alloc":h["alloc"].mean(),
        "share_loss":(h["short_total"]<0).mean(),"worst":h["short_total"].min()}).round(4)
    out["held_by_window"]=h.groupby("w")["short_total"].agg(["count","mean","sum"]).round(4)
    # book drawdown
    bd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            bd.append(d[["day","book_return"]].assign(w=w))
    B=pd.concat(bd).dropna().groupby(["w","day"])["book_return"].mean().reset_index()
    B["wn"]=B["w"].str[1:].astype(int); B=B.sort_values(["wn","day"])
    v=(1+B["book_return"]).cumprod(); dd=v/v.cummax()-1
    B["dd"]=dd.values
    out["dd_by_window"]=B.groupby("w")["dd"].min().round(4)
    out["worst_book_days"]=B["book_return"].nsmallest(8).round(4).reset_index(drop=True)
    return out
