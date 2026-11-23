def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            ts=pd.to_datetime(b["timestamp"])
            ch=((ts.dt.hour+1)%24).values
            n=len(c)
            def fwd(h):
                r=np.full(n,np.nan); r[:n-h]=c[h:]/c[:n-h]-1; return r
            def back(h):
                r=np.full(n,np.nan); r[h:]=c[h:]/c[:n-h]-1; return r
            lr=np.log(c); r1=np.r_[np.nan,np.diff(lr)]
            vol=pd.Series(r1).rolling(168).std().values
            df=pd.DataFrame({"coin":coin,"w":w,"ch":ch,"wd":ts.dt.weekday.values,
              "f1":fwd(1),"f2":fwd(2),"f4":fwd(4),"f8":fwd(8),"f24":fwd(24),
              "b2":back(2),"b24":back(24),"vol":vol,
              "vz":(b["volume"]/b["volume"].rolling(168).mean()).values,
              "fc":b["forecast"].values,"alloc":b["postRebalance_current_allocation"].values})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    out={}
    # hour of close: 1h fwd return (from that close) mean in bp
    g=D.groupby("ch")["f1"]
    out["f1_by_closehour_bp"]=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()}).round(2)
    # counter-trend pre-move cases at each close hour: signed 2h fwd with 24h trend
    ct=D[(D.b2*D.b24<0)].copy()
    ct["s2"]=np.sign(ct.b24)*ct.f2; ct["s8"]=np.sign(ct.b24)*ct.f8
    g=ct.groupby("ch")["s2"]
    out["countertrend_signed_f2_by_hour_bp"]=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count(),"s8_bp":ct.groupby("ch")["s8"].mean()*1e4}).round(2)
    # reversal of the 2h pre-move itself (any trend), all hours: -sign(b2)*f2
    D["rev2"]=-np.sign(D.b2)*D.f2
    D["b2q"]=D.groupby("coin")["b2"].transform(lambda x:pd.qcut(x.abs(),5,labels=False,duplicates="drop"))
    g=D[D.ch%2==0].groupby("b2q")["rev2"]
    out["reversal_of_2h_move_by_abs_quintile_bp"]=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()}).round(2)
    # 24h momentum on 24h grid
    d24=D[D.ch==0].copy(); d24["s"]=np.sign(d24.b24)*d24.f24
    d24["q"]=d24.groupby("coin")["b24"].transform(lambda x:pd.qcut(x.abs(),5,labels=False,duplicates="drop"))
    g=d24.groupby("q")["s"]
    out["24h_continuation_by_abs24_quintile_bp"]=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()}).round(2)
    # vol regime: hourly abs return by vol tercile; reversal of 2h by vol tercile
    D["vq"]=D.groupby("coin")["vol"].transform(lambda x:pd.qcut(x,3,labels=False,duplicates="drop"))
    g=D[D.ch%2==0].groupby("vq")["rev2"]
    out["rev2_by_vol_tercile_bp"]=pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()}).round(2)
    # volume ratio by close hour
    out["volume_ratio_by_hour"]=D.groupby("ch")["vz"].mean().round(3)
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            x=d.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    DD=pd.concat(dd); DD["wd"]=pd.to_datetime(DD["day"]).dt.weekday
    out["book_by_weekday_bp"]=(DD.groupby("wd")["book_return"].mean()*1e4).round(2)
    out["book_by_coin_bp"]=(DD.groupby("coin")["book_return"].mean()*1e4).round(2)
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades"]=tr.groupby("coin").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur=("duration_minutes","median")).round(3)
    return out
