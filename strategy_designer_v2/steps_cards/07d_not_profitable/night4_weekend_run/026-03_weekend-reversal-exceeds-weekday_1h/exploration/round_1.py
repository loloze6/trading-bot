def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    usual={}
    for coin,ws in data["bars"].items():
        r48=[]
        for w,df in ws.items():
            c=df["close"].values
            r48+=list(c[48::48]/c[:-48:48]-1) if len(c)>96 else []
        usual[coin]=(np.mean(r48),np.std(r48))
        for w,df in ws.items():
            ts=pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            c=df["close"].values; n=len(c)
            end=ts+pd.Timedelta(hours=1)
            for i in range(48,n-48):
                e=end[i]
                if e.hour!=0 or e.weekday() not in (0,2,4): continue
                past=c[i]/c[i-48]-1
                sat=c[i-24]/c[i-48]-1; sun=c[i]/c[i-24]-1
                rows.append(dict(coin=coin,w=w,year=e.year,wd=e.weekday(),past=past,sat=sat,sun=sun,
                    f6=c[i+6]/c[i]-1,f12=c[i+12]/c[i]-1,f24=c[i+24]/c[i]-1,f48=c[i+48]/c[i]-1,
                    f24_48=c[i+48]/c[i+24]-1,last6=c[i]/c[i-6]-1))
    d=pd.DataFrame(rows)
    d["mu"]=d.coin.map(lambda x:usual[x][0]); d["sd"]=d.coin.map(lambda x:usual[x][1])
    d["z"]=d.past/d.sd
    d["s"]=-np.sign(d.past)
    for h in ["f6","f12","f24","f48","f24_48"]:
        d["rev_"+h]=d.s*d[h]
    d["rev_un48"]=d.s*(d.f48-d.mu)
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    wk=d[d.wd==0]; wd=d[d.wd!=0]
    out["rev by horizon weekend"]=pd.DataFrame({h:tt(wk["rev_"+h]) for h in ["f6","f12","f24","f48","f24_48","un48"]}).T
    out["rev by horizon weekday"]=pd.DataFrame({h:tt(wd["rev_"+h]) for h in ["f6","f12","f24","f48","f24_48","un48"]}).T
    d["q"]=d.groupby("wd")["z"].transform(lambda x:pd.qcut(x.abs(),5,labels=False))
    out["weekend rev48 by |z| quintile"]=wk.assign(q=d.q).groupby("q").apply(lambda g:pd.Series({"n":len(g),"absz":g.z.abs().mean(),"rev48%":100*g.rev_un48.mean(),"t":tt(g.rev_un48)["t"],"rev24%":100*g.rev_f24.mean()}))
    out["weekday rev48 by |z| quintile"]=wd.assign(q=d.q).groupby("q").apply(lambda g:pd.Series({"n":len(g),"rev48%":100*g.rev_un48.mean(),"t":tt(g.rev_un48)["t"]}))
    out["weekend by coin"]=wk.groupby("coin").apply(lambda g:tt(g.rev_un48))
    out["weekend by year"]=wk.groupby("year").apply(lambda g:tt(g.rev_un48))
    # sign-sign direction by up/down
    out["weekend by sign of move"]=wk.groupby(np.sign(wk.past)).apply(lambda g:pd.Series({"n":len(g),"fut48%":100*g.f48.mean(),"rev_un%":100*g.rev_un48.mean(),"t":tt(g.rev_un48)["t"]}))
    # regressions of f48 on components
    def corr(a,b):
        m=a.notna()&b.notna(); r,p=stats.pearsonr(a[m],b[m]); return pd.Series({"corr":r,"n":m.sum(),"t":r*np.sqrt((m.sum()-2)/(1-r*r))})
    out["weekend corr with next48"]=pd.DataFrame({k:corr(wk[k]/wk.sd,wk.f48/wk.sd) for k in ["past","sat","sun","last6"]}).T
    out["weekend corr with next24"]=pd.DataFrame({k:corr(wk[k]/wk.sd,wk.f24/wk.sd) for k in ["past","sat","sun","last6"]}).T
    # book
    days=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            x=df.copy(); x["coin"]=coin; days.append(x)
    D=pd.concat(days); D["wd"]=pd.to_datetime(D.day).dt.weekday
    out["book daily ret by weekday"]=D.groupby("wd").book_return.agg(lambda x:x.mean()*1e4).rename("bp")
    tr=[]
    for coin,ws in data["trades"].items():
        for w,df in ws.items():
            if len(df): tr.append(df.assign(coin=coin))
    T=pd.concat(tr)
    out["trades"]=pd.Series({"n":len(T),"gross%":T.profit_loss_percent.mean(),"net%":T.net_profit_loss_percent.mean(),"dur_h":T.duration_minutes.mean()/60,"win":(T.profit_loss_percent>0).mean()})
    out["trades by side"]=T.groupby("side")[["profit_loss_percent","net_profit_loss_percent"]].mean()
    return out
