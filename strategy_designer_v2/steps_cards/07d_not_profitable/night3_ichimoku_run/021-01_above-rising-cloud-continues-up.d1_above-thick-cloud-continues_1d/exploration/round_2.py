def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    B = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b[["close", "high", "low", "forecast", "regime", "postRebalance_current_allocation"]].copy().reset_index(drop=True)
            b["wn"] = int(w[1:]); b["coin"] = c
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["fwd26"] = b["close"].shift(-26) / b["close"] - 1
            b["past26"] = b["close"] / b["close"].shift(26) - 1
            b["past52"] = b["close"] / b["close"].shift(52) - 1
            b["ext26"] = b["close"] / b["close"].rolling(26).mean() - 1
            b["offhi"] = b["close"] / b["high"].rolling(52, min_periods=20).max() - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["grid"] = (b.index % 26 == 0)
            b["gain"] = b["pos"] * b["ret1"]
            B.append(b)
    B = pd.concat(B, ignore_index=True)
    # per-coin 26-bar mean over all windows on grid
    G = B[B.grid].dropna(subset=["fwd26"])
    mu26 = G.groupby("coin")["fwd26"].mean()
    G = G.assign(ex26=G["fwd26"] - G["coin"].map(mu26))
    R = G[G.regime == "trending"]
    out["n_regime_grid"] = len(R)
    for col in ["forecast", "past26", "past52", "ext26", "offhi"]:
        x = R.dropna(subset=[col]).copy()
        x["q"] = pd.qcut(x[col], 3, labels=False, duplicates="drop")
        g = x.groupby("q").agg(lo=(col, "min"), hi=(col, "max"),
                               ex26_pct=("ex26", lambda s: s.mean() * 100),
                               t=("ex26", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))),
                               n=("ex26", "size"))
        out["grid_" + col] = g
    # same graded by past26 on ALL grid bars (no regime)
    x = G.dropna(subset=["past26"]).copy()
    x["q"] = pd.qcut(x["past26"], 5, labels=False)
    out["all_grid_past26"] = x.groupby("q").agg(lo=("past26", "min"), hi=("past26", "max"),
                               ex26_pct=("ex26", lambda s: s.mean() * 100),
                               t=("ex26", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))),
                               n=("ex26", "size"))
    sl = stats.linregress(x["past26"].clip(-1, 2), x["ex26"])
    out["all_grid_slope_past26"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(x)})
    # falls: per-window daily book, worst 30-day stretches in pooled book
    rows = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            dd = d[["day", "book_return"]].copy(); dd["coin"] = c; dd["wn"] = int(w[1:]); rows.append(dd)
    D = pd.concat(rows)
    P = D.groupby(["wn", "day"])["book_return"].mean().reset_index().sort_values(["wn", "day"]).dropna()
    P["r30"] = P.groupby("wn")["book_return"].transform(lambda s: (1 + s).rolling(30).apply(np.prod, raw=True) - 1)
    worst = P.nsmallest(8, "r30")[["wn", "r30"]]
    out["worst_30d_book"] = worst.groupby("wn")["r30"].min()
    # holdings in worst windows 16-20 by coin: in-market share, mean pos, gain
    W = B[B.wn.between(16, 20)]
    out["w16_20_coin"] = W.groupby("coin").agg(in_share=("pos", lambda s: (s > 1e-6).mean()),
                                               gain_bps=("gain", lambda s: s.mean() * 1e4),
                                               coin_bps=("ret1", lambda s: s.mean() * 1e4))
    # loss days: held bars by entering condition; daily gain when held, by past26 sign and ext26 sign
    H = B[B.pos > 1e-6].dropna(subset=["past26", "ext26"])
    H = H.assign(p=np.sign(H.past26), e=np.sign(H.ext26))
    out["held_by_sign"] = H.groupby(["p", "e"]).agg(gain_bps=("gain", lambda s: s.mean() * 1e4),
                                                   ret_bps=("ret1", lambda s: s.mean() * 1e4),
                                                   sd_bps=("ret1", lambda s: s.std() * 1e4), n=("gain", "size"))
    return out
