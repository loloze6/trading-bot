def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins = list(data["bars"].keys())
    rows = []; rb = []
    for c in coins:
        for w, b in data["bars"][c].items():
            x = b[["close", "forecast", "postRebalance_current_allocation"]].copy().reset_index(drop=True)
            x["ret1"] = x["close"].shift(-1) / x["close"] - 1
            x["gain"] = x["postRebalance_current_allocation"] * x["ret1"]
            x["ret20"] = x["close"].shift(-20) / x["close"] - 1
            x["mom90"] = x["close"] / x["close"].shift(90) - 1
            x["mom20"] = x["close"] / x["close"].shift(20) - 1
            x["ma50"] = x["close"] / x["close"].rolling(50).mean() - 1
            x["coin"] = c; x["window"] = w
            rb.append(x)
            g = x.iloc[::20].copy()
            rows.append(g)
    X = pd.concat(rb); G = pd.concat(rows).dropna(subset=["ret20", "forecast"])
    m20 = G.groupby("coin")["ret20"].mean()
    G["ex"] = G["ret20"] - G["coin"].map(m20)
    G["fside"] = np.where(G["forecast"] > 0, "fpos", np.where(G["forecast"] < 0, "fneg", "f0"))
    out["grid ret20 by forecast side"] = G.groupby("fside").agg(n=("ret20", "size"), ret20=("ret20", "mean"), ex=("ex", "mean"), t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    G["mtrend"] = np.where(G["mom90"] > 0, "up90", np.where(G["mom90"] <= 0, "down90", "na"))
    def fit(s):
        if len(s) < 30: return pd.Series({"n": len(s)})
        r = stats.linregress(s["forecast"], s["ex"])
        return pd.Series({"n": len(s), "slope": r.slope, "t": r.slope / r.stderr, "ret20": s["ret20"].mean()})
    out["grid slope by 90d trend"] = G.groupby("mtrend").apply(fit)
    out["grid by trend x side"] = G.groupby(["mtrend", "fside"]).agg(n=("ret20", "size"), ret20=("ret20", "mean"), ex=("ex", "mean"))
    G["m20q"] = pd.qcut(G["mom20"], 4, labels=False, duplicates="drop")
    out["grid by mom20 quartile x side"] = G.groupby(["m20q", "fside"]).agg(m20=("mom20", "mean"), n=("ret20", "size"), ret20=("ret20", "mean"))
    X["side"] = np.sign(X["postRebalance_current_allocation"])
    X["trend"] = np.where(X["ma50"] > 0, "above50", np.where(X["ma50"] <= 0, "below50", "na"))
    out["bar gain by trend x side"] = X.groupby(["trend", "side"]).agg(n=("gain", "size"), gain=("gain", "mean"), ret1=("ret1", "mean"), alloc=("postRebalance_current_allocation", "mean"))
    # exposure
    out["exposure"] = pd.Series({"mean_abs_alloc": X["postRebalance_current_allocation"].abs().mean(), "mean_alloc": X["postRebalance_current_allocation"].mean(), "share_short": (X.side < 0).mean()})
    return out
