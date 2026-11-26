def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    # book daily returns: Sharpe overall and with top trades' days removed
    D = []
    for c in days:
        for w in days[c]:
            d = days[c][w].copy(); d["coin"] = c; d["window"] = w; D.append(d)
    D = pd.concat(D)
    bd = D.groupby(["window", "day"])["book_return"].mean().dropna()
    out["book_daily"] = pd.Series(dict(mean=bd.mean(), sharpe=bd.mean() / bd.std() * np.sqrt(365), n=len(bd)))
    T = pd.concat([trades[c][w].assign(coin=c, window=w) for c in trades for w in trades[c] if len(trades[c][w])])
    T = T.sort_values("net_profit_loss_percent", ascending=False)
    out["top10_trades_by_coin_window"] = T.head(10).groupby(["coin", "window"]).size()
    T["dur_d"] = T["duration_minutes"] / 1440
    T["durq"] = pd.cut(T["dur_d"], [0, 7.5, 14.5, 30, 1e9])
    out["trades_by_duration"] = T.groupby("durq")["net_profit_loss_percent"].agg(["mean", "sum", "count"])
    out["trades_year"] = T.assign(y=pd.to_datetime(T["entry_time"]).dt.year).groupby("y")["net_profit_loss_percent"].agg(["mean", "sum", "count"])
    # grid at several horizons: slope of fwd on z, by ER tercile (chop / mid / trend)
    res = []
    for h in [3, 7, 14]:
        g = []
        for c in bars:
            drift = pd.concat([(bars[c][w]["close"].shift(-h) / bars[c][w]["close"] - 1).iloc[::h] for w in bars[c]]).mean()
            for w in bars[c]:
                b = bars[c][w].reset_index(drop=True)
                r = b["close"].pct_change()
                z = (b["close"] / b["close"].shift(7) - 1) / (r.rolling(30).std() * np.sqrt(7))
                er = (b["close"] - b["close"].shift(30)).abs() / b["close"].diff().abs().rolling(30).sum()
                fwd = b["close"].shift(-h) / b["close"] - 1 - drift
                usual = r.rolling(30).std() * np.sqrt(h)
                s = pd.DataFrame(dict(z=z, er=er, fwd=fwd, fs=fwd / usual, coin=c, window=w, y=b["timestamp"].astype("datetime64[ns]").dt.year if "timestamp" in b else 0)).iloc[::h].dropna()
                g.append(s)
        G = pd.concat(g)
        G["erq"] = pd.qcut(G["er"], 3, labels=["chop", "mid", "trend"])
        for q, s in G.groupby("erq"):
            lr = stats.linregress(s["z"], s["fwd"])
            res.append(dict(h=h, erq=q, slope=lr.slope, t=lr.slope / lr.stderr, n=len(s),
                            zpos_mean=s.loc[s.z >= 1, "fwd"].mean(), zneg_mean=s.loc[s.z <= -1, "fwd"].mean(),
                            n_pos=(s.z >= 1).sum(), n_neg=(s.z <= -1).sum()))
        if h == 7:
            G7 = G
    out["slope_by_h_er"] = pd.DataFrame(res)
    # signed momentum strength in low-ER: sign(z)*fwd/usual for |z|>=1
    s = G7[(G7.erq != "trend") & (G7.z.abs() >= 1)]
    sm = np.sign(s.z) * s.fs
    out["lowER_signed_strength"] = pd.Series(dict(mean=sm.mean(), t=sm.mean() / sm.std() * np.sqrt(len(sm)), n=len(sm)))
    out["lowER_slope_by_coin"] = G7[G7.erq != "trend"].groupby("coin").apply(lambda x: stats.linregress(x.z, x.fwd).slope)
    out["lowER_slope_by_window"] = G7[G7.erq != "trend"].groupby("window").apply(lambda x: stats.linregress(x.z, x.fwd).slope)
    return out
