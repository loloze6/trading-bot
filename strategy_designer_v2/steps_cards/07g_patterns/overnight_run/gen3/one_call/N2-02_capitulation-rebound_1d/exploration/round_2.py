def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            vol20=pd.Series(r1).rolling(20).std().values
            sma200=pd.Series(c).rolling(200,min_periods=100).mean().values
            ts=pd.to_datetime(b["timestamp"])
            f1=np.r_[c[1:]/c[:-1]-1,np.nan]
            f3=np.r_[c[3:]/c[:-3]-1,[np.nan]*3] if n>3 else np.full(n,np.nan)
            for i in range(n):
                rows.append((coin,w,i,r1[i],vol20[i],c[i]/sma200[i]-1 if sma200[i]==sma200[i] else np.nan,b["forecast"].iloc[i],b["regime"].iloc[i],ts.iloc[i].weekday(),ts.iloc[i].year,f1[i],f3[i]))
    d=pd.DataFrame(rows,columns="coin w i r1 vol dist fc regime wd yr f1 f3".split())
    d["z1"]=d.r1/d.vol
    d["dn"]=(d.z1<=-1)
    def summ(g,col):
        return g[col].agg(["count","mean",lambda x: x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan]).rename(columns={"<lambda_0>":"t"})
    out={}
    dn=d[d.dn]
    out["dn_next1_coin"]=summ(dn.groupby("coin"),"f1")
    out["dn_next1_year"]=summ(dn.groupby("yr"),"f1")
    out["dn_next1_regime"]=summ(dn.groupby("regime"),"f1")
    dn=dn.copy(); dn["above"]=dn.dist>0
    out["dn_next1_aboveSMA"]=summ(dn.groupby("above"),"f1")
    # non-overlapping f3 after down days: take only down days not within 3 bars of previous counted
    sel=[]
    for (cn,w),g in d.groupby(["coin","w"]):
        last=-10
        for i,z,f in zip(g.i,g.z1,g.f3):
            if z<=-1 and i-last>=3 and f==f: sel.append((cn,f)); last=i
    s=pd.DataFrame(sel,columns=["coin","f3"])
    out["dn_next3_nonoverlap"]=pd.Series({"n":len(s),"mean":s.f3.mean(),"t":s.f3.mean()/s.f3.std()*np.sqrt(len(s)),"base_f3_mean":d[d.i%3==0].f3.mean()})
    out["base_next1"]=summ(d.groupby(lambda x: "all"),"f1")
    # weekday by year and by coin
    out["wd_year_t"]=d.groupby(["yr","wd"])["f1"].mean().unstack().round(4)
    out["wd_coin"]=d.groupby(["coin","wd"])["f1"].mean().unstack().round(4)
    d["thfr"]=d.wd.isin([3,4])
    out["thfr_vs_rest_year"]=d.groupby(["yr","thfr"])["f1"].mean().unstack().round(4)
    # trades >30d
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr); T["days"]=T.duration_minutes/1440
    T["long30"]=T.days>30
    T["yr"]=pd.to_datetime(T.entry_time).dt.year
    out["long_trades_year"]=T[T.long30].groupby("yr")["net_profit_loss_percent"].agg(["count","mean","median"])
    T["efb"]=pd.cut(T.entry_forecast,[0,5,10,21])
    out["dur_by_entryfc"]=T.groupby(["efb","long30"],observed=True)["net_profit_loss_percent"].agg(["count","mean"])
    return out
