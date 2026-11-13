def explore(data):
    import numpy as np, pandas as pd
    rows=[]; tr=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            r=b["close"].pct_change().shift(-1)
            v=b["postRebalance_total_value"]
            br=v.pct_change().shift(-1)
            vol=b["close"].pct_change().rolling(20,min_periods=10).std()
            mom=b["close"].pct_change(20)
            d=pd.DataFrame({"coin":c,"w":w,"f":b["forecast"],"a":b["postRebalance_current_allocation"],
                            "r":r,"br":br,"vol":vol,"mom":mom,"year":pd.to_datetime(b["timestamp"]).dt.year})
            d["wnum"]=int(w[1:])
            rows.append(d.dropna(subset=["r","br"]))
        for w,t in data["trades"][c].items():
            if len(t): t=t.copy(); t["coin"]=c; t["w"]=w; tr.append(t)
    D=pd.concat(rows); T=pd.concat(tr)
    out={}
    D["inv"]=D["a"].abs()>1e-6
    D["gross"]=D["a"]*D["r"]
    out["overall"]=pd.Series({"share_invested":D["inv"].mean(),"mean_book":D["br"].mean(),"mean_coin":D["r"].mean(),
        "mean_gross_pos_ret":D["gross"].mean(),"coin_mean_when_inv":D.loc[D.inv,"r"].mean(),
        "coin_mean_when_flat":D.loc[~D.inv,"r"].mean(),"mean_alloc_when_inv":D.loc[D.inv,"a"].mean(),
        "fee_drag_per_bar":(D["gross"]-D["br"]).mean()})
    fb=pd.cut(D["f"],[-0.1,0.001,5,10,15,20.1])
    g=D.groupby(fb,observed=True)
    out["by_forecast"]=pd.DataFrame({"n":g.size(),"coin_next":g["r"].mean(),"book":g["br"].mean(),
        "t":g["r"].mean()/(g["r"].std()/np.sqrt(g.size()))})
    T["days"]=T["duration_minutes"]/1440
    out["trades"]=pd.Series({"n":len(T),"mean_days":T["days"].mean(),"median_days":T["days"].median(),
        "mean_gross%":T["profit_loss_percent"].mean(),"mean_net%":T["net_profit_loss_percent"].mean(),
        "mean_comm":T["total_commission"].mean(),"win_gross":(T["profit_loss_percent"]>0).mean(),
        "share_lt5d":(T["days"]<5).mean(),"side_long":(T["side"]=="LONG").mean()})
    T["dur_b"]=pd.cut(T["days"],[0,2,5,15,40,1000])
    g=T.groupby("dur_b",observed=True)
    out["trades_by_dur"]=pd.DataFrame({"n":g.size(),"gross":g["profit_loss_percent"].mean(),"net":g["net_profit_loss_percent"].mean(),"sum_net":g["net_profit_loss_percent"].sum()})
    D["volq"]=D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=["calm","mid","vol"]))
    g=D[D.inv].groupby("volq",observed=True)
    out["inv_by_vol"]=pd.DataFrame({"n":g.size(),"coin":g["r"].mean(),"book":g["br"].mean(),"sum_book":g["br"].sum()})
    D["momq"]=np.where(D["mom"]>0,"up20","down20")
    g=D[D.inv].groupby("momq")
    out["inv_by_mom"]=pd.DataFrame({"n":g.size(),"coin":g["r"].mean(),"book":g["br"].mean(),"sum_book":g["br"].sum()})
    g=D.groupby("year")
    out["by_year"]=pd.DataFrame({"inv":g["inv"].mean(),"book_sum":g["br"].sum(),"coin_sum":g["r"].sum(),"coin_when_inv":g.apply(lambda x:x.loc[x.inv,"r"].mean())})
    g=D.groupby("coin")
    out["by_coin"]=pd.DataFrame({"inv":g["inv"].mean(),"book_mean":g["br"].mean(),"coin_mean":g["r"].mean(),"coin_inv":g.apply(lambda x:x.loc[x.inv,"r"].mean())})
    return out
