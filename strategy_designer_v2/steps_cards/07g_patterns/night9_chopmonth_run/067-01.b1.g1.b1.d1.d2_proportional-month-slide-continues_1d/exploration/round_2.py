def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def ctt(df, col, key="day"):
        dd = df.groupby(key)[col].sum()
        if len(dd) < 3: return (np.nan, len(dd))
        return (dd.mean() / (dd.std() / np.sqrt(len(dd))), len(dd))
    # daily-level frame from bars
    dl = []
    for coin, wd in bars.items():
        for w, b in wd.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "w": w, "day": b["timestamp"].astype(str).str[:10]})
            d["ret"] = c.pct_change()
            d["sd30"] = d["ret"].rolling(30).std()
            d["z"] = d["ret"] / d["sd30"]
            d["next1"] = c.shift(-1) / c - 1
            d["next3"] = c.shift(-3) / c - 1
            d["r60"] = (c / c.shift(60) - 1) * 100
            d["r30"] = (c / c.shift(30) - 1) * 100
            d["i"] = np.arange(len(b))
            d["wdn"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            d["regime"] = b["regime"]
            d["pos"] = b["postRebalance_current_allocation"].astype(float)
            dl.append(d)
    D = pd.concat(dl, ignore_index=True)
    medv = D.groupby("coin")["sd30"].median()
    D["agit"] = np.where(D["sd30"] > D["coin"].map(medv), "agit", "calm")
    D["trend"] = np.where(D["r60"] > 10, "rising", np.where(D["r60"] < -10, "falling", np.where(D["r60"].notna(), "choppy", "na")))
    D["drift1"] = D["coin"].map(D.groupby("coin")["next1"].mean())
    D["ex1"] = D["next1"] - D["drift1"]
    Dz = D.dropna(subset=["z", "ex1"]).copy()
    Dz["zbin"] = pd.qcut(Dz["z"], 7, labels=False)
    rows = []
    for (tr, zb), x in Dz.groupby(["trend", "zbin"]):
        t, nd = ctt(x, "ex1")
        rows.append(dict(trend=tr, zbin=zb, z=x["z"].mean(), n=len(x), days=nd, ex1=x["ex1"].mean(), t=t))
    out["next1_by_trend_zbin"] = pd.DataFrame(rows).set_index(["trend", "zbin"])
    rows = []
    for (ag, zb), x in Dz.groupby(["agit", "zbin"]):
        t, nd = ctt(x, "ex1")
        rows.append(dict(agit=ag, zbin=zb, z=x["z"].mean(), n=len(x), days=nd, ex1=x["ex1"].mean(), t=t))
    out["next1_by_agit_zbin"] = pd.DataFrame(rows).set_index(["agit", "zbin"])
    # spearman z vs ex1 per year (stability) for lower half (falls)
    rows = []
    for y, x in Dz[Dz.z < 0].groupby("year"):
        r, p = stats.spearmanr(x["z"], x["ex1"])
        rows.append(dict(year=y, n=len(x), rho=r, p=p))
    out["falls_z_vs_next1_by_year"] = pd.DataFrame(rows).set_index("year")
    # weekday clustered
    rows = []
    for wdn, x in D.dropna(subset=["ex1"]).groupby("wdn"):
        t, nd = ctt(x, "ex1")
        rows.append(dict(wdn=wdn, ex1=x["ex1"].mean(), days=nd, t_clustered=t))
    out["weekday_next1_clustered(wdn=day of the bar; next1 is following day)"] = pd.DataFrame(rows).set_index("wdn")
    # theme: r30 vs next10 in choppy, grid, split by agitation, on both sides, clustered
    G = D[D["i"] % 10 == 0].copy()
    allg = []
    for coin, wd in bars.items():
        for w, b in wd.items():
            c = b["close"].astype(float).reset_index(drop=True)
            f = c.shift(-10) / c - 1
            allg.append(pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(c)), "fwd10": f}))
    F = pd.concat(allg)
    G = G.merge(F, on=["coin", "w", "i"])
    G = G.dropna(subset=["fwd10"])
    G["ex10"] = G["fwd10"] - G["coin"].map(G.groupby("coin")["fwd10"].mean())
    rows = []
    for (tr, ag), x in G.dropna(subset=["r30"]).groupby(["trend", "agit"]):
        if len(x) < 15: continue
        r, p = stats.spearmanr(x["r30"], x["ex10"])
        x = x.copy(); x["sig"] = np.sign(x["r30"]) * x["ex10"]
        t, nd = ctt(x, "sig")
        up = x[x.r30 > 0]; dn = x[x.r30 < 0]
        rows.append(dict(trend=tr, agit=ag, n=len(x), rho=r, p=p, signed_ex=x["sig"].mean(), t=t, days=nd,
                         ex_after_up=up["ex10"].mean(), n_up=len(up), ex_after_down=dn["ex10"].mean(), n_dn=len(dn)))
    out["r30_vs_ex10_by_profile"] = pd.DataFrame(rows).set_index(["trend", "agit"])
    # book: largest gains/losses days context
    Dy = []
    for coin, wd in data["days"].items():
        for w, d in wd.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; Dy.append(d)
    Dy = pd.concat(Dy).dropna(subset=["book_return"])
    q = Dy["book_return"].quantile([0.01, 0.99])
    big_l = Dy[Dy.book_return <= q.iloc[0]]; big_g = Dy[Dy.book_return >= q.iloc[1]]
    out["book_tails"] = pd.DataFrame({"n": [len(big_l), len(big_g)], "mean_book": [big_l.book_return.mean(), big_g.book_return.mean()],
                                      "mean_coin": [big_l.coin_return.mean(), big_g.coin_return.mean()],
                                      "sum_share_of_total": [big_l.book_return.sum() / Dy.book_return.sum(), big_g.book_return.sum() / Dy.book_return.sum()]},
                                     index=["worst1pct", "best1pct"])
    return out
