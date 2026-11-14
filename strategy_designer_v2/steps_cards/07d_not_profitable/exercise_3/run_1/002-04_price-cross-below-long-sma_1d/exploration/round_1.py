import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    drows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            allr.append(pd.Series(c).pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            dist=b.get("debug_info.components.below_ma.last_history_value")
            if dist is None: continue
            alloc=b["postRebalance_current_allocation"]
            past10=c/c.shift(10)-1
            past30=c/c.shift(30)-1
            ddist=dist-dist.shift(10)
            for i in range(0,len(b)-10,10):
                r=c.iloc[i+10]/c.iloc[i]-1
                rows.append(dict(coin=coin,w=w,dist=dist.iloc[i],alloc=alloc.iloc[i],fc=b["forecast"].iloc[i],
                                 ex=r-10*mu,past10=past10.iloc[i],past30=past30.iloc[i],ddist=ddist.iloc[i],
                                 year=b["timestamp"].iloc[i].year if hasattr(b["timestamp"].iloc[i],'year') else pd.to_datetime(b["timestamp"].iloc[i]).year))
            # daily: position gain per bar
            g=alloc.shift(1)*(c/c.shift(1)-1)
            for i in range(1,len(b)):
                drows.append(dict(coin=coin,w=w,g=g.iloc[i],dist=dist.iloc[i-1],past10=past10.iloc[i-1],ddist=ddist.iloc[i-1],alloc=alloc.iloc[i-1]))
    df=pd.DataFrame(rows); dd=pd.DataFrame(drows)
    act=df[df.alloc<0].copy()
    act["gain"]=act.alloc*act.ex
    def summ(g):
        return pd.Series(dict(n=len(g),mean_ex=g.ex.mean(),gain=g.gain.mean(),t_gain=stats.ttest_1samp(g.gain,0).statistic if len(g)>2 else np.nan))
    out={}
    act["distq"]=pd.qcut(act.dist,4,labels=False)
    out["by_dist_quartile"]=act.groupby("distq").apply(summ).join(act.groupby("distq").dist.agg(['min','max']))
    act["p10s"]=np.sign(act.past10)
    out["by_past10_sign"]=act.groupby("p10s").apply(summ)
    act["dds"]=np.sign(act.ddist)
    out["by_ddist_sign"]=act.groupby("dds").apply(summ)
    act["p30q"]=pd.qcut(act.past30,4,labels=False)
    out["by_past30_q"]=act.groupby("p30q").apply(summ).join(act.groupby("p30q").past30.agg(['min','max']))
    out["by_coin"]=act.groupby("coin").apply(summ)
    out["by_year"]=act.groupby("year").apply(summ)
    # flat blocks excess for comparison
    out["flat_mean_ex"]=pd.Series(dict(n=(df.alloc==0).sum(),mean_ex=df[df.alloc==0].ex.mean()))
    # trades fees
    tr=pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"]=pd.Series(dict(n=len(tr),gross=tr.profit_loss_percent.mean(),net=tr.net_profit_loss_percent.mean(),
                                 dur_days=tr.duration_minutes.mean()/1440,win=(tr.profit_loss_percent>0).mean()))
    da=dd[dd.alloc<0].dropna()
    da["dq"]=pd.qcut(da.ddist,4,labels=False)
    out["daily_gain_by_ddist_q"]=da.groupby("dq").g.agg(['count','mean','std']).join(da.groupby("dq").ddist.agg(['min','max']))
    return out
