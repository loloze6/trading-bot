def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20,min_periods=15).std()
            z=r1/vol
            ret30=c/c.shift(30)-1
            ret10=c/c.shift(10)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            rng=(b["high"]-b["low"])/c
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"vol":vol,"ret30":ret30,"ret10":ret10,
                            "f5":f5,"f1":f1,"rng":rng,"wd":ts.dt.weekday,"yr":ts.dt.year,"fc":b["forecast"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    g=D[D.pos%5==0].copy()
    drift5=g.groupby("coin")["f5"].mean(); sd5=g.groupby("coin")["f5"].std()
    g["u5"]=g["f5"]-g.coin.map(drift5); g["s5"]=g["u5"]/g.coin.map(sd5)
    drift1=D.groupby("coin")["f1"].mean()
    D["u1"]=D["f1"]-D.coin.map(drift1)
    def summ(df,col,key):
        o=df.dropna(subset=[col,key]).groupby(key)[col].agg(["mean","count","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"])); return o.drop(columns="std")
    g["zb"]=pd.cut(g.z,[-99,-2,-1,1,2,99])
    D["zb"]=pd.cut(D.z,[-99,-2,-1,1,2,99])
    g["trend"]=np.where(g.ret30<0,"down30","up30")
    g["vq"]=g.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    g["r30q"]=g.groupby("coin")["ret30"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    g["r10q"]=g.groupby("coin")["ret10"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    g["rngq"]=g.groupby("coin")["rng"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out={}
    out["u5 by z bin"]=summ(g,"u5","zb")
    out["u5 by z bin x trend30"]=g.dropna(subset=["u5","zb"]).groupby(["trend","zb"])["u5"].agg(["mean","count"])
    out["u1 by z bin"]=summ(D,"u1","zb")
    out["u5 by vol tercile"]=summ(g,"u5","vq")
    out["u5 by ret30 quintile"]=summ(g,"u5","r30q")
    out["u5 by ret10 quintile"]=summ(g,"u5","r10q")
    out["u5 by range quintile"]=summ(g,"u5","rngq")
    out["u1 by weekday"]=summ(D,"u1","wd")
    out["u5 by year"]=summ(g,"u5","yr")
    # graded regressions
    res={}
    for k in ["ret30","ret10","z","rng"]:
        s=g.dropna(subset=[k,"s5"]); lr=stats.linregress(s[k],s["s5"]); res[k]=[lr.slope,lr.slope/lr.stderr,len(s)]
    out["s5 on x slope,t,n"]=pd.DataFrame(res,index=["slope","t","n"]).T
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): tr.append(t.assign(coin=coin))
    T=pd.concat(tr)
    out["trades"]=T.groupby("coin")["net_profit_loss_percent"].agg(["mean","count","median"])
    return out
