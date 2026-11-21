def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 5
    # book decomposition
    rows = []
    allbars = []
    for c, ws in data["bars"].items():
        # coin mean daily return over all windows
        dr = pd.concat([data["days"][c][w]["coin_return"] for w in ws]).dropna()
        mu = dr.mean()
        for w, b in ws.items():
            d = data["days"][c][w]
            b = b.copy()
            b["coin"] = c; b["win"] = w
            b["pos"] = b["postRebalance_current_allocation"]
            b["fwd1"] = b["close"].shift(-1) / b["close"] - 1
            b["fwd"] = b["close"].shift(-H) / b["close"] - 1
            b["past20"] = b["close"] / b["close"].shift(20) - 1
            b["past90"] = b["close"] / b["close"].shift(60) - 1
            b["ma50"] = b["close"] / b["close"].rolling(50, min_periods=30).mean() - 1
            # swing lows, side 2, confirmed 2 bars later
            lo = b["low"].values; n = len(b)
            piv = np.full(n, np.nan)
            for i in range(2, n - 2):
                if lo[i] <= lo[i-2:i+3].min():
                    piv[i] = lo[i]
            # count of swing lows within 2% below close (support below), last 90 bars, known at close
            cl = b["close"].values
            below = np.zeros(n); above_near = np.zeros(n)
            for t in range(n):
                s = max(0, t - 90); e = t - 1  # pivots confirmed by t need i<=t-2
                p = piv[s:max(s, t-1)]
                p = p[~np.isnan(p)]
                if len(p):
                    below[t] = np.sum((p <= cl[t]) & (p >= cl[t] * 0.97))
                    above_near[t] = np.sum((p > cl[t]) & (p <= cl[t] * 1.03))
            b["sup_below"] = below; b["sup_above"] = above_near
            b["grid"] = (np.arange(n) % H == 0)
            allbars.append(b)
            rows.append(pd.DataFrame({"book": d["book_return"], "mkt": d["coin_return"]}).assign(coin=c, win=w, mu=mu))
    B = pd.concat(allbars, ignore_index=True)
    mus = {}
    for c in data["bars"]:
        g = B[(B.coin == c) & B.grid]
        mus[c] = g["fwd"].mean()
    B["drift5"] = B["coin"].map(mus)
    B["unus"] = B["fwd"] - B["drift5"]
    # gain decomposition on bars
    B["mu1"] = B["coin"].map({c: B[B.coin == c]["fwd1"].mean() for c in data["bars"]})
    gain = (B["pos"] * B["fwd1"]).groupby(B["coin"]).mean()
    mkt = (B["pos"] * B["mu1"]).groupby(B["coin"]).mean()
    out["gain_decomp_per_bar"] = pd.DataFrame({"gain": gain, "from_drift": mkt, "timing": gain - mkt,
                                               "mean_pos": B.groupby("coin")["pos"].mean(),
                                               "share_short": B.groupby("coin")["pos"].apply(lambda x: (x < 0).mean())})
    G = B[B.grid & B["fwd"].notna()].copy()
    # short cases: forecast<0
    S = G[G["forecast"] < 0].copy()
    S["unus_short"] = -S["unus"]
    S["fq"] = pd.qcut(S["forecast"].abs(), 4, labels=False, duplicates="drop")
    out["short_by_forecast_quartile"] = S.groupby("fq")["unus_short"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    S["trend"] = np.where(S["ma50"] < 0, "below_ma50", "above_ma50")
    out["short_by_trend"] = S.groupby("trend").agg(unus=("unus_short", "mean"), total=("fwd", lambda x: -x.mean()), n=("fwd", "size"))
    S["p20q"] = pd.qcut(S["past20"], 4, labels=False)
    out["short_by_past20_q"] = S.groupby("p20q").agg(unus=("unus_short", "mean"), total=("fwd", lambda x: -x.mean()), n=("fwd", "size"), p20=("past20","mean"))
    out["short_by_year"] = S.groupby(pd.to_datetime(S["timestamp"]).dt.year).agg(unus=("unus_short", "mean"), n=("fwd","size"))
    # support below (bounce idea, long): unusual move by count of swing lows just below
    G["sb"] = G["sup_below"].clip(upper=4)
    out["long_by_support_below_count"] = G.groupby("sb").agg(unus=("unus", "mean"), total=("fwd", "mean"), n=("fwd", "size"),
                                                             t=("unus", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    G["sa"] = G["sup_above"].clip(upper=4)
    out["by_support_above_count"] = G.groupby("sa").agg(unus=("unus", "mean"), total=("fwd", "mean"), n=("fwd", "size"),
                                                        t=("unus", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    # support below, split by trend
    G["trend"] = np.where(G["ma50"] < 0, "below_ma50", "above_ma50")
    out["support_below_x_trend"] = G.groupby(["trend", "sb"]).agg(unus=("unus", "mean"), n=("fwd", "size"))
    out["usual_move_5d"] = float(G["fwd"].std())
    return out
