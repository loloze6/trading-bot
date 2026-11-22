import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd20=r1.rolling(20,min_periods=15).std()
            z=r1/sd20
            r20=c/c.shift(20)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"sd20":sd20,"r20":r20,
                             "f5":f5,"f1":f1,"up":(b["regime"]=="trending").astype(int),
                             "fc":b["forecast"].astype(float),
                             "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                             "yr":pd.to_datetime(b["timestamp"]).dt.year,
                             "range":(b["high"]-b["low"])/c,
                             "clv":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    m5=A[A.pos%5==0].groupby("coin")["f5"].mean()
    m1=A.groupby("coin")["f1"].mean()
    A["x5"]=A["f5"]-A["coin"].map(m5)
    A["x1"]=A["f1"]-A["coin"].map(m1)
    G=A[A.pos%5==0].dropna(subset=["x5","z"]).copy()
    G["zb"]=pd.cut(G.z,[-99,-2,-1,0,1,2,99])
    def summ(g,col="x5"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["z bins x regime -> excess 5d"]=G.groupby(["up","zb"],observed=True).apply(summ).round(3)
    G["vb"]=G.groupby("coin")["sd20"].transform(lambda s: pd.qcut(s,3,labels=["lo","mid","hi"]))
    out["vol tercile x regime -> excess 5d"]=G.groupby(["up","vb"],observed=True).apply(summ).round(3)
    G["r20b"]=G.groupby("coin")["r20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["20d return quintile -> excess 5d"]=G.groupby("r20b").apply(summ).round(3)
    G["clvb"]=pd.cut(G.clv,[0,0.2,0.5,0.8,1.0001],include_lowest=True)
    out["close location x z>1 -> excess5"]=G[G.z>1].groupby("clvb",observed=True).apply(summ).round(3)
    out["weekday -> excess 1d"]=A.groupby("wd").apply(lambda g: summ(g,"x1")).round(3)
    out["year x regime -> excess5 z>1"]=G[G.z>1].groupby(["yr","up"]).apply(summ).round(3)
    # slopes by regime
    sl={}
    for u in [0,1]:
        g=G[(G.up==u)&(G.z>0)]
        s=stats.linregress(g.z,g.x5); sl[f"up{u}_zpos"]=(s.slope*100,s.slope/s.stderr,len(g))
        g=G[(G.up==u)&(G.z<0)]
        s=stats.linregress(g.z,g.x5); sl[f"up{u}_zneg"]=(s.slope*100,s.slope/s.stderr,len(g))
    out["slope %per z, t, n"]=pd.DataFrame(sl,index=["slope%","t","n"]).T.round(3)
    # book
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; D.append(dd)
    D=pd.concat(D,ignore_index=True)
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book by window"]=bk.groupby(level=0).agg(["mean","std"]).mul(100).round(3).sort_index(key=lambda s: s.str[1:].astype(int))
    q=bk.book_return.quantile([0.02,0.98])
    out["book tails: coin ret same day"]=pd.DataFrame({
        "worst2%_book":[bk[bk.book_return<=q.iloc[0]].book_return.mean()*100, bk[bk.book_return<=q.iloc[0]].coin_return.mean()*100],
        "best2%_book":[bk[bk.book_return>=q.iloc[1]].book_return.mean()*100, bk[bk.book_return>=q.iloc[1]].coin_return.mean()*100]},index=["book%","coin%"]).round(3)
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): tt=t.copy(); tt["coin"]=coin; T.append(tt)
    T=pd.concat(T,ignore_index=True)
    T["fb"]=pd.cut(T.entry_forecast.astype(float),[0,1,3,8,21])
    out["trades by entry forecast"]=T.groupby(["side","fb"],observed=True)["net_profit_loss_percent"].agg(["count","mean","median"]).round(3)
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean"]).round(3)
    return out
