import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd=r1.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"win":w,
                "prof":(b["regime"]=="unknown").values,
                "z3":(c/c.shift(3)-1)/sd,"z1":r1/sd,
                "rng":((b["high"]-b["low"])/c)/sd,
                "clv":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "f5":c.shift(-5)/c-1,"f1":c.shift(-1)/c-1,
                "z10":(c/c.shift(10)-1)/sd,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos":np.arange(len(b)),
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    g=D[D.pos%5==0].copy()
    drift=g.groupby("coin")["f5"].mean(); usual=g.groupby("coin")["f5"].std()
    g["u5"]=g["f5"]-g["coin"].map(drift); g["s5"]=g["u5"]/g["coin"].map(usual)
    def tab(df,col,q=5):
        df=df.dropna(subset=[col,"u5"]).copy()
        df["b"]=pd.qcut(df[col],q,labels=False,duplicates="drop")
        def f(x):
            dd=x.groupby("day")["u5"].sum()
            return pd.Series({"n":len(x),"days":len(dd),"mean_u5":x.u5.mean(),"strength":x.s5.mean(),
                              "t_day":dd.mean()/(dd.std()/np.sqrt(len(dd))) if len(dd)>2 else np.nan})
        return df.groupby(["prof","b"]).apply(f)
    out={}
    out["z3 quintile by profile -> unusual 5d"]=tab(g,"z3")
    out["z10 quintile by profile"]=tab(g,"z10")
    out["range(scaled) quintile by profile"]=tab(g,"rng")
    out["close location quintile by profile"]=tab(g,"clv")
    # one-day
    D2=D.dropna(subset=["f1"]).copy()
    m1=D2.groupby("coin")["f1"].mean(); D2["u1"]=D2.f1-D2.coin.map(m1)
    out["weekday next-day unusual by profile"]=D2.groupby(["prof","wd"])["u1"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    # book
    days=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd.copy(); x["coin"]=coin; x["win"]=w; days.append(x)
    DY=pd.concat(days)
    bk=DY.groupby(["win","day"])["book_return"].mean().dropna()
    out["book by window"]=bk.groupby(level=0).agg(["count","mean","std","sum"])
    pos=D[D.alloc.abs()>0]
    out["position share, in profile share"]=pd.Series({"bars_in_pos":len(pos),"share_short":(pos.alloc<0).mean(),"prof_share_all":D.prof.mean()})
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): tt=t.copy(); tt["coin"]=coin; tr.append(tt)
    T=pd.concat(tr)
    T["ef"]=pd.qcut(T.entry_forecast.astype(float),4,labels=False,duplicates="drop")
    out["trades by entry forecast quartile"]=T.groupby("ef")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
