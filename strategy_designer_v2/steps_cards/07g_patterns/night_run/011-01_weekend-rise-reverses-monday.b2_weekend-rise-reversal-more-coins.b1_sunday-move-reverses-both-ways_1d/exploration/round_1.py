def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            sc=r.abs().shift(1).rolling(60,min_periods=20).mean()
            z=r/sc
            vr=v/v.shift(1).rolling(30,min_periods=10).median()
            vol20=r.rolling(20,min_periods=10).std()
            f1=c.shift(-1)/c-1
            f2=c.shift(-2)/c-1
            r7=c/c.shift(7)-1
            ts=pd.to_datetime(b["timestamp"],utc=True)
            d=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.dayofweek,"year":ts.dt.year,"z":z,"r":r,"f1":f1,"f2":f2,"vr":vr,"vol20":vol20,"r7":r7,"pos":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # excess over coin mean daily return
    cm=D.groupby("coin")["f1"].transform("mean")
    D["x1"]=D["f1"]-cm
    def slope(g,y="x1",x="z"):
        g=g[[x,y]].dropna()
        if len(g)<30: return pd.Series({"n":len(g)})
        res=stats.linregress(g[x],g[y])
        return pd.Series({"n":len(g),"slope_bp":res.slope*1e4,"t":res.slope/res.stderr})
    out={}
    out["next1d_on_z_by_signal_weekday(0=Mon)"]=D.groupby("wd").apply(slope)
    out["mean_ret_by_weekday_bp"]=D.groupby("wd").agg(n=("r","count"),mean_bp=("r",lambda s:s.mean()*1e4),t=("r",lambda s:s.mean()/s.std()*np.sqrt(s.count())))
    # sunday by volume tercile
    S=D[D.wd==6].dropna(subset=["z","x1","vr"]).copy()
    S["vq"]=pd.qcut(S["vr"],3,labels=["lowvol","mid","highvol"])
    out["sunday_slope_by_relvolume"]=S.groupby("vq").apply(slope)
    # all days by vol20 tercile
    A=D.dropna(subset=["z","x1","vol20"]).copy()
    A["volq"]=A.groupby("coin")["vol20"].transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    out["allday_slope_by_volterc"]=A.groupby("volq").apply(slope)
    out["sunday_slope_by_year"]=D[D.wd==6].groupby("year").apply(slope)
    # r7 momentum on 7-day grid
    G=D[D.pos%7==0].copy(); G["f7"]=np.nan
    rows2=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b.sort_values("timestamp")["close"].astype(float).reset_index(drop=True)
            idx=np.arange(7,len(c)-7,7)
            for i in idx:
                rows2.append((coin,c[i]/c[i-7]-1,c[i+7]/c[i]-1))
    M=pd.DataFrame(rows2,columns=["coin","r7","f7"])
    M["f7x"]=M["f7"]-M.groupby("coin")["f7"].transform("mean")
    M["z7"]=M["r7"]/M.groupby("coin")["r7"].transform("std")
    out["weekly_f7_on_z7"]=slope(M,"f7x","z7").to_frame().T
    # book by weekday
    br=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["wd"]=pd.to_datetime(dd["day"]).dt.dayofweek; br.append(dd)
    B=pd.concat(br)
    out["book_ret_by_weekday_bp"]=B.groupby("wd")["book_return"].agg(lambda s:s.mean()*1e4)
    return out
