def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted({w for c in coins for w in days[c].keys()}, key=lambda s: int(s[1:]))
    # book daily
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
    B["eq"] = (1 + B["book"]).cumprod()
    B["peak"] = B["eq"].cummax(); B["dd"] = B["eq"] / B["peak"] - 1
    yrs = len(B) / 365
    yr = B["eq"].iloc[-1] ** (1 / yrs) - 1
    out = {"book summary": pd.Series({"days": len(B), "yearly": yr, "maxdd": B["dd"].min(),
                                      "calmar": yr / -B["dd"].min(), "sharpe": B.book.mean() / B.book.std() * np.sqrt(365)})}
    # drawdown episodes
    B["ep"] = (B["dd"] == 0).cumsum()
    ep = B[B.dd < 0].groupby("ep").agg(depth=("dd", "min"), length=("dd", "size"), start_w=("w", "first"), end_w=("w", "last"))
    out["deepest episodes"] = ep.sort_values("depth").head(6)
    per_w = B.groupby("w").agg(book=("book", "sum"), hold=("hold", "sum"), mindd=("dd", "min"))
    out["per window"] = per_w.loc[wins]
    # bar-level contributions
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            r = b["close"].pct_change().shift(-1)
            pos = b["postRebalance_current_allocation"]
            lr = np.log(b["close"]).diff()
            # recompute ER30, p7, p30
            er = (np.log(b.close) - np.log(b.close.shift(30))).abs() / lr.abs().rolling(30).sum()
            p7 = b.close / b.close.shift(7) - 1; p30 = b.close / b.close.shift(30) - 1
            vol = b.close.pct_change().rolling(30).std()
            vol_rel = vol / vol.rolling(180, min_periods=60).median()
            df = pd.DataFrame({"coin": c, "w": w, "pos": pos, "r": r, "gain": pos * r,
                               "regime_on": (b["regime"] == "mean_reversion"), "fc": b["forecast"],
                               "er": er, "p7": p7, "p30": p30, "volrel": vol_rel})
            recs.append(df)
    X = pd.concat(recs).dropna(subset=["r"])
    X["side"] = np.sign(X.pos)
    held = X[X.pos != 0]
    out["held by side & regime_on"] = held.groupby(["side", "regime_on"]).gain.agg(["count", "mean", "sum"])
    held = held.assign(agree=np.sign(held.p7) == np.sign(held.side), month_agree=np.sign(held.p30) == held.side,
                       erq=pd.qcut(held.er, 4, labels=False), vq=pd.qcut(held.volrel, 4, labels=False))
    out["held by er quartile"] = held.groupby("erq").agg(n=("gain", "size"), mean=("gain", "mean"), er=("er", "mean"))
    out["held by volrel quartile"] = held.groupby("vq").agg(n=("gain", "size"), mean=("gain", "mean"), v=("volrel", "mean"))
    out["held by week agrees with side"] = held.groupby(["agree", "month_agree"]).gain.agg(["count", "mean", "sum"])
    out["held by coin side"] = held.groupby(["coin", "side"]).gain.agg(["count", "mean", "sum"])
    out["abs pos mean"] = pd.Series({"abs pos held": held.pos.abs().mean(), "share days fc!=0": (X.fc != 0).mean()})
    return out
