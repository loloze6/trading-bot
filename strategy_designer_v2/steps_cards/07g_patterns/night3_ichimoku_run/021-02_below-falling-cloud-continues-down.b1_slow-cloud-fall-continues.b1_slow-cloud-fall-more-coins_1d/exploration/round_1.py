def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(c).pct_change()
            vol20 = r1.rolling(20).std()
            past26 = pd.Series(c) / pd.Series(c).shift(26) - 1
            mid52 = (hi.rolling(52).max() + lo.rolling(52).min()) / 2
            mid26 = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            pos52 = pd.Series(c) / mid52 - 1
            pos26 = pd.Series(c) / mid26 - 1
            # range position within 52-day range
            rng = (pd.Series(c) - lo.rolling(52).min()) / (hi.rolling(52).max() - lo.rolling(52).min())
            sf = b.get("debug_info.components.slow_fall.last_history_value")
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, year=ts[i].year, fwd=c[i+H]/c[i]-1,
                                 regime=b["regime"].iloc[i], past26=past26.iloc[i], vol20=vol20.iloc[i],
                                 pos52=pos52.iloc[i], pos26=pos26.iloc[i], rng=rng.iloc[i],
                                 sf=(sf.iloc[i] if sf is not None else np.nan)))
            z = r1 / vol20.shift(1)
            fwd1 = r1.shift(-1)
            fwd5 = pd.Series(c).shift(-5) / pd.Series(c) - 1
            daily.append(pd.DataFrame(dict(coin=coin, w=w, wd=ts.dt.weekday, year=ts.dt.year,
                                           r1=r1, z=z, fwd1=fwd1, fwd5=fwd5,
                                           alloc=b["postRebalance_current_allocation"])))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    d = pd.concat(daily, ignore_index=True)
    out = {}
    def summ(df, key, col="ex"):
        return df.groupby(key)[col].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x)) if len(x) > 2 else np.nan]).rename(columns={"<lambda_0>": "t"})
    out["regime_ex"] = summ(g, "regime")
    out["regime_fwd"] = summ(g, "regime", "fwd")
    out["year_trending_fwd"] = summ(g[g.regime == "trending"], "year", "fwd")
    out["year_all_fwd"] = summ(g, "year", "fwd")
    for v in ["past26", "vol20", "pos52", "pos26", "rng"]:
        gg = g.dropna(subset=[v]).copy()
        gg["q"] = gg.groupby("coin")[v].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False) if len(x) >= 10 else np.nan)
        out["q_" + v] = summ(gg.dropna(subset=["q"]), "q")
        out["corr_" + v] = "spearman %.3f p %.4f n %d" % (*stats.spearmanr(gg[v], gg["ex"]), len(gg))
    t = g[g.regime == "trending"].dropna(subset=["pos52"])
    t = t.copy(); t["q"] = pd.qcut(t["pos52"].rank(method="first"), 4, labels=False)
    out["trending_by_pos52_q"] = summ(t, "q")
    t2 = g[g.regime == "trending"].dropna(subset=["vol20"]).copy()
    t2["q"] = pd.qcut(t2["vol20"].rank(method="first"), 4, labels=False)
    out["trending_by_vol_q"] = summ(t2, "q")
    dd = d.dropna(subset=["z", "fwd5"]).copy()
    dd["zb"] = pd.cut(dd["z"], [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    out["after_daily_z_fwd5"] = dd.groupby("zb")["fwd5"].agg(["count", "mean", "std"])
    out["after_daily_z_fwd1"] = dd.groupby("zb")["fwd1"].agg(["count", "mean", "std"])
    out["weekday_r1"] = d.dropna(subset=["r1"]).groupby("wd")["r1"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; bk.append(x)
    bk = pd.concat(bk, ignore_index=True)
    bk["year"] = pd.to_datetime(bk["day"]).dt.year
    out["book_by_year"] = bk.groupby("year")[["book_return", "coin_return"]].mean()
    out["book_by_coin"] = bk.groupby("coin")[["book_return", "coin_return"]].mean()
    tr = []
    for coin, wins in data["trades"].items():
        for w, x in wins.items():
            if len(x): x = x.copy(); x["coin"] = coin; tr.append(x)
    tr = pd.concat(tr, ignore_index=True)
    out["trades_side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", "std"])
    out["trades_dur_q"] = tr.groupby(pd.qcut(tr["duration_minutes"], 4, duplicates="drop"))["net_profit_loss_percent"].agg(["count", "mean"])
    return out
