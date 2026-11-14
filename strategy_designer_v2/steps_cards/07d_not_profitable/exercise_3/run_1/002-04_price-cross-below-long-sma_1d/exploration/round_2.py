import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; drows=[]
    for coin,ws in data["bars"].items():
        allr=[pd.Series(b["close"].values).pct_change().dropna() for b in ws.values()]
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            dist=b.get("debug_info.components.below_ma.last_history_value")
            if dist is None: continue
            sma=c/(1+dist/100)
            slope20=sma/sma.shift(20)-1
            alloc=b["postRebalance_current_allocation"]
            past30=c/c.shift(30)-1
            hi60=c.rolling(60,min_periods=20).max()
            dd60=c/hi60-1
            for i in range(0,len(b)-10,10):
                r=c.iloc[i+10]/c.iloc[i]-1
                rows.append(dict(coin=coin,w=w,alloc=alloc.iloc[i],ex=r-10*mu,slope=slope20.iloc[i],
                                 past30=past30.iloc[i],dd60=dd60.iloc[i],dist=dist.iloc[i]))
        for w,d in data["days"][coin].items():
            d=d.dropna(subset=["book_return","coin_return"])
            drows.append(pd.DataFrame(dict(coin=coin,w=w,br=d.book_return.values,cr=d.coin_return.values)))
    df=pd.DataFrame(rows)
    act=df[df.alloc<0].dropna(subset=["slope"]).copy()
    act["gain"]=act.alloc*act.ex
    def summ(g):
        return pd.Series(dict(n=len(g),mean_ex=g.ex.mean(),gain=g.gain.mean(),
                              t_gain=stats.ttest_1samp(g.gain,0).statistic if len(g)>2 else np.nan))
    out={}
    act["sq"]=pd.qcut(act.slope,4,labels=False)
    out["by_sma_slope_q"]=act.groupby("sq").apply(summ).join(act.groupby("sq").slope.agg(['min','max']))
    act["ss"]=np.sign(act.slope)
    out["by_sma_slope_sign"]=act.groupby("ss").apply(summ)
    a2=act.dropna(subset=["dd60"]).copy()
    a2["dq"]=pd.qcut(a2.dd60,4,labels=False)
    out["by_dd60_q"]=a2.groupby("dq").apply(summ).join(a2.groupby("dq").dd60.agg(['min','max']))
    out["slope_x_dist"]=act.assign(deep=act.dist<-17).groupby(["ss","deep"]).apply(summ)
    dd=pd.concat(drows)
    # book by window: sum of log returns averaged over coins per window
    wk=dd.groupby("w").agg(book=("br","mean"),coin=("cr","mean"),n=("br","count"))
    wk["book_total"]=dd.groupby("w").br.sum()/6
    out["book_by_window"]=wk
    return out
