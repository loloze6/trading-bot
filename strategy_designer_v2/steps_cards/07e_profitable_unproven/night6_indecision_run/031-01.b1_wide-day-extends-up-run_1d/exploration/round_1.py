def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # --- book daily returns, decomposition
    rows = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].last()
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"])
            dd = dd.set_index("day")
            dd["alloc_prev"] = alloc.shift(1).reindex(dd.index)
            dd["coin"] = c; dd["window"] = w
            rows.append(dd.reset_index())
    D = pd.concat(rows)
    D["year"] = D["day"].dt.year
    coin_mean = D.groupby("coin")["coin_return"].mean()
    D["mkt_part"] = D["alloc_prev"] * D["coin"].map(coin_mean)
    D["timing_part"] = D["alloc_prev"] * (D["coin_return"] - D["coin"].map(coin_mean))
    book = D.groupby(["window", "day"])[["book_return", "coin_return", "mkt_part", "timing_part"]].mean()
    out["book decomposition (mean daily)"] = pd.Series({
        "book": book["book_return"].mean(), "hold": book["coin_return"].mean(),
        "market rise part": book["mkt_part"].mean(), "timing part": book["timing_part"].mean(),
        "timing t": book["timing_part"].mean() / (book["timing_part"].std() / np.sqrt(book["timing_part"].count())),
        "n days": book["book_return"].count()})
    out["by coin"] = D.groupby("coin")[["book_return", "coin_return", "mkt_part", "timing_part", "alloc_prev"]].mean()
    bk = book.reset_index(); bk["year"] = pd.to_datetime(bk["day"]).dt.year
    out["by year"] = bk.groupby("year")[["book_return", "coin_return", "mkt_part", "timing_part"]].mean()
    out["by window"] = bk.groupby("window")[["book_return", "coin_return", "timing_part"]].sum()
    # --- trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for w, t in data["trades"][c].items()])
    pl = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(pl), "mean net %": pl.mean(), "win share": (pl > 0).mean(),
                               "sum net": pl.sum(), "sum top 10": pl.head(10).sum(), "sum top 5%": pl.head(int(len(pl)*0.05)).sum(),
                               "mean duration days": T["duration_minutes"].mean()/1440})
    # --- conditional forward returns: regime up-run vs not, by horizon, graded by range ratio and close location
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; rng = (b["high"] - b["low"]) / cl
            rr = (b["high"] - b["low"]) / (b["high"] - b["low"]).rolling(20).mean()
            r5 = cl / cl.shift(5) - 1
            loc = ((b["close"] - b["low"]) / (b["high"] - b["low"])).replace([np.inf, -np.inf], np.nan)
            body = (b["close"] - b["open"]).abs() / (b["high"] - b["low"])
            for h in [1, 3, 5, 10]:
                fwd = cl.shift(-h) / cl - 1
                idx = np.arange(0, len(b), h)
                recs.append(pd.DataFrame({"coin": c, "w": w, "h": h, "fwd": fwd.iloc[idx].values,
                    "r5": r5.iloc[idx].values, "rr": rr.iloc[idx].values, "loc": loc.iloc[idx].values,
                    "body": body.iloc[idx].values, "regime": b["regime"].iloc[idx].values}))
    R = pd.concat(recs).dropna(subset=["fwd"])
    R["drift"] = R.groupby(["coin", "h"])["fwd"].transform("mean")
    R["ex"] = R["fwd"] - R["drift"]
    def tm(x): 
        x = x.dropna(); return pd.Series({"mean ex %": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "n": len(x)})
    R["up"] = R["regime"] == "trending"
    out["excess by horizon x up-run"] = R.groupby(["h", "up"])["ex"].apply(tm).unstack()
    R["rrq"] = R.groupby("h")["rr"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["h3 in up-run, by range-ratio quartile"] = R[(R.h == 3) & R.up].groupby("rrq")["ex"].apply(tm).unstack()
    out["h3 not up-run, by range-ratio quartile"] = R[(R.h == 3) & ~R.up].groupby("rrq")["ex"].apply(tm).unstack()
    R["r5q"] = R.groupby("h")["r5"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["h3 by 5d-return quintile"] = R[R.h == 3].groupby("r5q")["ex"].apply(tm).unstack()
    out["h10 by 5d-return quintile"] = R[R.h == 10].groupby("r5q")["ex"].apply(tm).unstack()
    R["locq"] = pd.cut(R["loc"], [-0.01, 0.33, 0.67, 1.01], labels=["low", "mid", "high"])
    out["h3 up-run by close location"] = R[(R.h == 3) & R.up].groupby("locq")["ex"].apply(tm).unstack()
    return out
