def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        coin_rows = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, hi, lo = b["close"].astype(float), b["high"].astype(float), b["low"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame(index=b.index)
            df["coin"] = coin
            df["win"] = w
            df["fwd"] = c.shift(-H) / c - 1
            df["r1"] = r1
            df["r5"] = c / c.shift(5) - 1
            df["r20"] = c / c.shift(20) - 1
            df["vol20"] = r1.rolling(20).std()
            df["volratio"] = r1.rolling(5).std() / r1.rolling(60, min_periods=30).std()
            ph20 = hi.shift(1).rolling(20).max()
            pl20 = lo.shift(1).rolling(20).min()
            df["dist_hi20"] = c / ph20 - 1
            df["dist_lo20"] = c / pl20 - 1
            bo = (c > ph20)
            lvl = ph20.where(bo)
            last_lvl = lvl.shift(1).rolling(3, min_periods=1).max()
            df["fail_broad"] = (last_lvl.notna()) & (c < last_lvl)
            df["fail_depth"] = np.where(df["fail_broad"], 1 - c / last_lvl, np.nan)
            # breakdowns (mirror): close below prior 20d low
            bd = (c < pl20)
            df["bo"] = bo
            df["bd"] = bd
            df["range"] = (hi - lo) / c
            df["clv"] = (c - lo) / (hi - lo).replace(0, np.nan)
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday.values
            df["fc"] = b["forecast"].values
            df["alloc"] = b["postRebalance_current_allocation"].values
            df["grid"] = (np.arange(len(b)) % H == 0)
            coin_rows.append(df)
        cd = pd.concat(coin_rows, ignore_index=True)
        g = cd[cd["grid"] & cd["fwd"].notna()]
        cd["ex"] = cd["fwd"] - g["fwd"].mean()
        cd["usual"] = g["fwd"].std()
        rows.append(cd)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["grid"] & A["fwd"].notna()].copy()
    G["z"] = G["ex"] / G["usual"]

    def summ(gr):
        x = gr["ex"].dropna()
        n = len(x)
        t = x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean_ex": x.mean(), "t": t, "mean_z": gr["z"].mean()})

    out = {}
    feats = ["r1", "r5", "r20", "vol20", "volratio", "dist_hi20", "dist_lo20", "range", "clv"]
    for f in feats:
        try:
            q = G.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
            out["q_" + f] = G.assign(q=q).groupby("q").apply(summ)
        except Exception as e:
            out["q_" + f] = "err " + str(e)
    sp = {}
    for f in feats:
        s = G[[f, "z"]].dropna()
        rr, p = stats.spearmanr(s[f], s["z"])
        sp[f] = [rr, p, len(s)]
    out["spearman_feat_z"] = pd.DataFrame(sp, index=["rho", "p", "n"]).T
    out["by_weekday"] = G.groupby("wd").apply(summ)
    out["breakout_today"] = G.groupby("bo").apply(summ)
    out["breakdown_today"] = G.groupby("bd").apply(summ)
    out["fail_broad"] = G.groupby("fail_broad").apply(summ)
    fb = G[G["fail_broad"]]
    try:
        rr, p = stats.spearmanr(fb["fail_depth"], fb["ex"])
        out["fail_broad_depth_spearman"] = "rho=%.3f p=%.3f n=%d" % (rr, p, len(fb))
    except Exception as e:
        out["fail_broad_depth_spearman"] = str(e)
    out["fail_broad_by_coin"] = fb.groupby("coin").apply(summ)
    # by year
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_corr_coin"] = float(bk.corr().iloc[0, 1])
    out["book_mean_std"] = bk.agg(["mean", "std", "count"])
    act = A[A["alloc"].abs() > 1e-6]
    out["active_bars_share"] = float(len(act) / len(A))
    out["active_by_coin"] = act.groupby("coin").size()
    # trades summary
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                T.append(t.assign(coin=coin))
    if T:
        T = pd.concat(T, ignore_index=True)
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
        out["trades_duration_days"] = (T["duration_minutes"] / 1440).describe()
    return out
