import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            prev_hi20 = c.shift(1).rolling(20).max()
            above = c > prev_hi20
            # most recent breakout 1-3 bars ago and its old high
            fb_depth = pd.Series(np.nan, index=c.index)
            for k in (3, 2, 1):
                m = above.shift(k).fillna(False).astype(bool)
                fb_depth[m] = (c / prev_hi20.shift(k) - 1)[m]
            failed = fb_depth < 0
            bo_strength = (c / prev_hi20 - 1).where(above)
            ret20 = c / c.shift(20) - 1
            ret5 = c / c.shift(5) - 1
            vol20 = r1.rolling(20).std()
            z1 = r1 / vol20.shift(1)
            dist_hi = c / c.rolling(20).max() - 1
            dist_lo = c / c.rolling(20).min() - 1
            rng = (b["high"] - b["low"]) / c
            df = pd.DataFrame({"fwd": fwd, "failed": failed, "fb_depth": fb_depth,
                               "bo_strength": bo_strength, "ret20": ret20, "ret5": ret5,
                               "vol20": vol20, "z1": z1, "dist_hi": dist_hi, "dist_lo": dist_lo,
                               "rng": rng, "fc": b["forecast"].astype(float),
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday})
            df["grid"] = (np.arange(n) % H) == 0
            df["coin"] = coin; df["win"] = w
            recs.append(df)
        d = pd.concat(recs, ignore_index=True)
        g = d[d["grid"] & d["fwd"].notna()]
        drift = g["fwd"].mean(); sd = g["fwd"].std()
        d["unus"] = d["fwd"] - drift
        d["str"] = d["unus"] / sd
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    G = D[D["grid"] & D["fwd"].notna()].copy()

    def summ(df, col):
        out = df.groupby(col, observed=True)["unus"].agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        out["strength"] = df.groupby(col, observed=True)["str"].mean()
        return out.drop(columns="std").round(4)

    res = {}
    # failed breakout depth buckets (on all bars where live, sampled once per grid)
    F = G[G["failed"]].copy()
    F["dq"] = pd.qcut(F["fb_depth"], 3, labels=["deep", "mid", "shallow"])
    res["failed_by_depth"] = summ(F, "dq")
    # live successful breakouts: close above prior 20 high
    B = G[G["bo_strength"].notna()].copy()
    B["bq"] = pd.qcut(B["bo_strength"], 3, labels=["small", "mid", "large"])
    res["breakout_by_strength"] = summ(B, "bq")
    # 20-day return quintiles (all grid bars)
    G["r20q"] = pd.qcut(G["ret20"], 5, labels=False)
    res["by_ret20_quintile"] = summ(G.dropna(subset=["ret20"]), "r20q")
    G["r5q"] = pd.qcut(G["ret5"], 5, labels=False)
    res["by_ret5_quintile"] = summ(G.dropna(subset=["ret5"]), "r5q")
    # large one-day moves (z)
    G["zq"] = pd.cut(G["z1"], [-np.inf, -2, -1, 1, 2, np.inf])
    res["by_1d_z"] = summ(G.dropna(subset=["z1"]), "zq")
    # volatility level: within coin tercile
    G["vq"] = G.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    res["by_vol_tercile"] = summ(G.dropna(subset=["vq"]), "vq")
    # distance to 20d high / low
    G["dhq"] = pd.qcut(G["dist_hi"].rank(method="first"), 5, labels=False)
    res["by_dist_hi_quintile"] = summ(G.dropna(subset=["dist_hi"]), "dhq")
    G["rq"] = G.groupby("coin")["rng"].transform(lambda s: pd.qcut(s, 3, labels=False))
    res["by_range_tercile"] = summ(G, "rq")
    # weekday next-day return (all bars)
    D["r1f"] = D.groupby(["coin", "win"])["fwd"].transform(lambda s: s) # placeholder
    nd = []
    for (coin, w), df in D.groupby(["coin", "win"]):
        pass
    res["failed_by_coin"] = summ(F, "coin")
    # book: daily returns, best and worst days and what preceded them
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w
            x["prev_coin5"] = x["close"] / x["close"].shift(5) - 1
            days.append(x)
    Dy = pd.concat(days, ignore_index=True)
    br = Dy["book_return"]
    Dy["bq"] = pd.qcut(br.rank(method="first"), 20, labels=False)
    act = Dy[br.abs() > 1e-12]
    res["book_active_days"] = pd.Series({"n_active": len(act), "share_active": len(act) / br.notna().sum(),
                                         "mean_active": act["book_return"].mean(),
                                         "corr_book_coin_active": act["book_return"].corr(act["coin_return"])})
    ext = pd.concat([act.nsmallest(30, "book_return").assign(k="worst30"),
                     act.nlargest(30, "book_return").assign(k="best30")])
    res["book_extremes"] = ext.groupby("k")[["book_return", "coin_return", "prev_coin5"]].mean().round(4)
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["dq"] = pd.cut(T["days"], [0, 5, 10, 20, 1e9])
    res["trades_by_duration"] = T.groupby("dq", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    return res
