def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    # --- book decomposition by coin and window
    rows = []
    for c in bars:
        allr = pd.concat([bars[c][w]["close"].pct_change() for w in bars[c]])
        mu = allr.mean()
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            r1 = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            g = (a * r1).dropna()
            m = (a * mu)[g.index]
            d = days[c][w]
            rows.append(dict(coin=c, window=w, book_sum=d["book_return"].sum(), gain=g.sum(), market=m.sum(),
                             inpos=(a.abs() > 0).mean(), coin_sum=d["coin_return"].sum()))
    df = pd.DataFrame(rows)
    out["by_coin"] = df.groupby("coin")[["book_sum", "gain", "market", "inpos"]].agg({"book_sum": "sum", "gain": "sum", "market": "sum", "inpos": "mean"})
    out["by_window"] = df.groupby("window")[["book_sum", "gain", "market", "coin_sum"]].sum()
    # --- trades concentration
    T = pd.concat([trades[c][w].assign(coin=c, window=w) for c in trades for w in trades[c] if len(trades[c][w])])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades_summary"] = pd.Series({"n": len(p), "mean": p.mean(), "median": p.median(), "win_share": (p > 0).mean(),
                                       "top5_sum": p.head(5).sum(), "total_sum": p.sum(), "top10_sum": p.head(10).sum()})
    # --- horizon of signal: entry bars (forecast turns >0), forward returns minus drift
    res = []
    for c in bars:
        for h in [1, 3, 7, 14, 21, 28]:
            drift = pd.concat([(bars[c][w]["close"].shift(-h) / bars[c][w]["close"] - 1).iloc[::h] for w in bars[c]]).mean()
            for w in bars[c]:
                b = bars[c][w].reset_index(drop=True)
                f = b["forecast"].fillna(0)
                ent = (f > 0) & (f.shift(1).fillna(0) <= 0)
                fr = b["close"].shift(-h) / b["close"] - 1 - drift
                for i in np.where(ent & fr.notna())[0]:
                    res.append(dict(coin=c, h=h, u=fr[i]))
    R = pd.DataFrame(res)
    out["entry_horizon"] = R.groupby("h")["u"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # --- all grid bars: z = 7d return / (30d std*sqrt7), next 7d return; by z bin and by trend state
    g = []
    for c in bars:
        drift = pd.concat([(bars[c][w]["close"].shift(-7) / bars[c][w]["close"] - 1).iloc[::7] for w in bars[c]]).mean()
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            r = b["close"].pct_change()
            z = (b["close"] / b["close"].shift(7) - 1) / (r.rolling(30).std() * np.sqrt(7))
            r30 = b["close"] / b["close"].shift(30) - 1
            er = (b["close"] - b["close"].shift(30)).abs() / b["close"].diff().abs().rolling(30).sum()
            fwd = b["close"].shift(-7) / b["close"] - 1 - drift
            vol = r.rolling(30).std()
            s = pd.DataFrame(dict(z=z, r30=r30, er=er, fwd=fwd, vol=vol, coin=c)).iloc[::7].dropna()
            g.append(s)
    G = pd.concat(g)
    G["zbin"] = pd.cut(G["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["grid_by_z"] = G.groupby("zbin")["fwd"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    G["erq"] = pd.qcut(G["er"], 3, labels=["chop", "mid", "trend"])
    G["sgn"] = np.sign(G["z"])
    out["grid_er_slope"] = G.groupby("erq").apply(lambda s: pd.Series(dict(slope=stats.linregress(s["z"], s["fwd"]).slope, t=stats.linregress(s["z"], s["fwd"]).slope / stats.linregress(s["z"], s["fwd"]).stderr, n=len(s))))
    G["r30pos"] = G["r30"] > 0
    out["grid_r30_up_vs_z"] = G[G["z"] >= 1].groupby("r30pos")["fwd"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    G["volq"] = G.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["grid_zpos_by_volq"] = G[G["z"] >= 1].groupby("volq")["fwd"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["grid_slope_by_coin"] = G.groupby("coin").apply(lambda s: pd.Series(dict(slope=stats.linregress(s["z"], s["fwd"]).slope, n=len(s))))
    return out
