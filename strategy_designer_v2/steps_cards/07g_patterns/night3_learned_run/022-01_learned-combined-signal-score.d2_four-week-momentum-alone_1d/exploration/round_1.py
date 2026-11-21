def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(allr); usual[coin] = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            vol_rel = vol20 / r1.rolling(60, min_periods=40).std()
            r5p = c / c.shift(5) - 1
            r10p = c / c.shift(10) - 1
            nh = c / c.rolling(30).max()
            rng = (b["high"] - b["low"]) / c
            rng_rel = rng / rng.rolling(20).mean()
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n - H, H):
                fwd = c[i + H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, f=b["forecast"][i], r1=r1[i], r5p=r5p[i], r10p=r10p[i],
                                 vol20=vol20[i], vol_rel=vol_rel[i], nh=nh[i], rng_rel=rng_rel[i],
                                 wd=ts[i].weekday(), yr=ts[i].year,
                                 ex=(fwd - drift[coin]) / usual[coin], exr=fwd - drift[coin]))
    d = pd.DataFrame(rows)
    out = {"cells": len(d)}
    def by(col, q=5):
        x = d.dropna(subset=[col]).copy()
        x["g"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = x.groupby("g")["ex"]
        r = pd.DataFrame({"n": g.size(), "mean_strength": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size())),
                          "mean_ret": x.groupby("g")["exr"].mean()})
        sp = stats.spearmanr(x[col], x["ex"])
        r.loc["spearman", "mean_strength"] = sp.correlation; r.loc["spearman", "t"] = sp.correlation * np.sqrt(len(x))
        return r
    for col in ["f", "r1", "r5p", "r10p", "vol20", "vol_rel", "nh", "rng_rel"]:
        out["quintile_" + col] = by(col)
    # momentum conditioned on vol regime
    x = d.dropna(subset=["vol_rel", "f"]).copy()
    x["vg"] = x.groupby("coin")["vol_rel"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    x["fx"] = x["f"] / 10 * x["exr"]
    g = x.groupby("vg")["fx"]
    out["mom_by_volrel_tercile"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    x["sp"] = x.groupby("vg").apply(lambda z: 0).reindex(x["vg"]).values
    out["mom_by_coin"] = x.groupby("coin")["fx"].agg(["size", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    out["mom_by_year"] = x.groupby("yr")["fx"].agg(["size", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    g = d.groupby("wd")["ex"]
    out["weekday_start"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    # book: daily
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    D = pd.concat(dd)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = B.groupby(level=0).agg(lambda s: s.sum()).describe()
    b = B["book_return"]; hb = B["coin_return"]
    out["book_vs_hold"] = pd.Series({"corr": b.corr(hb), "book_sd": b.std(), "hold_sd": hb.std(),
                                     "book_mean": b.mean(), "hold_mean": hb.mean(),
                                     "book_worst1pct_mean": b[b <= b.quantile(0.01)].mean(),
                                     "hold_on_book_worst1pct": hb[b <= b.quantile(0.01)].mean(),
                                     "book_best1pct": b[b >= b.quantile(0.99)].mean(),
                                     "hold_on_book_best1pct": hb[b >= b.quantile(0.99)].mean()})
    # book return by forecast sign / allocation
    al = []
    for coin, wins in data["bars"].items():
        for w, bb in wins.items():
            nx = bb["close"].shift(-1) / bb["close"] - 1
            al.append(pd.DataFrame({"a": bb["postRebalance_current_allocation"], "g": bb["postRebalance_current_allocation"] * nx}))
    A = pd.concat(al).dropna()
    A["side"] = np.sign(A["a"])
    out["gain_by_side"] = A.groupby("side")["g"].agg(["size", "mean", "sum"])
    return out
