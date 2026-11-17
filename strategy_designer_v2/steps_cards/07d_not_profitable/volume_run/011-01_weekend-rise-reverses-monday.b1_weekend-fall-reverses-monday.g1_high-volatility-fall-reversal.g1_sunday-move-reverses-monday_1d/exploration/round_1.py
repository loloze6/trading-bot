def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; drows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            b["ts"]=pd.to_datetime(b["timestamp"])
            b["wd"]=b["ts"].dt.dayofweek
            b["r"]=b["close"].pct_change()
            b["vol20"]=b["r"].rolling(20,min_periods=10).std()
            b["z"]=b["r"]/b["vol20"]
            b["nxt"]=b["close"].shift(-1)/b["close"]-1
            b["alloc"]=b["postRebalance_current_allocation"]
            b["gain"]=b["alloc"]*b["nxt"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["r5"]=b["close"]/b["close"].shift(5)-1
            b["r20"]=b["close"]/b["close"].shift(20)-1
            b["coin"]=c; b["win"]=w
            b["year"]=b["ts"].dt.year
            rows.append(b)
    B=pd.concat(rows)
    mu=B.groupby("coin")["r"].mean()
    B["ex"]=B["nxt"]-B["coin"].map(mu)
    S=B[(B.regime=="mean_reversion")&B.nxt.notna()]
    out={}
    out["sunday_summary"]=pd.Series({"n":len(S),"mean_gain":S.gain.mean(),"t_gain":S.gain.mean()/S.gain.std()*np.sqrt(len(S)),
        "mean_fee_all_bars":B.fee.mean()*7,"mean_abs_alloc":S.alloc.abs().mean(),"mean_alloc":S.alloc.mean(),
        "fee_per_sunday":B.fee.sum()/len(S)})
    # weekday reversal: slope of next excess return on -z, all weekdays
    res={}
    for d in range(7):
        g=B[(B.wd==d)].dropna(subset=["z","ex"])
        sl=stats.linregress(-g.z,g.ex)
        res[d]={"n":len(g),"slope":sl.slope,"t":sl.slope/sl.stderr,"corr":sl.rvalue}
    out["reversal_by_weekday(0=Mon)"]=pd.DataFrame(res).T
    S=S.dropna(subset=["z"])
    S["zq"]=pd.qcut(S.z,6,labels=False)
    out["sunday_by_z_sextile"]=S.groupby("zq").agg(z=("z","mean"),n=("z","size"),next_ex=("ex","mean"),gain=("gain","mean"),alloc=("alloc","mean"))
    S["r20q"]=pd.qcut(S.r20,4,labels=False)
    out["sunday_by_r20_quart"]=S.groupby("r20q").agg(r20=("r20","mean"),n=("z","size"),gain=("gain","mean"),
        corr=("z",lambda x: np.corrcoef(-x,S.loc[x.index,"ex"])[0,1]))
    S["volq"]=S.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["sunday_by_vol_tercile"]=S.groupby("volq").agg(vol=("vol20","mean"),n=("z","size"),gain=("gain","mean"),
        corr=("z",lambda x: np.corrcoef(-x,S.loc[x.index,"ex"])[0,1]))
    out["by_coin"]=S.groupby("coin").agg(gain=("gain","mean"),n=("z","size"))
    out["by_year"]=S.groupby("year").agg(gain=("gain","mean"),n=("z","size"))
    # book days
    D=pd.concat([d.assign(coin=c,win=w) for c in data["days"] for w,d in data["days"][c].items()])
    bd=D.groupby(["win","day"])[["book_return","coin_return"]].mean()
    out["book_daily"]=pd.Series({"book_mean":bd.book_return.mean(),"book_sd":bd.book_return.std(),
        "hold_mean":bd.coin_return.mean(),"hold_sd":bd.coin_return.std(),"ndays":len(bd)})
    # long vs short side
    S["side"]=np.sign(S.alloc)
    out["by_side"]=S.groupby("side").agg(n=("z","size"),gain=("gain","mean"),nxt=("nxt","mean"))
    return out
