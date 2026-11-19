def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # coin mean daily return over all windows
    drows = []
    for c in days:
        cm = pd.concat([days[c][w]["coin_return"] for w in days[c]]).mean()
        for w in days[c]:
            d = days[c][w].copy(); d["coin"] = c; d["w"] = w; d["cm"] = cm
            drows.append(d)
    D = pd.concat(drows)
    # position at day level: last allocation of each day
    pos = []
    fees = []
    gains = []
    grid = []
    for c in bars:
        allr = []
        for w in bars[c]:
            b = bars[c][w].copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            allr.append(b["close"].iloc[::72].pct_change().shift(-1).dropna())
        cm72 = pd.concat(allr).mean() if allr else 0
        for w in bars[c]:
            b = bars[c][w].copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"]
            b["g"] = a * b["ret1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["past72"] = b["close"] / b["close"].shift(72) - 1
            v = b["volume"]
            b["conc"] = np.log(v.rolling(72).mean() / v.rolling(72).median())
            b["fwd72"] = b["close"].shift(-72) / b["close"] - 1
            b["coin"] = c; b["w"] = w; b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            gains.append(b[["g", "fee", "past72", "conc", "regime", "coin", "year", "postRebalance_current_allocation", "ret1"]])
            gg = b.iloc[::72].copy(); gg["exc"] = gg["fwd72"] - cm72
            grid.append(gg[["past72", "conc", "fwd72", "exc", "regime", "coin", "year"]])
    G = pd.concat(gains)
    R = pd.concat(grid).dropna(subset=["exc", "past72", "conc"])
    # book summary
    out["book daily mean"] = D["book_return"].mean()
    out["coin daily mean"] = D["coin_return"].mean()
    out["mean alloc"] = G["postRebalance_current_allocation"].mean()
    out["mean abs alloc"] = G["postRebalance_current_allocation"].abs().mean()
    out["hourly gain sum per bar mean (pre-fee)"] = G["g"].mean()
    out["fee per bar mean"] = G["fee"].mean()
    # drift part of book: allocation x coin mean hourly return
    chm = G.groupby("coin")["ret1"].mean()
    G["drift"] = G["postRebalance_current_allocation"] * G["coin"].map(chm)
    out["drift part per bar"] = G["drift"].mean()
    out["timing part per bar"] = G["g"].mean() - G["drift"].mean()
    # by year
    out["by year"] = G.groupby("year").agg(gain=("g", "mean"), fee=("fee", "mean"), alloc=("postRebalance_current_allocation", "mean"))
    out["by coin"] = G.groupby("coin").agg(gain=("g", "mean"), fee=("fee", "mean"), alloc=("postRebalance_current_allocation", "mean"))
    # grid in fallen state
    F = R[R["past72"] < 0].copy()
    F["concq"] = pd.qcut(F["conc"], 5, labels=False)
    F["fallq"] = pd.qcut(F["past72"], 5, labels=False)
    def summ(x):
        return pd.Series({"n": len(x), "exc": x["exc"].mean(), "t": x["exc"].mean() / (x["exc"].std() / np.sqrt(len(x)))})
    out["fallen grid by conc quintile (0=even)"] = F.groupby("concq").apply(summ)
    out["fallen grid by fall quintile (0=deepest)"] = F.groupby("fallq").apply(summ)
    out["fallen all"] = summ(F)
    U = R[R["past72"] >= 0]
    out["rising all"] = summ(U)
    out["fallen by year"] = F.groupby("year").apply(summ)
    # fall x conc
    F["fall2"] = (F["fallq"] <= 1).map({True: "deep", False: "shallow"})
    F["conc2"] = (F["concq"] <= 1).map({True: "even", False: "bursty"})
    out["fall x conc"] = F.groupby(["fall2", "conc2"]).apply(summ)
    return out
