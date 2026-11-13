def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); a=b["postRebalance_current_allocation"].astype(float)
            v=b["postRebalance_total_value"].astype(float)
            r1=c.shift(-1)/c-1; br=v.shift(-1)/v-1
            r10=c.shift(-10)/c-1
            lr=np.log(c).diff()
            vol=lr.rolling(30).std()
            mom=c/c.shift(20)-1
            raw=b["debug_info.components.below_ma.last_history_value"].astype(float)
            df=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "a":a,"f":b["forecast"].astype(float),"r1":r1,"br":br,"r10":r10,"vol":vol,"mom":mom,"raw":raw})
            df["volq"]=df.groupby("coin")["vol"].transform(lambda x:x) 
            rows.append(df)
    d=pd.concat(rows,ignore_index=True).dropna(subset=["r1","br"])
    d["gross"]=d["a"]*d["r1"]; d["fee"]=d["gross"]-d["br"]
    d["volq"]=d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=["calm","mid","volatile"]) if x.notna().sum()>10 else np.nan)
    act=d[d["a"]!=0].copy()
    out={}
    out["overall"]=pd.Series({"bars":len(d),"active_share":len(act)/len(d),"mean_gross_all":d.gross.mean(),
        "mean_fee_all":d.fee.mean(),"mean_book_all":d.br.mean(),"t_gross":d.gross.mean()/d.gross.std()*np.sqrt(len(d)),
        "mean_alloc_active":act.a.mean(),"mean_r1_active":act.r1.mean(),"mean_r1_inactive":d[d.a==0].r1.mean(),
        "corr_a_f":d[["a","f"]].corr().iloc[0,1]})
    act["fq"]=pd.qcut(act["f"].rank(method="first"),5,labels=["deepest","q2","q3","q4","shallow"])
    out["by_forecast_q"]=act.groupby("fq").agg(n=("r1","size"),f=("f","mean"),a=("a","mean"),r1=("r1","mean"),r10=("r10","mean"),gross=("gross","mean"),fee=("fee","mean"))
    out["by_year"]=d.groupby("year").agg(active=("a",lambda x:(x!=0).mean()),gross=("gross","mean"),fee=("fee","mean"),book=("br","mean"),coin=("r1","mean"))
    out["by_coin"]=d.groupby("coin").agg(active=("a",lambda x:(x!=0).mean()),gross=("gross","mean"),fee=("fee","mean"),book=("br","mean"),coin_r=("r1","mean"))
    act["momsign"]=np.where(act["mom"]>0,"up20","down20")
    out["active_by_mom_vol"]=act.groupby(["momsign","volq"]).agg(n=("r1","size"),r1=("r1","mean"),gross=("gross","mean"),fee=("fee","mean"))
    # fee drivers
    d["da"]=d.groupby(["coin","w"])["a"].diff().abs()
    out["turnover"]=pd.Series({"mean_abs_alloc_change":d["da"].mean(),"share_bars_alloc_change":(d["da"]>1e-6).mean(),
        "fee_sum_over_gross_sum_active":act.fee.sum()/abs(act.gross.sum()) if act.gross.sum()!=0 else np.nan})
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()],ignore_index=True)
    tr["days"]=tr["duration_minutes"]/1440
    out["trades"]=tr.groupby("side").agg(n=("days","size"),days_mean=("days","mean"),days_med=("days","median"),
        gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),win=("profit_loss_percent",lambda x:(x>0).mean()))
    tr["dq"]=pd.qcut(tr["days"].rank(method="first"),4,labels=["short","q2","q3","long"])
    out["trades_by_duration"]=tr.groupby("dq").agg(n=("days","size"),days=("days","mean"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),comm=("total_commission","mean"))
    out["by_window"]=d.groupby("w").agg(active=("a",lambda x:(x!=0).mean()),gross=("gross","mean"),fee=("fee","mean"),coin=("r1","mean"))
    return out
