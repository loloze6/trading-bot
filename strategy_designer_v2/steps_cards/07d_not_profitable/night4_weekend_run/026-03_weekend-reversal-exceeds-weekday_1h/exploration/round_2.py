def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    usual={}
    for coin,ws in data["bars"].items():
        r24=[];r48=[]
        for w,df in ws.items():
            c=df["close"].values
            if len(c)>96:
                r24+=list(c[24::24]/c[:-24:24]-1); r48+=list(c[48::48]/c[:-48:48]-1)
        usual[coin]=(np.mean(r24),np.std(r24),np.mean(r48),np.std(r48))
        for w,df in ws.items():
            ts=pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            c=df["close"].values; n=len(c)
            fc=df["forecast"].values
            end=ts+pd.Timedelta(hours=1)
            for i in range(48,n-48):
                e=end[i]
                if e.hour!=0: continue
                rows.append(dict(coin=coin,year=e.year,wd=e.weekday(),
                    prev=c[i-24]/c[i-48]-1,last=c[i]/c[i-24]-1,
                    f24=c[i+24]/c[i]-1,f48=c[i+48]/c[i]-1,fc=fc[i]))
    d=pd.DataFrame(rows)
    d["m24"]=d.coin.map(lambda x:usual[x][0]);d["s24"]=d.coin.map(lambda x:usual[x][1])
    d["m48"]=d.coin.map(lambda x:usual[x][2]);d["s48"]=d.coin.map(lambda x:usual[x][3])
    d["z"]=d["last"]/d.s24
    d["dir"]=-np.sign(d["last"])
    d["un24"]=d.dir*(d.f24-d.m24); d["un48"]=d.dir*(d.f48-d.m48)
    d["tot24"]=d.dir*d.f24; d["str24"]=d.un24/d.s24
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    # reversal of the day ending at 00:00, by weekday the day ended (0 = Sunday's day ending Monday 00:00)
    out["last-24h reversal next24 by end weekday"]=d.groupby("wd").apply(lambda g:pd.Series({"n":len(g),"un24%":100*g.un24.mean(),"t24":tt(g.un24)["t"],"tot24%":100*g.tot24.mean(),"strength":g.str24.mean(),"un48%":100*g.un48.mean(),"t48":tt(g.un48)["t"]}))
    sun=d[d.wd==0].copy()
    sun["q"]=pd.qcut(sun.z.abs(),5,labels=False)
    out["sunday reversal by |z| quintile"]=sun.groupby("q").apply(lambda g:pd.Series({"n":len(g),"abs_last%":100*g["last"].abs().mean(),"un24%":100*g.un24.mean(),"t":tt(g.un24)["t"],"tot24%":100*g.tot24.mean(),"un48%":100*g.un48.mean()}))
    out["sunday reversal by sign"]=sun.groupby(np.sign(sun["last"])).apply(lambda g:tt(g.un24))
    out["sunday by coin"]=sun.groupby("coin").apply(lambda g:tt(g.un24))
    out["sunday by year"]=sun.groupby("year").apply(lambda g:tt(g.un24))
    # saturday continuation: sat (prev) in its own direction over next 48h at Monday
    sun["cont48"]=np.sign(sun.prev)*(sun.f48-sun.m48)
    out["saturday continuation next48"]=tt(sun.cont48)
    # book's forecast sign vs raw weekend move sign
    sun["wk"]=sun.prev+sun["last"]
    sun["agree"]=np.sign(sun.fc)==-np.sign(sun.wk)
    out["forecast sign agrees with -weekend move"]=sun.groupby("agree").apply(lambda g:pd.Series({"n":len(g),"fc_dir_next48%":100*(np.sign(g.fc)*(g.f48-g.m48)).mean(),"t":tt(np.sign(g.fc)*(g.f48-g.m48))["t"]}))
    return out
