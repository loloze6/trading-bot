def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allf = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            vol = b["sizing_realised_vol"].values if "sizing_realised_vol" in b else np.full(n, np.nan)
            r60 = pd.Series(c).pct_change(60).values
            r5 = pd.Series(c).pct_change(5).values
            for i in range(0, n - 10, 10):
                f = c[i+10]/c[i]-1
                allf.append(f)
                rows.append(dict(coin=coin, w=w, i=i, fwd=f, reg=b["regime"].iloc[i],
                                 fc=b["forecast"].iloc[i],
                                 r30=b.get("debug_info.components.month_fall.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                                 vol=vol[i], r60=r60[i], r5=r5[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
        drift[coin] = np.mean(allf) if allf else np.nan
    df = pd.DataFrame(rows)
    df["drift"] = df["coin"].map(drift)
    df["unus"] = df["fwd"] - df["drift"]
    df["volrel"] = df["vol"] / df.groupby("coin")["vol"].transform("median")
    ch = df[df["reg"] == "unknown"].copy()
    def summ(g):
        return pd.Series(dict(n=len(g), fwd=g["fwd"].mean(), unus=g["unus"].mean(),
                              t_unus=g["unus"].mean()/(g["unus"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out["drift_by_coin"] = pd.Series(drift)
    ch["r30b"] = pd.cut(ch["r30"], [-100,-20,-10,-5,0,5,10,20,1000])
    out["choppy_by_r30"] = ch.groupby("r30b").apply(summ)
    sh = ch[ch["fc"] < 0].copy()
    sh["volb"] = pd.qcut(sh["volrel"], 3, labels=["lowvol","mid","highvol"])
    out["short_by_vol"] = sh.groupby("volb").apply(summ)
    sh["r5b"] = pd.cut(sh["r5"], [-10,-0.05,0,0.05,10])
    out["short_by_r5"] = sh.groupby("r5b").apply(summ)
    sh["r60b"] = pd.cut(sh["r60"], [-1,-0.05,0,0.05,1])
    out["short_by_r60"] = sh.groupby("r60b").apply(summ)
    out["short_by_window"] = sh.groupby("w").apply(summ)
    out["short_by_coin"] = sh.groupby("coin").apply(summ)
    # book by window
    bw = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bw.append(dict(w=w, coin=coin, book=d["book_return"].sum(), hold=d["coin_return"].sum()))
    bw = pd.DataFrame(bw)
    out["book_by_window"] = bw.groupby("w")[["book","hold"]].mean()
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["w"]=w; tr.append(tt)
    tr = pd.concat(tr)
    tr["days"] = tr["duration_minutes"]/1440
    tr["db"] = pd.cut(tr["days"], [0,3,10,20,40,1000])
    out["trades_by_duration"] = tr.groupby("db")[["profit_loss_percent","net_profit_loss_percent"]].agg(["count","mean"])
    out["trades_by_side"] = tr.groupby("side")[["profit_loss_percent","net_profit_loss_percent"]].agg(["count","mean"])
    return out
