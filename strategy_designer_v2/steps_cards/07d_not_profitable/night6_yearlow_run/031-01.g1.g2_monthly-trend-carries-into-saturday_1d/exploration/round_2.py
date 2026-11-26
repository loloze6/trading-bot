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
            b["vr"]=b["vol20"]/b["vol60"]
            b["hi60"]=b["close"]/b["close"].rolling(60).max()-1
            b["coin"]=c; b["w"]=w; b["wn"]=int(w[1:]); b["year"]=b["ts"].dt.year; b["wd"]=b["ts"].dt.weekday
            b["gain"]=b["postRebalance_current_allocation"]*b["r1"]
            b["nextday"]=(b["ts"]+pd.Timedelta(days=1)).dt.normalize()
            rows.append(b)
            d=data["days"][c][w].copy(); d["coin"]=c; d["w"]=w; d["wn"]=int(w[1:]); dayrows.append(d)
    B=pd.concat(rows,ignore_index=True)
    D=pd.concat(dayrows,ignore_index=True)
    D["day"]=pd.to_datetime(D["day"]).dt.normalize()
    mu=B.groupby("coin")["r1"].mean()
    B["ex"]=B["r1"]-B["coin"].map(mu)
    out={}
    # book daily
    bk=D.groupby(["wn","day"])["book_return"].mean().dropna().reset_index().sort_values(["wn","day"]).reset_index(drop=True)
    bk["v"]=(1+bk["book_return"]).cumprod()
    bk["dd"]=bk["v"]/bk["v"].cummax()-1
    out["max dd"]=float(bk["dd"].min())
    ti=bk["dd"].idxmin(); pi=bk.loc[:ti,"v"].idxmax()
    out["deepest fall: windows, days, years"]=f"w{bk.loc[pi,'wn']}->w{bk.loc[ti,'wn']}, {ti-pi} days, years {bk.loc[pi,'day'].year}-{bk.loc[ti,'day'].year}"
    bk["indd"]=False; bk.loc[pi:ti,"indd"]=True
    # dd by year
    bk["year"]=bk["day"].dt.year
    out["book by year"]=bk.groupby("year").agg(n=("book_return","size"),mean=("book_return","mean"),sd=("book_return","std"),mindd=("dd","min"))
    # cases
    T=B[(B.regime=="trending")&B.r1.notna()].copy()
    T["sg"]=np.sign(T["forecast"]); T["sx"]=T["sg"]*T["ex"]
    key=bk.set_index(["wn","day"])["indd"]
    T["indd"]=[key.get((a,b_),False) for a,b_ in zip(T["wn"],T["nextday"])]
    out["cases in deepest fall vs rest"]=T.groupby("indd").agg(n=("r1","size"),longshare=("sg",lambda s:(s>0).mean()),sx=("sx","mean"),gain=("gain","mean"),vol20=("vol20","mean"),ret20=("ret20","mean"),absalloc=("postRebalance_current_allocation",lambda s:s.abs().mean()))
    out["by side"]=T.groupby("sg").agg(n=("r1","size"),sx=("sx","mean"),ex=("ex","mean"),gain=("gain","mean"),gsd=("gain","std"),gmin=("gain","min"))
    # side condition alone: all Saturdays (no signal grading) mean ex
    S=B[(B.wd==4)&B.r1.notna()]
    out["all Friday->Sat unsigned ex mean, t, n"]=pd.Series({"mean":S.ex.mean(),"t":stats.ttest_1samp(S.ex,0).statistic,"n":len(S)})
    # vol terciles
    T["vt"]=T.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["by vol tercile, side"]=T.groupby(["vt","sg"]).agg(n=("r1","size"),sx=("sx","mean"),ex=("ex","mean"),gain=("gain","mean"),gsd=("gain","std"))
    # vol ratio terciles
    T["vrt"]=pd.qcut(T["vr"].rank(method="first"),3,labels=False)
    out["by vol20/vol60 tercile"]=T.groupby("vrt").agg(n=("r1","size"),vr=("vr","mean"),sx=("sx","mean"),gain=("gain","mean"),gsd=("gain","std"))
    # |forecast| strength
    T["ft"]=pd.qcut(T["forecast"].abs().rank(method="first"),3,labels=False)
    out["by |forecast| tercile, side"]=T.groupby(["ft","sg"]).agg(n=("r1","size"),f=("forecast","mean"),sx=("sx","mean"),gain=("gain","mean"),gsd=("gain","std"))
    # condition alone check for long side in low/mid vol: non-Friday bars with ret20>0 in same vol tercile
    B["vt"]=B.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    O=B[(B.wd!=4)&B.r1.notna()&B.ret20.notna()]
    O["sg"]=np.sign(O["ret20"]); O["sx"]=O["sg"]*O["ex"]
    out["non-Friday days, signed by ret20: by vol tercile, side"]=O.groupby(["vt","sg"]).agg(n=("r1","size"),sx=("sx","mean"))
    # gross vs net on trades
    tr=pd.concat([t.assign(coin=c) for c in data["trades"] for w,t in data["trades"][c].items()],ignore_index=True)
    out["trades"]=tr.groupby("side").agg(n=("side","size"),pl=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_h=("duration_minutes",lambda s:s.mean()/60))
    return out
