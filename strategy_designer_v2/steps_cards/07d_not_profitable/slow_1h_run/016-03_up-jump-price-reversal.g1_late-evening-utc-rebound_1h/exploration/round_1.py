def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; trs=[]; dec=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            b["hour"]=ts.dt.hour
            r1=b["close"].shift(-1)/b["close"]-1
            b["gain"]=b["postRebalance_current_allocation"]*r1
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["coin"]=c; b["win"]=w
            rows.append(b[["coin","win","hour","gain","fee","postRebalance_current_allocation"]])
            # decision bars 19:00 start
            f24=b["close"]/b["close"].shift(24)-1
            r2=b["close"].shift(-2)/b["close"]-1
            vol=np.log(b["close"]).diff().rolling(240).std()
            d=pd.DataFrame({"coin":c,"win":w,"f24":f24,"r2":r2,"vol":vol,"hour":b["hour"],
                            "fc":b["forecast"].shift(-1)})
            dec.append(d[d.hour==19])
            t=data["trades"][c][w]
            if len(t): trs.append(t.assign(coin=c))
    B=pd.concat(rows); D=pd.concat(dec).dropna(); T=pd.concat(trs)
    out={}
    out["gain_fee_by_hour"]=B.groupby("hour").agg(gain=("gain","sum"),fee=("fee","sum"),pos=("postRebalance_current_allocation","mean")).query("pos!=0 or fee>0")
    out["totals"]=pd.Series({"gross_sum":B.gain.sum(),"fee_sum":B.fee.sum(),"n_bars":len(B)})
    out["trades"]=pd.Series({"n":len(T),"mean_gross_pct":T.profit_loss_percent.mean(),"mean_net_pct":T.net_profit_loss_percent.mean(),
        "median_dur_min":T.duration_minutes.median(),"mean_dur_min":T.duration_minutes.mean(),"share_win_gross":(T.profit_loss_percent>0).mean()})
    T["dbin"]=pd.cut(T.duration_minutes,[0,60,120,180,1e9])
    out["trades_by_dur"]=T.groupby("dbin").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    out["trades_by_coin"]=T.groupby("coin").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),comm=("total_commission","mean"))
    D["q"]=pd.qcut(D.f24.rank(method="first"),5,labels=False)
    g=D.groupby("q").agg(n=("r2","size"),f24=("f24","mean"),r2_bps=("r2",lambda x:x.mean()*1e4),
                       t=("r2",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    out["r2_by_f24_quintile"]=g
    D["vq"]=pd.qcut(D.vol.rank(method="first"),3,labels=False)
    D["fz"]=D.f24/D.vol
    out["r2_falls_by_volterc"]=D[D.f24<0].groupby("vq").agg(n=("r2","size"),r2_bps=("r2",lambda x:x.mean()*1e4),f24=("f24","mean"))
    out["r2_by_coin_fall"]=D[D.f24<0].groupby("coin").r2.agg(["size",lambda x:x.mean()*1e4])
    return out
