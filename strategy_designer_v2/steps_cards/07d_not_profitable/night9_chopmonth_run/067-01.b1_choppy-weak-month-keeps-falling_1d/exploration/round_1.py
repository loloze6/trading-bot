import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=7
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            n=len(b)
            fwd=np.full(n,np.nan)
            fwd[:n-H]=c[H:]/c[:n-H]-1
            r60=np.full(n,np.nan); r60[60:]=c[60:]/c[:-60]-1
            lr=np.log(c); dr=np.r_[np.nan,np.diff(lr)]
            vol30=pd.Series(dr).rolling(30).std().values
            vol90=pd.Series(dr).rolling(90,min_periods=60).std().values
            raw=b.get("debug_info.components.month_fall.last_history_value")
            r30=np.full(n,np.nan); r30[30:]=c[30:]/c[:-30]-1
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n,H):
                rows.append(dict(coin=coin,w=w,day=ts[i].normalize(),fwd=fwd[i],fc=b["forecast"].iloc[i],
                    reg=b["regime"].iloc[i],r30=r30[i],r60=r60[i],ag=vol30[i]/vol90[i] if vol90[i]>0 else np.nan,
                    alloc=b["postRebalance_current_allocation"].iloc[i]))
    g=pd.DataFrame(rows).dropna(subset=["fwd"])
    drift=g.groupby("coin")["fwd"].mean()
    g["drift"]=g.coin.map(drift); g["ex"]=g.fwd-g.drift
    out={}
    def summ(d,col):
        x=d[col].dropna(); 
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    ch=g[g.reg=="unknown"].copy()
    ch["short_tot"]=-ch.fwd; ch["short_ex"]=-ch.ex
    sh=ch[ch.fc<=-2].copy()
    sh["fb"]=pd.cut(sh.fc,[-21,-12,-8,-5,-2])
    out["short by forecast depth: total & excess"]=sh.groupby("fb").apply(lambda d: pd.concat([summ(d,"short_tot").add_prefix("tot_"),summ(d,"short_ex").add_prefix("ex_")]))
    out["choppy nonsignal (fc>-2) short_tot/ex"]=pd.concat([summ(ch[ch.fc>-2],"short_tot"),summ(ch[ch.fc>-2],"short_ex")],axis=1)
    # by raw 30d return quintiles in choppy, all bars (both sides)
    ch["q30"]=pd.qcut(ch.r30,5)
    out["choppy fwd by 30d return quintile"]=ch.groupby("q30").apply(lambda d: pd.concat([summ(d,"fwd").add_prefix("fwd_"),summ(d,"ex").add_prefix("ex_")]))
    # agitation within shorts
    sh["agq"]=pd.qcut(sh.ag,3)
    out["short by agitation tercile"]=sh.groupby("agq").apply(lambda d: pd.concat([summ(d,"short_tot").add_prefix("tot_"),summ(d,"short_ex").add_prefix("ex_")]))
    out["short by 60d return sign"]=sh.groupby(np.sign(sh.r60)).apply(lambda d: pd.concat([summ(d,"short_tot").add_prefix("tot_"),summ(d,"short_ex").add_prefix("ex_")]))
    out["short by window"]=sh.groupby("w").apply(lambda d: pd.concat([summ(d,"short_tot").add_prefix("tot_"),summ(d,"short_ex").add_prefix("ex_")]))
    out["short by coin"]=sh.groupby("coin").apply(lambda d: summ(d,"short_tot"))
    # book daily returns by window
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd.append(d.assign(coin=coin,w=w))
    D=pd.concat(dd)
    bw=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book by window"]=bw.groupby("w").agg(book_mean=("book_return","mean"),book_sum=("book_return","sum"),coin_mean=("coin_return","mean"),days=("day","count"))
    # trades
    T=pd.concat([t.assign(coin=c,w=w) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_h=("duration_minutes",lambda x:(x/1440).mean()))
    T["fb"]=pd.cut(T.entry_forecast,[-21,-12,-8,-5,-2,0])
    out["trades by entry forecast"]=T.groupby("fb").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    return out
