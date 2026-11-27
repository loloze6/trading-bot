import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; drift={}
    for coin,ws in data["bars"].items():
        drift[coin]=pd.concat([b["close"].astype(float).pct_change().dropna() for b in ws.values()]).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); ts=pd.to_datetime(b["timestamp"])
            r=c.pct_change(); fwd=c.shift(-1)/c-1; f2=c.shift(-2)/c-1
            prevdown=(r.shift(1)<0)
            vol30=r.rolling(30).std()
            tr60=c/c.shift(60)-1
            df=pd.DataFrame({"coin":coin,"win":w,"day":ts.dt.floor("D"),"r":r,"fwd":fwd,"f2":f2,
                "z":r/vol30.shift(1),"tr60":tr60,"prevdown":prevdown,
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "fc":b["forecast"].astype(float),"pos":(c.index%1==0)})
            df["grid2"]=(np.arange(len(df))%2==0)
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["dr"]=d.coin.map(drift); d["ex"]=d.fwd-d.dr; d["ex2"]=d.f2-2*d.dr
    d=d.dropna(subset=["fwd","z","tr60"])
    d["trend"]=pd.cut(d.tr60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    def summ(g,col="ex"):
        g=g.dropna(subset=[col]); s=g.groupby("day")[col].sum()
        t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
        return pd.Series({"n":len(g),"days":len(s),"mean":g[col].mean(),"t_day":t})
    out={}
    up=d[d.r>0].copy()
    up["zq"]=up.groupby("trend").z.transform(lambda x:pd.qcut(x,4,labels=False))
    out["upday_by_trend_zq"]=up.groupby(["trend","zq","prevdown"]).apply(summ).round(4)
    reg=[]
    for tr in ["falling","choppy","rising"]:
        for pdn in [True,False]:
            g=up[(up.trend==tr)&(up.prevdown==pdn)]
            s=stats.linregress(g.z,g.fwd)
            reg.append({"trend":tr,"prevdown":pdn,"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    out["reg_fwd_on_upz"]=pd.DataFrame(reg).round(4)
    dn=d[d.r<0].copy()
    dn["zq"]=dn.groupby("trend").z.transform(lambda x:pd.qcut(x,4,labels=False))
    out["downday_by_trend_zq"]=dn.groupby(["trend","zq"]).apply(summ).round(4)
    fu=up[(up.trend=="falling")&(up.grid2)]
    fu["zq"]=pd.qcut(fu.z,3,labels=False)
    out["fall_up_2d_grid"]=fu.groupby("zq").apply(lambda g:summ(g,"ex2")).round(4)
    # book: position and gain by trend
    d["gain"]=d.alloc*d.fwd
    out["book_by_trend"]=d.groupby("trend").agg(n=("gain","size"),inpos=("alloc",lambda x:(x!=0).mean()),
        meanalloc=("alloc","mean"),gain_sum=("gain","sum")).round(5)
    act=d[d.alloc!=0]
    out["alloc_stats"]=act.alloc.describe().round(4)
    return out
