def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    regc = {}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            for r, c in b["regime"].value_counts().items():
                regc[r] = regc.get(r, 0) + c
            c = b["close"]
            lr = c.pct_change()
            sd = lr.rolling(30).std()
            f = pd.DataFrame({"coin": coin, "w": w})
            f["ts"] = pd.to_datetime(b["timestamp"])
            f["inprof"] = (b["regime"] != "chop").values
            f["fc"] = b["forecast"].values
            f["s1"] = lr / sd
            f["s3"] = (c / c.shift(3) - 1) / (sd * np.sqrt(3))
            f["s7"] = (c / c.shift(7) - 1) / (sd * np.sqrt(7))
            f["s14"] = (c / c.shift(14) - 1) / (sd * np.sqrt(14))
            rng = (b["high"] - b["low"])
            f["cloc"] = (c - b["low"]) / rng.replace(0, np.nan)
            f["rngsd"] = (rng / c) / sd
            f["vol_ratio"] = b["volume"] / b["volume"].rolling(20).mean()
            f["dhigh20"] = (c / b["high"].rolling(20).max() - 1) / sd
            f["sd30"] = sd
            f["sdratio"] = lr.rolling(7).std() / sd
            for h in (1, 3, 5):
                f[f"fw{h}"] = c.shift(-h) / c - 1
            f["pos"] = np.arange(len(b))
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    A["wd"] = A["ts"].dt.dayofweek
    out = {"regime counts": pd.Series(regc)}
    def daypool_t(x, days):
        d = pd.DataFrame({"x": x - x.mean(), "d": days}).groupby("d")["x"].sum()
        D = len(d)
        if D < 3: return np.nan, D
        se = np.sqrt((d**2).sum() * D / (D - 1)) / len(x)
        return x.mean() / se, D
    feats = ["s1", "s3", "s7", "s14", "cloc", "rngsd", "vol_ratio", "dhigh20", "sd30", "sdratio"]
    for h in (3, 5):
        G = A[(A["pos"] % h == 0)].copy()
        G = G.dropna(subset=[f"fw{h}"])
        G["ex"] = G[f"fw{h}"] - G.groupby("coin")[f"fw{h}"].transform("mean")
        P = G[G["inprof"]]
        t, D = daypool_t(P["ex"].values, P["day"].values)
        out[f"h{h} all in-profile"] = pd.Series({"n": len(P), "mean_ex": P["ex"].mean(), "t_day": t, "days": D,
                                                 "mean_total": P[f"fw{h}"].mean()})
        summ = []
        for ft in feats:
            Q = P.dropna(subset=[ft])
            rho, p = stats.spearmanr(Q[ft], Q["ex"])
            q = pd.qcut(Q[ft], 5, labels=False, duplicates="drop")
            m = Q.groupby(q)["ex"].mean()
            tt = []
            for k in m.index:
                s = Q[q == k]
                tt.append(daypool_t(s["ex"].values, s["day"].values)[0])
            summ.append(pd.Series({"rho": rho, "p": p, "n": len(Q),
                                   **{f"q{k}": m[k] for k in m.index},
                                   "t_q0": tt[0], "t_q4": tt[-1]}, name=ft))
        out[f"h{h} feature quintiles (excess)"] = pd.DataFrame(summ).round(4)
        if h == 3:
            wd = P.groupby("wd")["ex"].agg(["mean", "count"])
            wd["t"] = [daypool_t(P[P.wd == k]["ex"].values, P[P.wd == k]["day"].values)[0] for k in wd.index]
            out["h3 weekday"] = wd.round(4)
            out["h3 by year"] = P.groupby(P["ts"].dt.year)["ex"].agg(["mean", "count"]).round(4)
            out["h3 by coin"] = P.groupby("coin")["ex"].agg(["mean", "count"]).round(4)
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    if T:
        T = pd.concat(T)
        T["fq"] = pd.qcut(T["entry_forecast"], 3, labels=False, duplicates="drop")
        out["trades by entry forecast tercile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["mean", "count", "median"]).round(3)
        out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
