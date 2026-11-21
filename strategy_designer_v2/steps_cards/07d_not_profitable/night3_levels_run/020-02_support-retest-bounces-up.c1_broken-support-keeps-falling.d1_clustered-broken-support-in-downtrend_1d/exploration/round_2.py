def explore(data):
    import pandas as pd, numpy as np
    rows=[]; drift={}
    for coin,ws in data["bars"].items():
        allf=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c); s=pd.Series(c)
            ma=s.rolling(50).mean().values; r20p=s.pct_change(20).values
            raw=b["debug_info.components.low_cluster.last_history_value"].values if "debug_info.components.low_cluster.last_history_value" in b else np.full(n,np.nan)
            for i in range(0,n-5,5):
                f=c[i+5]/c[i]-1; allf.append(f)
                rows.append(dict(coin=coin,w=w,f=f,reg=b["regime"].iloc[i],raw=raw[i],
                    fc=b["forecast"].iloc[i],al=b["postRebalance_current_allocation"].iloc[i],
                    dma=c[i]/ma[i]-1 if not np.isnan(ma[i]) else np.nan,r20=r20p[i],
                    year=pd.Timestamp(b["timestamp"].iloc[i]).year))
        drift[coin]=np.mean(allf)
    d=pd.DataFrame(rows); d["u"]=d["f"]-d["coin"].map(drift)
    act=d[(d.reg=="mean_reversion")&(d.raw>0)].copy()
    out={}
    out["fc_dist_active"]=act["fc"].describe()
    out["fc_abs_share_ge19"]=float((act.fc.abs()>=19).mean())
    out["alloc_dist_active"]=act["al"].describe()
    act["rq"]=pd.qcut(act.raw.rank(method="first"),5,labels=False)
    out["rq_alloc_mean"]=act.groupby("rq")[["al","fc"]].mean()
    out["top_raw_by_year"]=act[act.rq==4].groupby("year")["u"].agg(["size","mean"])
    out["bot_raw_by_year"]=act[act.rq==0].groupby("year")["u"].agg(["size","mean"])
    act["r20h"]=np.where(act.r20<act.r20.median(),"deep","shallow")
    act["rh"]=np.where(act.rq>=3,"hi","lo")
    out["raw_x_r20"]=act.groupby(["rh","r20h"])["u"].agg(["size","mean",lambda v: v.mean()/(v.std()/np.sqrt(len(v)))])
    act["dh"]=pd.cut(act.dma,[-1,-0.2,-0.08,0])
    out["raw_x_dma"]=act.groupby(["rh","dh"])["u"].agg(["size","mean"])
    out["coin_top_raw"]=act[act.rq>=3].groupby("coin")["u"].agg(["size","mean"])
    # book daily: gain from drift vs timing, by window
    bd=pd.concat([x.assign(coin=c,w=w) for c,ws in data["days"].items() for w,x in ws.items()])
    out["book_mean_daily"]=float(bd.book_return.mean())
    out["book_by_window_neg_share"]=float((bd.groupby("w").book_return.mean()<0).mean())
    # trades: duration and net by entry forecast
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trade_dur_days"]=(tr.duration_minutes/1440).describe()
    out["trade_net_median"]=float(tr.net_profit_loss_percent.median())
    out["trade_comm_mean"]=float(tr.total_commission.mean())
    return out
