def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; tr=[]; dd=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            r=b["close"].shift(-1)/b["close"]-1
            # move during the next bar, which starts at ts+1h
            nh=(ts+pd.Timedelta(hours=1))
            d=pd.DataFrame({"coin":c,"w":w,"r":r,"hr":nh.dt.hour,"wd":nh.dt.dayofweek,"yr":nh.dt.year,
                            "pos":b["postRebalance_current_allocation"],"close":b["close"].values})
            lr=np.log(b["close"]).diff()
            d["vol7"]=lr.rolling(168).std()
            d["past24"]=b["close"]/b["close"].shift(24)-1
            d["fut24"]=b["close"].shift(-24)/b["close"]-1
            d["past72"]=b["close"]/b["close"].shift(72)-1
            d["fut72"]=b["close"].shift(-72)/b["close"]-1
            d["i"]=np.arange(len(d))
            rows.append(d)
        for w,t in data["trades"][c].items():
            t=t.copy(); t["coin"]=c; tr.append(t)
    A=pd.concat(rows,ignore_index=True)
    g=A.dropna(subset=["r"]).groupby("hr")["r"]
    byhr=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    g=A.dropna(subset=["r"]).groupby("wd")["r"]
    bywd=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count()))})
    ev=A[A.hr.isin([20,21])].dropna(subset=["r"])
    g=ev.groupby("coin")["r"]
    evcoin=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count()))})
    g=ev.groupby("yr")["r"]
    evyr=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    T=pd.concat(tr,ignore_index=True)
    trs=pd.DataFrame({"gross_mean_pct":[T.profit_loss_percent.mean()],"net_mean_pct":[T.net_profit_loss_percent.mean()],
                      "comm_mean":[T.total_commission.mean()],"n":[len(T)],"dur_min_mean":[T.duration_minutes.mean()]})
    # mean reversion 24h, non-overlapping grid
    G=A[(A.i%24==0)].dropna(subset=["past24","fut24"]).copy()
    G["q"]=G.groupby("coin")["past24"].transform(lambda x: pd.qcut(x,5,labels=False))
    g=G.groupby("q")["fut24"]
    rev24=pd.DataFrame({"past_mean":G.groupby("q")["past24"].mean(),"fut_mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    G=A[(A.i%72==0)].dropna(subset=["past72","fut72"]).copy()
    G["q"]=G.groupby("coin")["past72"].transform(lambda x: pd.qcut(x,5,labels=False))
    g=G.groupby("q")["fut72"]
    rev72=pd.DataFrame({"fut_mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # vol quintile vs evening and other hours
    V=A.dropna(subset=["r","vol7"]).copy()
    V["vq"]=V.groupby("coin")["vol7"].transform(lambda x: pd.qcut(x,5,labels=False))
    V["eve"]=V.hr.isin([20,21])
    g=V.groupby(["vq","eve"])["r"]
    volq=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    return {"byhour":byhr,"byweekday":bywd,"evening_by_coin":evcoin,"evening_by_year":evyr,"trades":trs,"rev24":rev24,"rev72":rev72,"volq":volq}
