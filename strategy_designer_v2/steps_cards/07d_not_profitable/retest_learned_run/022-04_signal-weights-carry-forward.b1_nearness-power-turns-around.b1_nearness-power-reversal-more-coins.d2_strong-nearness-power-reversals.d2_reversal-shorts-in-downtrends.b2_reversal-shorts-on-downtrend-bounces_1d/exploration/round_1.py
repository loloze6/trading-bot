def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    trs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["fwd1"] = c.shift(-1)/c - 1
            b["fwd5"] = c.shift(-5)/c - 1
            b["r20"] = c/c.shift(20) - 1
            b["r5"] = c/c.shift(5) - 1
            b["r60"] = c/c.shift(60) - 1
            b["vol20"] = c.pct_change().rolling(20).std()
            b["pos"] = b["postRebalance_current_allocation"].fillna(0)
            b["gain"] = b["pos"]*b["fwd1"]
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["grid"] = (np.arange(len(b)) % 5 == 0)
            rows.append(b)
        for w, t in data["trades"].get(coin, {}).items():
            if t is not None and len(t):
                t = t.copy(); t["coin"] = coin; t["win"] = w
                trs.append(t)
    B = pd.concat(rows, ignore_index=True)
    T = pd.concat(trs, ignore_index=True)
    held = B[B["pos"] != 0]
    out["held summary"] = pd.Series({
        "share bars held": (B["pos"] != 0).mean(),
        "mean abs pos when held": held["pos"].abs().mean(),
        "median abs pos": held["pos"].abs().median(),
        "mean gain per held bar": held["gain"].mean(),
        "mean fwd1 held (short sign)": -held["fwd1"].mean(),
        "share pos short": (held["pos"] < 0).mean(),
    })
    out["trades"] = pd.Series({
        "n": len(T),
        "mean pl %": T["profit_loss_percent"].mean(),
        "mean net %": T["net_profit_loss_percent"].mean(),
        "median net": T["net_profit_loss_percent"].median(),
        "win rate": (T["net_profit_loss_percent"] > 0).mean(),
        "mean dur days": T["duration_minutes"].mean()/1440,
        "t net": stats.ttest_1samp(T["net_profit_loss_percent"].dropna(), 0).statistic,
    })
    # grid cases with forecast<0
    g = B[B["grid"] & (B["forecast"] < 0) & B["fwd5"].notna()].copy()
    drift = B[B["grid"] & B["fwd5"].notna()].groupby("coin")["fwd5"].mean()
    g["short5"] = -g["fwd5"]
    g["unusual"] = -(g["fwd5"] - g["coin"].map(drift))
    g["fq"] = pd.qcut(g["forecast"].abs().rank(method="first"), 4, labels=["q1 weak","q2","q3","q4 strong"])
    out["by forecast strength"] = g.groupby("fq").agg(n=("short5","size"), short5=("short5","mean"),
        unusual=("unusual","mean"), absfc=("forecast", lambda x: x.abs().mean()), abspos=("pos", lambda x: x.abs().mean()))
    g["r20q"] = pd.qcut(g["r20"], 3, labels=["deep fall","mid","shallow"])
    out["by r20 depth"] = g.groupby("r20q").agg(n=("short5","size"), r20=("r20","mean"), short5=("short5","mean"), unusual=("unusual","mean"))
    g["r5q"] = pd.qcut(g["r5"], 3, labels=["small bounce","mid","big bounce"])
    out["by r5 bounce"] = g.groupby("r5q").agg(n=("short5","size"), r5=("r5","mean"), short5=("short5","mean"), unusual=("unusual","mean"))
    g["r60q"] = pd.qcut(g["r60"], 3, labels=["r60 low","mid","r60 high"])
    out["by r60"] = g.groupby("r60q").agg(n=("short5","size"), r60=("r60","mean"), short5=("short5","mean"))
    out["by year"] = g.groupby("year").agg(n=("short5","size"), short5=("short5","mean"), unusual=("unusual","mean"))
    # condition alone: gate bars with no signal (forecast==0) vs signal
    G = B[B["grid"] & B["fwd5"].notna()].copy()
    G["gate"] = (G["r20"] < 0) & (G["r5"] > 0)
    G["sig"] = G["forecast"] < 0
    out["gate vs signal short5"] = G.groupby(["gate","sig"]).agg(n=("fwd5","size"), short5=("fwd5", lambda x: -x.mean()))
    # book daily, drawdown
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dl.append(d)
    D = pd.concat(dl)
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["wn"] = bk["win"].str[1:].astype(int)
    bk = bk.sort_values(["wn","day"])
    v = (1+bk["book_return"].fillna(0)).cumprod()
    dd = v/v.cummax()-1
    out["max dd"] = dd.min()
    bk["dd"] = dd.values
    out["book by window"] = bk.groupby("wn").agg(book=("book_return", lambda x: (1+x.fillna(0)).prod()-1),
        coin=("coin_return", lambda x: (1+x.fillna(0)).prod()-1), mindd=("dd","min"))
    T["absfc"] = T["entry_forecast"].abs()
    T["fq"] = pd.qcut(T["absfc"].rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["trades by entry forecast"] = T.groupby("fq").agg(n=("net_profit_loss_percent","size"),
        net=("net_profit_loss_percent","mean"), pl=("profit_loss_percent","mean"))
    return out
