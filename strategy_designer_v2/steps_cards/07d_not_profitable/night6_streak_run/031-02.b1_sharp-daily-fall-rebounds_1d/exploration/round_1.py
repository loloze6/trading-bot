def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    days, bars = data["days"], data["bars"]
    # book daily returns (mean across coins per day within window), chained in window order
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    B = B.dropna()
    v = (1 + B["book_return"]).cumprod()
    dd_ = v / v.cummax() - 1
    B["dd"] = dd_.values
    out["book_maxdd"] = float(dd_.min())
    h = (1 + B["coin_return"]).cumprod()
    out["hold_maxdd"] = float((h / h.cummax() - 1).min())
    out["corr_book_hold_daily"] = float(B["book_return"].corr(B["coin_return"]))
    # drawdown by window
    B["bv"] = v.values
    wstat = B.groupby("wn").agg(book=("book_return", lambda x: (1 + x).prod() - 1),
                                hold=("coin_return", lambda x: (1 + x).prod() - 1),
                                min_dd=("dd", "min"))
    out["by_window"] = wstat.round(3)

    # per-coin bar-level features
    feats = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            r = b["close"].pct_change()
            vol = r.rolling(60, min_periods=20).std()
            b["z"] = r / vol
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["ret20z"] = b["ret20"] / (vol * np.sqrt(20))
            b["ma50"] = b["close"] / b["close"].rolling(50, min_periods=30).mean() - 1
            b["volratio"] = r.rolling(10).std() / vol
            b["fwd2"] = b["close"].shift(-2) / b["close"] - 1
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["wn"] = int(w[1:])
            b["alloc"] = b["postRebalance_current_allocation"]
            b["gain"] = b["alloc"] * (b["close"].shift(-1) / b["close"] - 1)
            feats.append(b[["coin", "wn", "pos", "timestamp", "forecast", "z", "ret20", "ret20z", "ma50", "volratio", "fwd2", "alloc", "gain"]])
    F = pd.concat(feats)
    drift = F[F["pos"] % 2 == 0].groupby("coin")["fwd2"].mean()
    F["ex2"] = F["fwd2"] - F["coin"].map(drift)
    G = F[(F["pos"] % 2 == 0)].dropna(subset=["fwd2", "ret20z"])
    out["alloc_share_held"] = float((F["alloc"].abs() > 1e-6).mean())
    out["alloc_mean_when_fc0"] = float(F.loc[F["forecast"] <= 0, "alloc"].mean())
    out["alloc_mean_when_fcpos"] = float(F.loc[F["forecast"] > 0, "alloc"].mean())
    # position gain split by forecast>0 vs not
    F["fcpos"] = F["forecast"] > 0
    out["gain_by_fc"] = F.groupby("fcpos")["gain"].agg(["mean", "count"])

    sig = G["forecast"] > 0
    def summ(m):
        x = G.loc[m, "ex2"]
        return pd.Series({"n": len(x), "mean_ex2": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # trend state terciles of ret20z
    q = G["ret20z"].quantile([1/3, 2/3]).values
    G["trend"] = np.where(G["ret20z"] < q[0], "down", np.where(G["ret20z"] > q[1], "up", "mid"))
    res = {}
    for tr in ["down", "mid", "up"]:
        res[(tr, "signal")] = summ(sig & (G["trend"] == tr))
        res[(tr, "nosignal")] = summ(~sig & (G["trend"] == tr))
    out["trend_x_signal"] = pd.DataFrame(res).T
    G["above_ma"] = G["ma50"] > 0
    res = {}
    for a in [True, False]:
        res[(a, "signal")] = summ(sig & (G["above_ma"] == a))
        res[(a, "nosignal")] = summ(~sig & (G["above_ma"] == a))
    out["ma50_x_signal"] = pd.DataFrame(res).T
    qv = G["volratio"].quantile([1/3, 2/3]).values
    G["vr"] = np.where(G["volratio"] < qv[0], "lowvol", np.where(G["volratio"] > qv[1], "highvol", "midvol"))
    res = {}
    for a in ["lowvol", "midvol", "highvol"]:
        res[(a, "signal")] = summ(sig & (G["vr"] == a))
        res[(a, "nosignal")] = summ(~sig & (G["vr"] == a))
    out["volratio_x_signal"] = pd.DataFrame(res).T
    # z buckets of fall
    Gs = G[sig].copy()
    Gs["zb"] = pd.cut(-Gs["z"], [0, 0.5, 1, 1.5, 2, 3, 99])
    out["fall_size_buckets"] = Gs.groupby("zb")["ex2"].agg(["count", "mean"])
    # in deepest book falls: days in dd < -15%: trend state
    return out
