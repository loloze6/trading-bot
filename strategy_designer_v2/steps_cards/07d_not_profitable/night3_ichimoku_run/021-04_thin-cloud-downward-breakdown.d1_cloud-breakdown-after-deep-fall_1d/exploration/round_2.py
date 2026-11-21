def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; H=26; out={}
    drift={}
    for c in bars:
        rets=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            for i in range(0,len(cl)-H,H): rets.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(rets)
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True); cl=df["close"].values; f=df["forecast"].fillna(0).values
            al=df["postRebalance_current_allocation"].fillna(0).values
            raw=df.get("debug_info.components.fall26.last_history_value")
            for i in range(len(df)):
                if f[i]<0 and (i==0 or f[i-1]>=0):
                    fwd=cl[i+H]/cl[i]-1 if i+H<len(cl) else np.nan
                    rows.append(dict(c=c,w=w,i=i,f=f[i],al=al[i],fwd=fwd,
                        r26=(cl[i]/cl[i-26]-1) if i>=26 else (raw.iloc[i] if raw is not None else np.nan),
                        r60=(cl[i]/cl[i-60]-1) if i>=60 else np.nan,
                        r10=(cl[i]/cl[i-10]-1) if i>=10 else np.nan,
                        dd=(cl[i]/cl[max(0,i-60):i+1].max()-1),
                        fwd5=cl[i+5]/cl[i]-1 if i+5<len(cl) else np.nan))
    d=pd.DataFrame(rows)
    def s(x):
        x=x.dropna(subset=["fwd"])
        return pd.Series(dict(n=len(x),fwd=x.fwd.mean(),t=stats.ttest_1samp(x.fwd,0).statistic if len(x)>2 else np.nan,med=x.fwd.median(),shortwin=(x.fwd<0).mean()))
    out["entries_all"]=s(d)
    for col in ["f","r26","r10","dd","r60"]:
        dd=d.dropna(subset=[col,"fwd"])
        if len(dd)>12:
            out["by_"+col]=dd.groupby(pd.qcut(dd[col],4,labels=False,duplicates="drop")).apply(s)
    out["corr"]=d[["fwd","fwd5","f","r26","r10","dd","r60"]].corr(method="spearman")["fwd"]
    out["by_coin"]=d.groupby("c").apply(s)
    # book decomposition
    B=pd.concat([df.assign(c=c,w=w) for c in data["days"] for w,df in data["days"][c].items()])
    md={c:pd.concat([df for df in data["days"][c].values()]).coin_return.mean() for c in data["days"]}
    pos=[]
    for c in bars:
        for w,df in bars[c].items():
            x=df[["timestamp","postRebalance_current_allocation","close"]].copy()
            x["day"]=pd.to_datetime(x.timestamp).dt.floor("D")
            x=x.groupby("day").last()
            x["c"]=c; x["w"]=w; x["mkt"]=x.postRebalance_current_allocation.shift(1)*md[c]
            pos.append(x)
    P=pd.concat(pos)
    out["book"]=pd.Series(dict(book_mean=B.book_return.mean(),market_part=P.mkt.mean(),timing=B.book_return.mean()-P.mkt.mean(),share_days_short=(P.postRebalance_current_allocation<0).mean(),mean_abs_alloc=P.postRebalance_current_allocation.abs().mean()))
    # book by coin's own window return
    wr=B.groupby(["c","w"]).agg(book=("book_return","sum"),coin=("coin_return","sum"))
    wr["coinq"]=pd.qcut(wr.coin,4,labels=False)
    out["book_by_coin_window_trend"]=wr.groupby("coinq")[["book","coin"]].agg(["mean","count"])
    tr=pd.concat([t.assign(c=c) for c in data["trades"] for w,t in data["trades"][c].items()])
    tr["dur_d"]=tr.duration_minutes/1440
    out["trades_by_dur"]=tr.groupby(pd.cut(tr.dur_d,[0,5,15,25,27,200]))["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades_big_losers"]=pd.Series(dict(share_loss_gt20=(tr.profit_loss_percent<-20).mean(),sum_pl=tr.profit_loss_percent.sum(),sum_pl_excl_worst10=tr.profit_loss_percent.sort_values().iloc[10:].sum()))
    return out
