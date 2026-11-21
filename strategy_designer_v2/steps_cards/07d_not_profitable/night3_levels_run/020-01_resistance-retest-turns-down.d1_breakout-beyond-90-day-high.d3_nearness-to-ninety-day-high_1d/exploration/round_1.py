def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    # book daily, mean across coins, per window
    rows = []
    for c in coins:
        for w, d in data["days"][c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["window", "day"])[["book_return", "coin_return"]].mean().reset_index()
    wo = sorted(B["window"].unique(), key=lambda s: int(s[1:]))
    B["wn"] = B["window"].map({w: i for i, w in enumerate(wo)})
    B = B.sort_values(["wn", "day"])
    br = B["book_return"].fillna(0).values
    eq = np.cumprod(1 + br)
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1
    out["book mean, coin mean, maxDD"] = pd.Series({"book_mean": np.nanmean(B.book_return), "hold_mean": np.nanmean(B.coin_return), "maxDD": dd.min()})
    B["dd"] = dd
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["per window"] = B.groupby("window").agg(book=("book_return", "mean"), hold=("coin_return", "mean"), mindd=("dd", "min"), n=("book_return", "size")).reindex(wo)
    out["per year"] = B.groupby("year").agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("book_return", "size"))
    # bar-level: position, gain, by side and forecast bucket
    rb = []
    for c in coins:
        for w, b in data["bars"][c].items():
            x = b[["close", "forecast", "postRebalance_current_allocation"]].copy()
            x["ret1"] = x["close"].shift(-1) / x["close"] - 1
            x["gain"] = x["postRebalance_current_allocation"] * x["ret1"]
            x["ret20"] = x["close"].shift(-20) / x["close"] - 1
            x["mom20"] = x["close"] / x["close"].shift(20) - 1
            x["mom90"] = x["close"] / x["close"].shift(90) - 1
            x["vol20"] = x["ret1"].shift(1).rolling(20).std()
            x["coin"] = c; x["window"] = w
            rb.append(x)
    X = pd.concat(rb)
    cm = X.groupby("coin")["ret1"].mean()
    X["mkt"] = X["postRebalance_current_allocation"] * X["coin"].map(cm)
    X["side"] = np.sign(X["postRebalance_current_allocation"]).map({1: "long", -1: "short", 0: "flat"})
    out["by side"] = X.groupby("side").agg(n=("gain", "size"), gain_mean=("gain", "mean"), gain_sum=("gain", "sum"), mkt_sum=("mkt", "sum"), alloc=("postRebalance_current_allocation", "mean"))
    X["fq"] = pd.qcut(X["forecast"], 5, labels=False, duplicates="drop")
    out["by forecast quintile"] = X.groupby("fq").agg(f=("forecast", "mean"), alloc=("postRebalance_current_allocation", "mean"), gain_mean=("gain", "mean"), ret1=("ret1", "mean"), n=("gain", "size"))
    out["by coin"] = X.groupby("coin").agg(gain_mean=("gain", "mean"), ret1=("ret1", "mean"), alloc=("postRebalance_current_allocation", "mean"))
    # trades
    T = pd.concat([t.assign(coin=c) for c in coins for t in data["trades"][c].values()])
    out["trades by side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), mean=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()), dur_days=("duration_minutes", lambda s: s.mean() / 1440))
    # conditions of short-side gains: mom90 regime
    S = X[X.side == "short"].copy()
    S["m90q"] = pd.qcut(S["mom90"], 4, labels=False, duplicates="drop")
    out["short gain by mom90 quartile"] = S.groupby("m90q").agg(m90=("mom90", "mean"), gain=("gain", "mean"), n=("gain", "size"))
    L = X[X.side == "long"].copy()
    L["vq"] = pd.qcut(L["vol20"], 4, labels=False, duplicates="drop")
    out["long gain by vol quartile"] = L.groupby("vq").agg(vol=("vol20", "mean"), gain=("gain", "mean"), alloc=("postRebalance_current_allocation", "mean"), n=("gain", "size"))
    # deepest falls: book side held during worst 30 book days
    B2 = B.copy()
    worst = B2.nsmallest(30, "book_return")
    out["worst 30 days"] = pd.Series({"book_mean": worst.book_return.mean(), "coin_mean": worst.coin_return.mean(), "share_coin_down": (worst.coin_return < 0).mean()})
    return out
