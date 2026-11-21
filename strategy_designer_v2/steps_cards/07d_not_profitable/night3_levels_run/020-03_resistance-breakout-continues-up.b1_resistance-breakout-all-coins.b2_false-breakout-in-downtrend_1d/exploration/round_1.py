def explore(data):
    import numpy as np, pandas as pd
    rows=[]; trows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            nxt=b["close"].shift(-1)/b["close"]-1
            a=b["postRebalance_current_allocation"].fillna(0)
            g=a*nxt
            raw=b.get("debug_info.components.break.last_history_value")
            fresh=(raw.fillna(0)>0) if raw is not None else pd.Series(False,index=b.index)
            sign=np.sign(a)
            df=pd.DataFrame({"coin":coin,"w":w,"g":g,"a":a,"sign":sign,"fresh":fresh,
                             "fc":b["forecast"],"reg":b["regime"],"nxt":nxt,
                             "cost":(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]})
            rows.append(df)
            t=data["trades"][coin][w]
            if len(t):
                t=t.copy();t["coin"]=coin;t["w"]=w;trows.append(t)
    d=pd.concat(rows); t=pd.concat(trows)
    out={}
    out["by_pos_sign"]=d.groupby("sign").agg(bars=("g","size"),mean_gain=("g","mean"),sum_gain=("g","sum"),mean_abs_alloc=("a",lambda x:x.abs().mean()),mean_nxt=("nxt","mean"))
    out["forecast_sign_bars"]=d.groupby(np.sign(d["fc"])).size()
    out["fresh_bars"]=int(d["fresh"].sum())
    out["fc_on_fresh"]=d.loc[d.fresh,"fc"].describe()
    out["fc_nonfresh_mr"]=d.loc[(~d.fresh)&(d.reg=="mean_reversion"),"fc"].describe()
    out["total_gain_sum"]=float(d.g.sum()); out["total_cost_sum"]=float(d.cost.clip(lower=0).sum())
    out["trades_by_side"]=t.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),med_net=("net_profit_loss_percent","median"),days=("duration_minutes",lambda x:(x/1440).mean()),win=("net_profit_loss_percent",lambda x:(x>0).mean()))
    t["days"]=t.duration_minutes/1440
    t["dur_bin"]=pd.cut(t.days,[0,5,10,11,20,40,1000])
    out["trades_by_dur"]=t.groupby(["side","dur_bin"]).agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"))
    out["gain_by_regime_sign"]=d.groupby(["reg","sign"]).agg(bars=("g","size"),sum_gain=("g","sum"))
    return out
