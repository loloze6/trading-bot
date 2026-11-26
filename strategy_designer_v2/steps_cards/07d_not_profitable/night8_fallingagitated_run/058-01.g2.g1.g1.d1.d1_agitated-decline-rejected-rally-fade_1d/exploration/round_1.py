def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    daybook = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r = c.pct_change()
            nxt = c.shift(-1)/c - 1
            s30 = r.rolling(30).std()
            up = r > 0
            first_up = up & (r.shift(1) <= 0)
            alloc = b["postRebalance_current_allocation"].fillna(0)
            ret3 = c/c.shift(3) - 1
            ret60 = c/c.shift(60) - 1 if len(c) > 60 else pd.Series(np.nan, index=c.index)
            dist = (c - h)/c/s30
            uprng = r/s30
            lowpos = (c - l)/(h - l).replace(0, np.nan)
            prevr = r.shift(1)/s30
            for i in range(len(b)-1):
                rows.append(dict(coin=coin, w=w, i=i, ts=b["timestamp"].iloc[i], alloc=alloc.iloc[i],
                                 nxt=nxt.iloc[i], r=r.iloc[i], fu=bool(first_up.iloc[i]),
                                 regime=b["regime"].iloc[i], dist=dist.iloc[i], upz=uprng.iloc[i],
                                 prevz=prevr.iloc[i], ret3=ret3.iloc[i], ret60=ret60.iloc[i],
                                 lowpos=lowpos.iloc[i], fc=b["forecast"].iloc[i]))
    df = pd.DataFrame(rows)
    df["pnl"] = df["alloc"]*df["nxt"]
    drift = df.groupby("coin")["nxt"].mean()
    df["short_ex"] = -(df["nxt"] - df["coin"].map(drift))
    case = df[(df["alloc"] < 0)].copy()
    out["n_case_bars"] = len(case)
    out["case_pnl_desc"] = case["pnl"].describe()
    # worst trades
    case["year"] = pd.to_datetime(case["ts"]).dt.year
    out["by_year"] = case.groupby("year").agg(n=("pnl","size"), pnl_sum=("pnl","sum"), sx=("short_ex","mean"))
    out["by_window"] = case.groupby("w").agg(n=("pnl","size"), pnl_sum=("pnl","sum"), sx=("short_ex","mean"))
    out["by_coin"] = case.groupby("coin").agg(n=("pnl","size"), pnl_sum=("pnl","sum"), sx=("short_ex","mean"), alloc=("alloc","mean"))
    # quantile groupings of features
    for f in ["dist","upz","prevz","ret3","ret60","lowpos"]:
        q = pd.qcut(case[f], 4, duplicates="drop")
        g = case.groupby(q, observed=True).agg(n=("pnl","size"), sx=("short_ex","mean"),
                                               pnl=("pnl","mean"), worst=("pnl","min"))
        g.index = g.index.astype(str)
        out["q_"+f] = g
    # worst 15 trades' features (no dates)
    worst = case.nsmallest(15, "pnl")[["coin","w","alloc","nxt","upz","dist","prevz","ret3","ret60","lowpos"]]
    out["worst15"] = worst.reset_index(drop=True)
    # book drawdown: daily book returns averaged over coins
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["day","book_return"]].copy(); x["w"] = w; x["coin"] = coin; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["w","day"])["book_return"].mean().reset_index()
    bk["wn"] = bk["w"].str[1:].astype(int)
    bk = bk.sort_values(["wn","day"])
    v = (1+bk["book_return"].fillna(0)).cumprod()
    draw = v/v.cummax()-1
    out["max_dd"] = float(draw.min())
    bk["draw"] = draw.values
    out["dd_by_window"] = bk.groupby("w")["draw"].min()
    out["book_by_window_sum"] = bk.groupby("w")["book_return"].sum()
    return out
