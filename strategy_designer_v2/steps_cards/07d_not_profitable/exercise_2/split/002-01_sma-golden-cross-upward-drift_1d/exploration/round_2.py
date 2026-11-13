def explore(data):
    import numpy as np, pandas as pd
    rows=[]; tr=[]; dd=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            r=b["close"].pct_change().shift(-1)
            v=b["postRebalance_total_value"]
            br=v.pct_change().shift(-1)
            inv=b["postRebalance_current_allocation"].abs()>1e-6
            run=(inv!=inv.shift()).cumsum()
            age=inv.groupby(run).cumcount()
            mom=b["close"].pct_change(20)
            raw=b["debug_info.components.sma_cross.last_history_value"]
            d=pd.DataFrame({"coin":c,"w":w,"inv":inv,"age":age,"r":r,"br":br,"mom":mom,"raw":raw,"f":b["forecast"]})
            rows.append(d.dropna(subset=["r","br"]))
            peak=v.cummax(); bdd=(v/peak-1).min()
            cp=b["close"]; cdd=(cp/cp.cummax()-1).min()
            dd.append({"coin":c,"w":w,"book_dd":bdd,"coin_dd":cdd,"book_ret":v.iloc[-1]/v.iloc[0]-1,"coin_ret":cp.iloc[-1]/cp.iloc[0]-1})
        for w,t in data["trades"][c].items():
            if len(t): t=t.copy(); t["coin"]=c; t["w"]=w; tr.append(t)
    D=pd.concat(rows); T=pd.concat(tr); DD=pd.DataFrame(dd)
    out={}
    DI=D[D.inv]
    ab=pd.cut(DI["age"],[-1,10,30,60,120,2000])
    g=DI.groupby(ab,observed=True)
    out["inv_by_age"]=pd.DataFrame({"n":g.size(),"coin":g["r"].mean(),"book":g["br"].mean(),"sum_book":g["br"].sum(),"t":g["r"].mean()/(g["r"].std()/np.sqrt(g.size()))})
    DF=D[~D.inv]
    g=DF.groupby(np.where(DF["mom"]>0,"up20","down20"))
    out["flat_by_mom"]=pd.DataFrame({"n":g.size(),"coin":g["r"].mean(),"sum_coin":g["r"].sum()})
    rb=pd.qcut(DI["raw"],5)
    g=DI.groupby(rb,observed=True)
    out["inv_by_raw_spread"]=pd.DataFrame({"n":g.size(),"coin":g["r"].mean(),"book":g["br"].mean()})
    T["eb"]=pd.cut(T["entry_forecast"],[-0.1,2,5,10,20.1])
    g=T.groupby("eb",observed=True)
    out["trades_by_entry_f"]=pd.DataFrame({"n":g.size(),"days":g["duration_minutes"].mean()/1440,"gross":g["profit_loss_percent"].mean(),"win":(g["profit_loss_percent"].apply(lambda s:(s>0).mean()))})
    out["dd_summary"]=pd.Series({"mean_book_dd":DD.book_dd.mean(),"mean_coin_dd":DD.coin_dd.mean(),"worst_book_dd":DD.book_dd.min(),"worst_coin_dd":DD.coin_dd.min(),"share_win_book_beats_coin":(DD.book_ret>DD.coin_ret).mean(),"mean_book_ret":DD.book_ret.mean(),"mean_coin_ret":DD.coin_ret.mean()})
    g=DD.groupby("w")
    out["dd_by_window"]=pd.DataFrame({"book_dd":g.book_dd.mean(),"coin_dd":g.coin_dd.mean(),"book_ret":g.book_ret.mean(),"coin_ret":g.coin_ret.mean()})
    out["trades_per_coin_window"]=T.groupby(["coin","w"]).size().describe()
    return out
