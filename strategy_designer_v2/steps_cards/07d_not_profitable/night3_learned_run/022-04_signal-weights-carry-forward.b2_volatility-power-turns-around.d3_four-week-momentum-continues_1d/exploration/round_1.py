def explore(data):
    import pandas as pd, numpy as np
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    # book daily returns: mean across coins per (window, day)
    rows = []
    for c in coins:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["g"] = b["pos"]*b["ret1"]
            b["r28"] = b["close"]/b["close"].shift(28)-1
            b["vol20"] = b["close"].pct_change().rolling(20).std()
            b["vol60"] = b["close"].pct_change().rolling(60).std()
            b["r5"] = b["close"]/b["close"].shift(5)-1
            b["coin"] = c; b["w"] = w
            rows.append(b[["day","coin","w","pos","g","ret1","r28","vol20","vol60","r5","forecast"]])
    B = pd.concat(rows)
    B["wn"] = B["w"].str[1:].astype(int)
    D = []
    for c in coins:
        for w, d in days[c].items():
            x = d[["day","book_return"]].copy(); x["coin"]=c; x["w"]=w; D.append(x)
    D = pd.concat(D); D["wn"]=D["w"].str[1:].astype(int)
    bk = D.groupby(["wn","day"])["book_return"].mean().reset_index().sort_values(["wn","day"])
    bk["eq"] = (1+bk["book_return"].fillna(0)).cumprod()
    bk["peak"] = bk["eq"].cummax(); bk["dd"] = bk["eq"]/bk["peak"]-1
    # per-window stats
    pw = bk.groupby("wn").agg(n=("book_return","size"), mean=("book_return","mean"),
        sum=("book_return","sum"), mindd=("dd","min"))
    # in-window max drawdown
    def wdd(s):
        e=(1+s.fillna(0)).cumprod(); return (e/e.cummax()-1).min()
    pw["own_dd"] = bk.groupby("wn")["book_return"].apply(wdd)
    # deepest fall episode
    trough = bk["dd"].idxmin(); tr = bk.loc[trough]
    pk_i = bk.loc[:trough][bk.loc[:trough,"eq"]==bk.loc[trough,"peak"]].index[-1]
    ep = bk.loc[pk_i:trough]
    info = pd.Series({"maxdd":tr["dd"],"days_in_fall":len(ep),"windows_spanned":ep["wn"].nunique(),
                      "first_w":ep["wn"].min(),"last_w":ep["wn"].max()})
    # classify bar-level gain by situation
    B = B.dropna(subset=["g"])
    B["side"] = np.sign(B["pos"])
    B["volq"] = B.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    B["volratio"] = B["vol20"]/B["vol60"]
    B["vrq"] = B.groupby("coin")["volratio"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    B["agree5"] = np.sign(B["r5"])==np.sign(B["r28"])
    B["absfq"] = pd.qcut(B["forecast"].abs(),4,labels=False,duplicates="drop")
    def agg(k):
        g = B.groupby(k)["g"]
        return pd.DataFrame({"n":g.size(),"mean_bps":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.size())),
                             "p1pct":g.quantile(0.01)*1e4})
    # in fall episode: side
    epk = set(zip(ep["wn"],ep["day"]))
    B["infall"] = [ (a,b) in epk for a,b in zip(B["wn"],B["day"])]
    fall = B[B["infall"]].groupby(["coin","side"])["g"].agg(["size","sum"])
    return {"fall_info":info, "per_window":pw.round(4), "by_side":agg("side"),
            "by_vol":agg(["volq","side"]), "by_volratio":agg(["vrq","side"]),
            "by_agree5":agg(["agree5","side"]), "by_absf":agg("absfq"),
            "fall_by_coin_side":fall.round(4)}
