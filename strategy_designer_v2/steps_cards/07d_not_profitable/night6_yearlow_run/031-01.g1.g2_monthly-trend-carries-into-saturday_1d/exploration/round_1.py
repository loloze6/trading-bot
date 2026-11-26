def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; dayrows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy().reset_index(drop=True)
            b["ts"]=pd.to_datetime(b["timestamp"])
            b["r1"]=b["close"].shift(-1)/b["close"]-1
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            b["ret5"]=b["close"]/b["close"].shift(5)-1
            lr=np.log(b["close"]).diff()
            b["vol20"]=lr.rolling(20).std()
            b["vol60"]=lr.rolling(60).std()
            b["hi60"]=b["close"]/b["close"].rolling(60).max()-1
            b["coin"]=c; b["w"]=w; b["year"]=b["ts"].dt.year; b["wd"]=b["ts"].dt.weekday
            b["gain"]=b["postRebalance_current_allocation"]*b["r1"]
            rows.append(b)
            d=data["days"][c][w].copy(); d["coin"]=c; d["w"]=w; dayrows.append(d)
    B=pd.concat(rows,ignore_index=True)
    D=pd.concat(dayrows,ignore_index=True)
    mu=B.groupby("coin")["r1"].mean()
    B["ex"]=B["r1"]-B["coin"].map(mu)
    T=B[(B.regime=="trending")&B.r1.notna()].copy()
    out={}
    out["wd of trending"]=T["wd"].value_counts()
    T["side"]=np.sign(T["postRebalance_current_allocation"])
    g=T.groupby("side").agg(n=("gain","size"),gain=("gain","mean"),ex=("ex","mean"),r1=("r1","mean"),alloc=("postRebalance_current_allocation","mean"))
    out["by side"]=g
    T["ft"]=pd.qcut(T["forecast"].rank(method="first"),5,labels=False)
    out["by forecast quintile"]=T.groupby("ft").agg(n=("r1","size"),f=("forecast","mean"),r1=("r1","mean"),ex=("ex","mean"),gain=("gain","mean"),gsd=("gain","std"))
    T["vt"]=T.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    T["sg"]=np.sign(T["forecast"])
    T["sx"]=T["sg"]*T["ex"]
    out["by vol tercile"]=T.groupby("vt").agg(n=("r1","size"),sx=("sx","mean"),gain=("gain","mean"),gsd=("gain","std"),gmin=("gain","min"))
    out["by year"]=T.groupby("year").agg(n=("r1","size"),sx=("sx","mean"),gain=("gain","mean"),gsd=("gain","std"))
    T["ht"]=pd.cut(T["hi60"],[-1,-0.3,-0.15,-0.05,0.001])
    out["by dist from 60d high, side"]=T.groupby(["ht","sg"]).agg(n=("r1","size"),sx=("sx","mean"),gain=("gain","mean"))
    # book
    D=D.sort_values(["w","day"])
    bk=D.groupby(["w","day"])["book_return"].mean().dropna()
    bk=bk.reindex(sorted(bk.index,key=lambda x:(int(x[0][1:]),x[1])))
    v=(1+bk).cumprod(); dd=v/v.cummax()-1
    out["max dd"]=float(dd.min())
    # episodes: worst days of the book
    worst=bk.nsmallest(30)
    wk=pd.DataFrame({"r":worst.values,"w":[i[0] for i in worst.index]})
    out["30 worst book days sum, mean"]=pd.Series({"sum":worst.sum(),"mean":worst.mean(),"total_sum_all":bk.sum()})
    # loss cases: biggest losing coin-cases, what preceded
    T["lossq"]=T["gain"]<T["gain"].quantile(0.05)
    out["worst 5% cases profile vs rest"]=T.groupby("lossq")[["ret20","ret5","vol20","hi60","forecast","postRebalance_current_allocation"]].mean()
    out["worst 5% side share"]=T[T.lossq].groupby("sg").size()
    # dd episode location
    trough=dd.idxmin(); peak=v.loc[:trough].idxmax()
    out["dd peak/trough window"]=f"{peak[0]} -> {trough[0]}"
    return out
