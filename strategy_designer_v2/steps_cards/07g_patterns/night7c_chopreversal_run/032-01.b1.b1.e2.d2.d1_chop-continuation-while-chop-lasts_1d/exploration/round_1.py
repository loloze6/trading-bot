def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            p7 = c / c.shift(7) - 1
            p30 = c / c.shift(30) - 1
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            sd30 = r1.rolling(30).std()
            sc = p7 / (sd30 * np.sqrt(7))
            f7 = c.shift(-7) / c - 1
            f1 = c.shift(-1) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r1": r1, "p7": p7, "p30": p30,
                               "er": er, "sd30": sd30, "sc": sc, "f7": f7, "f1": f1,
                               "fc": b["forecast"].astype(float), "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                               "yr": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 7 == 0)].dropna(subset=["f7"]).copy()
    G["ex"] = G["f7"] - G.groupby("coin")["f7"].transform("mean")
    G = G.dropna(subset=["sc", "er"])
    G["vrel"] = G["sd30"] / G.groupby("coin")["sd30"].transform("median")
    G["agree"] = np.sign(G["p7"]) == np.sign(G["p30"])
    G["erb"] = pd.cut(G["er"], [0, 0.15, 0.3, 0.45, 1.01])
    G["vb"] = pd.cut(G["vrel"], [0, 0.75, 1.0, 1.3, 10])

    def slope(g):
        if len(g) < 15: return pd.Series({"n": len(g)})
        s = stats.linregress(g["sc"], g["ex"])
        sg = (np.sign(g["sc"]) * g["ex"])
        return pd.Series({"n": len(g), "slope": s.slope, "t_slope": s.slope / s.stderr,
                          "signed_ex_mean": sg.mean(), "t_signed": sg.mean() / (sg.std() / np.sqrt(len(g)))})
    out = {}
    out["by_er_agree"] = G.groupby(["erb", "agree"], observed=True).apply(slope)
    out["by_vol_agree"] = G.groupby(["vb", "agree"], observed=True).apply(slope)
    out["by_coin_all"] = G.groupby("coin").apply(slope)
    out["by_year_all"] = G.groupby("yr").apply(slope)
    # 30-day momentum alone
    G["sc30"] = G["p30"] / (G["sd30"] * np.sqrt(30))
    def s30(g):
        s = stats.linregress(g["sc30"], g["ex"]); return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out["p30_scaled_by_er"] = G.groupby("erb", observed=True).apply(s30)
    # forecast quintiles among active
    act = G[G["fc"] != 0].copy()
    act["q"] = pd.qcut(act["fc"].abs(), 5, labels=False, duplicates="drop")
    act["sx"] = np.sign(act["fc"]) * act["ex"]
    out["fc_quintile"] = act.groupby("q")["sx"].agg(["count", "mean", "std"])
    out["fc_side"] = act.groupby(np.sign(act["fc"]))["sx"].agg(["count", "mean", "std"])
    # after large daily moves (all bars, 1-day forward, next-day reversal)
    A["z1"] = A["r1"] / A["sd30"].shift(1)
    A["zb"] = pd.cut(A["z1"], [-50, -2, -1, 1, 2, 50])
    out["next_day_after_z1"] = A.dropna(subset=["f1", "zb"]).groupby("zb", observed=True)["f1"].agg(["count", "mean", "std"])
    out["weekday_r1"] = A.dropna(subset=["f1"]).groupby("wd")["f1"].agg(["count", "mean", "std"])
    # book: daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), yr=("yr", "first")).dropna()
    out["book_by_year"] = bk.groupby("yr")[["br", "cr"]].agg(["mean", "std", "count"])
    out["book_by_window"] = bk.groupby(level=0)[["br", "cr"]].mean()
    return out
