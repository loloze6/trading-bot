def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["r1"] = r1
            d["r7"] = c / c.shift(7) - 1
            d["r30"] = c / c.shift(30) - 1
            d["er"] = (c - c.shift(30)).abs() / r1.abs().mul(c.shift(1)).rolling(30).sum().replace(0, np.nan)
            # use abs price diffs for ER
            d["er"] = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            d["vol30"] = r1.rolling(30).std()
            d["z7"] = d["r7"] / (d["vol30"] * np.sqrt(7))
            d["z1"] = r1 / d["vol30"].shift(1)
            d["f1"] = c.shift(-1) / c - 1
            d["f7"] = c.shift(-7) / c - 1
            d["fc"] = b["forecast"].astype(float)
            d["regime"] = b["regime"]
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            d["volrank"] = d["vol30"].rolling(180, min_periods=60).rank(pct=True)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["f1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(mu1)
    # 7-day grid
    G7 = D[D["pos"] % 7 == 0].dropna(subset=["f7", "z7", "er"]).copy()
    mu7 = G7.groupby("coin")["f7"].mean()
    G7["x7"] = G7["f7"] - G7["coin"].map(mu7)
    G7["sx7"] = np.sign(G7["z7"]) * G7["x7"]
    G7["erb"] = pd.qcut(G7["er"], 3, labels=["lowER", "midER", "highER"])
    G7["zb"] = pd.qcut(G7["z7"].abs(), 3, labels=["smallz", "midz", "bigz"])
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out["7d_signed_next7_by_ER_x_absz"] = G7.groupby(["erb", "zb"])["sx7"].apply(tt).unstack()
    # slope next7 on z7 per ER bucket
    sl = []
    for k, g in G7.groupby("erb"):
        res = stats.linregress(g["z7"], g["x7"]); sl.append(pd.Series({"n": len(g), "slope": res.slope, "t": res.slope / res.stderr}, name=k))
    out["7d_slope_next7_on_z7_by_ER"] = pd.DataFrame(sl)
    # 1-day: next day after large daily z1, all bars, by vol rank
    A = D.dropna(subset=["x1", "z1"]).copy()
    A["sx1"] = np.sign(A["z1"]) * A["x1"]
    A["z1b"] = pd.qcut(A["z1"].abs(), 4, labels=["q1", "q2", "q3", "q4"])
    A["vb"] = pd.cut(A["volrank"], [0, 1/3, 2/3, 1.0], labels=["lowvol", "midvol", "highvol"])
    out["1d_signed_next_by_absz1_x_vol"] = A.groupby(["vb", "z1b"])["sx1"].apply(tt).unstack()
    # up vs down large moves
    A["dir"] = np.where(A["z1"] > 0, "up", "down")
    out["1d_next_after_q4_by_dir"] = A[A["z1b"] == "q4"].groupby("dir")["x1"].apply(tt).unstack()
    # weekday
    out["weekday_x1"] = A.groupby("wd")["x1"].apply(tt).unstack()
    # chop-regime forecast quintiles
    C = D[(D["regime"] == "chop") & D["x1"].notna()].copy()
    C["sx"] = np.sign(C["fc"]) * C["x1"]
    C["fq"] = pd.qcut(C["fc"].rank(method="first"), 5, labels=False)
    out["chop_fc_quintile_x1"] = C.groupby("fq").agg(fc=("fc", "mean"), n=("x1", "size"), x1=("x1", "mean"), sx=("sx", "mean"))
    out["chop_by_side"] = C.groupby(np.sign(C["fc"]))["x1"].apply(tt).unstack()
    out["chop_by_year_sx"] = C.groupby("year")["sx"].apply(tt).unstack()
    # non-chop bars: does z7 predict next day?
    N = D[(D["regime"] != "chop")].dropna(subset=["x1", "z7"])
    N = N.assign(sx=np.sign(N["z7"]) * N["x1"])
    N["erb"] = pd.qcut(N["er"], 3, labels=["lowER", "midER", "highER"])
    out["nonchop_signed_x1_by_ER"] = N.groupby("erb")["sx"].apply(tt).unstack()
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["db"] = pd.cut(T["days"], [0, 1.5, 3.5, 7.5, 1e9], labels=["1d", "2-3d", "4-7d", "8d+"])
    out["trades_by_duration"] = T.groupby(["db", "side"]).agg(n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean")).reset_index()
    # book days: largest gains/losses
    B = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            B.append(dd.assign(coin=coin, win=w))
    B = pd.concat(B)
    out["book_return_by_window_mean"] = B.groupby("win")[["book_return", "coin_return"]].mean()
    return out
