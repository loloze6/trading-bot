def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            ts=pd.to_datetime(b["timestamp"])
            b["wd"]=ts.dt.weekday
            c=b["close"].values
            n=len(b)
            r1=np.full(n,np.nan); r2=np.full(n,np.nan); rprev=np.full(n,np.nan); r3after=np.full(n,np.nan); rwk=np.full(n,np.nan)
            r1[:-1]=c[1:]/c[:-1]-1
            r2[:-2]=c[2:]/c[:-2]-1
            rprev[1:]=c[1:]/c[:-1]-1
            # return of the following day (tue) alone
            tue=np.full(n,np.nan); tue[:-2]=c[2:]/c[1:-1]-1
            # 7-day prior return
            r7=np.full(n,np.nan); r7[7:]=c[7:]/c[:-7]-1
            pos=b["postRebalance_current_allocation"].values
            fee=b["total_portfolio_value"].shift(-1).values  # placeholder
            gain=pos*r1
            feecost=(b["total_portfolio_value"]-b["postRebalance_total_value"]).values/b["total_portfolio_value"].values
            df=pd.DataFrame({"coin":coin,"w":w,"wd":b["wd"],"fc":b["forecast"],"pos":pos,"prevpos":b["previous_allocation"],
                             "r1":r1,"r2":r2,"tue":tue,"rsun":rprev,"r7":r7,"gain":gain,"fee":feecost,"vol":b["volume"]})
            df["volrel"]=df["vol"]/df["vol"].rolling(60,min_periods=20).mean()
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    out={}
    out["by weekday: mean pos, mean gain, mean fee"]=d.groupby("wd")[["pos","gain","fee","r1"]].mean()
    sun=d[(d.wd==6)]
    act=sun[sun.fc<0]
    out["active sundays count"]=len(act)
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    m1=d.r1.mean()
    out["active: mon ret, tue ret, gain, fee"]=pd.DataFrame({"mon":tt(act.r1),"tue":tt(act.tue),"gain":tt(act.gain),"fee":tt(act.fee),"r1_all":tt(d.r1)})
    act=act.copy()
    act["q"]=pd.qcut(-act.fc,4,labels=False,duplicates="drop")
    out["by forecast quartile"]=act.groupby("q").agg(n=("r1","size"),fc=("fc","mean"),pos=("pos","mean"),mon=("r1","mean"),tue=("tue","mean"),gain=("gain","mean"),fee=("fee","mean"))
    sunall=sun.copy()
    sunall["up"]=sunall.rsun>0
    out["sunday up vs down: mon,tue"]=sunall.groupby("up")[["r1","tue","r2"]].mean()
    act["r7up"]=act.r7>0
    out["active by prior 7d ret sign"]=act.groupby("r7up").agg(n=("r1","size"),mon=("r1","mean"),tue=("tue","mean"),gain=("gain","mean"))
    act["vq"]=pd.qcut(act.volrel,3,labels=False,duplicates="drop")
    out["active by rel volume tercile"]=act.groupby("vq").agg(n=("r1","size"),mon=("r1","mean"),tue=("tue","mean"),gain=("gain","mean"))
    out["active by coin"]=act.groupby("coin").agg(n=("r1","size"),mon=("r1","mean"),tue=("tue","mean"),gain=("gain","mean"),fee=("fee","mean"))
    # weekday control: non-sunday up days, next day return
    wk=d[(d.wd<5)&(d.rsun>0)]
    out["weekday up-days next1 next2"]=pd.DataFrame({"next1":tt(wk.r1),"next2":tt(wk.r2)})
    # book daily return stats
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["wd"]=pd.to_datetime(x["day"]).dt.weekday; x["coin"]=coin; dd.append(x)
    dd=pd.concat(dd)
    out["book daily by weekday"]=dd.groupby("wd")[["book_return","coin_return"]].agg(["mean","std"])
    return out
