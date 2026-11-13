def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            r=b["close"].pct_change().shift(-1)
            pos=b["postRebalance_current_allocation"].astype(float).fillna(0)
            ret1=b["close"].pct_change()
            sd=ret1.rolling(60,min_periods=20).std()
            z=ret1/sd
            yr=pd.to_datetime(b["timestamp"]).dt.year
            d=pd.DataFrame({"coin":coin,"w":w,"year":yr,"pos":pos,"nr":r,"r0":ret1,"z":z,"reg":b["regime"],"fc":b["forecast"]})
            d["pnl"]=d.pos*d.nr
            # previous position for 2-day hold
            d["prevpos"]=d.pos.shift(1)
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["nr"])
    out={}
    out["overall"]=pd.Series({"mean_pos":D.pos.mean(),"share_in_mkt":(D.pos.abs()>1e-6).mean(),"mean_pnl":D.pnl.mean(),"mean_coin_ret":D.nr.mean(),"drift_part":D.pos.mean()*D.nr.mean(),"n":len(D)})
    g=D.groupby("coin").agg(pnl=("pnl","mean"),pos=("pos","mean"),coin=("nr","mean"))
    g["drift_part"]=g.pos*g.coin; out["by_coin"]=g
    gy=D.groupby("year").agg(pnl=("pnl","mean"),pos=("pos","mean"),coin=("nr","mean"),n=("pnl","size"))
    gy["drift_part"]=gy.pos*gy.coin; out["by_year"]=gy
    out["by_window_pnlsum"]=D.groupby("w").pnl.sum().round(4)
    out["by_regime"]=D.groupby("reg").agg(pnl_sum=("pnl","sum"),pos=("pos","mean"),coin=("nr","mean"),n=("pnl","size"))
    D["zb"]=pd.cut(D.z,[-99,-3,-2,-1.5,-1,-0.5,0,99])
    def tt(x):
        return pd.Series({"n":len(x),"mean":x.mean(),"up":(x>0).mean(),"t":stats.ttest_1samp(x,0).statistic if len(x)>2 else np.nan})
    out["next_ret_by_z"]=D.groupby("zb").nr.apply(tt).unstack()
    out["next_ret_by_z_reg"]=D.groupby(["zb","reg"]).nr.apply(tt).unstack()
    # pnl by position bucket
    D["pb"]=pd.cut(D.pos,[-1,1e-6,0.1,0.5,10])
    out["pnl_by_pos"]=D.groupby("pb").agg(pnl_sum=("pnl","sum"),n=("pnl","size"),nr=("nr","mean"))
    # trades concentration
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    p=T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades"]=pd.Series({"n":len(T),"win":(p>0).mean(),"mean":p.mean(),"top10_share_of_sum":p.head(10).sum()/p.sum(),"top5pct_share":p.head(int(len(p)*0.05)).sum()/p.sum(),"med_dur_days":T.duration_minutes.median()/1440})
    return out
