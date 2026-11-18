def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; days=[]
    for c in data["bars"]:
        allr=[]
        for w,b in data["bars"][c].items():
            b=b.copy()
            b["r1"]=b["close"].shift(-1)/b["close"]-1
            allr.append(b["r1"].dropna())
        cm=pd.concat(allr).mean()
        for w,b in data["bars"][c].items():
            b=b.copy().reset_index(drop=True)
            b["coin"]=c; b["win"]=w
            b["r1"]=b["close"].shift(-1)/b["close"]-1
            b["r10"]=b["close"].shift(-10)/b["close"]-1
            hh=b["high"].rolling(20).max().shift(1)
            b["brk"]=(b["close"]-hh)/hh*100
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            b["ret5"]=b["close"]/b["close"].shift(5)-1
            b["vr"]=b["volume"]/b["volume"].rolling(20).mean().shift(1)
            b["cm"]=cm
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["r1"]
            rows.append(b)
        for w,d in data["days"][c].items():
            d=d.copy(); d["coin"]=c; d["win"]=w; days.append(d)
    B=pd.concat(rows); D=pd.concat(days)
    out={}
    act=B[B["pos"].abs()>1e-9]
    out["exposure share, mean pos when in"]=pd.Series({"share":len(act)/len(B),"meanpos":act["pos"].mean(),
        "gross mean gain/bar":B["gain"].mean(),"fee mean/bar":B["fee"].mean(),
        "mkt part":(B["pos"]*B["cm"]).mean(),"r1 in-pos mean":act["r1"].mean(),"r1 all mean":B["r1"].mean()})
    # next-day return on breakout bars by breakout size tercile, ret20, vol ratio
    br=B[B["regime"]=="trending"].dropna(subset=["r1"])
    for col in ["brk","ret20","vr","debug_info.components.width.post_pipeline_value"]:
        x=br.dropna(subset=[col])
        q=pd.qcut(x[col],3,labels=["lo","mid","hi"])
        g=x.groupby(q)
        out["r1 & r10 by "+col[-20:]]=pd.DataFrame({"n":g.size(),"r1":g["r1"].mean(),"r10":g["r10"].mean(),"gain":g["gain"].mean(),"fee":g["fee"].mean()})
    # by consecutive breakout days
    br2=B.copy(); br2["t"]=(br2["regime"]=="trending").astype(int)
    br2["run"]=br2.groupby(["coin","win"])["t"].transform(lambda s: s.groupby((s!=s.shift()).cumsum()).cumsum())
    x=br2[br2["t"]==1].dropna(subset=["r1"]); x["runc"]=x["run"].clip(upper=4)
    g=x.groupby("runc"); out["by run length"]=pd.DataFrame({"n":g.size(),"r1":g["r1"].mean(),"gain":g["gain"].mean(),"fee":g["fee"].mean()})
    D=D.dropna(subset=["book_return"])
    dd=D.groupby("day")[["book_return","coin_return"]].mean()
    out["daily book vs hold"]=pd.DataFrame({"mean":dd.mean(),"std":dd.std(),"sharpe":dd.mean()/dd.std()*np.sqrt(365)})
    g=B.groupby("coin"); out["by coin"]=pd.DataFrame({"gain":g["gain"].mean(),"fee":g["fee"].mean(),"share":g["pos"].apply(lambda s:(s.abs()>0).mean())})
    D["year"]=pd.to_datetime(D["day"]).dt.year
    g=D.groupby("year"); out["by year"]=pd.DataFrame({"book":g["book_return"].mean(),"coin":g["coin_return"].mean()})
    return out
