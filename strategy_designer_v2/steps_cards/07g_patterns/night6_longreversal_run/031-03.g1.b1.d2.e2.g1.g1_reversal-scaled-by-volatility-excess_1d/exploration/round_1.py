def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]["XMRUSD"]
    rows = []
    for w, b in bars.items():
        b = b.copy().reset_index(drop=True)
        c = b["close"]
        r = c.pct_change()
        b["r1"] = r
        b["nxt"] = c.shift(-1)/c - 1
        b["nxt3"] = c.shift(-3)/c - 1
        b["nxt5"] = c.shift(-5)/c - 1
        b["vol30"] = r.rolling(30, min_periods=20).std()
        b["volratio"] = b["vol30"]/b["vol30"].rolling(180, min_periods=45).mean()
        b["z1"] = r/b["vol30"]
        b["r3"] = c/c.shift(3)-1
        b["z3"] = b["r3"]/(b["vol30"]*np.sqrt(3))
        b["r60"] = c/c.shift(60)-1
        b["z60"] = b["r60"]/(b["vol30"]*np.sqrt(60))
        b["range"] = (b["high"]-b["low"])/c
        b["rangez"] = b["range"]/b["range"].rolling(30, min_periods=20).mean()
        b["clv"] = ((c-b["low"])-(b["high"]-c))/(b["high"]-b["low"]).replace(0,np.nan)
        b["volz"] = np.log(b["volume"].replace(0,np.nan))-np.log(b["volume"].replace(0,np.nan)).rolling(30,min_periods=20).mean()
        b["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
        b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
        b["pos"] = np.arange(len(b))
        b["w"] = w
        b["gain"] = b["postRebalance_current_allocation"]*b["nxt"]
        rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    mu = d["nxt"].mean()
    d["ex"] = d["nxt"] - mu
    def grp(col, q=5, y="ex"):
        s = d[[col, y]].dropna()
        s["q"] = pd.qcut(s[col], q, labels=False, duplicates="drop")
        g = s.groupby("q")[y].agg(["mean","count","std"])
        g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["xmean"] = s.groupby("q")[col].mean()
        return g.round(5)
    out["fcst_quint_ex"] = grp("forecast", 10)
    out["z1_dec_ex"] = grp("z1", 10)
    out["volratio_quint_ex"] = grp("volratio", 5)
    # fade by vol regime: slope of ex on -z1 per volratio tercile
    s = d[["z1","volratio","ex"]].dropna()
    s["vq"] = pd.qcut(s["volratio"],3,labels=False)
    res={}
    for k,g in s.groupby("vq"):
        lr = stats.linregress(-g["z1"], g["ex"])
        res[k]=[lr.slope, lr.slope/lr.stderr, len(g), g["volratio"].mean()]
    out["fade_slope_by_volterc"]=pd.DataFrame(res,index=["slope","t","n","vr"]).T
    # asymmetry up vs down
    s = d[["z1","ex"]].dropna()
    res={}
    for nm,g in [("up",s[s.z1>0]),("down",s[s.z1<0])]:
        lr=stats.linregress(-g["z1"],g["ex"]); res[nm]=[lr.slope,lr.slope/lr.stderr,len(g)]
    out["fade_slope_up_vs_down"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # weekday
    g = d.groupby("wd")["ex"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["ex_by_weekday_of_signal"]=g.round(5)
    res={}
    for k,g in s.join(d["wd"]).groupby("wd"):
        lr=stats.linregress(-g["z1"],g["ex"]); res[k]=[lr.slope,lr.slope/lr.stderr,len(g)]
    out["fade_slope_by_weekday"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # other predictors, slopes on ex
    res={}
    for col in ["z1","z3","z60","rangez","clv","volz","volratio"]:
        g=d[[col,"ex"]].dropna(); lr=stats.linregress(g[col],g["ex"]); res[col]=[lr.slope,lr.slope/lr.stderr,len(g)]
    out["slopes_next1"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # non-overlapping 3 and 5 day
    for h,col in [(3,"nxt3"),(5,"nxt5")]:
        g = d[(d["pos"]%h==0)].copy()
        g["exh"]=g[col]-d.groupby("w").apply(lambda x: 0).sum()  # placeholder
        m = g[col].mean(); g["exh"]=g[col]-m
        res={}
        for p in ["z1","z3","z60","clv","volz","rangez"]:
            gg=g[[p,"exh"]].dropna(); lr=stats.linregress(gg[p],gg["exh"]); res[p]=[lr.slope,lr.slope/lr.stderr,len(gg)]
        out[f"slopes_next{h}_nonoverlap"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # clv and volume interaction with fade
    out["clv_quint_ex"]=grp("clv",5)
    out["volz_quint_ex"]=grp("volz",5)
    # by year fade slope
    res={}
    for k,g in d[["z1","ex","yr"]].dropna().groupby("yr"):
        lr=stats.linregress(-g["z1"],g["ex"]); res[k]=[lr.slope,lr.slope/lr.stderr,len(g)]
    out["fade_slope_by_year"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # book gains: largest days
    gq = d[["gain","z1","volratio","rangez"]].dropna()
    gq["gq"]=pd.qcut(gq["gain"],[0,0.02,0.1,0.9,0.98,1],labels=False)
    out["book_extremes_context"]=gq.groupby("gq")[["gain","z1","volratio","rangez"]].agg(["mean"]).round(4)
    tr = pd.concat([t for t in data["trades"]["XMRUSD"].values()],ignore_index=True)
    out["trades_by_side"]=tr.groupby("side")["net_profit_loss_percent"].agg(["mean","count","median"])
    return out
