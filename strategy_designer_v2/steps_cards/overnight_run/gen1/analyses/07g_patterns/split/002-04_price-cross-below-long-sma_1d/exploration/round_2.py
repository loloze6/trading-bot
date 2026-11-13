def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            b["ts"]=pd.to_datetime(b["timestamp"])
            cl=b["close"].astype(float)
            b["r1"]=cl.pct_change()
            b["f1"]=cl.shift(-1)/cl-1
            b["f10"]=cl.shift(-10)/cl-1
            b["f20"]=cl.shift(-20)/cl-1
            b["p10"]=cl/cl.shift(10)-1
            b["p30"]=cl/cl.shift(30)-1
            b["dist"]=b["debug_info.components.below_ma.last_history_value"].astype(float)
            b["alloc"]=b["postRebalance_current_allocation"].astype(float)
            b["bv"]=b["postRebalance_total_value"].astype(float)
            b["br"]=b["bv"].pct_change()
            b["bf1"]=b["br"].shift(-1)
            below=b["dist"]<0
            b["xdown"]=below&(~below.shift(1).fillna(below))
            b["xup"]=(~below)&(below.shift(1).fillna(~below))
            b["coin"]=c; b["win"]=w
            rows.append(b[["coin","win","ts","r1","f1","f10","f20","p10","p30","dist","forecast","alloc","br","bf1","xdown","xup"]])
    d=pd.concat(rows,ignore_index=True)
    out={}
    def agg(x):
        x=x.dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"up":(x>0).mean()})
    out["f10_after_cross_down"]=agg(d.loc[d.xdown,"f10"])
    out["f20_after_cross_down"]=agg(d.loc[d.xdown,"f20"])
    out["f10_after_cross_up"]=agg(d.loc[d.xup,"f10"])
    out["f20_after_cross_up"]=agg(d.loc[d.xup,"f20"])
    out["f10_all"]=agg(d["f10"])
    # cross count per window
    out["crosses_per_coin"]=d.groupby("coin")[["xdown","xup"]].sum()
    # deep below: past 30d return
    d["deep"]=d["forecast"]<=-15
    d["pb"]=pd.cut(d["p30"],[-1,-0.3,-0.15,0,0.15,10])
    out["f10_by_p30_belowSMA"]=d[d.dist<0].groupby("pb")["f10"].apply(agg).unstack()
    out["f10_by_p30_aboveSMA"]=d[d.dist>=0].groupby("pb")["f10"].apply(agg).unstack()
    # momentum p10 top quintile by side of SMA
    d["mom"]=d["p10"]>0.104
    out["f10_mom_top_by_side"]=d.groupby([d.dist<0,"mom"])["f10"].apply(agg).unstack()
    # weekday robustness by year halves
    d["wd"]=d.ts.dt.dayofweek
    d["half"]=np.where(d.ts.dt.year<=2021,"<=2021",">=2022")
    out["f1_weekday_by_half"]=d.groupby(["half","wd"])["f1"].mean().unstack()
    out["f1_thu_fri_vs_rest_by_coin"]=d.groupby(["coin",d.wd.isin([3,4])])["f1"].mean().unstack()
    # book largest losses: what preceded
    q=d["br"].quantile([0.01,0.99])
    lo=d[d.br<=q.iloc[0]]; hi=d[d.br>=q.iloc[1]]
    out["largest_losses_context"]=pd.Series({"n":len(lo),"mean_br":lo.br.mean(),"mean_r1":lo.r1.mean(),"mean_alloc":lo.alloc.mean(),"mean_dist":lo.dist.mean(),"next_coin_f10":lo.f10.mean(),"mean_p10":lo.p10.mean()})
    out["largest_gains_context"]=pd.Series({"n":len(hi),"mean_br":hi.br.mean(),"mean_r1":hi.r1.mean(),"mean_alloc":hi.alloc.mean(),"mean_dist":hi.dist.mean(),"next_coin_f10":hi.f10.mean(),"mean_p10":hi.p10.mean()})
    # trades: by entry forecast
    tr=[]
    for c,ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=c; tr.append(t)
    t=pd.concat(tr,ignore_index=True)
    t["days"]=t.duration_minutes/1440
    t["efb"]=pd.cut(t.entry_forecast.astype(float),[-20.01,-15,-10,-5,-2,0.01])
    out["trades_by_entry_forecast"]=t.groupby("efb").agg(n=("net_profit_loss_percent","size"),mean=("net_profit_loss_percent","mean"),med=("net_profit_loss_percent","median"),days=("days","median"))
    out["trades_short_gross_vs_net_by_dur"]=t.assign(db=pd.cut(t.days,[0,1.5,3,7,20,1e5])).groupby("db").agg(gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),px=("entry_price","count"))
    t["pxret"]=-(t.exit_price/t.entry_price-1)*100
    out["short_price_ret_by_dur"]=t.assign(db=pd.cut(t.days,[0,1.5,3,7,20,1e5])).groupby("db")["pxret"].agg(["mean","median"])
    out["n_trades_total"]=len(t)
    return out
