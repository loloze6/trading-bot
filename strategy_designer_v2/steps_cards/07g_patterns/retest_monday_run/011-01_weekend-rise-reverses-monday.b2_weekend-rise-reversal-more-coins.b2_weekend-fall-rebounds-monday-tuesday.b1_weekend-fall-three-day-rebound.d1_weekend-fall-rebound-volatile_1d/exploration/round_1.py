import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        # coin mean non-overlapping 3-bar return pooled
        g3=[]; g1=[]
        for w, b in wins.items():
            c=b["close"].values
            g3+=list(c[3::3][:len(c[0::3])]/c[0::3][:len(c[3::3])]-1)
        m3=np.mean(g3) if g3 else np.nan
        for w, b in wins.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            b["wd"]=ts.dt.weekday.values; b["year"]=ts.dt.year.values
            c=b["close"]
            b["r1"]=c/c.shift(1)-1
            b["r2"]=c/c.shift(2)-1
            b["vol20"]=b["r1"].rolling(20).std()
            b["z"]=b["r1"]/b["vol20"]
            b["z2"]=b["r2"]/(b["vol20"]*np.sqrt(2))
            b["vr"]=b["volume"]/b["volume"].rolling(20).mean().shift(1)
            b["vr2"]=(b["volume"]+b["volume"].shift(1))/(2*b["volume"].rolling(20).mean().shift(2))
            b["f3"]=c.shift(-3)/c-1
            b["x3"]=b["f3"]-m3
            b["x3s"]=b["x3"]/(b["vol20"]*np.sqrt(3))
            b["f1"]=c.shift(-1)/c-1
            b["f7"]=c.shift(-7)/c-1
            b["coin"]=coin; b["win"]=w
            b["volq"]=b["vol20"]/b["vol20"].rolling(120,min_periods=60).median()
            rows.append(b[["coin","win","wd","year","r1","z","z2","vr","vr2","f1","f3","x3","x3s","f7","vol20","volq","forecast","postRebalance_current_allocation"]])
    D=pd.concat(rows).dropna(subset=["z","x3"])
    out={}
    # slope of standardized excess 3d on z, by weekday
    res=[]
    for d,g in D.groupby("wd"):
        s=stats.linregress(g["z"],g["x3s"])
        fall=g[g.z<-1]["x3"]; rise=g[g.z>1]["x3"]
        res.append([d,len(g),s.slope,s.slope/s.stderr,fall.mean(),stats.ttest_1samp(fall,0).statistic,len(fall),rise.mean(),stats.ttest_1samp(rise,0).statistic,len(rise)])
    out["by_weekday_z_on_excess3"]=pd.DataFrame(res,columns=["wd","n","slope","t","fall_x3","fall_t","nf","rise_x3","rise_t","nr"])
    # weekday raw next-day returns
    out["next_day_by_wd"]=D.groupby("wd")["f1"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # Sunday cases: 2-day weekend z, volume ratio interaction
    S=D[D.wd==6].dropna(subset=["z2","vr2"])
    res=[]
    for name,col in [("z1",S.z),("z2",S.z2)]:
        s=stats.linregress(col,S["x3s"]); res.append([name,len(S),s.slope,s.slope/s.stderr])
    Sf=S[S.z<0]
    for q,g in Sf.groupby(pd.qcut(Sf.vr2,3,labels=["lowvol","mid","highvol"])):
        s=stats.linregress(g.z,g.x3s); res.append(["fall_vr_"+str(q),len(g),s.slope,s.slope/s.stderr])
    for q,g in Sf.groupby(pd.qcut(Sf.volq,3,labels=["calm","mid","agit"])):
        s=stats.linregress(g.z,g.x3s); res.append(["fall_volq_"+str(q),len(g),s.slope,s.slope/s.stderr])
    out["sunday_detail"]=pd.DataFrame(res,columns=["case","n","slope","t"])
    # Sunday falls by year
    out["sunday_fall_by_year"]=Sf.groupby("year")["x3"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # all weekdays falls by vol level (volq tercile), all days
    Dn=D.dropna(subset=["volq"])
    Dn["vt"]=pd.qcut(Dn.volq,3,labels=["calm","mid","agit"])
    res=[]
    for (vt,wk),g in Dn.groupby(["vt",Dn.wd>=5]):
        s=stats.linregress(g.z,g.x3s); res.append([vt,wk,len(g),s.slope,s.slope/s.stderr])
    out["slope_by_vol_weekend"]=pd.DataFrame(res,columns=["vol","weekend","n","slope","t"])
    # book days
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["wd"]=pd.to_datetime(d["day"]).dt.weekday; d["coin"]=coin; dd.append(d)
    DD=pd.concat(dd).dropna(subset=["book_return"])
    out["book_by_wd"]=DD.groupby("wd")["book_return"].agg(["mean","std","count"])
    q=DD.book_return.quantile([0.01,0.99])
    out["book_tails_wd"]=pd.DataFrame({"worst":DD[DD.book_return<=q[0.01]].wd.value_counts().sort_index(),
                                       "best":DD[DD.book_return>=q[0.99]].wd.value_counts().sort_index()})
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values() if len(t)])
    T["dur_d"]=T.duration_minutes/1440
    out["trades"]=pd.DataFrame({"n":[len(T)],"mean_net":[T.net_profit_loss_percent.mean()],"win":[(T.net_profit_loss_percent>0).mean()],"dur":[T.dur_d.mean()]})
    out["trades_by_fc_tercile"]=T.groupby(pd.qcut(T.entry_forecast.rank(method="first"),3,labels=["lo","mid","hi"]))["net_profit_loss_percent"].agg(["mean","count"])
    return out
