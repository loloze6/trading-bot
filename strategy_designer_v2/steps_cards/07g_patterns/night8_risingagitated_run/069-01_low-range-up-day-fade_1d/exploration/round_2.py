import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            r1=c.pct_change()
            hh=h.rolling(20).max(); ll=l.rolling(20).min()
            pos=(c-ll)/(hh-ll)
            vol30=r1.rolling(30).std()
            volpct=vol30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"day":ts.dt.floor("D"),
                "r1":r1,"pos":pos,"nxt":c.shift(-1)/c-1,"nxt2":c.shift(-2)/c-1,
                "tr60":c/c.shift(60)-1,"vp":volpct,"bk":b["postRebalance_total_value"].shift(-1)/b["postRebalance_total_value"]-1,
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    d=pd.concat(rows)
    d["ex"]=d["nxt"]-d.groupby("coin")["nxt"].transform("mean")
    d["ex2"]=d["nxt2"]-d.groupby("coin")["nxt2"].transform("mean")
    d=d.dropna(subset=["r1","pos","ex"])
    d["prof"]=np.where(d.tr60>0.1,"rising",np.where(d.tr60<-0.1,"falling","choppy"))
    d["ag"]=np.where(d.vp>0.5,"agit","calm"); d.loc[d.vp.isna(),"ag"]="na"
    def tday(g,col="ex"):
        g=g.dropna(subset=[col]); x=g[col]; m=x.mean()
        dev=(x-m).groupby(g["day"]).sum(); G=len(dev)
        se=np.sqrt((dev**2).sum()*G/(G-1))/len(g) if G>1 else np.nan
        return pd.Series({"n":len(g),"days":G,"mean%":m*100,"t":m/se})
    out={}
    up=d[d.r1>0].copy(); dn=d[d.r1<0].copy()
    up["q"]=pd.qcut(up.pos,5,labels=False); dn["q"]=pd.qcut(dn.pos,5,labels=False)
    lu=up[up.q<=1]
    out["lowup_trend_x_agit"]=lu.groupby(["prof","ag"]).apply(tday)
    out["lowup_2day"]=lu.groupby("prof").apply(lambda g:tday(g,"ex2"))
    nr=up[up.prof!="rising"]
    out["up_notrising_by_posquint"]=nr.groupby("q").apply(tday)
    out["up_rising_by_posquint"]=up[up.prof=="rising"].groupby("q").apply(tday)
    hd=dn[dn.q>=3]
    out["highdown_trend_x_agit"]=hd.groupby(["prof","ag"]).apply(tday)
    out["highdown_by_window_sign"]=pd.Series({"pos_windows":int((hd.groupby("w")["ex"].mean()>0).sum()),"windows":hd.w.nunique()})
    out["lowup_by_window_sign_notrising"]=pd.Series({"neg_windows":int((lu[lu.prof!="rising"].groupby("w")["ex"].mean()<0).sum()),"windows":lu.w.nunique()})
    out["lowup_by_coin"]=lu[lu.prof!="rising"].groupby("coin").apply(tday)
    sh=d[d.alloc<0]
    out["book_short_bar_gain_by_prof"]=sh.groupby("prof")["bk"].agg(["count","mean"])
    return out
