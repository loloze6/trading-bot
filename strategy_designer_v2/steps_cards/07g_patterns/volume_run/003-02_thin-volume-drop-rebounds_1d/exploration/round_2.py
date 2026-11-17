def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20).std()
            z=r1/vol.shift(1)
            vr=v/v.rolling(30).mean()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"vr":vr,"r1":r1,
                            "f5":c.shift(-5)/c-1,"f3":c.shift(-3)/c-1,"f10":c.shift(-10)/c-1,
                            "wd":ts.dt.weekday,"yr":ts.dt.year,"wn":int(w[1:])})
            rows.append(d)
    D=pd.concat(rows)
    out={}
    def tt(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    # weekday: the day's own return (r1 on bar with start weekday wd)
    R=D.dropna(subset=["r1"])
    mcoin=R.groupby("coin")["r1"].mean()
    R=R.assign(xr=R.r1-R.coin.map(mcoin))
    out["wd_own_ret"]=R.groupby("wd")["xr"].apply(tt).unstack()
    R["half"]=np.where(R.yr<=2021,"early","late")
    out["wd_by_half"]=R.groupby(["half","wd"])["xr"].apply(tt).unstack()
    out["wd_by_coin_t"]=R.groupby(["coin","wd"])["xr"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x)))).unstack()
    # weekend vs weekday vol
    out["wd_absret"]=R.groupby("wd")["r1"].apply(lambda x:x.abs().mean())
    # up-move continuation, multiple horizons, non-overlapping
    for h,col in [(3,"f3"),(5,"f5"),(10,"f10")]:
        G=D[D.pos%h==0].dropna(subset=["z",col]).copy()
        m=G.groupby("coin")[col].mean()
        G["x"]=G[col]-G.coin.map(m)
        G["zb"]=pd.cut(G.z,[-99,-2,-1,0,1,2,99])
        out[f"z_h{h}"]=G.groupby("zb")["x"].apply(tt).unstack()
    G=D[D.pos%5==0].dropna(subset=["z","f5","vr"]).copy()
    m=G.groupby("coin")["f5"].mean(); G["x"]=G.f5-G.coin.map(m)
    U=G[G.z>1]
    out["up_by_coin"]=U.groupby("coin")["x"].apply(tt).unstack()
    out["up_by_half"]=U.groupby(np.where(U.yr<=2021,"early","late"))["x"].apply(tt).unstack()
    sl=stats.linregress(U.z,U.x); out["up_slope_z"]=pd.Series({"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(U)})
    sl2=stats.linregress(np.log(U.vr),U.x); out["up_slope_logvr"]=pd.Series({"slope":sl2.slope,"t":sl2.slope/sl2.stderr})
    slall=stats.linregress(G.z,G.x); out["all_slope_z"]=pd.Series({"slope":slall.slope,"t":slall.slope/slall.stderr,"n":len(G)})
    # volume ratio alone
    G["vq"]=pd.qcut(G.vr,5,labels=False)
    out["vr_quint_x5"]=G.groupby("vq")["x"].apply(tt).unstack()
    out["vr_quint_x5_up"]=G[G.r1>0].groupby("vq")["x"].apply(tt).unstack()
    out["vr_quint_x5_down"]=G[G.r1<0].groupby("vq")["x"].apply(tt).unstack()
    return out
