def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["wn"] = int(w[1:])
            rows.append(dd)
    D = pd.concat(rows)
    P = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"]).dropna()
    eq = (1 + P["book_return"]).cumprod()
    P["dd"] = (eq / eq.cummax() - 1).values
    out["by_window"] = P.groupby("wn").agg(book_bps=("book_return", lambda s: s.mean() * 1e4),
                                           hold_bps=("coin_return", lambda s: s.mean() * 1e4),
                                           min_dd=("dd", "min"), n=("book_return", "size"))
    B = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b[["close", "high", "forecast", "postRebalance_current_allocation"]].copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["past26"] = b["close"] / b["close"].shift(26) - 1
            b["ext26"] = b["close"] / b["close"].rolling(26).mean() - 1
            b["offhi"] = b["close"] / b["high"].rolling(52, min_periods=20).max() - 1
            b["vol20"] = b["close"].pct_change().rolling(20).std()
            b["coin"] = c
            B.append(b)
    B = pd.concat(B)
    mu = B.groupby("coin")["ret1"].transform("mean")
    B["pos"] = B["postRebalance_current_allocation"]
    B["gain"] = B["pos"] * B["ret1"]
    B["drift"] = B["pos"] * mu
    B["ex"] = B["ret1"] - mu
    out["split"] = pd.Series({"in_market_share": (B.pos > 1e-6).mean(),
                              "mean_pos_in": B.loc[B.pos > 1e-6, "pos"].mean(),
                              "gain_bps": B.gain.mean() * 1e4, "drift_bps": B.drift.mean() * 1e4,
                              "timing_bps": (B.gain - B.drift).mean() * 1e4,
                              "coin_mean_bps": B.ret1.mean() * 1e4})
    H = B[B.pos > 1e-6]
    for col in ["forecast", "past26", "ext26", "offhi", "vol20"]:
        x = H.dropna(subset=[col, "ex"]).copy()
        x["q"] = pd.qcut(x[col], 5, labels=False, duplicates="drop")
        out["held_" + col] = x.groupby("q").agg(lo=(col, "min"), hi=(col, "max"),
                                                ex_bps=("ex", lambda s: s.mean() * 1e4),
                                                gain_bps=("gain", lambda s: s.mean() * 1e4),
                                                n=("ex", "size"))
    F = B[B.pos <= 1e-6].dropna(subset=["ex"])
    out["flat_ex_bps"] = F.ex.mean() * 1e4
    return out
