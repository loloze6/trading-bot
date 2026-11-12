def explore(data):
    import pandas as pd, numpy as np
    rows=[]; trs=[]; dd=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            b["r1"]=b["close"].shift(-1)/b["close"]-1
            b["r20"]=b["close"].shift(-20)/b["close"]-1
            b["past20"]=b["close"]/b["close"].shift(20)-1
            b["past60"]=b["close"]/b["close"].shift(60)-1
            b["alloc"]=b["postRebalance_current_allocation"]
            b["raw"]=b["debug_info.components.above_ma.last_history_value"]
            b["dfc"]=b["forecast"].diff(5)
            b["coin"]=c; b["w"]=w
            # days above sma run length
            above=(b["raw"]>0).astype(int)
            grp=(above!=above.shift()).cumsum()
            b["run"]=above.groupby(grp).cumcount()+1
            b.loc[above==0,"run"]=0
            v=b["postRebalance_total_value"]; dd.append({"coin":c,"w":w,"maxdd":(v/v.cummax()-1).min(),
                "ret":v.iloc[-1]/v.iloc[0]-1,"coin_ret":b["close"].iloc[-1]/b["close"].iloc[0]-1,
                "coin_dd":(b["close"]/b["close"].cummax()-1).min()})
            rows.append(b)
            t=data["trades"][c][w].copy(); t["coin"]=c; trs.append(t)
    B=pd.concat(rows).dropna(subset=["r1"]); B["gross"]=B["alloc"]*B["r1"]
    T=pd.concat(trs); D=pd.DataFrame(dd)
    out={}
    out["dd_summary"]=D[["maxdd","ret","coin_ret","coin_dd"]].describe().loc[["mean","50%","min"]]
    on=B[B["forecast"]>0].copy()
    on["runb"]=pd.cut(on["run"],[0,10,30,90,200,5000])
    out["by_run"]=on.groupby("runb").agg(n=("r1","size"),fc=("forecast","mean"),alloc=("alloc","mean"),r1=("r1","mean"),r20=("r20","mean"),gross=("gross","mean"))
    on["fqh"]=on["forecast"]>=10
    out["fc_x_past20"]=on.groupby(["fqh",on["past20"]>0]).agg(n=("r1","size"),r1=("r1","mean"),r20=("r20","mean"),gross=("gross","mean"))
    out["fc_rising"]=on.groupby(on["dfc"]>0).agg(n=("r1","size"),r1=("r1","mean"),r20=("r20","mean"),gross=("gross","mean"))
    out["past60_sign_on"]=on.groupby(on["past60"]>0).agg(n=("r1","size"),r1=("r1","mean"),r20=("r20","mean"))
    # trades: entry forecast and losses
    T["efq"]=pd.qcut(T["entry_forecast"].rank(method="first"),4,labels=False)
    out["trades_by_entry_fc"]=T.groupby("efq").agg(n=("side","size"),efc=("entry_forecast","mean"),days=("duration_minutes",lambda x:x.mean()/1440),g=("profit_loss_percent","mean"),win=("profit_loss_percent",lambda x:(x>0).mean()))
    out["trades_per_window"]=T.groupby(["coin"]).size()/24
    # gross daily: sum of losses in down days large alloc
    B["coin_down20"]=B["past20"]<-0.1
    out["loss_by_state"]=B[B["alloc"]>0].groupby(B["coin_down20"]).agg(n=("r1","size"),alloc=("alloc","mean"),gross=("gross","mean"),gsum=("gross","sum"))
    out["alloc_high_r1_sd"]=B[B["alloc"]>0].groupby(pd.cut(B["alloc"],[0,0.5,1,1.5,2.5])).agg(n=("r1","size"),r1=("r1","mean"),sd=("r1","std"),gross=("gross","mean"),gsd=("gross","std"))
    return out
