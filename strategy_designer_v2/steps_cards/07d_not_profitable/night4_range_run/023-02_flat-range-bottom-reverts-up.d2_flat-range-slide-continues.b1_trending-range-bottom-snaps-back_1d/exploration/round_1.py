import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # book daily returns and holding
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    byday = D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_daily"] = pd.Series({"book_mean": byday.book_return.mean(), "hold_mean": byday.coin_return.mean(),
        "book_sd": byday.book_return.std(), "hold_sd": byday.coin_return.std(), "n_days": len(byday)})
    # per coin
    out["by_coin"] = D.groupby("coin")[["book_return","coin_return"]].mean()
    out["by_year"] = D.groupby("year")[["book_return","coin_return"]].mean()
    # market vs timing: position * coin mean daily return
    res=[]; cells=[]
    for c in bars:
        allr=[]
        for w,b in bars[c].items():
            allr.append(b.close.pct_change().shift(-1).dropna())
        mu = pd.concat(allr).mean()
        # 5-bar grid
        r5all=[]
        for w,b in bars[c].items():
            cl=b.close.values; n=len(cl)
            for i in range(0,n-5,5):
                r5all.append(cl[i+5]/cl[i]-1)
        mu5=np.mean(r5all)
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            nxt=b.close.shift(-1)/b.close-1
            a=b.postRebalance_current_allocation.fillna(0)
            res.append(pd.DataFrame({"gain":a*nxt,"mkt":a*mu,"alloc":a,"coin":c}))
            cl=b.close.values; n=len(cl)
            # 30d features at each bar
            hi=b.high.rolling(30).max(); lo=b.low.rolling(30).min()
            nm=(b.close-b.close.shift(30)).abs()/(hi-lo)
            pos=(b.close-(hi+lo)/2)/(hi-lo)
            f10=b.close/b.close.shift(10)-1
            vol=b.close.pct_change().rolling(20).std()
            for i in range(0,n-5,5):
                cells.append(dict(coin=c,w=w,f=b.forecast.iloc[i],r5=cl[i+5]/cl[i]-1,ex=cl[i+5]/cl[i]-1-mu5,
                    nm=nm.iloc[i],pos=pos.iloc[i],f10=f10.iloc[i],vol=vol.iloc[i],
                    dir=np.sign(b.close.iloc[i]-b.close.iloc[i-30]) if i>=30 else np.nan,
                    year=pd.to_datetime(b.timestamp.iloc[i]).year))
    R=pd.concat(res)
    out["gain_split"]=pd.Series({"gain_mean":R.gain.mean(),"mkt_part":R.mkt.mean(),"timing":R.gain.mean()-R.mkt.mean(),
        "share_bars_in":(R.alloc.abs()>0).mean(),"mean_alloc_when_in":R.alloc[R.alloc.abs()>0].mean()})
    C=pd.DataFrame(cells)
    A=C[C.f>0].copy()
    A["fq"]=pd.qcut(A.f,4,labels=False,duplicates="drop")
    g=A.groupby("fq").agg(n=("ex","size"),f=("f","mean"),r5=("r5","mean"),ex=("ex","mean"),f10=("f10","mean"))
    out["active_by_forecast_q"]=g
    A["posq"]=pd.qcut(A.pos,3,labels=False,duplicates="drop")
    out["active_by_pos"]=A.groupby("posq").agg(n=("ex","size"),pos=("pos","mean"),r5=("r5","mean"),ex=("ex","mean"))
    A["nmq"]=pd.qcut(A.nm,3,labels=False,duplicates="drop")
    out["active_by_nm"]=A.groupby("nmq").agg(n=("ex","size"),nm=("nm","mean"),r5=("r5","mean"),ex=("ex","mean"))
    A["volq"]=pd.qcut(A.vol,3,labels=False,duplicates="drop")
    out["active_by_vol"]=A.groupby("volq").agg(n=("ex","size"),vol=("vol","mean"),r5=("r5","mean"),ex=("ex","mean"))
    out["active_by_year"]=A.groupby("year").agg(n=("ex","size"),r5=("r5","mean"),ex=("ex","mean"))
    out["active_by_coin"]=A.groupby("coin").agg(n=("ex","size"),r5=("r5","mean"),ex=("ex","mean"))
    # trades
    T=pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values() if len(t)])
    T["eq"]=pd.qcut(T.entry_forecast,4,labels=False,duplicates="drop")
    out["trades_by_entryq"]=T.groupby("eq").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"),days=("duration_minutes",lambda x:(x/1440).mean()),win=("net_profit_loss_percent",lambda x:(x>0).mean()))
    out["trades_all"]=pd.Series({"n":len(T),"gross":T.profit_loss_percent.mean(),"net":T.net_profit_loss_percent.mean(),
        "med_days":T.duration_minutes.median()/1440,"sd_net":T.net_profit_loss_percent.std()})
    return out
