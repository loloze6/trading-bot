def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    ev=[]; base=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            n=len(c)
            if n<80: continue
            r=pd.Series(c).pct_change()
            z=10*r/r.abs().rolling(60,min_periods=20).mean()
            hi=pd.Series(c).rolling(21).max()
            newhi=(pd.Series(c)>=hi-1e-12)
            lo=pd.Series(c).rolling(21).min()
            newlo=(pd.Series(c)<=lo+1e-12)
            vol=r.rolling(20).std()
            volrank=vol.rolling(250,min_periods=60).rank(pct=True)
            fwd=pd.Series(c).shift(-H)/pd.Series(c)-1
            ts=pd.to_datetime(b["timestamp"])
            fc=b["forecast"].astype(float)
            ma50=pd.Series(c).rolling(50).mean()
            dfw=pd.DataFrame({"coin":coin,"w":w,"i":range(n),"r":r,"z":z,"newhi":newhi,"newlo":newlo,
                "volrank":volrank,"fwd":fwd,"wd":ts.dt.weekday,"yr":ts.dt.year,"fc":fc,
                "above50":pd.Series(c)>ma50,"r20":pd.Series(c)/pd.Series(c).shift(20)-1})
            mu=dfw["fwd"].mean()
            dfw["ex"]=dfw["fwd"]-mu
            ev.append(dfw)
    d=pd.concat(ev)
    d=d.dropna(subset=["fwd","z"])
    nono=d[d["i"]%H==0]
    def tt(x):
        x=x.dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    def merged(mask):
        out=[]
        for (coin,w),g in d[mask].groupby(["coin","w"]):
            last=-99
            for i,ex in zip(g["i"],g["ex"]):
                if i-last>H: out.append(ex); last=i
        return tt(pd.Series(out))
    res={}
    zb=pd.cut(nono["z"],[-1e9,-20,-10,-5,0,5,10,20,1e9])
    res["fwd5 ex by z bucket (nonoverlap)"]=nono.groupby(zb)["ex"].apply(tt).unstack()
    res["by newhi/newlo"]=pd.DataFrame({"newhi_z>=10":merged((d.newhi)&(d.z>=10)),
        "newhi_z<10":merged((d.newhi)&(d.z<10)),"newlo_any":merged(d.newlo),"newlo_z<=-10":merged(d.newlo&(d.z<=-10)),
        "z<=-20":merged(d.z<=-20),"z>=20 inside":merged((~d.newhi)&(d.z>=20)),"newhi_z>=20":merged(d.newhi&(d.z>=20))}).T
    res["newhi z>=10 by coin"]=pd.DataFrame({c:merged((d.newhi)&(d.z>=10)&(d.coin==c)) for c in d.coin.unique()}).T
    res["newhi z>=10 by year"]=pd.DataFrame({y:merged((d.newhi)&(d.z>=10)&(d.yr==y)) for y in sorted(d.yr.unique())}).T
    res["newhi z>=10 by volrank"]=pd.DataFrame({str(q):merged((d.newhi)&(d.z>=10)&(d.volrank>q[0])&(d.volrank<=q[1])) for q in [(0,.33),(.33,.66),(.66,1)]}).T
    res["nonoverlap by weekday"]=nono.groupby("wd")["ex"].apply(tt).unstack()
    res["nonoverlap by volrank"]=nono.groupby(pd.cut(nono.volrank,[0,.2,.4,.6,.8,1]))["ex"].apply(tt).unstack()
    res["nonoverlap by r20"]=nono.groupby(pd.qcut(nono.r20,5))["ex"].apply(tt).unstack()
    # 1-day next return by weekday all bars (1-bar nonoverlap ok)
    d["r1n"]=d.groupby(["coin","w"])["r"].shift(-1)
    res["next1d by weekday"]=d.groupby("wd")["r1n"].apply(tt).unstack()
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    tr["dur_d"]=tr.duration_minutes/1440
    res["trades by duration"]=tr.groupby(pd.cut(tr.dur_d,[0,1,2,5,10,1e9]))["net_profit_loss_percent"].agg(["count","mean","median"])
    res["trades by entry_fc"]=tr.groupby(pd.cut(tr.entry_forecast,[0,5,10,15,19.99,20]))["net_profit_loss_percent"].agg(["count","mean"])
    res["trades by coin"]=tr.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","sum"])
    return res
