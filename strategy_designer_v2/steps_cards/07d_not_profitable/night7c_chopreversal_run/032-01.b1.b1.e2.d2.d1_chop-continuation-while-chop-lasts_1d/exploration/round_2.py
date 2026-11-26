def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted({w for c in coins for w in days[c].keys()}, key=lambda s: int(s[1:]))
    out = {}
    # book daily with drawdown flag
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy(); d["coin"] = c; frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).dropna()
        g["w"] = w; rows.append(g)
    B = pd.concat(rows).reset_index()
    B["eq"] = (1 + B["book"]).cumprod(); B["peak"] = B.eq.cummax(); B["dd"] = B.eq / B.peak - 1
    B["ep"] = (B.dd == 0).cumsum()
    ep = B[B.dd < 0].groupby("ep").dd.min().sort_values()
    top = ep.index[:3]
    # within the deepest episodes, the fall segment (peak to trough)
    fallday = set()
    for e in top:
        s = B[B.ep == e]
        tr = s.dd.idxmin()
        fallday |= set(B.loc[s.index[0]:tr, "day"])
    # bar-level
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            r = b.close.pct_change().shift(-1)
            lr = np.log(b.close).diff()
            er = (np.log(b.close) - np.log(b.close.shift(30))).abs() / lr.abs().rolling(30).sum()
            p7 = b.close / b.close.shift(7) - 1; p30 = b.close / b.close.shift(30) - 1
            vol = b.close.pct_change().rolling(30).std()
            vol90 = b.close.pct_change().rolling(90, min_periods=60).std()
            vr = vol / vol90
            sc = p7 / (vol * np.sqrt(7))
            f7 = b.close.shift(-7) / b.close - 1
            day = pd.to_datetime(b.timestamp).dt.floor("D")
            df = pd.DataFrame({"coin": c, "w": w, "day": day, "pos": b.postRebalance_current_allocation, "r": r,
                               "on": b.regime == "mean_reversion", "fc": b.forecast, "er": er, "p7": p7, "p30": p30,
                               "vr": vr, "sc": sc, "f7": f7, "i": np.arange(len(b))})
            df["gain"] = df.pos * df.r
            recs.append(df)
    X = pd.concat(recs)
    X["inf"] = X.day.isin(fallday)
    H = X[(X.pos != 0) & X.r.notna()].copy()
    H["side"] = np.sign(H.pos)
    H["wk_agree"] = np.sign(H.p7) == H.side
    out["in falls vs not: held"] = H.groupby(["inf", "on", "wk_agree"]).gain.agg(["count", "mean", "sum"])
    out["in falls: side"] = H.groupby(["inf", "side"]).gain.agg(["count", "mean", "sum"])
    H["vq"] = pd.qcut(H.vr, 4, labels=False)
    out["held by vr quartile, on"] = H.groupby(["vq", "on"]).agg(n=("gain", "size"), mean=("gain", "mean"), vr=("vr", "mean"))
    out["fall share of days by vq"] = H.groupby("vq").inf.mean()
    # grid check: signal vs condition alone
    G = X[(X.i % 7 == 0) & X.f7.notna() & X.er.notna() & X.vr.notna()].copy()
    drift = G.groupby("coin").f7.mean()
    G["ex"] = G.f7 - G.coin.map(drift)
    chop = G.er < 0.3
    sig = chop & (np.sign(G.p7) == np.sign(G.p30)) & (G.p7 != 0)
    G["dir"] = np.sign(G.p30)
    G["sx"] = G.ex * G.dir
    G["vlow"] = G.vr < G.vr.median()
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    res = {}
    for vl in [True, False]:
        res[("signal", vl)] = tt(G.loc[sig & (G.vlow == vl), "sx"])
        res[("chop no agree, p30 dir", vl)] = tt(G.loc[chop & ~sig & (G.vlow == vl), "sx"])
        res[("all bars long", vl)] = tt(G.loc[G.vlow == vl, "ex"])
        res[("all bars p30 dir", vl)] = tt(G.loc[G.vlow == vl, "sx"])
    out["grid: signed excess 7d by vol state"] = pd.DataFrame(res).T
    # signal by |sc| strength terciles within vol state
    S = G[sig].copy(); S["st"] = pd.qcut(S.sc.abs(), 3, labels=False)
    out["signal: strength x vol state"] = S.groupby(["vlow", "st"]).sx.agg(["count", "mean"])
    # signal by side
    out["signal by side"] = S.groupby("dir").sx.agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    return out
