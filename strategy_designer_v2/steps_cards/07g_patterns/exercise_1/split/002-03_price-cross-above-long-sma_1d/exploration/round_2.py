def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,df in ws.items():
            d=df[["timestamp","close","forecast","postRebalance_current_allocation","postRebalance_total_value"]].copy()
            d["dist"]=df["debug_info.components.above_ma.last_history_value"]
            d["coin"]=c; d["win"]=w
            d["r1"]=d.close.pct_change()
            d["f1"]=d.close.shift(-1)/d.close-1
            d["f5"]=d.close.shift(-5)/d.close-1
            d["f20"]=d.close.shift(-20)/d.close-1
            d["vol20"]=d.r1.rolling(20).std()
            d["mom20"]=d.close/d.close.shift(20)-1
            d["bk"]=d.postRebalance_total_value.pct_change()
            d["on"]=(d.forecast>0).astype(int)
            d["xup"]=(d.on.diff()==1)
            d["xdn"]=(d.on.diff()==-1)
            d["since"]=d.groupby((d.on.diff()!=0).cumsum()).cumcount()
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["ts"]=pd.to_datetime(A.timestamp)
    A["wd"]=A.ts.dt.weekday
    out={}
    tt=lambda x:x.mean()/x.std()*np.sqrt(x.count())
    out["weekday r1 t by coin"]=A.groupby(["coin","wd"]).r1.apply(tt).unstack().round(2)
    out["weekday r1 t by year"]=A.groupby([A.ts.dt.year,"wd"]).r1.apply(tt).unstack().round(2)
    out["bk by weekday on bars"]=A[A.on.shift(1)==1].groupby("wd").agg(bk=("bk","mean"),t=("bk",tt),r1=("r1","mean"))
    out["after cross up"]=pd.Series({"n":A.xup.sum(),"f5":A.loc[A.xup,"f5"].mean(),"f20":A.loc[A.xup,"f20"].mean(),"f20med":A.loc[A.xup,"f20"].median(),"hit20":(A.loc[A.xup,"f20"]>0).mean()})
    out["after cross down"]=pd.Series({"n":A.xdn.sum(),"f5":A.loc[A.xdn,"f5"].mean(),"f20":A.loc[A.xdn,"f20"].mean(),"f20med":A.loc[A.xdn,"f20"].median(),"hit20":(A.loc[A.xdn,"f20"]>0).mean()})
    sb=pd.cut(A.since,[-1,5,20,60,150,1e9])
    out["by days in state"]=A.groupby([A.on,sb]).agg(n=("f20","count"),f20=("f20","mean"),f20med=("f20","median"),hit=("f20",lambda x:(x>0).mean()))
    out["f20 skew by on"]=A.groupby("on").f20.agg(["mean","median","skew",lambda x:x.quantile(.9),lambda x:x.quantile(.1)])
    mb=pd.qcut(A.mom20,5)
    out["mom20 quintile x on"]=A.groupby([mb,"on"]).f20.mean().unstack()
    # book big days
    B=A.dropna(subset=["bk"]).copy()
    B["bkq"]=B.groupby("coin").bk.transform(lambda x:pd.qcut(x.rank(method="first"),[0,.01,.99,1],labels=["worst1%","mid","best1%"]))
    out["around book extremes"]=B.groupby("bkq").agg(n=("bk","count"),bk=("bk","mean"),prev_mom20=("mom20","mean"),vol=("vol20","mean"),dist=("dist","mean"),f5=("f5","mean"),f20=("f20","mean"),wdsat=("wd",lambda x:(x==5).mean()))
    # concentration of book return
    out["top 5% days share of book sum"]=B.groupby("coin").bk.apply(lambda x:x[x>=x.quantile(.95)].sum()/x.sum())
    return out
