def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float)
            r0=c.pct_change(); nr=r0.shift(-1)
            sd=r0.rolling(60,min_periods=20).std(); z=r0/sd
            sma50=c.rolling(50,min_periods=30).mean()
            mom20=c/c.shift(20)-1
            yr=pd.to_datetime(b["timestamp"]).dt.year
            pos=b["postRebalance_current_allocation"].astype(float).fillna(0)
            d=pd.DataFrame({"coin":coin,"w":w,"year":yr,"pos":pos,"nr":nr,"z":z,"reg":b["regime"],
                            "above":np.where(c>sma50,"above50","below50"),"mom":np.where(mom20>0,"mom_up","mom_dn"),
                            "sd":sd})
            d["pnl"]=d.pos*d.nr
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["nr","z"])
    out={}
    def tt(x):
        return pd.Series({"n":len(x),"mean":x.mean(),"up":(x>0).mean(),"t":stats.ttest_1samp(x,0).statistic if len(x)>2 else np.nan})
    drop=D[D.z<=-1.5].copy()
    out["drop15_by_reg_trend"]=drop.groupby(["reg","above"]).nr.apply(tt).unstack()
    out["drop15_by_reg_mom"]=drop.groupby(["reg","mom"]).nr.apply(tt).unstack()
    dt=drop[drop.reg=="trending"]
    out["drop15_trend_by_year"]=dt.groupby("year").nr.apply(tt).unstack()
    out["drop15_trend_by_coin"]=dt.groupby("coin").nr.apply(tt).unstack()
    # vol-normalised next return (does rebound scale with vol only?)
    drop["nr_sd"]=drop.nr/drop.sd
    out["drop15_nrsd_by_reg"]=drop.groupby("reg").nr_sd.apply(tt).unstack()
    # pnl concentration across bars
    p=D.pnl.sort_values(ascending=False)
    tot=p.sum()
    out["pnl_conc"]=pd.Series({"tot":tot,"top20_bars_share":p.head(20).sum()/tot,"top1pct_share":p.head(int(len(p)*0.01)).sum()/tot,
        "pnl_ex_top20":p.iloc[20:].sum(),"neg_bars_sum":p[p<0].sum()})
    # pnl from big-position bars by regime & trend
    big=D[D.pos>0.5]
    out["bigpos"]=big.groupby(["reg","above"]).agg(n=("pnl","size"),pnl_sum=("pnl","sum"),nr=("nr","mean"))
    # days table
    dd=pd.concat([x.assign(coin=c) for c,ws in data["days"].items() for w,x in ws.items()])
    out["days"]=pd.Series({"book_mean":dd.book_return.mean(),"coin_mean":dd.coin_return.mean(),
        "corr":dd[["book_return","coin_return"]].corr().iloc[0,1],
        "beta":np.polyfit(dd.dropna().coin_return,dd.dropna().book_return,1)[0]})
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades_desc"]=pd.Series({"gross_mean":T.profit_loss_percent.mean(),"comm_mean":T.total_commission.mean(),
        "net_mean":T.net_profit_loss_percent.mean(),"entry_fc_mean":T.entry_forecast.mean(),"share_long":(T.side=="LONG").mean()})
    return out
