def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    rows=[]; brs=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            b["ret1"]=b["close"].shift(-1)/b["close"]-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["ret1"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["coin"]=c; b["w"]=w
            b["dist"]=b["close"]/b["close"].rolling(364,min_periods=1).max()-1
            b["m30"]=b["close"]/b["close"].shift(30)-1
            b["m7"]=b["close"]/b["close"].shift(7)-1
            b["fwd7"]=b["close"].shift(-7)/b["close"]-1
            brs.append(b)
    B=pd.concat(brs)
    d=[]
    for c in data["days"]:
        for w,x in data["days"][c].items():
            x=x.copy(); x["coin"]=c; x["w"]=w; d.append(x)
    D=pd.concat(d)
    out["daily"]=pd.Series({"book_mean":D.book_return.mean(),"coin_mean":D.coin_return.mean(),
        "mean_pos":B.pos.mean(),"share_long":(B.pos>0).mean(),"share_trending":(B.regime=="trending").mean(),
        "mean_pos_when_trending":B.pos[B.regime=="trending"].mean(),
        "gross_gain_mean":B.gain.mean(),"fee_per_bar":B.fee.mean(),
        "mean_absturnover":B["allocation_change"].abs().mean() if "allocation_change" in B else np.nan})
    out["by_coin"]=B.groupby("coin").agg(gain=("gain","mean"),fee=("fee","mean"),pos=("pos","mean"),r=("ret1","mean"))
    T=B[B.regime=="trending"].copy()
    T["fq"]=pd.qcut(T.forecast.rank(method="first"),5,labels=False)
    out["trend_by_fcq"]=T.groupby("fq").agg(fc=("forecast","mean"),pos=("pos","mean"),ret1=("ret1","mean"),gain=("gain","mean"),fee=("fee","mean"),n=("gain","size"))
    T["dq"]=pd.qcut(T.dist.rank(method="first"),5,labels=False)
    out["trend_by_dist"]=T.groupby("dq").agg(dist=("dist","mean"),ret1=("ret1","mean"),pos=("pos","mean"),gain=("gain","mean"))
    N=B[B.regime!="trending"]
    N=N.copy();N["dq"]=pd.qcut(N.dist.rank(method="first"),5,labels=False)
    out["nontrend_by_dist"]=N.groupby("dq").agg(dist=("dist","mean"),ret1=("ret1","mean"),pos=("pos","mean"))
    out["by_year"]=B.assign(y=pd.to_datetime(B.timestamp).dt.year).groupby("y").agg(gain=("gain","mean"),r=("ret1","mean"),pos=("pos","mean"),trend=("regime",lambda s:(s=="trending").mean()))
    out["sizing"]=B.loc[B.regime=="trending",["sizing_realised_vol","pos","forecast"]].describe()
    return out
