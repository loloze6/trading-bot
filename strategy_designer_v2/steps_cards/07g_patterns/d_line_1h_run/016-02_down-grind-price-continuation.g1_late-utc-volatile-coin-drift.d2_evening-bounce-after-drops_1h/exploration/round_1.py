def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; grid24=[]; book=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            r1=c.shift(-1)/c-1
            lr=np.log(c).diff()
            vol=lr.rolling(168,min_periods=84).std()
            p24=c/c.shift(24)-1
            z24=np.log(c/c.shift(24))/(vol*np.sqrt(24))
            eff=np.log(c/c.shift(24)).abs()/lr.abs().rolling(24).sum()
            f24=c.shift(-24)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour,"wd":ts.dt.weekday,"r1":r1,
                            "alloc":b["postRebalance_current_allocation"].astype(float),
                            "fee":(b["total_portfolio_value"]-b["postRebalance_total_value"]).astype(float)/b["total_portfolio_value"].astype(float),
                            "fc":b["forecast"].astype(float)})
            rows.append(d)
            g=pd.DataFrame({"coin":coin,"w":w,"z24":z24,"eff":eff,"f24":f24,"hour":ts.dt.hour,"vol":vol}).iloc[::24]
            grid24.append(g)
    D=pd.concat(rows); G=pd.concat(grid24).dropna()
    out={}
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean_bp":x.mean()*1e4,"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["hourly_ret_by_hour"]=D.groupby("hour")["r1"].apply(tt).unstack()
    out["hourly_ret_by_weekday"]=D.groupby("wd")["r1"].apply(tt).unstack()
    D["gain"]=D["alloc"]*D["r1"]
    act=D[D["alloc"].abs()>1e-9]
    out["book_gain_vs_fee_by_hour"]=pd.DataFrame({"gain_bp_sum_per_coinday":D.groupby("hour")["gain"].sum()/ (len(D)/24)*1e4,
                                                 "fee_bp_sum_per_coinday":D.groupby("hour")["fee"].sum()/(len(D)/24)*1e4}).loc[lambda x:(x.abs().sum(1)>0)]
    out["active_bars_by_hour"]=act.groupby("hour").size()
    out["mean_alloc_active"]=float(act["alloc"].mean())
    G["zq"]=pd.qcut(G["z24"],5,labels=False)
    out["f24_by_z24_quintile"]=G.groupby("zq")["f24"].apply(tt).unstack()
    G["eq"]=pd.qcut(G["eff"],3,labels=False)
    G["sf"]=np.sign(G["z24"])*G["f24"]
    out["signed_f24_by_eff_tercile_and_absz_big"]=G[G["z24"].abs()>1].groupby("eq")["sf"].apply(tt).unstack()
    G["vq"]=G.groupby("coin")["vol"].transform(lambda v:pd.qcut(v,3,labels=False))
    out["f24_by_vol_tercile"]=G.groupby("vq")["f24"].apply(tt).unstack()
    return out
