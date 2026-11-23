def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd60 = r1.rolling(60, min_periods=20).std()
            sd20 = r1.rolling(20, min_periods=20).std()
            volr = sd20 / r1.rolling(60, min_periods=60).std()
            vol = b["volume"].astype(float)
            vrel = vol / vol.rolling(20, min_periods=10).mean().shift(1)
            r2b = c / c.shift(2) - 1
            f2 = c.shift(-2) / c - 1
            f1 = c.shift(-1) / c - 1
            f5 = c.shift(-5) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "r1": r1, "z": r1 / sd60, "z2": r2b / sd60, "volr": volr, "vrel": vrel,
                               "f1": f1, "f2": f2, "f5": f5, "sd60": sd60, "fc": b["forecast"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # drift per coin of 2-bar
    dr = {}
    for coin, wins in data["bars"].items():
        vals = []
        for w, b in wins.items():
            c = b.sort_values("timestamp")["close"].astype(float).values
            vals += list(c[2::2] / c[:-2:2] - 1)
        dr[coin] = np.mean(vals)
    D["x2"] = D["f2"] - D["coin"].map(dr)
    D["s2"] = -np.sign(D["z"]) * D["x2"]  # contrarian signed excess
    D = D.dropna(subset=["z", "x2"])
    out = {}
    def summ(g):
        n = len(g); m = g["s2"].mean(); t = m / (g["s2"].std() / np.sqrt(n)) if n > 2 else np.nan
        sl = stats.linregress(g["z"], g["x2"]).slope if n > 5 else np.nan
        bigz = g[g["z"].abs() > 1]
        mb = bigz["s2"].mean(); tb = mb / (bigz["s2"].std() / np.sqrt(len(bigz))) if len(bigz) > 2 else np.nan
        return pd.Series({"n": n, "mean_contra": m, "t": t, "slope_x2_on_z": sl, "n_absz>1": len(bigz), "mean_contra_big": mb, "t_big": tb})
    D["hv"] = np.where(D["volr"] >= 1, "highvol", "lowvol")
    D.loc[D["volr"].isna(), "hv"] = "na"
    out["by_weekday_x_vol"] = D[D.hv != "na"].groupby(["wd", "hv"]).apply(summ)
    S = D[(D.wd == 6) & (D.hv != "na")].copy()
    S["vq"] = pd.qcut(S["vrel"], 3, labels=["lowV", "midV", "highV"])
    out["sunday_by_volume_tercile_x_vol"] = S.groupby(["hv", "vq"]).apply(summ)
    S["zq"] = pd.qcut(S["z"].abs(), 4, labels=False)
    out["sunday_highvol_by_absz_quartile"] = S[S.hv == "highvol"].groupby("zq").apply(summ)
    S["vrq"] = pd.qcut(S["volr"], 5, labels=False)
    out["sunday_by_volratio_quintile"] = S.groupby("vrq").apply(summ)
    # sign asymmetry
    S["dir"] = np.where(S["z"] > 0, "up", "down")
    out["sunday_by_dir_x_vol"] = S.groupby(["hv", "dir"]).apply(summ)
    out["sunday_highvol_by_year"] = S[S.hv == "highvol"].groupby("year").apply(summ)
    # weekend 2-day (Fri close->Sun close) on Sunday rows
    S2 = S.copy(); S2["z"] = S2["z2"]; S2["s2"] = -np.sign(S2["z2"]) * S2["x2"]
    out["sunday_weekend2day_z_x_vol"] = S2.dropna(subset=["z"]).groupby("hv").apply(summ)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)], ignore_index=True)
    T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", lambda s: (s > 0).mean()])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
