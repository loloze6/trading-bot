def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    # ---- hourly returns by hour and weekday (pooled, per-coin demeaned by coin's mean over all windows)
    hr_rows = []
    ev_rows = []
    grid_rows = []
    for coin in bars:
        allr = []
        for w, b in bars[coin].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values.astype(float); v = b["volume"].values.astype(float)
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]  # return of next bar after close of bar t
            df = pd.DataFrame({"coin":coin,"w":w,"hour":((ts+pd.Timedelta(hours=1)).dt.hour).values,
                               "wd":((ts+pd.Timedelta(hours=1)).dt.dayofweek).values,"r":r1})
            hr_rows.append(df)
            n = len(c)
            # 48h events at every day-end bar (hour 23) : past 48h ret, next 48h ret, vol ratio
            for i in np.where(ts.dt.hour.values==23)[0]:
                if i-168 < 0 or i+48 >= n: continue
                # check contiguity
                if (ts.iloc[i]-ts.iloc[i-48]) != pd.Timedelta(hours=48) or (ts.iloc[i+48]-ts.iloc[i])!=pd.Timedelta(hours=48): continue
                past = c[i]/c[i-48]-1; nxt = c[i+48]/c[i]-1; nxt24 = c[i+24]/c[i]-1
                vr = v[i-47:i+1].mean()/max(v[i-167:i-47].mean(),1e-12)
                rv = np.std(np.diff(np.log(c[i-167:i+1])))
                ev_rows.append((coin,w,int(ts.iloc[i].dayofweek),past,nxt,nxt24,vr,rv))
            # non-overlapping 24h grid
            for i in range(24, n-24, 24):
                grid_rows.append((coin,w,c[i]/c[i-24]-1, c[i+24]/c[i]-1, np.std(np.diff(np.log(c[max(0,i-168):i+1])))))
    H = pd.concat(hr_rows).dropna()
    H["rd"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    def tt(x): 
        x = np.asarray(x); x=x[~np.isnan(x)]
        return x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan
    g = H.groupby("hour")["rd"].agg(["mean","count"]); g["t"]=H.groupby("hour")["rd"].apply(tt)
    out["hourly ret by UTC hour (demeaned, bps)"] = (g.assign(mean=g["mean"]*1e4)).round(3)
    g = H.groupby("wd")["rd"].agg(["mean","count"]); g["t"]=H.groupby("wd")["rd"].apply(tt)
    out["hourly ret by weekday (demeaned, bps)"] = (g.assign(mean=g["mean"]*1e4)).round(3)
    E = pd.DataFrame(ev_rows, columns=["coin","w","dow","past","nxt","nxt24","vr","rv"])
    # standardize by coin usual 48h move
    sd = E.groupby("coin")["past"].transform("std"); mu = E.groupby("coin")["nxt"].transform("mean")
    E["z"]=E["past"]/sd; E["un"]=(E["nxt"]-mu)/sd
    res=[]
    for d,grp in E.groupby("dow"):
        # non-overlap: one event per day-of-week per week -> independent within dow
        sl,ic,rr,p,se = stats.linregress(grp["z"],grp["un"])
        up=grp[grp.z>0]; dn=grp[grp.z<0]
        res.append((d,len(grp),sl,sl/se,up["un"].mean(),tt(up["un"]),dn["un"].mean(),tt(dn["un"])))
    out["48h past z -> next48 unusual (in usual moves), by day-end dow (6=Sun)"]=pd.DataFrame(res,columns=["dow","n","slope","t_slope","up_mean","t_up","dn_mean","t_dn"]).round(3)
    # Sunday events by vol ratio terciles and sign
    S=E[E.dow==6].copy()
    S["vrq"]=pd.qcut(S["vr"],3,labels=["thin","mid","thick"])
    S["sgn"]=np.sign(S["z"])
    r=[]
    for (q,s),grp in S.groupby(["vrq","sgn"],observed=True):
        r.append((q,s,len(grp),grp["un"].mean(),tt(grp["un"]),np.corrcoef(grp.z,grp.un)[0,1]))
    out["Sunday: vol tercile x sign -> next48 unusual"]=pd.DataFrame(r,columns=["vr","sign","n","mean","t","corr_z"]).round(3)
    # Sunday weekend z quintile
    S["zq"]=pd.qcut(S["z"],5,labels=False)
    out["Sunday weekend z quintile -> next48 unusual"]=S.groupby("zq").agg(n=("un","size"),zmean=("z","mean"),un=("un","mean"),t=("un",tt)).round(3)
    # 24h grid: past 24h z quintile
    G=pd.DataFrame(grid_rows,columns=["coin","w","p","n","rv"])
    s=G.groupby("coin")["p"].transform("std"); m=G.groupby("coin")["n"].transform("mean")
    G["z"]=G.p/s; G["un"]=(G.n-m)/s
    G["zq"]=G.groupby("coin")["z"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["24h grid: past24 z quintile -> next24 unusual"]=G.groupby("zq").agg(n=("un","size"),z=("z","mean"),un=("un","mean"),t=("un",tt)).round(3)
    G["vq"]=G.groupby("coin")["rv"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["24h grid: realized vol quintile -> next24 unusual"]=G.groupby("vq").agg(n=("un","size"),un=("un","mean"),t=("un",tt),slope_corr=("un",lambda x: np.corrcoef(G.loc[x.index,"z"],x)[0,1])).round(3)
    # book: daily returns by weekday
    D=[]
    for coin in days:
        for w,d in days[coin].items():
            dd=d.copy(); dd["wd"]=pd.to_datetime(dd["day"]).dt.dayofweek; dd["coin"]=coin; D.append(dd)
    D=pd.concat(D).dropna(subset=["book_return"])
    out["book daily ret by weekday (bps)"]=D.groupby("wd").agg(book=("book_return",lambda x:x.mean()*1e4),t=("book_return",tt),coin=("coin_return",lambda x:x.mean()*1e4)).round(3)
    T=pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()]) if len(trades) else pd.DataFrame()
    if len(T):
        out["trades by coin"]=T.groupby("coin").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean())).round(3)
    return out
