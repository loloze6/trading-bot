def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    res = {}
    # Book daily returns: mean over coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index().sort_values(["wn","day"])
    B = B.dropna()
    v = (1+B["book"]).cumprod(); peak = v.cummax(); dd = v/peak-1
    B["dd"] = dd.values
    res["max_dd"] = float(dd.min())
    # per window stats
    g = B.groupby("wn")
    res["per_window"] = pd.DataFrame({"book_mean": g["book"].mean(), "hold_mean": g["hold"].mean(),
        "book_sd": g["book"].std(), "book_min_day": g["book"].min(), "book_total": g["book"].apply(lambda x: (1+x).prod()-1),
        "hold_total": g["hold"].apply(lambda x: (1+x).prod()-1), "n": g.size()})
    # worst drawdown episode: window spans
    i_trough = int(np.argmin(dd.values)); i_peak = int(np.argmax(v.values[:i_trough+1]))
    ep = B.iloc[i_peak:i_trough+1]
    res["worst_dd_episode"] = pd.Series({"days": len(ep), "windows": str(sorted(ep.wn.unique())),
        "book_sum": ep.book.sum(), "hold_sum": ep.hold.sum(), "corr_book_hold": ep.book.corr(ep.hold)})
    # worst 20 book days: what hold did
    w20 = B.nsmallest(30, "book")
    res["worst30_days"] = pd.Series({"book_mean": w20.book.mean(), "hold_mean": w20.hold.mean(), "share_hold_neg": (w20.hold<0).mean()})
    # Bar-level analysis on down days
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            rng = ((b["high"]-b["low"])/cl).rolling(30).mean()
            sc = r1/rng
            fwd = cl.shift(-1)/cl-1
            fwd3 = cl.shift(-3)/cl-1
            r20 = cl/cl.shift(20)-1
            r60 = cl/cl.shift(60)-1
            r5 = cl/cl.shift(5)-1
            vol10 = r1.rolling(10).std(); vol60 = r1.rolling(60).std()
            dfb = pd.DataFrame({"coin":c,"w":w,"r1":r1,"sc":sc,"fwd":fwd,"fwd3":fwd3,"r20":r20,"r60":r60,"r5":r5,
                "volratio":vol10/vol60,"fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                "pos":np.arange(len(b))})
            recs.append(dfb)
    X = pd.concat(recs, ignore_index=True)
    mu = X.groupby("coin")["fwd"].mean()
    X["ex"] = X["fwd"] - X["coin"].map(mu)
    X["gain"] = X["alloc"]*X["fwd"]
    dn = X[(X.r1<0)].dropna(subset=["fwd","sc"])
    dn = dn.assign(q=pd.qcut(-dn.sc, 5, labels=False))
    res["by_scaled_fall_quintile"] = dn.groupby("q").agg(n=("ex","size"), ex=("ex","mean"), fwd=("fwd","mean"),
        sd=("fwd","std"), alloc=("alloc","mean"), gain=("gain","mean"), gain_sd=("gain","std"))
    def tab(df, col, bins, name):
        df = df.dropna(subset=[col])
        df = df.assign(b=pd.cut(df[col], bins))
        res[name] = df.groupby("b", observed=True).agg(n=("ex","size"), ex=("ex","mean"), t=("ex", lambda x: x.mean()/x.std()*np.sqrt(len(x))),
            gain=("gain","mean"), gain_sd=("gain","std"))
    allb = X.dropna(subset=["fwd"])
    for nm, df in [("down", dn), ("notdown", allb[allb.r1>=0])]:
        tab(df, "r20", [-9,-0.2,-0.1,0,0.1,0.2,9], f"{nm}_by_r20")
        tab(df, "volratio", [0,0.7,1,1.3,9], f"{nm}_by_volratio")
        tab(df, "r5", [-9,-0.15,-0.05,0,0.05,9], f"{nm}_by_r5")
    # top quintile falls within falling vs not
    top = dn[dn.q>=3]
    tab(top, "r20", [-9,-0.1,0,0.1,9], "topfalls_by_r20")
    # gain on position days by quintile of allocation
    res["gain_share_by_q"] = dn.groupby("q")["gain"].sum()/dn["gain"].sum()
    return res
