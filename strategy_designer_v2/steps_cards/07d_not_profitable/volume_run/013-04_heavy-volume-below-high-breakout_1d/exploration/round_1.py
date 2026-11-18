def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    daysrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["alloc"] = b["postRebalance_current_allocation"].fillna(0)
            b["fwd1"] = b["close"].shift(-1) / b["close"] - 1
            b["gain"] = b["alloc"] * b["fwd1"]
            b["in"] = b["alloc"].abs() > 1e-9
            # 30-bar forward return
            b["fwd30"] = b["close"].shift(-30) / b["close"] - 1
            b["exit"] = (b["in"].shift(1, fill_value=False)) & (~b["in"])
            b["entry"] = (~b["in"].shift(1, fill_value=False)) & (b["in"])
            b["trend"] = b["regime"] == "trending"
            b["coin"] = coin; b["w"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","w","year","alloc","fwd1","gain","in","fwd30","exit","entry","trend","forecast"]])
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            daysrows.append(d)
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(daysrows, ignore_index=True)
    out["exposure"] = pd.Series({
        "share bars in": B["in"].mean(),
        "share bars trending": B["trend"].mean(),
        "mean alloc when in": B.loc[B["in"], "alloc"].mean(),
        "mean fwd1 when in": B.loc[B["in"], "fwd1"].mean(),
        "mean fwd1 all": B["fwd1"].mean(),
        "mean fwd1 out": B.loc[~B["in"], "fwd1"].mean(),
        "n entries": int(B["entry"].sum()),
    })
    # spell length
    sp = []
    for (c, w), g in B.groupby(["coin","w"]):
        run = 0
        for v in g["in"].values:
            if v: run += 1
            elif run: sp.append(run); run = 0
        if run: sp.append(run)
    sp = pd.Series(sp)
    out["spell lengths"] = sp.describe()
    # after exit: forward 30 return vs coin mean
    cm = B.groupby("coin")["fwd30"].mean()
    B["ex30"] = B["fwd30"] - B["coin"].map(cm)
    ex = B[B["exit"]].dropna(subset=["ex30"])
    en = B[B["entry"]].dropna(subset=["ex30"])
    out["after exit / entry 30d excess"] = pd.DataFrame({
        "n": [len(ex), len(en)],
        "mean ex30": [ex["ex30"].mean(), en["ex30"].mean()],
        "t": [stats.ttest_1samp(ex["ex30"], 0).statistic, stats.ttest_1samp(en["ex30"], 0).statistic],
    }, index=["exit", "entry"])
    # post-exit 30-day window: share of time back in
    # book daily
    D["year"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["w","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).dropna()
    wk = bk.groupby(level=0).agg(br=("br","sum"), cr=("cr","sum"), n=("br","size"))
    out["window sums"] = wk
    # by year book vs coin
    D2 = D.dropna(subset=["book_return"])
    out["by year"] = D2.groupby("year").agg(book=("book_return","mean"), coin=("coin_return","mean"), n=("book_return","size"))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades"] = pd.Series({
        "n": len(T),
        "mean net pnl%": T["net_profit_loss_percent"].mean(),
        "median net": T["net_profit_loss_percent"].median(),
        "win share": (T["net_profit_loss_percent"] > 0).mean(),
        "mean dur days": T["duration_minutes"].mean() / 1440,
        "mean commission": T["total_commission"].mean(),
    })
    # forward 30 excess at bars in trend vs not
    g = B.dropna(subset=["ex30"])
    out["trend bars ex30 (overlap)"] = g.groupby("trend")["ex30"].agg(["mean","count"])
    return out
