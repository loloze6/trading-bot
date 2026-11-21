def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; book=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy()
            ts=pd.to_datetime(d["timestamp"],utc=True)
            d["hr"]=((ts+pd.Timedelta(hours=1)).dt.hour)
            d["wd"]=(ts+pd.Timedelta(hours=1)).dt.weekday
            c=d["close"]
            d["r1"]=c.shift(-1)/c-1
            d["r2"]=c.shift(-2)/c-1
            d["r72"]=c/c.shift(72)-1
            d["rpast1"]=c/c.shift(1)-1
            d["rpast24"]=c/c.shift(24)-1
            d["vol24"]=d["rpast1"].rolling(24).std()
            d["lv"]=np.log(d["volume"].replace(0,np.nan))
            d["lvrel"]=d["lv"]-d["lv"].rolling(168).mean()
            d["coin"]=coin; d["w"]=w
            d["gross"]=d["postRebalance_current_allocation"]*d["r1"]
            d["fee"]=(d["total_portfolio_value"]-d["postRebalance_total_value"])/d["total_portfolio_value"]
            rows.append(d[["coin","w","hr","wd","r1","r2","r72","rpast1","rpast24","vol24","lvrel","gross","fee","postRebalance_current_allocation"]])
    A=pd.concat(rows,ignore_index=True)
    A["ex1"]=A["r1"]-A.groupby("coin")["r1"].transform("mean")
    A["ex2"]=A["r2"]-A.groupby("coin")["r2"].transform("mean")
    out={}
    g=A.dropna(subset=["ex1"]).groupby("hr")["ex1"]
    h=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count(),
                    "lvrel":A.groupby("hr")["lvrel"].mean()})
    # by hour: slope of next-1h excess on 72h fall: spread bottom tercile r72 minus top tercile
    sp=[]
    for hr,s in A.dropna(subset=["ex1","r72"]).groupby("hr"):
        q=s.groupby("coin")["r72"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
        lo=s.loc[q==0,"ex1"]; hi=s.loc[q==2,"ex1"]
        tt=stats.ttest_ind(lo,hi,equal_var=False)
        sp.append((hr,(lo.mean()-hi.mean())*1e4,tt.statistic))
    sp=pd.DataFrame(sp,columns=["hr","fallMinusRise_bp","welch_t"]).set_index("hr")
    out["by_coming_hour"]=h.join(sp)
    # reversal after large 1h moves, by size quintile of past 1h return scaled by vol
    B=A.dropna(subset=["ex1","rpast1","vol24"]).copy()
    B["z"]=B["rpast1"]/B["vol24"]
    B["zq"]=pd.qcut(B["z"],10,labels=False)
    g=B.groupby("zq")["ex1"]
    out["next1h_by_past1h_zdecile"]=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # 24h return deciles -> next 1h
    B["q24"]=B.groupby("coin")["rpast24"].transform(lambda x: pd.qcut(x,10,labels=False,duplicates="drop"))
    g=B.groupby("q24")["ex1"]
    out["next1h_by_past24h_decile"]=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # vol level -> next 1h abs/mean
    B["vq"]=B.groupby("coin")["vol24"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    g=B.groupby("vq")["ex1"]
    out["next1h_by_vol_quintile"]=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # weekday at 21h, 2h return
    s=A[(A["hr"]==21)].dropna(subset=["ex2"])
    g=s.groupby("wd")["ex2"]
    out["ex2_at21_by_weekday"]=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # book: gross vs fee, active bars
    act=A[A["postRebalance_current_allocation"].abs()>0]
    out["book_gross_vs_fee"]=pd.DataFrame({"sum_gross":[A["gross"].sum()],"sum_fee":[A["fee"].sum()],
        "n_active":[len(act)],"mean_gross_active_bp":[act["gross"].mean()*1e4],"mean_alloc_active":[act["postRebalance_current_allocation"].mean()]})
    out["book_by_coin"]=A.groupby("coin").agg(gross=("gross","sum"),fee=("fee","sum"))
    return out
