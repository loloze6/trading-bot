def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["regime"]=b["regime"].values
            d["r30"]=c/c.shift(30)-1
            d["r5"]=c/c.shift(5)-1
            lr=np.log(c).diff()
            d["v30"]=lr.rolling(30).std()
            for h in (5,10,20): d[f"f{h}"]=c.shift(-h)/c-1
            d["pos"]=np.arange(len(b))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["day"]=D.ts.dt.floor("D"); D["year"]=D.ts.dt.year; D["wd"]=D.ts.dt.dayofweek
    vmed=D.groupby("coin")["v30"].median()
    D["agit"]=D["v30"]>D["coin"].map(vmed)
    def ct(x,col):
        x=x.dropna(subset=[col])
        if len(x)<5: return pd.Series({"n":len(x)})
        m=x[col].mean(); s=(x[col]-m).groupby(x["day"]).sum(); G=len(s)
        se=np.sqrt((s**2).sum()*G/(G-1))/len(x)
        return pd.Series({"n":len(x),"days":G,"mean":m,"median":x[col].median(),"t":m/se if se>0 else np.nan})
    out={}
    for h in (5,10,20):
        g=D[D.pos%h==0].dropna(subset=[f"f{h}"]).copy()
        g["u"]=g[f"f{h}"]-g.coin.map(g.groupby("coin")[f"f{h}"].mean())
        ch=g[(g.regime=="chop")].dropna(subset=["r30"]).copy()
        ch["q"]=pd.qcut(ch.r30,5,labels=False)
        out[f"chop_r30_q_h{h}"]=ch.groupby("q").apply(ct,col="u")
        if h==10:
            ch["ag"]=ch.agit.map({True:"agit",False:"calm"})
            ch["side"]=np.where(ch.r30<0,"fall","rise")
            ch["su"]=np.where(ch.r30<0,-1,1)*ch.u
            # within side, terciles of |r30|
            ch["t3"]=ch.groupby("side")["r30"].transform(lambda s: pd.qcut(s.abs(),3,labels=False))
            out["chop_side_tercile_signed"]=ch.groupby(["side","t3"]).apply(ct,col="su")
            out["chop_side_agit_signed"]=ch.groupby(["side","ag"]).apply(ct,col="su")
            ch["q5"]=pd.qcut(ch.r5,3,labels=False)
            ch["q30"]=pd.qcut(ch.r30,3,labels=False)
            out["chop_r30t_x_r5t_u"]=ch.groupby(["q30","q5"]).apply(ct,col="u")
            out["chop_fall_by_coin"]=ch[ch.side=="fall"].groupby("coin").apply(ct,col="su")
            out["all_weekday_u"]=g.groupby("wd").apply(ct,col="u")
    tr=[]
    for coin,wd in data["trades"].items():
        for w,t in wd.items():
            x=t.copy(); x["coin"]=coin; tr.append(x)
    T=pd.concat(tr,ignore_index=True)
    T["fq"]=pd.qcut(T.entry_forecast.abs().rank(method="first"),3,labels=False)
    out["trades_by_forecast_tercile"]=T.groupby("fq").agg(n=("net_profit_loss_percent","size"),mean=("net_profit_loss_percent","mean"),med=("net_profit_loss_percent","median"),win=("net_profit_loss_percent",lambda s:(s>0).mean()))
    T["dur"]=T.duration_minutes/1440
    out["trades_dur"]=T.dur.describe()
    return out
