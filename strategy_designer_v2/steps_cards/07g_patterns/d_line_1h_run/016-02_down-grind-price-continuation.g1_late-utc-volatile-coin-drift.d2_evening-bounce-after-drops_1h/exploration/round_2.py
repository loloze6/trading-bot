def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    E=[]; G=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            lr=np.log(c).diff()
            vol=lr.rolling(168,min_periods=84).std()
            z24=np.log(c/c.shift(24))/(vol*np.sqrt(24))
            eff=np.log(c/c.shift(24)).abs()/lr.abs().rolling(24).sum()
            vr=b["volume"].astype(float)
            vconc=vr.rolling(24).max()/vr.rolling(24).sum()
            f2=c.shift(-2)/c-1
            f24=c.shift(-24)/c-1
            f48=c.shift(-48)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour,"wd":ts.dt.weekday,"z24":z24,"eff":eff,"vconc":vconc,"f2":f2,"f24":f24,"f48":f48})
            E.append(d[d["hour"]==20])
            G.append(d.iloc[::24])
    E=pd.concat(E).dropna(subset=["f2","z24"]); G=pd.concat(G).dropna()
    out={}
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean_bp":x.mean()*1e4,"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    E["zq"]=pd.qcut(E["z24"],5,labels=False)
    out["eve_f2_by_z24_quintile"]=E.groupby("zq")["f2"].apply(tt).unstack()
    out["eve_f2_by_coin"]=E.groupby("coin")["f2"].apply(tt).unstack()
    E["half"]=np.where(E["w"].str[1:].astype(int)<=12,"w1-12","w13-24")
    out["eve_f2_by_half"]=E.groupby("half")["f2"].apply(tt).unstack()
    out["eve_f2_by_weekday"]=E.groupby("wd")["f2"].apply(tt).unstack()
    # daily reversal: regression f24 on z24, eff, z24*eff, vconc, z24*vconc
    X=pd.DataFrame({"z":G["z24"],"z_eff":G["z24"]*(G["eff"]-G["eff"].mean()),"z_vc":G["z24"]*(G["vconc"]-G["vconc"].mean())})
    X=(X-X.mean()); X["c"]=1.0
    y=G["f24"].values
    beta,res,rk,sv=np.linalg.lstsq(X.values,y,rcond=None)
    resid=y-X.values@beta; s2=resid@resid/(len(y)-X.shape[1])
    se=np.sqrt(np.diag(s2*np.linalg.inv(X.values.T@X.values)))
    out["reg_f24_on_z_eff_vconc"]=pd.DataFrame({"beta_bp":beta*1e4,"t":beta/se},index=X.columns)
    G["zq"]=pd.qcut(G["z24"],5,labels=False)
    out["f24_by_zq_by_coin_t"]=G.groupby(["coin","zq"])["f24"].apply(lambda x:x.mean()/(x.std()/np.sqrt(len(x)))).unstack()
    out["f24_by_zq_by_half"]=G.assign(half=np.where(G["w"].str[1:].astype(int)<=12,"a","b")).groupby(["half","zq"])["f24"].apply(lambda x:x.mean()*1e4).unstack()
    low=G[G["zq"]==0].copy(); low["eq"]=pd.qcut(low["eff"],3,labels=False); low["vq"]=pd.qcut(low["vconc"],3,labels=False)
    out["lowq_f24_by_eff"]=low.groupby("eq")["f24"].apply(tt).unstack()
    out["lowq_f24_by_vconc"]=low.groupby("vq")["f24"].apply(tt).unstack()
    out["lowq_f48"]=tt(low["f48"])
    return out
