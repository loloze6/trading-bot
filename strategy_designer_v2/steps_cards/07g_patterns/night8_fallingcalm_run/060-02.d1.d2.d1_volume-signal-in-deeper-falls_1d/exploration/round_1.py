def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; v=b["volume"].values; n=len(b)
            s=pd.Series(c); vs=pd.Series(v)
            ret20=s/s.shift(20)-1; ret60=s/s.shift(60)-1
            m30=vs.rolling(30).mean(); lv=np.log(m30/m30.shift(30))
            r1=s.pct_change()
            sd30=r1.rolling(30).std()
            ag=sd30/sd30.rolling(60,min_periods=30).median()
            for i in range(0,n-H,H):
                fr=c[i+H]/c[i]-1
                rows.append(dict(coin=coin,w=w,i=i,fr=fr,ret20=ret20[i],ret60=ret60[i],lv=lv[i],
                    r1=r1[i],ag=ag[i],fc=b["forecast"].iloc[i],wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                    day=str(pd.Timestamp(b["timestamp"].iloc[i]).date())))
    d=pd.DataFrame(rows)
    d["ex"]=d["fr"]-d.groupby("coin")["fr"].transform("mean")
    out={}
    def tab(g,col="ex"):
        a=g[col].dropna()
        return pd.Series(dict(n=len(a),mean=a.mean(),t=a.mean()/(a.std()/np.sqrt(len(a))) if len(a)>2 else np.nan))
    # 1 in-position cases by side
    ip=d[d.fc!=0].copy(); ip["sx"]=ip.ex*np.sign(ip.fc)
    ip["side"]=np.where(ip.fc>0,"long","short")
    out["side_signed"]=ip.groupby("side").apply(lambda g:tab(g,"sx"))
    ip["fq"]=pd.qcut(ip.fc,5,labels=False,duplicates="drop")
    out["fc_quint_raw_ex"]=ip.groupby("fq").apply(tab)
    # 2 volume change vs fwd return by trend bucket
    d["tr"]=pd.cut(d.ret60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    d["lvq"]=d.groupby("tr")["lv"].transform(lambda x:pd.qcut(x,3,labels=False,duplicates="drop"))
    out["trend_x_lvtercile"]=d.groupby(["tr","lvq"]).apply(tab).unstack()
    # correlation lv vs ex by trend & by ret20 bins
    d["r20b"]=pd.cut(d.ret20,[-9,-0.25,-0.1,0,0.1,0.25,99])
    def cor(g):
        g=g[["lv","ex"]].dropna()
        if len(g)<10: return pd.Series(dict(n=len(g),r=np.nan,t=np.nan))
        r=g.corr().iloc[0,1]; return pd.Series(dict(n=len(g),r=r,t=r*np.sqrt((len(g)-2)/(1-r*r))))
    out["lv_ex_corr_by_ret20"]=d.groupby("r20b").apply(cor)
    out["lv_ex_corr_by_trend_ag"]=d.assign(agb=np.where(d.ag>1,"agit","calm")).groupby(["tr","agb"]).apply(cor)
    # 3 ret20 alone vs fwd by trend
    out["ret20bin_ex"]=d.groupby("r20b").apply(tab)
    # 4 after large daily moves
    d["r1b"]=pd.qcut(d.r1,5,labels=False)
    out["r1quint_x_trend"]=d.groupby(["tr","r1b"]).apply(tab)["mean"].unstack()
    out["weekday"]=d.groupby("wd").apply(tab)
    # 5 book daily: long vs short contributions, by window
    bl=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            a=b["postRebalance_current_allocation"].shift(1); r=b["close"].pct_change()
            bl.append(pd.DataFrame(dict(w=w,g=a*r,side=np.sign(a))))
    bl=pd.concat(bl).dropna()
    out["bar_gain_by_side"]=bl.groupby("side")["g"].agg(["count","mean","sum"])
    out["bar_gain_by_window"]=bl[bl.side!=0].groupby("w")["g"].agg(["count","mean","sum"])
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades_side"]=tr.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median","std"])
    return out
