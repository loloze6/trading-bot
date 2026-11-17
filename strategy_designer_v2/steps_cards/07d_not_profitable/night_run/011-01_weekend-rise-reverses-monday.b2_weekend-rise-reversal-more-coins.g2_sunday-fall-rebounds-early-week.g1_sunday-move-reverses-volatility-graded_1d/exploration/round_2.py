def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True); b["ts"]=pd.to_datetime(b["timestamp"])
            c=b["close"]; r=c.pct_change()
            b["vol20"]=r.rolling(20).std(); b["vol60"]=r.rolling(60).std(); b["vr"]=b["vol20"]/b["vol60"]
            b["r"]=r
            b["g1"]=b["postRebalance_current_allocation"]*(c.shift(-1)/c-1)
            b["day2"]=c.shift(-2)/c.shift(-1)-1
            b["feeshare"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["fee_next"]=b["feeshare"].shift(-1)
            b["coin"]=coin; b["w"]=w
            s=b[(b["ts"].dt.weekday==6)&(b["forecast"]!=0)]
            rows.append(s)
    S=pd.concat(rows)
    a=S["postRebalance_current_allocation"]
    out={}
    out["gross_mon_gain_mean"]=f"{S['g1'].mean():.6f} t {stats.ttest_1samp(S['g1'].dropna(),0)[0]:.2f} n {S['g1'].notna().sum()}"
    out["entry_fee_mean"]=float(S["feeshare"].mean())
    out["exit_fee_mean"]=float(S["fee_next"].mean())
    g2=(a*S["day2"]).dropna()
    out["hypothetical_day2_gain_same_alloc"]=f"{g2.mean():.6f} t {stats.ttest_1samp(g2,0)[0]:.2f}"
    side=-np.sign(S["r"])
    S["s1"]=side*(S["g1"]/a.replace(0,np.nan)).abs()*np.sign(S["g1"]) 
    S["sd2"]=side*S["day2"]
    S["vrq"]=pd.qcut(S["vr"],4,labels=False)
    out["by_vol_ratio_q"]=S.groupby("vrq").apply(lambda q: pd.Series({"n":len(q),"g1":q.g1.mean(),"sd2":q.sd2.mean(),"t_sd2":stats.ttest_1samp(q.sd2.dropna(),0)[0],"absalloc":q.postRebalance_current_allocation.abs().mean()}))
    S["vq"]=pd.qcut(S["vol20"],4,labels=False)
    out["by_vol20_q"]=S.groupby("vq").apply(lambda q: pd.Series({"n":len(q),"g1":q.g1.mean(),"t_g1":stats.ttest_1samp(q.g1.dropna(),0)[0],"sd2":q.sd2.mean(),"absalloc":q.postRebalance_current_allocation.abs().mean()}))
    # worst Monday book losses: share of loss from top decile
    g=S["g1"].dropna().sort_values()
    out["worst5pct_sum_vs_total"]=f"worst5% sum {g.iloc[:len(g)//20].sum():.3f} total {g.sum():.3f}"
    out["worst_side"]=S.loc[g.index[:len(g)//20] if False else S['g1'].nsmallest(len(g)//20).index].pipe(lambda q: f"short share {(q.postRebalance_current_allocation<0).mean():.2f}, mean |z| {(q.r/q.vol20).abs().mean():.2f}") if False else ""
    W=S.nsmallest(len(g)//20,"g1")
    out["worst5pct_profile"]=pd.Series({"short_share":(W.postRebalance_current_allocation<0).mean(),"mean_absz":(W.r/W.vol20).abs().mean(),"all_absz":(S.r/S.vol20).abs().mean(),"mean_vr":W.vr.mean(),"all_vr":S.vr.mean()})
    return out
