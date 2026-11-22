import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; hr=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r1=c.pct_change()
            typ=r1.abs().shift(1).rolling(720,min_periods=200).mean()
            vr=b["volume"]/b["volume"].shift(1).rolling(720,min_periods=200).mean()
            z=r1/typ
            r24=c.shift(1)/c.shift(25)-1
            f6=c.shift(-6)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"],utc=True)
            df=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"r24":r24,"f6":f6,"f1":f1,
                             "hour":ts.dt.hour,"wd":ts.dt.weekday,"typ":typ,
                             "alloc":b["postRebalance_current_allocation"]})
            df["grid"]=(np.arange(len(df))%6==0)
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    g=d[d.grid].dropna(subset=["f6","z","vr"]).copy()
    drift=g.groupby("coin")["f6"].mean()
    g["u6"]=g["f6"]-g["coin"].map(drift)
    g["zb"]=pd.cut(g["z"],[-99,-4,-2.5,-1.5,1.5,2.5,4,99])
    g["vb"]=pd.cut(g["vr"],[0,0.67,1.5,3,999])
    def agg(x):
        n=len(x); m=x.mean(); s=x.std()
        return pd.Series({"n":n,"mean_bp":m*1e4,"t":m/(s/np.sqrt(n)) if n>2 else np.nan})
    zv=g.groupby(["zb","vb"],observed=True)["u6"].apply(agg).unstack()
    # unusual move signed in direction of the hour's move (continuation)
    g["cont"]=np.sign(g["z"])*g["u6"]
    big=g[g["z"].abs()>2.5]
    contv=big.groupby("vb",observed=True)["cont"].apply(agg).unstack()
    # by realised vol level (typ quintile within coin)
    g["volq"]=g.groupby("coin")["typ"].transform(lambda s: pd.qcut(s,5,labels=False))
    volq=g.groupby("volq")["u6"].apply(agg).unstack()
    # prior 24h return quintile -> next 6h
    g["r24q"]=g.groupby("coin")["r24"].transform(lambda s: pd.qcut(s,5,labels=False))
    r24q=g.groupby("r24q")["u6"].apply(agg).unstack()
    # hour of day, 1h returns all bars
    h=d.dropna(subset=["f1"]).copy()
    h["u1"]=h["f1"]-h["coin"].map(h.groupby("coin")["f1"].mean())
    hour=h.groupby("hour")["u1"].apply(agg).unstack()
    # book days by weekday
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; dd.append(x)
    dd=pd.concat(dd); dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday
    bw=dd.groupby("wd")[["book_return","coin_return"]].mean()*1e4
    # trades
    tr=[]
    for coin,ws in data["trades"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; tr.append(x)
    tr=pd.concat(tr)
    tr["eh"]=pd.to_datetime(tr["entry_time"],utc=True).dt.hour
    tr["dur_h"]=tr["duration_minutes"]/60
    tr["durb"]=pd.cut(tr["dur_h"],[0,6.5,12,24,1e4])
    tsum=tr.groupby("durb",observed=True).agg(n=("net_profit_loss_percent","size"),
        gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    return {"u6 by z-bin x vol-bin":zv,"continuation |z|>2.5 by vol":contv,
            "u6 by vol quintile":volq,"u6 by prior24h quintile":r24q,
            "u1 by hour":hour,"book/coin daily bp by weekday":bw,"trades by duration":tsum}
