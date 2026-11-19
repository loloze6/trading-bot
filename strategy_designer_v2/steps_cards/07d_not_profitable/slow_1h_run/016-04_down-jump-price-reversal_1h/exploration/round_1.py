def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    rows=[]; grid=[]; fstats=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            al=b["postRebalance_current_allocation"].fillna(0).values
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            gross=np.nansum(al*r1)
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"]).values
            feer=np.nansum(fee/b["total_portfolio_value"].values)
            turn=np.nansum(np.abs(np.diff(np.r_[0,al])))
            rows.append(dict(coin=c,w=w,gross=gross,fee=feer,turn=turn,nbars=len(b),
                             meanal=al.mean(),fracin=(np.abs(al)>1e-9).mean(),
                             fracshort=(al<-1e-9).mean()))
            f=b["forecast"].values; reg=b["regime"].values
            fstats.append(dict(coin=c,act=(reg=="mean_reversion").mean(),
                               fneg=((reg=="mean_reversion")&(f<0)).sum(),fpos=((reg=="mean_reversion")&(f>0)).sum()))
            for i in range(0,len(b)-72,72):
                grid.append(dict(coin=c,w=w,f=f[i],al=al[i],reg=reg[i],
                                 r=cl[i+72]/cl[i]-1,past=(cl[i]/cl[i-72]-1) if i>=72 else np.nan))
    R=pd.DataFrame(rows); G=pd.DataFrame(grid); F=pd.DataFrame(fstats)
    G["ex"]=G["r"]-G.groupby("coin")["r"].transform("mean")
    byc=R.groupby("coin")[["gross","fee","turn","nbars"]].sum()
    byc["gross_per_day"]=byc.gross/byc.nbars*24; byc["fee_per_day"]=byc.fee/byc.nbars*24
    byc["turn_per_day"]=byc.turn/byc.nbars*24
    byc["meanal"]=R.groupby("coin").meanal.mean(); byc["fracshort"]=R.groupby("coin").fracshort.mean()
    fs=F.groupby("coin").sum()
    a=G[G.reg=="mean_reversion"].copy()
    a["fb"]=pd.cut(a.f,[-21,-5,-1,0,1,5,21])
    fb=a.groupby("fb").ex.agg(["count","mean"])
    fb["t"]=a.groupby("fb").ex.apply(lambda x:x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan)
    # past fall size grading
    a["pb"]=pd.qcut(a.past,5,duplicates="drop")
    pb=a.groupby("pb").ex.agg(["count","mean"])
    oth=G[G.reg!="mean_reversion"].ex.agg(["count","mean"])
    # daily book
    D=pd.concat([d.assign(coin=c) for c in days for d in days[c].values()])
    dd=D.groupby("coin")[["book_return","coin_return"]].mean()
    return {"per_coin_cost":byc.round(5),"forecast_sign_counts":fs,
            "fallen_ex_by_forecast":fb.round(4),"fallen_ex_by_pastfall":pb.round(4),
            "unfallen_ex":oth.round(4),"daily_means":dd.round(5)}
