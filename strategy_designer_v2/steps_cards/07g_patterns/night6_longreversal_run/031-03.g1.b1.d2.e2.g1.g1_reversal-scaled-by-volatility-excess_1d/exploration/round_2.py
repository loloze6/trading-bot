def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for w, b in data["bars"]["XMRUSD"].items():
        b = b.copy().reset_index(drop=True)
        c = b["close"]; r = c.pct_change()
        b["nxt"] = c.shift(-1)/c - 1
        b["nxt2"] = c.shift(-2)/c - 1
        b["vol30"] = r.rolling(30, min_periods=20).std()
        b["volratio"] = b["vol30"]/b["vol30"].rolling(180, min_periods=45).mean()
        b["z1"] = r/b["vol30"]
        b["clv"] = ((c-b["low"])-(b["high"]-c))/(b["high"]-b["low"]).replace(0,np.nan)
        b["range"] = (b["high"]-b["low"])/c
        b["rangez"] = b["range"]/b["range"].rolling(30, min_periods=20).mean()
        b["lowtail"] = (np.minimum(b["open"],c)-b["low"])/c/b["vol30"]
        b["hightail"] = (b["high"]-np.maximum(b["open"],c))/c/b["vol30"]
        b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
        b["pos"] = np.arange(len(b)); b["w"] = w
        b["fc"] = b["forecast"]
        rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["nxt"] - d["nxt"].mean()
    s = d[["z1","clv","rangez","volratio","ex","yr","lowtail","hightail","fc"]].dropna(subset=["z1","clv","ex"])
    # multiple regression z1 + clv
    X = np.column_stack([np.ones(len(s)), s["z1"], s["clv"]])
    beta, *_ = np.linalg.lstsq(X, s["ex"], rcond=None)
    res = s["ex"] - X@beta
    sig2 = (res**2).sum()/(len(s)-3)
    se = np.sqrt(np.diag(sig2*np.linalg.inv(X.T@X)))
    out["ols_z1_clv"] = pd.DataFrame({"beta":beta,"t":beta/se},index=["c","z1","clv"])
    # clv residual vs forecast
    s2 = s.dropna(subset=["fc"])
    X = np.column_stack([np.ones(len(s2)), s2["fc"], s2["clv"]])
    beta, *_ = np.linalg.lstsq(X, s2["ex"], rcond=None)
    res = s2["ex"] - X@beta; sig2=(res**2).sum()/(len(s2)-3)
    se = np.sqrt(np.diag(sig2*np.linalg.inv(X.T@X)))
    out["ols_fc_clv"] = pd.DataFrame({"beta":beta,"t":beta/se},index=["c","fc","clv"])
    # clv by year
    r={}
    for k,g in s.groupby("yr"):
        lr=stats.linregress(g["clv"],g["ex"]); r[k]=[lr.slope,lr.slope/lr.stderr,len(g)]
    out["clv_slope_by_year"]=pd.DataFrame(r,index=["slope","t","n"]).T
    # clv by range tercile
    g3=s.dropna(subset=["rangez"]).copy(); g3["rq"]=pd.qcut(g3["rangez"],3,labels=False)
    r={}
    for k,g in g3.groupby("rq"):
        lr=stats.linregress(g["clv"],g["ex"]); r[k]=[lr.slope,lr.slope/lr.stderr,len(g),g["rangez"].mean()]
    out["clv_slope_by_range_terc"]=pd.DataFrame(r,index=["slope","t","n","rz"]).T
    # clv on up vs down days
    r={}
    for nm,g in [("up",s[s.z1>0]),("down",s[s.z1<0])]:
        lr=stats.linregress(g["clv"],g["ex"]); r[nm]=[lr.slope,lr.slope/lr.stderr,len(g)]
    out["clv_slope_up_vs_down"]=pd.DataFrame(r,index=["slope","t","n"]).T
    # tails
    r={}
    for col in ["lowtail","hightail"]:
        g=s[[col,"ex"]].dropna(); lr=stats.linregress(g[col],g["ex"]); r[col]=[lr.slope,lr.slope/lr.stderr,len(g)]
    out["tail_slopes"]=pd.DataFrame(r,index=["slope","t","n"]).T
    # down-day fade graded: deciles of z1 among down days
    dn=s[s.z1<0].copy(); dn["q"]=pd.qcut(dn["z1"],5,labels=False)
    gg=dn.groupby("q")["ex"].agg(["mean","count","std"]); gg["t"]=gg["mean"]/(gg["std"]/np.sqrt(gg["count"])); gg["z"]=dn.groupby("q")["z1"].mean()
    out["down_z1_quint"]=gg.round(5)
    # clv 2-day non-overlap
    g=d[d["pos"]%2==0][["clv","nxt2"]].dropna(); g["e"]=g["nxt2"]-g["nxt2"].mean()
    lr=stats.linregress(g["clv"],g["e"]); out["clv_next2_nonoverlap"]=pd.Series({"slope":lr.slope,"t":lr.slope/lr.stderr,"n":len(g)})
    # clv slope by window halves (w1-12 vs w13-24)
    s3=d[["clv","ex","w"]].dropna(); s3["half"]=s3["w"].str[1:].astype(int)>12
    r={}
    for k,g in s3.groupby("half"):
        lr=stats.linregress(g["clv"],g["ex"]); r[str(k)]=[lr.slope,lr.slope/lr.stderr,len(g)]
    out["clv_by_half"]=pd.DataFrame(r,index=["slope","t","n"]).T
    return out
