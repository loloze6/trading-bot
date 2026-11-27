def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            r=b["close"].pct_change()
            std30=r.rolling(30,min_periods=30).std()
            rw=((b["high"]-b["low"])/b["close"])/std30
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            cl=(b["high"]-b["close"])/rng
            f1=b["close"].shift(-1)/b["close"]-1
            f2=b["close"].shift(-2)/b["close"]-1
            ret60=b["close"]/b["close"].shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"ts":b["timestamp"],"rw":rw,"cl":cl,"f1":f1,"f2":f2,
                            "inprof":(b["regime"]!="chop"),"regime":b["regime"],"ret60":ret60,
                            "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],"pos":np.arange(len(b)),"r":r})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift1=D.groupby("coin")["r"].mean()
    D["u1"]=D["f1"]-D["coin"].map(drift1)
    D["u2"]=D["f2"]-2*D["coin"].map(drift1)
    def stat(m,col="u1",grid=1):
        s=D[m & D[col].notna()]
        if grid==2: s=s[s["pos"]%2==0]
        if len(s)<5: return [len(s),np.nan,np.nan,np.nan]
        mu=s[col].mean()
        g=s.groupby("ts")[col].agg(["sum","count"])
        se=np.sqrt(((g["sum"]-g["count"]*mu)**2).sum())/len(s)
        return [len(s),s["ts"].nunique(),mu,mu/se if se>0 else np.nan]
    out={}
    res={}
    ip=D["inprof"]
    for rwth in [1.0,1.5,2.0,2.5,3.0]:
        for clth in [0.5,0.6,0.75,0.9]:
            base=(D["rw"]>=rwth)&(D["cl"]>=clth)
            res[f"prof rw>={rwth} cl>={clth}"]=stat(base&ip)
    out["in profile, next day"]=pd.DataFrame(res,index=["n","days","mean_u1","t"]).T
    res={}
    for rwth in [1.5,2.0]:
        for clth in [0.6,0.75]:
            base=(D["rw"]>=rwth)&(D["cl"]>=clth)
            res[f"ALL rw>={rwth} cl>={clth}"]=stat(base)
            res[f"outprof rw>={rwth} cl>={clth}"]=stat(base&~ip)
            res[f"rising60 rw>={rwth} cl>={clth}"]=stat(base&(D["ret60"]>0.10))
            res[f"prof 2d rw>={rwth} cl>={clth}"]=stat(base&ip,"u2",1)
    out["other cases"]=pd.DataFrame(res,index=["n","days","mean","t"]).T
    res={}
    res["prof no signal (rw<2 or cl<.75)"]=stat(ip&~((D["rw"]>=2)&(D["cl"]>=0.75)))
    res["prof all"]=stat(ip)
    res["prof cl>=.75 any rw"]=stat(ip&(D["cl"]>=0.75))
    res["prof rw>=2 any cl"]=stat(ip&(D["rw"]>=2))
    out["controls"]=pd.DataFrame(res,index=["n","days","mean","t"]).T
    tr=sum(len(t) for ws in data["trades"].values() for t in ws.values())
    out["trades, coin-bars, inprof share, active bars"]=pd.Series({"trades":tr,"bars":len(D),"inprof":ip.mean(),
        "regime_mr_bars":(D["regime"]=="mean_reversion").sum(),"alloc>0 bars":(D["alloc"]>0).sum()})
    # graded: within prof, by rw bins among cl>=0.6
    s=D[ip&(D["cl"]>=0.6)&D["u1"].notna()]
    out["prof cl>=.6 by rw bin"]=s.groupby(pd.cut(s["rw"],[0,1,1.5,2,2.5,3,5,50]))["u1"].agg(["count","mean"])
    s=D[ip&(D["rw"]>=1.5)&D["u1"].notna()]
    out["prof rw>=1.5 by cl bin"]=s.groupby(pd.cut(s["cl"],[-0.01,0.25,0.5,0.6,0.75,0.9,1.0]))["u1"].agg(["count","mean"])
    return out
