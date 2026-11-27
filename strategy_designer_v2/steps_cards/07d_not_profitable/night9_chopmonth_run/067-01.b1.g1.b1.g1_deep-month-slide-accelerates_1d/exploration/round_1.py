def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    out={}
    # book per window
    rows=[]
    for c in days:
        for w,d in days[c].items():
            rows.append(pd.DataFrame({"w":w,"day":d["day"],"b":d["book_return"],"h":d["coin_return"]}))
    D=pd.concat(rows).dropna()
    g=D.groupby(["w","day"])[["b","h"]].mean().reset_index()
    pw=g.groupby("w").agg(book_mean=("b","mean"),hold_mean=("h","mean"),n=("b","size"))
    pw["book_sum"]=g.groupby("w")["b"].sum()
    out["per_window"]=pw
    # drift per coin (10 bar grid)
    drift={}
    for c in bars:
        r=[]
        for w,b in bars[c].items():
            cl=b["close"].values
            for i in range(0,len(cl)-10,10): r.append(cl[i+10]/cl[i]-1)
        drift[c]=np.mean(r) if r else 0
    # case-level samples on 10 grid, situation bars
    S=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True); cl=b["close"].values; n=len(cl)
            for H in (10,20):
                for i in range(0,n-H,H if H==10 else 10):
                    if H==20 and i%20!=0: continue
                    rg=b["regime"].iloc[i]
                    if rg not in("trending","unknown"): continue
                    r30=cl[i]/cl[i-30]-1 if i>=30 else np.nan
                    r5=cl[i]/cl[i-5]-1 if i>=5 else np.nan
                    r10=cl[i]/cl[i-10]-1 if i>=10 else np.nan
                    S.append(dict(c=c,w=w,H=H,rg=rg,alloc=b["postRebalance_current_allocation"].iloc[i],
                        fc=b["forecast"].iloc[i],z=b.get("debug_info.components.slide.last_history_value",pd.Series([np.nan]*n)).iloc[i],
                        fwd=cl[i+H]/cl[i]-1,drift=drift[c]*H/10,r5=r5,r10=r10,r30=r30,ts=b["timestamp"].iloc[i]))
    S=pd.DataFrame(S)
    S["short_unus"]=-(S.fwd-S.drift); S["short_tot"]=-S.fwd
    def summ(x):
        return pd.Series(dict(n=len(x),unus=x.short_unus.mean(),tot=x.short_tot.mean(),
            t=x.short_unus.mean()/(x.short_unus.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    T=S[(S.H==10)&(S.rg=="trending")].copy()
    T["held"]=T.alloc<0
    out["trend_by_held"]=T.groupby("held").apply(summ)
    T["zq"]=pd.qcut(T.fc.rank(method="first"),3,labels=["deep","mid","shallow"])
    out["trend_by_fc_tercile"]=T.groupby("zq").apply(summ)
    T["r5s"]=np.sign(T.r5); out["trend_by_r5sign"]=T.groupby("r5s").apply(summ)
    T["r10q"]=pd.qcut(T.r10.rank(method="first"),3,labels=["lo","mid","hi"])
    out["trend_by_r10"]=T.groupby("r10q").apply(summ)
    T["year"]=pd.to_datetime(T.ts).dt.year
    out["trend_by_year"]=T.groupby("year").apply(summ)
    out["trend_by_window"]=T.groupby("w").apply(summ)
    U=S[(S.H==10)&(S.rg=="unknown")]
    out["chop_up_month_short"]=summ(U)
    T20=S[(S.H==20)&(S.rg=="trending")]
    T20=T20.assign(held=T20.alloc<0)
    out["trend20_by_held"]=T20.groupby("held").apply(summ)
    # trades
    tr=pd.concat([t for c in data["trades"] for t in data["trades"][c].values() if len(t)])
    out["trades"]=tr.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur=("duration_minutes","mean"))
    return out
