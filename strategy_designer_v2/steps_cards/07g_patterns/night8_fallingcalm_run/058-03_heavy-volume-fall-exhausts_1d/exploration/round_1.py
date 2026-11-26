def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            n=len(b)
            r1=c.pct_change()
            r30=c/c.shift(30)-1
            r60=c/c.shift(60)-1
            r5=c/c.shift(5)-1
            vol30=r1.rolling(30).std()
            fwd5=c.shift(-5)/c-1
            fwd2=c.shift(-2)/c-1
            vr=b.get("debug_info.components.vol30_vs_year.last_history_value")
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n,5):
                if i+5>=n: continue
                rows.append(dict(coin=coin,w=w,reg=b["regime"].iloc[i],r30=r30.iloc[i],r60=r60.iloc[i],r5=r5.iloc[i],
                    r1=r1.iloc[i],vol30=vol30.iloc[i],fwd5=fwd5.iloc[i],fwd2=fwd2.iloc[i],
                    vr=(vr.iloc[i] if vr is not None else np.nan),fc=b["forecast"].iloc[i],
                    wd=ts.iloc[i].dayofweek,yr=ts.iloc[i].year))
    d=pd.DataFrame(rows)
    d["fc_prof"]=d["reg"].isin(["mean_reversion","unknown"])
    out={}
    out["regime counts"]=d["reg"].value_counts()
    def reg(x,col,y="fwd5"):
        x=x[[col,y]].dropna()
        if len(x)<20: return pd.Series({"n":len(x)})
        s=stats.linregress(x[col],x[y])
        q=pd.qcut(x[col],3,labels=False,duplicates="drop")
        m=x.groupby(q)[y].mean()
        return pd.Series({"n":len(x),"slope":s.slope,"t":s.slope/s.stderr,"corr":s.rvalue,
                          "lowT_mean":m.iloc[0],"midT_mean":m.iloc[1] if len(m)>2 else np.nan,"highT_mean":m.iloc[-1]})
    t={}
    for name,sub in [("fallcalm",d[d.fc_prof]),("fallcalm r30<0",d[d.reg=="mean_reversion"]),("other",d[~d.fc_prof]),("all",d)]:
        for col in ["r30","r60","r5","r1","vol30"]:
            t[(name,col)]=reg(sub,col)
    out["fwd5 on situation by profile"]=pd.DataFrame(t).T
    mr=d[d.reg=="mean_reversion"]
    out["mr vr vs fwd5"]=reg(mr,"vr")
    # interaction: deep fall x volume
    x=mr.dropna(subset=["r30","vr"]).copy()
    x["deep"]=x.r30<x.r30.median(); x["heavy"]=x.vr>x.vr.median()
    out["mr deep x heavy fwd5"]=x.groupby(["deep","heavy"])["fwd5"].agg(["mean","count","std"])
    # other profiles: by r60 bins
    o=d.dropna(subset=["r60","fwd5"]).copy()
    o["tb"]=pd.cut(o.r60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    o["vb"]=pd.qcut(o.vol30,2,labels=["lowvol","highvol"])
    g=o.groupby(["tb","vb"])["fwd5"].agg(["mean","count","std"])
    g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["fwd5 by trend x vol(inwindow)"]=g
    # by window in falling calm
    g=d[d.fc_prof].groupby("w")["fwd5"].agg(["mean","count"])
    out["fallcalm fwd5 by window"]=g
    g=d.groupby("wd")["fwd5"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["fwd5 by weekday"]=g
    # after large daily moves (all bars, fwd2 non overlapping grid of 5 fine)
    o=d.dropna(subset=["r1","vol30"]).copy(); o["z"]=o.r1/o.vol30
    o["zb"]=pd.cut(o.z,[-99,-2,-1,1,2,99])
    g=o.groupby("zb")[["fwd2","fwd5"]].agg(["mean","count"])
    out["after daily z move"]=g
    return out
