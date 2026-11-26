def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            nxt=c.shift(-1)/c-1
            hh20=b["high"].rolling(20).max()
            sd20=r.rolling(20).std()
            depth=(c-hh20)/hh20/sd20
            tr60=c/c.shift(60)-1
            vol30=r.rolling(30).std()
            volrel=vol30/vol30.expanding(30).median()
            alloc=b["postRebalance_current_allocation"]
            gain=alloc*nxt
            pv=b["postRebalance_total_value"]; tv=b["total_portfolio_value"]
            fee=(tv-pv)/tv
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "r":r,"nxt":nxt,"depth":depth,"tr60":tr60,"volrel":volrel,"fc":b["forecast"],
                "alloc":alloc,"gain":gain,"fee":fee,"chg":(alloc-b["previous_allocation"]).abs(),
                "pos":b.index})
            d["i"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["r"].mean()
    D["ex"]=-(D["nxt"]-D["coin"].map(drift))
    act=D[D["fc"]<0].dropna(subset=["nxt"])
    out={}
    def summ(g):
        return pd.Series({"n":len(g),"short_ex":g["ex"].mean(),"short_raw":-g["nxt"].mean(),
                          "t":g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))),"gain":g["gain"].mean(),"fee":g["fee"].mean(),"absalloc":g["alloc"].abs().mean()})
    act=act.copy()
    act["fcq"]=pd.qcut(act["fc"].rank(method="first"),5,labels=["deep","q2","q3","q4","shallow"])
    out["by_forecast_quint"]=act.groupby("fcq").apply(summ)
    act["dmq"]=pd.qcut(act["r"].rank(method="first"),5,labels=["smallup","q2","q3","q4","bigup"])
    out["by_daymove_quint"]=act.groupby("dmq").apply(summ)
    act["volq"]=pd.cut(act["volrel"],[0,0.8,1.0,1.25,10])
    out["by_volrel"]=act.groupby("volq").apply(summ)
    act["trq"]=pd.cut(act["tr60"],[-1,-0.4,-0.25,-0.1,10])
    out["by_trend60"]=act.groupby("trq").apply(summ)
    out["by_coin"]=act.groupby("coin").apply(summ)
    out["by_year"]=act.groupby("year").apply(summ)
    # all up days in falling (recomputed) without active forecast, by depth
    up=D[(D["r"]>0)&(D["tr60"]<-0.1)].dropna(subset=["nxt","depth"]).copy()
    up["dq"]=pd.qcut(up["depth"].rank(method="first"),5,labels=["deep","q2","q3","q4","shallow"])
    out["upfall_by_rawdepth"]=up.groupby("dq").apply(summ)
    # down days in falling market (no signal) as baseline
    dn=D[(D["r"]<=0)&(D["tr60"]<-0.1)].dropna(subset=["nxt"])
    out["falling_downdays"]=summ(dn)
    up2=D[(D["r"]>0)&(D["tr60"]>=-0.1)].dropna(subset=["nxt","depth"]).copy()
    up2["dq"]=pd.qcut(up2["depth"].rank(method="first"),5,labels=["deep","q2","q3","q4","shallow"])
    out["upNOTfall_by_rawdepth"]=up2.groupby("dq").apply(summ)
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()],ignore_index=True)
    out["trades"]=pd.Series({"n":len(T),"mean_dur_days":T["duration_minutes"].mean()/1440,
        "mean_pl":T["profit_loss_percent"].mean(),"mean_net":T["net_profit_loss_percent"].mean(),
        "win":(T["net_profit_loss_percent"]>0).mean()})
    # fee share of gross
    pos=D[D["alloc"].abs()>0]
    out["gross_vs_fee"]=pd.Series({"gross_sum":D["gain"].sum(),"fee_sum":D["fee"].sum(),
        "rebalance_bars_while_held":((D["chg"]>1e-6)&(D["alloc"].abs()>0)&(D["alloc"].shift().abs()>0)).sum()})
    # book daily: worst windows
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            dd.append(t.assign(coin=coin,w=w))
    DD=pd.concat(dd)
    bk=DD.groupby(["w","day"])["book_return"].mean().reset_index()
    out["book_by_window"]=bk.groupby("w")["book_return"].agg(["mean","std","sum","min"])
    return out
