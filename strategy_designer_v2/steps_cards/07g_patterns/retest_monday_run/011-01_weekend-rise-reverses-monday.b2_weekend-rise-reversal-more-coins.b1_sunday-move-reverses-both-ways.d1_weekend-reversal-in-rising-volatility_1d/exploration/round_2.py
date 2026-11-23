def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    dr = {}
    for coin, wins in data["bars"].items():
        vals = []
        for w, b in wins.items():
            c = b.sort_values("timestamp")["close"].astype(float).values
            vals += list(c[2::2] / c[:-2:2] - 1)
        dr[coin] = np.mean(vals)
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd60 = r1.rolling(60, min_periods=20).std()
            volr = r1.rolling(20, min_periods=20).std() / r1.rolling(60, min_periods=60).std()
            vol = b["volume"].astype(float)
            vrel = vol / vol.rolling(20, min_periods=10).mean().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "z": r1 / sd60, "volr": volr, "vrel": vrel,
                               "f1": c.shift(-1) / c - 1, "g2": c.shift(-2) / c.shift(-1) - 1,
                               "f2": c.shift(-2) / c - 1})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["z", "f2", "volr"])
    D["x2"] = D["f2"] - D["coin"].map(dr)
    D["cont"] = np.sign(D["z"]) * D["x2"]
    D["cont1"] = np.sign(D["z"]) * D["f1"]
    D["cont_d2"] = np.sign(D["z"]) * D["g2"]
    D["hv"] = np.where(D["volr"] >= 1, "highvol", "lowvol")
    def summ(g, col="cont"):
        n = len(g); m = g[col].mean(); t = m / (g[col].std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean": m, "t": t})
    out = {}
    W = D[(D.wd == 2) & (D.hv == "lowvol")].copy()
    out["wed_lowvol_continuation_by_year"] = W.groupby("year").apply(summ)
    W["zq"] = pd.qcut(W["z"].abs(), 4, labels=False)
    out["wed_lowvol_by_absz_q"] = W.groupby("zq").apply(summ)
    out["wed_lowvol_day1_day2"] = pd.DataFrame({"day1": summ(W, "cont1"), "day2": summ(W, "cont_d2")})
    out["wed_lowvol_by_dir"] = W.assign(d=np.where(W.z > 0, "up", "down")).groupby("d").apply(summ)
    out["wed_lowvol_by_coin"] = W.groupby("coin").apply(summ)
    L = D[D.hv == "lowvol"].copy()
    L["vrq"] = pd.qcut(L["volr"], 3, labels=False)
    out["wed_by_volr_tercile_all"] = D[D.wd == 2].assign(vq=pd.qcut(D[D.wd == 2]["volr"], 5, labels=False)).groupby("vq").apply(summ)
    S = D[(D.wd == 6) & (D.hv == "highvol")].copy()
    S["vq"] = pd.qcut(S["vrel"], 5, labels=False)
    out["sun_highvol_reversal_by_volume_quintile"] = S.groupby("vq").apply(lambda g: -summ(g) * np.array([-1, 1, 1]))
    out["sun_highvol_day1_day2_rev"] = pd.DataFrame({"day1": -summ(S, "cont1"), "day2": -summ(S, "cont_d2")})
    M = D[(D.wd == 0) & (D.hv == "highvol")]
    out["mon_highvol_rev_by_year"] = M.groupby("year").apply(lambda g: -summ(g) * np.array([-1, 1, 1]))
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)], ignore_index=True)
    T["dur_d"] = (T["duration_minutes"] / 1440).round()
    T["ewd"] = pd.to_datetime(T["entry_time"]).dt.weekday
    out["trades_side_by_duration"] = T.groupby(["side", "dur_d"])["net_profit_loss_percent"].agg(["count", "mean"]).head(30)
    out["trades_side_by_entry_wd"] = T.groupby(["side", "ewd"])["net_profit_loss_percent"].agg(["count", "mean"])
    return out
