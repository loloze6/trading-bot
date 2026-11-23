def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, ws in data["bars"].items():
        # drift: non-overlapping 24h returns, all windows
        g=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-24,24)
            g.append(c[idx+24]/c[idx]-1)
        drift=np.concatenate(g).mean() if g else 0
        usual24=np.concatenate(g).std()
        for w,b in ws.items():
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            ch=((ts.dt.hour+1)%24).values
            r2=c/c.shift(2)-1
            usual=r2.abs().rolling(720,min_periods=200).mean()
            z2=r2/usual
            r168=c/c.shift(168)-1
            r24=c/c.shift(24)-1
            fwd=c.shift(-24)/c-1
            fwd8=c.shift(-8)/c-1
            vol=b["volume"].astype(float)
            vz=vol/vol.rolling(168,min_periods=48).mean()
            vola=c.pct_change().rolling(168,min_periods=100).std()
            df=pd.DataFrame({"coin":coin,"w":w,"ch":ch,"z2":z2,"r168":r168,"r24":r24,
                             "x":(fwd-drift),"x8":fwd8,"u":usual24,"vz":vz,"vola":vola,
                             "wd":ts.dt.weekday.values,"yr":ts.dt.year.values,"pos":np.arange(len(c))})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["z2","r168","x"])
    D["s"]=D["x"]/D["u"]
    out={}
    # by close hour: one sample per day per hour -> non-overlapping 24h
    res=[]
    for h in range(24):
        d=D[D.ch==h]
        a=d[(d.z2<0)&(d.r168>0)]
        sig=(-a.z2)*a.r168
        b2=d[d.z2<0]
        c2=d[d.z2>0]
        res.append({"h":h,"n_sig":len(a),"mean_x_sig":a.x.mean(),"t_sig":stats.ttest_1samp(a.x,0).statistic,
                    "corr_sig":np.corrcoef(sig,a.x)[0,1],
                    "corr_fall_all":np.corrcoef(-b2.z2,b2.x)[0,1],"n_fall":len(b2),
                    "corr_rise_all":np.corrcoef(c2.z2,c2.x)[0,1],
                    "corr_z2_s_all":np.corrcoef(d.z2,d.s)[0,1]})
    out["by_close_hour"]=pd.DataFrame(res).round(4)
    # pooled grid (positions multiple of 24)
    G=D[D.pos%24==0].copy()
    G["q_z24"]=pd.qcut(G.r24/G.u,5,labels=False)
    out["grid_by_24h_ret_quint"]=G.groupby("q_z24").agg(n=("x","size"),mx=("x","mean"),ms=("s","mean"),sd=("x","std")).assign(t=lambda t:t.mx/(t.sd/np.sqrt(t.n))).round(5)
    G["q_168"]=pd.qcut(G.r168,5,labels=False)
    out["grid_by_7d_ret_quint"]=G.groupby("q_168").agg(n=("x","size"),mx=("x","mean"),sd=("x","std")).assign(t=lambda t:t.mx/(t.sd/np.sqrt(t.n))).round(5)
    G["q_vol"]=G.groupby("coin")["vola"].transform(lambda v:pd.qcut(v,5,labels=False,duplicates="drop"))
    G["q_vz"]=pd.qcut(G.vz,5,labels=False,duplicates="drop")
    out["grid_by_vola_quint"]=G.groupby("q_vol").agg(n=("x","size"),mx=("x","mean"),sd=("x","std")).assign(t=lambda t:t.mx/(t.sd/np.sqrt(t.n))).round(5)
    out["grid_by_volume_ratio_quint"]=G.groupby("q_vz").agg(n=("x","size"),mx=("x","mean"),sd=("x","std")).assign(t=lambda t:t.mx/(t.sd/np.sqrt(t.n))).round(5)
    # interaction 24h ret x vol
    G["q2"]=pd.qcut(G.r24/G.u,3,labels=False); G["qv3"]=G.groupby("coin")["vola"].transform(lambda v:pd.qcut(v,3,labels=False,duplicates="drop"))
    out["grid_24hret_x_vola_meanx"]=G.pivot_table(index="q2",columns="qv3",values="s",aggfunc="mean").round(4)
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin
            d["c7"]=d["close"]/d["close"].shift(7)-1
            d["wd"]=pd.to_datetime(d["day"]).dt.weekday
            d["yr"]=pd.to_datetime(d["day"]).dt.year
            dd.append(d)
    DD=pd.concat(dd).dropna(subset=["book_return"])
    out["book_by_weekday"]=DD.groupby("wd").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size")).round(5)
    out["book_by_year"]=DD.groupby("yr").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size")).round(5)
    act=DD[DD.book_return!=0]
    hi=act.book_return.quantile(0.95); lo=act.book_return.quantile(0.05)
    out["book_extremes_prior7d"]=pd.DataFrame({"top5":[act[act.book_return>=hi].c7.mean(),act[act.book_return>=hi].coin_return.mean()],
        "bot5":[act[act.book_return<=lo].c7.mean(),act[act.book_return<=lo].coin_return.mean()],
        "all_active":[act.c7.mean(),act.coin_return.mean()]},index=["prior7d","coin_ret"]).round(4)
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    T["h"]=pd.to_datetime(T["entry_time"]).dt.hour
    out["trades_by_entry_hour"]=T.groupby("h").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur=("duration_minutes","median")).round(3)
    return out
