def explore(data):
    import numpy as np, pandas as pd
    rows=[]; dayrows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            b["ret1"]=b["close"].shift(-1)/b["close"]-1
            b["fwd30"]=b["close"].shift(-30)/b["close"]-1
            b["fwd10"]=b["close"].shift(-10)/b["close"]-1
            b["alloc"]=b["postRebalance_current_allocation"]
            b["trend"]=(b["regime"]=="trending")
            col="debug_info.components.stall.last_history_value"
            b["stall_raw"]=b[col] if col in b else np.nan
            b["coin"]=c; b["win"]=w
            b["pos"]=np.arange(len(b))
            rows.append(b[["coin","win","pos","ret1","fwd30","fwd10","alloc","trend","stall_raw","forecast","volume"]])
            d=data["days"][c][w].copy(); d["coin"]=c; d["win"]=w
            dayrows.append(d)
    B=pd.concat(rows); D=pd.concat(dayrows)
    out={}
    out["share bars trending"]=B["trend"].mean()
    out["share bars allocated (|alloc|>0.01)"]=(B["alloc"].abs()>0.01).mean()
    tr=B[B["trend"]]
    out["share trending bars with alloc>0.01"]=(tr["alloc"]>0.01).mean()
    out["mean alloc when allocated"]=B.loc[B["alloc"]>0.01,"alloc"].mean()
    # coin mean daily ret
    cm=B.groupby("coin")["ret1"].mean()
    B["cm"]=B["coin"].map(cm)
    out["mean ret1 all bars"]=B["ret1"].mean()
    g=tr.copy(); g["has"]=g["alloc"]>0.01
    out["trending bars by in-position"]=g.groupby("has").agg(n=("ret1","size"),ret1=("ret1","mean"),fwd10=("fwd10","mean"),fwd30=("fwd30","mean"),stall=("stall_raw","mean"))
    out["trending by stall raw bucket"]=tr.groupby(pd.cut(tr["stall_raw"],[-1,0,5,15,30,60])).agg(n=("ret1","size"),ret1=("ret1","mean"),fwd30=("fwd30","mean"),alloc=("alloc","mean"))
    # not trending, by alloc
    out["non-trending mean ret1"]=B.loc[~B["trend"],"ret1"].mean()
    # book decomposition
    B["gain"]=B["alloc"]*B["ret1"]; B["mkt"]=B["alloc"]*B["cm"]
    out["mean bar gain (all)"]=B["gain"].mean(); out["mean bar mkt part"]=B["mkt"].mean()
    out["book daily mean by coin"]=D.groupby("coin")["book_return"].mean()
    out["book daily mean by year"]=D.assign(y=pd.to_datetime(D["day"]).dt.year).groupby("y")["book_return"].agg(["mean","count"])
    out["trending share by coin"]=B.groupby("coin")["trend"].mean()
    return out
