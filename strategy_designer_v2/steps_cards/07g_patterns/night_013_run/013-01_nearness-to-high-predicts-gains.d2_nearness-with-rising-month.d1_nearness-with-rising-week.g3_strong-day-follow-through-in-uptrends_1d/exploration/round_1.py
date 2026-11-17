def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            r1 = pd.Series(cl).pct_change()
            vol = r1.rolling(30).std()
            z = r1 / vol
            ret30 = pd.Series(cl).pct_change(30)
            ret7p = pd.Series(cl).pct_change(7)
            hi30 = pd.Series(b["high"].values).rolling(30).max()
            near = pd.Series(cl) / hi30 - 1
            volr = pd.Series(b["volume"].values) / pd.Series(b["volume"].values).rolling(30).mean()
            for i in range(0, n - 7, 7):
                rows.append(dict(coin=c, w=w, f=b["forecast"].iloc[i], reg=b["regime"].iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i],
                                 z=z.iloc[i], r30=ret30.iloc[i], r7p=ret7p.iloc[i], near=near.iloc[i],
                                 vol=vol.iloc[i], volr=volr.iloc[i],
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek,
                                 fwd=cl[i + 7] / cl[i] - 1))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    def tab(col, q=5, sub=None):
        d = (g if sub is None else g[sub]).dropna(subset=[col, "ex"]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = d.groupby("b")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t
    tr = g["reg"] == "trending"
    out["fc_quint_trending"] = tab("f", 5, tr & (g["f"] != 0))
    out["z_quint_all"] = tab("z")
    out["z_quint_nontrend"] = tab("z", 5, ~tr)
    out["r30_quint"] = tab("r30")
    out["r7p_quint"] = tab("r7p")
    out["near_quint"] = tab("near")
    out["vol_quint"] = tab("vol")
    out["volr_quint"] = tab("volr")
    out["regime_ex"] = g.groupby("reg")["ex"].agg(["mean", "count"])
    out["wd_ex"] = g.groupby("wd")["ex"].agg(["mean", "count"])
    # long vs short side position gain (bar-level)
    side = []
    for c in bars:
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].values
            r = b["close"].shift(-1).values / b["close"].values - 1
            side.append(pd.DataFrame(dict(a=a, r=r, coin=c)))
    s = pd.concat(side).dropna()
    s["g"] = s["a"] * s["r"]
    s["side"] = np.sign(s["a"])
    out["gain_by_side"] = s.groupby("side")["g"].agg(["mean", "sum", "count"])
    out["gain_by_coin_side"] = s.groupby(["coin", "side"])["g"].sum().unstack()
    # book daily
    dd = pd.concat([days[c][w].assign(coin=c, w=w) for c in days for w in days[c]])
    br = dd.groupby(["w", "day"])["book_return"].mean().dropna()
    cr = dd.groupby(["w", "day"])["coin_return"].mean().dropna()
    out["book_sharpe_by_coin"] = dd.groupby("coin")["book_return"].agg(lambda x: x.mean() / x.std() * np.sqrt(365))
    out["hold_sharpe_by_coin"] = dd.groupby("coin")["coin_return"].agg(lambda x: x.mean() / x.std() * np.sqrt(365))
    out["share_short_bars"] = float((s["a"] < 0).mean())
    out["share_long_bars"] = float((s["a"] > 0).mean())
    return out
