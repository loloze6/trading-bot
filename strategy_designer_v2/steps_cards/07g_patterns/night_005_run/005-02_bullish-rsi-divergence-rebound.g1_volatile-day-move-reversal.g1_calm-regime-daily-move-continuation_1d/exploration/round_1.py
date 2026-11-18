def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    out["coins"] = ", ".join(coins)
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            r1 = b["close"].pct_change()
            absm = r1.abs().rolling(60, min_periods=30).mean()
            vol20 = r1.rolling(20, min_periods=15).std()
            vrank = vol20.rolling(100, min_periods=50).rank(pct=True)
            ret20 = b["close"].pct_change(20)
            for i in range(0, n - 5, 5):
                rows.append(dict(coin=c, w=w, f=b["forecast"].iloc[i],
                                 pos=b["postRebalance_current_allocation"].iloc[i],
                                 r1=r1.iloc[i], sm=r1.iloc[i] / absm.iloc[i] if absm.iloc[i] else np.nan,
                                 vr=vrank.iloc[i], ret20=ret20.iloc[i],
                                 fwd5=cl[i + 5] / cl[i] - 1,
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday()))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")
    def tt(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    # forecast quintile by coin: raw excess and signed
    g["fq"] = g.groupby("coin")["f"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["fwd5 excess by forecast quintile (signed f)"] = g.groupby("fq")["ex"].apply(tt).unstack()
    # scaled move quintile, signed continuation, by vol rank half
    g["smq"] = pd.qcut(g["sm"].rank(method="first"), 5, labels=False)
    out["fwd5 excess by scaled-move quintile"] = g.groupby("smq")["ex"].apply(tt).unstack()
    g["vrq"] = pd.qcut(g["vr"], 3, labels=["lowvol", "mid", "highvol"])
    g["cont"] = np.sign(g["r1"]) * g["ex"]
    out["signed continuation by vol tercile"] = g.groupby("vrq")["cont"].apply(tt).unstack()
    out["fwd5 excess by vol tercile"] = g.groupby("vrq")["ex"].apply(tt).unstack()
    g["r20q"] = pd.qcut(g["ret20"].rank(method="first"), 5, labels=False)
    out["fwd5 excess by 20d return quintile"] = g.groupby("r20q")["ex"].apply(tt).unstack()
    out["fwd5 excess by weekday"] = g.groupby("wd")["ex"].apply(tt).unstack()
    out["position share long/short/flat"] = pd.Series(dict(long=(g.pos > 0.01).mean(), short=(g.pos < -0.01).mean(), flat=(g.pos.abs() <= 0.01).mean()))
    # book decomposition
    d = []
    for c in coins:
        for w, dd in days[c].items():
            b = bars[c][w]
            dd = dd.copy(); dd["coin"] = c; dd["w"] = w
            pos = b.groupby(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].last().values
            dd["pos_prev"] = np.r_[np.nan, pos[:-1]] if len(pos) == len(dd) else np.nan
            d.append(dd)
    D = pd.concat(d)
    D["mu"] = D.groupby("coin")["coin_return"].transform("mean")
    D["mkt"] = D["pos_prev"] * D["mu"]
    out["book decomposition"] = pd.Series(dict(book_mean=D.book_return.mean(), market_part=D.mkt.mean(), timing=D.book_return.mean() - D.mkt.mean(), mean_pos=D.pos_prev.mean(), mean_abs_pos=D.pos_prev.abs().mean()))
    D["side"] = np.where(D.pos_prev > 0.01, "long", np.where(D.pos_prev < -0.01, "short", "flat"))
    out["book by side"] = D.groupby(["coin", "side"])["book_return"].agg(["count", "mean", "sum"])
    out["book by window (mean x1e4)"] = (D.groupby("w")["book_return"].mean() * 1e4).round(2)
    # trades
    T = pd.concat([data["trades"][c][w].assign(coin=c) for c in coins for w in data["trades"][c]])
    out["trades by side"] = T.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
