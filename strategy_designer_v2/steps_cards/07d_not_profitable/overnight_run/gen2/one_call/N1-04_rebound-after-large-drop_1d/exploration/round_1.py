def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; trs=[]; dys=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            c=b["close"].astype(float)
            b["r1"]=c.shift(-1)/c-1
            b["ret"]=c.pct_change()
            b["vol20"]=b["ret"].rolling(20).std()
            b["ma50"]=c/c.rolling(50,min_periods=20).mean()-1
            b["mom20"]=c/c.shift(20)-1
            b["f"]=b["forecast"].astype(float)
            b["alloc"]=b["postRebalance_current_allocation"].astype(float)
            b["bv"]=b["postRebalance_total_value"].astype(float)
            b["bret"]=b["bv"].shift(-1)/b["bv"]-1
            b["coin"]=coin; b["w"]=w; b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","w","year","f","r1","ret","vol20","ma50","mom20","alloc","bret"]])
        for w,t in data["trades"][coin].items():
            t=t.copy(); t["coin"]=coin; t["w"]=w; trs.append(t)
    B=pd.concat(rows).dropna(subset=["r1"])
    T=pd.concat(trs)
    out={}
    B["fb"]=pd.cut(B["f"],[-0.1,0.001,2,8,16,19.99,20.1])
    out["fbucket"]=B.groupby("fb").agg(n=("r1","size"),mean_r1=("r1","mean"),hit=("r1",lambda x:(x>0).mean()),alloc=("alloc","mean"),bret=("bret","mean"))
    A=B[B.f>0]
    out["active_by_coin"]=A.groupby("coin").agg(n=("r1","size"),mean_r1=("r1","mean"),t=("r1",lambda x:x.mean()/x.std()*np.sqrt(len(x))),bret_sum=("bret","sum"))
    out["active_by_year"]=A.groupby("year").agg(n=("r1","size"),mean_r1=("r1","mean"),hit=("r1",lambda x:(x>0).mean()),bret_sum=("bret","sum"))
    A=A.copy()
    A["trend"]=np.where(A["ma50"]>0,"above_ma50","below_ma50")
    out["active_by_trend"]=A.groupby("trend").agg(n=("r1","size"),mean_r1=("r1","mean"),hit=("r1",lambda x:(x>0).mean()),t=("r1",lambda x:x.mean()/x.std()*np.sqrt(len(x))),bret_sum=("bret","sum"))
    A["volq"]=pd.qcut(A["vol20"],3,labels=["lowvol","midvol","highvol"])
    out["active_by_vol"]=A.groupby("volq").agg(n=("r1","size"),mean_r1=("r1","mean"),sd=("r1","std"),hit=("r1",lambda x:(x>0).mean()),bret_sum=("bret","sum"))
    A["momq"]=pd.qcut(A["mom20"],3,labels=["mom_low","mom_mid","mom_high"])
    out["active_by_mom20"]=A.groupby("momq").agg(n=("r1","size"),mean_r1=("r1","mean"),hit=("r1",lambda x:(x>0).mean()),bret_sum=("bret","sum"))
    # worst book days
    bb=B.dropna(subset=["bret"])
    out["book_tail"]=pd.Series({"n_days_alloc>0":int((bb.alloc>0).sum()),"share_days_in_mkt":(bb.alloc>0).mean(),
        "worst5pct_bret_mean":bb.bret.quantile(0.01),"sum_neg_bret_active":bb.loc[bb.bret<0,"bret"].sum(),"sum_pos_bret":bb.loc[bb.bret>0,"bret"].sum(),
        "mean_alloc_active":bb.loc[bb.alloc>0,"alloc"].mean()})
    T["dur_d"]=T["duration_minutes"]/1440
    out["trades"]=pd.Series({"n":len(T),"long_share":(T.side=="LONG").mean(),"dur_mean_d":T.dur_d.mean(),"dur_median_d":T.dur_d.median(),
        "gross_mean_pct":T.profit_loss_percent.mean(),"net_mean_pct":T.net_profit_loss_percent.mean(),
        "gross_win":(T.profit_loss_percent>0).mean(),"gross_minus_net_pct":(T.profit_loss_percent-T.net_profit_loss_percent).mean(),
        "gross_t":stats.ttest_1samp(T.profit_loss_percent,0).statistic})
    T["efb"]=pd.cut(T.entry_forecast,[0,2,8,16,20.1])
    out["trades_by_entryf"]=T.groupby("efb").agg(n=("profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur=("dur_d","mean"))
    # consecutive drops: was previous day also a drop
    B2=B.copy(); 
    out["window_bret"]=B.groupby("w")["bret"].sum().describe()
    return out
