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
            ret60=b["close"]/b["close"].shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"ts":b["timestamp"],"rw":rw,"cl":cl,"f1":f1,
                            "inprof":(b["regime"]!="chop"),"ret60":ret60,"r":r,
                            "year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift1=D.groupby("coin")["r"].mean()
    D["u1"]=D["f1"]-D["coin"].map(drift1)
    def stat(m):
        s=D[m & D["u1"].notna()]
        if len(s)<5: return [len(s),np.nan,np.nan,np.nan]
        mu=s["u1"].mean()
        g=s.groupby("ts")["u1"].agg(["sum","count"])
        se=np.sqrt(((g["sum"]-g["count"]*mu)**2).sum())/len(s)
        return [len(s),s["ts"].nunique(),mu,mu/se if se>0 else np.nan]
    ip=D["inprof"]
    out={}
    broad=(D["rw"]>=1.5)&(D["cl"]>=0.6)
    tested=(D["rw"]>=2)&(D["cl"]>=0.75)
    res={}
    res["prof broad"]=stat(ip&broad)
    res["prof tested"]=stat(ip&tested)
    res["prof broad not tested"]=stat(ip&broad&~tested)
    res["prof rw>=1.5 cl>=.5"]=stat(ip&(D["rw"]>=1.5)&(D["cl"]>=0.5))
    for lab,m in [("out rising",D["ret60"]>0.10),("out choppy",D["ret60"].abs()<=0.10),("out falling",D["ret60"]<-0.10)]:
        res[lab+" broad"]=stat(~ip&broad&m)
        res[lab+" tested"]=stat(~ip&tested&m)
    out["by group"]=pd.DataFrame(res,index=["n","days","mean","t"]).T
    s=D[ip&broad&D["u1"].notna()]
    out["prof broad by window"]=s.groupby("w")["u1"].agg(["count","mean"])
    out["prof broad by year"]=s.groupby("year")["u1"].agg(["count","mean"])
    out["prof broad by coin"]=s.groupby("coin")["u1"].agg(["count","mean"])
    from scipy import stats
    out["prof broad grading"]=pd.Series({
        "spearman rw":stats.spearmanr(s["rw"],s["u1"]).correlation,
        "spearman cl":stats.spearmanr(s["cl"],s["u1"]).correlation,
        "spearman rw*cl":stats.spearmanr(s["rw"]*s["cl"],s["u1"]).correlation,
        "top half rw*cl mean":s[(s["rw"]*s["cl"])>(s["rw"]*s["cl"]).median()]["u1"].mean(),
        "bottom half rw*cl mean":s[(s["rw"]*s["cl"])<=(s["rw"]*s["cl"]).median()]["u1"].mean(),
        "win rate":(s["f1"]>0).mean()})
    return out
