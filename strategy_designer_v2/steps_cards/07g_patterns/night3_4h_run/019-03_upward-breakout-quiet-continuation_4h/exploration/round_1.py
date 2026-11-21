def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    hourrows = []
    for coin, wins in data["bars"].items():
        # normal drift and usual move per coin over 18 bars
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr.extend(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr); usual = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            prH = hi.shift(1).rolling(12).max(); prL = lo.shift(1).rolling(12).min()
            S = prH - prL
            rng = (hi - lo)
            B = rng.rolling(180, min_periods=60).mean()
            narrow = B / S
            up = (c - prH) / c * 100
            dn = (prL - c) / c * 100
            r1 = c.pct_change()
            r12 = c / c.shift(12) - 1
            r36 = c / c.shift(36) - 1
            r180 = c / c.shift(180) - 1
            vol = r1.rolling(180, min_periods=60).std()
            volrel = r1.rolling(18).std() / vol
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            n = len(b)
            idx = np.arange(0, n - H, H)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ex": (fwd.values[idx] - drift) / usual,
                "exr": fwd.values[idx] - drift,
                "narrow": narrow.values[idx], "up": up.values[idx], "dn": dn.values[idx],
                "r1": (r1 / vol).values[idx], "r12": (r12).values[idx], "r36": r36.values[idx],
                "r180": r180.values[idx], "volrel": volrel.values[idx],
                "fc": b["forecast"].values[idx],
            })
            rows.append(d)
            hh = pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "f1": fwd1 / vol})
            hourrows.append(hh)
    D = pd.concat(rows).dropna(subset=["ex"])
    Hh = pd.concat(hourrows).dropna()
    out = {}
    def grp(col, q=5, sub=None):
        X = D if sub is None else sub
        X = X.dropna(subset=[col])
        g = pd.qcut(X[col].rank(method="first"), q, labels=False)
        t = X.groupby(g)["ex"].agg(["count", "mean"])
        t["t"] = X.groupby(g)["ex"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        t["exr_mean"] = X.groupby(g)["exr"].mean()
        t["colmean"] = X.groupby(g)[col].mean()
        return t
    out["n_grid"] = len(D)
    for col in ["r1", "r12", "r36", "r180", "volrel", "narrow"]:
        out["by_" + col] = grp(col)
    upb = D[D["up"] > 0]
    out["upbreak_count_mean_t"] = pd.Series({"n": len(upb), "mean": upb.ex.mean(), "t": upb.ex.mean()/(upb.ex.std()/np.sqrt(len(upb)))})
    out["upbreak_by_narrow"] = grp("narrow", 3, upb)
    out["upbreak_by_size"] = grp("up", 3, upb)
    dnb = D[D["dn"] > 0]
    out["dnbreak_count_mean_t"] = pd.Series({"n": len(dnb), "mean": dnb.ex.mean(), "t": dnb.ex.mean()/(dnb.ex.std()/np.sqrt(len(dnb)))})
    out["dnbreak_by_size"] = grp("dn", 3, dnb)
    out["fc_desc"] = D.loc[D.fc > 0, "fc"].describe()
    out["by_coin_r36"] = D.groupby("coin").apply(lambda X: pd.Series({"corr_r36": X[["r36","ex"]].dropna().corr().iloc[0,1], "corr_r180": X[["r180","ex"]].dropna().corr().iloc[0,1], "corr_volrel": X[["volrel","ex"]].dropna().corr().iloc[0,1]}))
    hr = Hh.groupby("hour")["f1"].agg(["count","mean","std"]); hr["t"] = hr["mean"]/(hr["std"]/np.sqrt(hr["count"]))
    out["by_hour_1bar_volnorm"] = hr
    wd = Hh.groupby("wd")["f1"].agg(["count","mean","std"]); wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["by_weekday_1bar_volnorm"] = wd
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, win=w))
    DD = pd.concat(dd)
    daily = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = daily.groupby(level=0).agg(["count", "mean", "sum"]).sort_values("sum").head(8)
    return out
