def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    wins = list(data["days"][coins[0]].keys())
    R = []
    for c in coins:
        for w in wins:
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["ma50d"] = b["close"]/b["close"].rolling(50, min_periods=30).mean()-1
            b["ma20d"] = b["close"]/b["close"].rolling(20).mean()-1
            b["dd20"] = b["close"]/b["close"].rolling(20).max()-1
            b["r20"] = b["close"]/b["close"].shift(20)-1
            b["slope50"] = b["close"].rolling(50, min_periods=30).mean().pct_change(10)
            b["held"] = (b["postRebalance_current_allocation"].astype(float).abs()>0).astype(int)
            b["fwd1"] = b["close"].shift(-1)/b["close"]-1
            b["fwd10"] = b["close"].shift(-10)/b["close"]-1
            b["coin"] = c; b["win"] = w; b["i"] = np.arange(len(b))
            d = data["days"][c][w].copy()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            if d["day"].dt.tz is None and b["day"].dt.tz is not None:
                b["day"] = b["day"].dt.tz_localize(None)
            d = d[["day","book_return"]]
            d["book_next"] = d["book_return"].shift(-1)
            m = b.merge(d, on="day", how="left")
            R.append(m)
    R = pd.concat(R, ignore_index=True)
    out["held_share"] = float(R["held"].mean())
    # coin mean 10-bar return over all windows (non-overlapping)
    nov = R[R["i"] % 10 == 0].dropna(subset=["fwd10"])
    cm = nov.groupby("coin")["fwd10"].mean()
    nov = nov.assign(ex=nov["fwd10"]-nov["coin"].map(cm))
    H = R[R["held"]==1].dropna(subset=["book_next"])
    for col in ["ma50d","dd20","slope50","ma20d"]:
        q = pd.qcut(H[col], 5, duplicates="drop")
        g = H.groupby(q, observed=True)["book_next"]
        out["held_nextday_book_by_"+col] = pd.DataFrame({"n":g.count(),"mean":g.mean(),"t":g.mean()/g.std()*np.sqrt(g.count()),"sum":g.sum()}).round(4)
    hn = nov[nov["held"]==1]
    for col in ["ma50d","slope50","dd20"]:
        q = pd.qcut(hn[col],4,duplicates="drop")
        g = hn.groupby(q, observed=True)["ex"]
        out["held_ex10_nonov_by_"+col] = pd.DataFrame({"n":g.count(),"mean":g.mean(),"t":g.mean()/g.std()*np.sqrt(g.count())}).round(4)
    # book daily return (mean over coins) split by share of held coins below ma50 / slope<0
    H2 = R.dropna(subset=["book_next"]).copy()
    H2["bad"] = ((H2["held"]==1)&(H2["slope50"]<0)).astype(int)
    H2["good"] = ((H2["held"]==1)&(H2["slope50"]>=0)).astype(int)
    out["book_contrib_slope"] = pd.Series({
        "sum_held_slope_neg": H2.loc[H2.bad==1,"book_next"].sum()/6,
        "sum_held_slope_pos": H2.loc[H2.good==1,"book_next"].sum()/6,
        "n_neg": H2.bad.sum(), "n_pos": H2.good.sum(),
        "mean_neg": H2.loc[H2.bad==1,"book_next"].mean(),
        "mean_pos": H2.loc[H2.good==1,"book_next"].mean()}).round(4)
    # book drawdown per window and held share / slope in worst windows
    bw = R.groupby("win", sort=False).apply(lambda g: pd.Series({"held":g.held.mean(),"held_slope_neg":((g.held==1)&(g.slope50<0)).mean(),"coin_mean_r":g.fwd1.mean()})).round(3)
    out["window_state"] = bw
    return out
