def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    regc = {}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            for r, cnt in b["regime"].value_counts().items():
                regc[str(r)] = regc.get(str(r), 0) + int(cnt)
            c = b["close"].astype(float)
            lr = c.pct_change()
            sd = lr.rolling(30).std()
            f = pd.DataFrame(index=b.index)
            f["coin"] = coin
            f["w"] = w
            f["ts"] = pd.to_datetime(b["timestamp"])
            f["reg"] = b["regime"].astype(str).values
            f["inprof"] = (b["regime"].astype(str) != "chop").values
            f["fc"] = b["forecast"].values
            f["alloc"] = b["postRebalance_current_allocation"].values
            f["s1"] = lr / sd
            f["s3"] = (c / c.shift(3) - 1) / (sd * np.sqrt(3))
            f["s7"] = (c / c.shift(7) - 1) / (sd * np.sqrt(7))
            f["s14"] = (c / c.shift(14) - 1) / (sd * np.sqrt(14))
            rng = (b["high"] - b["low"]).astype(float)
            f["cloc"] = (c - b["low"]) / rng.replace(0, np.nan)
            f["rngsd"] = (rng / c) / sd
            f["vol_ratio"] = b["volume"] / b["volume"].rolling(20).mean()
            f["dhigh20"] = (c / b["high"].rolling(20).max() - 1) / sd
            f["sd30"] = sd
            f["sdratio"] = lr.rolling(7).std() / sd
            f["r60"] = c / c.shift(60) - 1
            for h in (1, 3, 5):
                f[f"fw{h}"] = c.shift(-h) / c - 1
            f["pos"] = np.arange(len(b))
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    A["wd"] = A["ts"].dt.dayofweek
    out = {"regime counts": pd.Series(regc)}

    def daypool_t(x, days):
        x = np.asarray(x, float)
        if len(x) < 3: return np.nan, len(x)
        d = pd.DataFrame({"x": x - x.mean(), "d": days}).groupby("d")["x"].sum()
        D = len(d)
        if D < 3: return np.nan, D
        se = np.sqrt((d ** 2).sum() * D / (D - 1)) / len(x)
        return x.mean() / se, D

    feats = ["s1", "s3", "s7", "s14", "cloc", "rngsd", "vol_ratio", "dhigh20", "sd30", "sdratio", "r60"]
    for h in (3, 5):
        G = A[(A["pos"] % h == 0)].dropna(subset=[f"fw{h}"]).copy()
        G["ex"] = G[f"fw{h}"] - G.groupby("coin")[f"fw{h}"].transform("mean")
        P = G[G["inprof"]]
        t, D = daypool_t(P["ex"].values, P["day"].values)
        out[f"h{h} all in-profile"] = pd.Series({"n": len(P), "mean_ex": P["ex"].mean(), "t_day": t, "days": D,
                                                 "mean_total": P[f"fw{h}"].mean(),
                                                 "outside_n": int((~G["inprof"]).sum()),
                                                 "outside_mean_ex": G.loc[~G["inprof"], "ex"].mean()})
        summ = []
        for ft in feats:
            Q = P.dropna(subset=[ft])
            if len(Q) < 50: continue
            rho, p = stats.spearmanr(Q[ft], Q["ex"])
            q = pd.qcut(Q[ft], 5, labels=False, duplicates="drop")
            m = Q.groupby(q)["ex"].mean()
            ks = list(m.index)
            t0 = daypool_t(Q[q == ks[0]]["ex"].values, Q[q == ks[0]]["day"].values)[0]
            t4 = daypool_t(Q[q == ks[-1]]["ex"].values, Q[q == ks[-1]]["day"].values)[0]
            d = {"rho": rho, "p": p, "n": len(Q)}
            for k in ks: d[f"q{k}"] = m[k]
            d["t_q0"] = t0; d["t_q4"] = t4
            summ.append(pd.Series(d, name=ft))
        out[f"h{h} feature quintiles (excess)"] = pd.DataFrame(summ).round(4)
        if h == 3:
            wd = P.groupby("wd")["ex"].agg(["mean", "count"])
            wd["t"] = [daypool_t(P[P.wd == k]["ex"].values, P[P.wd == k]["day"].values)[0] for k in wd.index]
            out["h3 weekday"] = wd.round(4)
            out["h3 by year"] = P.groupby(P["ts"].dt.year)["ex"].agg(["mean", "count"]).round(4)
            out["h3 by coin"] = P.groupby("coin")["ex"].agg(["mean", "count"]).round(4)
            # s3 bins inside profile, incl. dips
            bins = [-np.inf, -2, -1, 0, 1, 1.1547, 2, np.inf]
            bb = pd.cut(P["s3"], bins)
            tab = P.groupby(bb, observed=True)["ex"].agg(["mean", "count"])
            tab["t"] = [daypool_t(P[bb == k]["ex"].values, P[bb == k]["day"].values)[0] for k in tab.index]
            out["h3 in-profile by s3 bin"] = tab.round(4)
    # book days
    Dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            Dd.append(d.assign(coin=coin, w=w))
    Dd = pd.concat(Dd, ignore_index=True).dropna(subset=["book_return"])
    nz = Dd[Dd["book_return"].abs() > 1e-9]
    out["book days nonzero"] = pd.Series({"n": len(nz), "mean": nz["book_return"].mean(),
                                          "top10_share_of_sum": nz["book_return"].nlargest(10).sum() / nz["book_return"].sum(),
                                          "bottom10_sum": nz["book_return"].nsmallest(10).sum()})
    out["book return by window"] = Dd.groupby("w")["book_return"].agg(["sum", "count"]).round(4)
    # trades
    T = [t.assign(coin=coin) for coin, wins in data["trades"].items() for w, t in wins.items() if len(t)]
    if T:
        T = pd.concat(T, ignore_index=True)
        T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=False)
        out["trades by entry forecast tercile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["mean", "count", "median"]).round(3)
        out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
        out["trades summary"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(),
                                           "win_share": (T["net_profit_loss_percent"] > 0).mean(),
                                           "mean_days": T["duration_minutes"].mean() / 1440})
    return out
