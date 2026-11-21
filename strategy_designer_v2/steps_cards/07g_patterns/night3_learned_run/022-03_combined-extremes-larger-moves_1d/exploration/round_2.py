def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    out = {}
    # 1) weekday effect on daily returns (non-overlapping by nature), per coin and by year half
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy()
            x["coin"] = coin; x["w"] = w
            x["wd"] = pd.to_datetime(x["day"]).dt.weekday
            x["yr"] = pd.to_datetime(x["day"]).dt.year
            dl.append(x)
    D = pd.concat(dl, ignore_index=True).dropna(subset=["coin_return"])
    D["un"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    D["z"] = D["un"] / D.groupby("coin")["coin_return"].transform("std")
    g = D.groupby("wd")["z"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    g["un_pct"] = D.groupby("wd")["un"].mean() * 100
    out["daily_weekday_pooled"] = g.round(4)
    pc = D.groupby(["coin", "wd"])["z"].mean().unstack().round(3)
    out["daily_weekday_percoin_z"] = pc
    D["half"] = np.where(D["yr"] <= 2021, "early", "late")
    g = D.groupby(["half", "wd"])["z"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["daily_weekday_by_half"] = g["t"].unstack().round(3)
    # 2) after large absolute 1-day moves: 5-day grid
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=15).std()
            fwd = c.shift(-H) / c - 1
            comb = b["debug_info.components.combined.last_history_value"]
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(c) - H, H):
                rows.append(dict(coin=coin, w=w, fwd=fwd[i], r1=r1[i], vol30=vol30[i],
                                 comb=comb[i], yr=ts[i].year))
    d = pd.DataFrame(rows)
    d["un"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["z"] = d["un"] / d.groupby("coin")["fwd"].transform("std")
    d["ar"] = (d["r1"] / d["vol30"]).abs()
    x = d.dropna(subset=["ar", "z"]).copy()
    x["q"] = x.groupby("coin")["ar"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    g = x.groupby("q")["z"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["absmove_quint"] = g.round(4)
    sp = stats.spearmanr(x["ar"], x["z"])
    out["absmove_rho"] = pd.Series({"rho": sp.correlation, "t": sp.correlation * np.sqrt(len(x)), "n": len(x)}).round(4)
    out["absmove_rho_percoin"] = x.groupby("coin").apply(lambda y: stats.spearmanr(y["ar"], y["z"]).correlation).round(3)
    # 3) combined score's sign: rho with signed forward z, by year and coin
    y = d.dropna(subset=["comb", "z"])
    out["comb_rho_year"] = y.groupby("yr").apply(lambda s: pd.Series({"rho": stats.spearmanr(s["comb"], s["z"]).correlation, "n": len(s)})).round(3)
    out["comb_rho_coin"] = y.groupby("coin").apply(lambda s: stats.spearmanr(s["comb"], s["z"]).correlation).round(3)
    # 4) book: market part vs timing
    bl = []
    for coin, wins in data["bars"].items():
        mu = pd.concat([data["days"][coin][w]["coin_return"] for w in wins]).mean()
        for w, b in wins.items():
            p = b["postRebalance_current_allocation"].astype(float)
            c = b["close"].astype(float)
            g1 = p * (c.shift(-1) / c - 1)
            bl.append(pd.DataFrame({"coin": coin, "gain": g1, "mkt": p * mu, "absp": p.abs()}))
    B = pd.concat(bl).dropna()
    out["book_parts_bps_per_bar"] = (B.groupby("coin")[["gain", "mkt", "absp"]].mean() * [1e4, 1e4, 1]).round(3)
    return out
