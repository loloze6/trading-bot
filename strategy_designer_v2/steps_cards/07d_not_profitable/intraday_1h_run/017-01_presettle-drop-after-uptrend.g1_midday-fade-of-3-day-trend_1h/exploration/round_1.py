def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]
    rows=[]; hourrows=[]; hzrows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"])
            cl=b["close"].astype(float)
            nxt=cl.shift(-1)/cl-1
            a=b["postRebalance_current_allocation"].astype(float)
            gross=a*nxt
            fee=1-b["postRebalance_total_value"].astype(float)/b["total_portfolio_value"].astype(float)
            r72=cl/cl.shift(72)-1
            act=a.abs()>0
            rows.append(dict(coin=c,win=w,gross=gross.sum(),fee=fee.sum(),nact=int(act.sum()),
                             absalloc=a[act].abs().mean(),turn=b["allocation_change"].astype(float).abs().sum() if "allocation_change" in b else np.nan))
            df=pd.DataFrame({"h":ts.dt.hour,"r72":r72,"n1":nxt,"n24":cl.shift(-24)/cl-1,"n4":cl.shift(-4)/cl-1})
            hourrows.append(df)
    R=pd.DataFrame(rows)
    per=R.groupby("coin")[["gross","fee","nact"]].sum()
    per["absalloc"]=R.groupby("coin")["absalloc"].mean()
    tot=pd.Series({"gross_sum":R.gross.sum(),"fee_sum":R.fee.sum(),"n_active":R.nact.sum(),
                   "gross_per_active":R.gross.sum()/R.nact.sum(),"fee_per_active":R.fee.sum()/R.nact.sum(),
                   "mean_absalloc":R.absalloc.mean()})
    H=pd.concat(hourrows)
    out=[]
    for h,g in H.groupby("h"):
        g1=g.dropna(subset=["r72","n1"])
        rho=stats.spearmanr(g1.r72,g1.n1)[0]
        s=-np.sign(g1.r72)*g1.n1
        out.append(dict(hour=h,n=len(g1),spearman=rho,fade_mean_bp=s.mean()*1e4,t=s.mean()/s.std()*np.sqrt(len(s))))
    hh=pd.DataFrame(out).set_index("hour")
    hz=[]
    for col in ["n1","n4","n24"]:
        g1=H[H.h==11].dropna(subset=["r72",col])
        s=-np.sign(g1.r72)*g1[col]
        q=pd.qcut(g1.r72,5,labels=False)
        hz.append(dict(h=col,n=len(g1),spearman=stats.spearmanr(g1.r72,g1[col])[0],fade_bp=s.mean()*1e4,t=s.mean()/s.std()*np.sqrt(len(s)),
                      q0_bp=g1[col][q==0].mean()*1e4,q4_bp=g1[col][q==4].mean()*1e4))
    return {"totals":tot,"per_coin":per,"by_hour_bar_ts":hh,"hour11_horizons":pd.DataFrame(hz)}
