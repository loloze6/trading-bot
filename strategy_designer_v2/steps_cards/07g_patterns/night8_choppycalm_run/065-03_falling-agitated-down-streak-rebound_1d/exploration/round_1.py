def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            n3 = c.shift(-3) / c - 1
            down = (r < 0).astype(int)
            streak = down.groupby((down == 0).cumsum()).cumsum()
            up = (r > 0).astype(int)
            ustreak = up.groupby((up == 0).cumsum()).cumsum()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            vol20 = r.rolling(20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "fa": (b["regime"] == "unknown").astype(int),
                "r": r, "nxt": nxt, "n3": n3, "streak": streak, "ustreak": ustreak,
                "r5": r5, "r20": r20, "rng": rng, "clpos": clpos,
                "z1": r / vol20, "z5": r5 / (vol20 * np.sqrt(5)),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    cm = d.groupby("coin")["nxt"].mean()
    d["x"] = d["nxt"] - d["coin"].map(cm)
    def tab(g, col="x"):
        o = g[col].agg(["mean", "count", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        return o.drop(columns="std")
    out = {}
    d["sk"] = d["streak"].clip(upper=4)
    out["streak_by_regime"] = tab(d.groupby(["fa", "sk"]))
    d["usk"] = d["ustreak"].clip(upper=4)
    out["upstreak_by_regime"] = tab(d.groupby(["fa", "usk"]))
    for v in ["z1", "z5", "r20", "clpos", "rng"]:
        q = d.groupby("fa")[v].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        d["q_" + v] = q
        out[v + "_quint_by_regime"] = tab(d.groupby(["fa", "q_" + v]))
    out["weekday_by_regime"] = tab(d.groupby(["fa", "wd"]))
    # 3-day non-overlapping
    g3 = d[d["pos"] % 3 == 0].copy()
    cm3 = g3.groupby("coin")["n3"].mean()
    g3["x3"] = g3["n3"] - g3["coin"].map(cm3)
    out["z5_quint_3d_nonoverlap"] = tab(g3.groupby(["fa", "q_z5"]), "x3")
    # within FA: z5 vs z1 joint regression
    fa = d[(d["fa"] == 1)].dropna(subset=["x", "z1", "z5"])
    X = np.column_stack([np.ones(len(fa)), fa["z1"], fa["z5"]])
    beta, *_ = np.linalg.lstsq(X, fa["x"].values, rcond=None)
    res = fa["x"].values - X @ beta
    out["fa_reg_x_on_z1_z5_beta"] = pd.Series(beta, index=["c", "z1", "z5"])
    out["fa_rows"] = len(fa)
    # book days: largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    dd = pd.concat(dd)
    bk = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0)["book_return"].agg(["mean", "std", "count", "sum"])
    out["held_by_year"] = tab(d[d["alloc"] > 0].groupby("year"))
    return out
