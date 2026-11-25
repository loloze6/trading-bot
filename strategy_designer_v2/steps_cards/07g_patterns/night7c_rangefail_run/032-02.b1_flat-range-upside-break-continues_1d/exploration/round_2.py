def explore(data):
    import numpy as np, pandas as pd
    H=5
    ev=[]; grid=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float)
            n=len(b)
            er=(c-c.shift(60)).abs()/c.diff().abs().rolling(60).sum()
            ph=hi.shift(1).rolling(60).max(); pl=lo.shift(1).rolling(60).min()
            mr=(hi-lo).rolling(60).mean()
            up=((c-ph)/mr); dn=((pl-c)/mr)
            r20=c/c.shift(20)-1
            r60=c/c.shift(60)-1
            pos=(c-pl)/(ph-pl)
            fwd=c.shift(-H)/c-1
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            for s in range(0,n,H):
                if s+H>=n: break
                grid.append(dict(coin=coin,w=w,fwd=fwd[s],r20=r20[s],r60=r60[s],pos=pos[s],er=er[s],day=day[s]))
                for side,x in (("up",up),("dn",dn)):
                    seg=[i for i in range(s,min(s+H,n-H)) if x[i]>0]
                    if seg:
                        i=seg[0]
                        ev.append(dict(coin=coin,w=w,side=side,mag=x[i],er=er[i],fwd=fwd[i],day=day[i],r60=r60[i]))
    g=pd.DataFrame(grid); e=pd.DataFrame(ev)
    drift=g.groupby("coin")["fwd"].mean()
    g["un"]=g["fwd"]-g["coin"].map(drift); e["un"]=e["fwd"]-e["coin"].map(drift)
    def summ(x):
        x=x.dropna(subset=["un"])
        if len(x)<3: return pd.Series({"n":len(x),"mean":x["un"].mean() if len(x) else np.nan,"t":np.nan,"days":x["day"].nunique()})
        m=x["un"].mean(); dsum=(x["un"]-m).groupby(x["day"]).sum(); D=len(dsum)
        se=np.sqrt((dsum**2).sum()*D/(D-1))/len(x)
        return pd.Series({"n":len(x),"mean":m,"t":m/se,"days":D})
    out={}
    e=e.dropna(subset=["er"])
    e["erb"]=pd.cut(e["er"],[0,0.2,0.3,0.45,1.01])
    out["events_side_er"]=e.groupby(["side","erb"]).apply(summ)
    for side in ("up","dn"):
        s=e[e["side"]==side].copy()
        s["mb"]=pd.qcut(s["mag"],3,duplicates="drop")
        out["mag_"+side]=s.groupby("mb").apply(summ)
        out["byyear_"+side]=s.groupby(s["day"].dt.year).apply(summ)
    out["slope_up_all"]=float(np.polyfit(e[e.side=="up"]["mag"],e[e.side=="up"]["un"],1)[0])
    gg=g.dropna(subset=["r20","pos"]).copy()
    gg["q20"]=pd.qcut(gg["r20"],5,labels=False)
    out["r20_quint"]=gg.groupby("q20").apply(summ)
    gg["qpos"]=pd.qcut(gg["pos"],5,labels=False)
    out["rangepos_quint"]=gg.groupby("qpos").apply(summ)
    gg["q60"]=pd.qcut(gg["r60"],5,labels=False)
    out["r60_quint"]=gg.groupby("q60").apply(summ)
    gg["wd"]=gg["day"].dt.dayofweek
    out["weekday_byyear_midweek"]=gg[gg.wd.isin([2,3])].groupby(gg["day"].dt.year).apply(summ)
    # book trades
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr) if tr else pd.DataFrame()
    if len(T):
        T["fb"]=pd.qcut(T["entry_forecast"],3,duplicates="drop")
        out["trades_by_entryfc"]=T.groupby("fb")["net_profit_loss_percent"].agg(["count","mean","median"])
        out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","sum"])
        out["trades_dur_days"]=T["duration_minutes"].describe()/1440
    return out
