def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy().reset_index(drop=True)
            b["ts"]=pd.to_datetime(b["timestamp"])
            b["wd"]=b["ts"].dt.dayofweek
            b["r"]=b["close"].pct_change()
            b["vol20"]=b["r"].rolling(20,min_periods=10).std()
            b["z"]=b["r"]/b["vol20"]
            b["nxt"]=b["close"].shift(-1)/b["close"]-1
            b["alloc"]=b["postRebalance_current_allocation"]
            b["gain"]=b["alloc"]*b["nxt"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["r20"]=b["close"]/b["close"].shift(20)-1
            b["r60"]=b["close"]/b["close"].shift(60)-1
            b["coin"]=c; b["win"]=w
            b["year"]=b["ts"].dt.year
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    mu=B.groupby("coin")["r"].mean()
    B["ex"]=B["nxt"]-B["coin"].map(mu)
    B["mu"]=B["coin"].map(mu)
    def corr(g):
        g=g.dropna(subset=["z","ex"])
        if len(g)<5: return np.nan
        return np.corrcoef(-g.z.values,g.ex.values)[0,1]
    S=B[(B.regime=="mean_reversion")&B.nxt.notna()].copy()
    out={}
    out["sunday_summary"]=pd.Series({"n":len(S),"mean_gain":S.gain.mean(),"t_gain":S.gain.mean()/S.gain.std()*np.sqrt(len(S)),
        "mean_abs_alloc":S.alloc.abs().mean(),"mean_alloc":S.alloc.mean(),
        "fee_per_sunday":B.fee.sum()/len(S),"market_part":(S.alloc*S.mu).mean(),
        "share_alloc_nonzero_offsunday":(B[B.regime!="mean_reversion"].alloc.abs()>1e-6).mean()})
    res={}
    for d in range(7):
        g=B[B.wd==d].dropna(subset=["z","ex"])
        sl=stats.linregress(-g.z,g.ex)
        res[d]={"n":len(g),"slope":sl.slope,"t":sl.slope/sl.stderr}
    out["reversal_by_weekday_0Mon"]=pd.DataFrame(res).T
    S=S.dropna(subset=["z"])
    S["zq"]=pd.qcut(S.z,6,labels=False)
    out["sunday_by_z_sextile"]=S.groupby("zq").agg(z=("z","mean"),n=("z","size"),next_ex=("ex","mean"),gain=("gain","mean"),alloc=("alloc","mean"))
    for col,k in [("r20",4),("r60",4),("vol20",3)]:
        S[col+"q"]=S.groupby("coin")[col].transform(lambda x: pd.qcut(x,k,labels=False,duplicates="drop"))
        g=S.groupby(col+"q")
        t=g.agg(m=(col,"mean"),n=("z","size"),gain=("gain","mean"),alloc=("alloc","mean"))
        t["corr"]=g.apply(corr)
        out["sunday_by_"+col]=t
    out["by_coin"]=S.groupby("coin").agg(gain=("gain","mean"),n=("z","size"))
    out["by_year"]=S.groupby("year").agg(gain=("gain","mean"),n=("z","size"))
    S["side"]=np.sign(S.alloc.round(6))
    out["by_side"]=S.groupby("side").agg(n=("z","size"),gain=("gain","mean"),nxt=("nxt","mean"),z=("z","mean"))
    D=pd.concat([d.assign(coin=c,win=w) for c in data["days"] for w,d in data["days"][c].items()],ignore_index=True)
    bd=D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book_daily"]=pd.Series({"book_mean":bd.book_return.mean(),"book_sd":bd.book_return.std(),
        "hold_mean":bd.coin_return.mean(),"hold_sd":bd.coin_return.std(),"ndays":len(bd)})
    # drawdown of chained book
    bd["wn"]=bd.win.str[1:].astype(int)
    bd=bd.sort_values(["wn","day"])
    eq=(1+bd.book_return.fillna(0)).cumprod()
    dd=eq/eq.cummax()-1
    bd["dd"]=dd.values
    out["dd_by_window"]=bd.groupby("wn").agg(ret=("book_return",lambda x:(1+x.fillna(0)).prod()-1),mindd=("dd","min"),hold=("coin_return",lambda x:(1+x.fillna(0)).prod()-1))
    out["max_dd"]=float(dd.min())
    # biggest losing Sundays
    S["absz"]=S.z.abs()
    S["losing"]=S.gain<S.gain.quantile(0.05)
    out["worst5pct_vs_rest"]=S.groupby("losing").agg(z=("absz","mean"),r20=("r20","mean"),vol=("vol20","mean"),alloc=("alloc",lambda x:x.abs().mean()),sameSign=("z",lambda x: np.nan))
    return out
