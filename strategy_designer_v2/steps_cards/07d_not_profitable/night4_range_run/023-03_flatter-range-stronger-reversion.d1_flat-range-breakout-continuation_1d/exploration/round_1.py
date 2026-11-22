def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    grid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            pos = b["postRebalance_current_allocation"].astype(float)
            r1 = c.shift(-1) / c - 1
            gain = pos * r1
            turn = (pos - b["previous_allocation"].astype(float)).abs()
            v = b["postRebalance_total_value"].astype(float)
            br = v / v.shift(1) - 1
            # recompute flatness and position in range, and 90d trend
            H = c.rolling(31).max(); L = c.rolling(31).min()
            flat = 1 - (c - c.shift(30)).abs() / (H - L)
            ret30 = c / c.shift(30) - 1
            ret10 = c / c.shift(10) - 1
            vol = c.pct_change().rolling(30).std()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": pos, "gain": gain, "turn": turn, "br": br,
                               "r1": r1, "fc": b["forecast"].astype(float), "flat": flat,
                               "ret30": ret30, "ret10": ret10, "vol": vol,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
            idx = np.arange(0, len(c) - 5, 5)
            f5 = (c.shift(-5) / c - 1).iloc[idx]
            g = df.iloc[idx].copy(); g["f5"] = f5.values
            grid.append(g)
    A = pd.concat(rows); G = pd.concat(grid).dropna(subset=["f5"])
    drift = G.groupby("coin")["f5"].mean()
    G["u5"] = G["f5"] - G["coin"].map(drift)
    G["sgn"] = np.sign(G["fc"])
    G["dirmove"] = G["sgn"] * G["f5"]
    # side split
    A["side"] = np.where(A["pos"] > 0, "long", np.where(A["pos"] < 0, "short", "flat"))
    out["side_gain"] = A.groupby("side").agg(n=("gain", "size"), mean_gain=("gain", "mean"),
                                             sum_gain=("gain", "sum"), mean_abs_pos=("pos", lambda x: x.abs().mean()))
    out["mean_turnover_per_bar"] = float(A["turn"].mean())
    out["mean_gain_per_bar"] = float(A["gain"].mean())
    out["fee_per_bar_est"] = float(A["turn"].mean() * 0.0019 / 2)
    # forecast strength bins
    G["fbin"] = pd.cut(G["fc"].abs(), [-0.01, 2, 5, 10, 15, 20.1])
    out["by_absfc"] = G[G.sgn != 0].groupby("fbin").agg(n=("u5", "size"), dirmove=("dirmove", "mean"),
                                                         unusual=("u5", lambda x: np.nan))
    G["dir_u"] = G["sgn"] * G["u5"]
    out["by_absfc"]["unusual"] = G[G.sgn != 0].groupby("fbin")["dir_u"].mean()
    # by flatness
    G["flbin"] = pd.qcut(G["flat"], 4)
    out["by_flat"] = G[G.sgn != 0].groupby("flbin").agg(n=("dir_u", "size"), dir_u=("dir_u", "mean"),
                                                        t=("dir_u", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # by side x 30d trend sign agreement
    G["side"] = np.where(G.sgn > 0, "long", "short")
    G["trend"] = np.where(G["ret30"] > 0, "up30", "down30")
    out["by_side_trend"] = G[G.sgn != 0].groupby(["side", "trend"]).agg(n=("dir_u", "size"), dir_u=("dir_u", "mean"),
                         dirmove=("dirmove", "mean"), t=("dir_u", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # by vol quartile
    G["vbin"] = pd.qcut(G["vol"], 4)
    out["by_vol"] = G[G.sgn != 0].groupby("vbin").agg(n=("dir_u", "size"), dir_u=("dir_u", "mean"),
                                                      t=("dir_u", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["by_year"] = G[G.sgn != 0].groupby("year").agg(n=("dir_u", "size"), dir_u=("dir_u", "mean"))
    # book daily: mean across coins per (window, bar idx)
    A["k"] = A.groupby(["coin", "w"]).cumcount()
    D = A.groupby(["w", "k"]).agg(br=("br", "mean"), hr=("r1", "mean"))
    D = D.dropna()
    out["book_mean_std"] = pd.Series({"book_mean": D.br.mean(), "book_std": D.br.std(),
                                      "hold_mean": D.hr.mean(), "hold_std": D.hr.std()})
    # drawdown on chained book in window order
    wo = sorted(D.index.get_level_values(0).unique(), key=lambda s: int(s[1:]))
    D = D.loc[wo]
    eq = (1 + D.br).cumprod(); dd = eq / eq.cummax() - 1
    out["maxdd"] = float(dd.min())
    # windows with largest book losses
    wl = D.groupby(level=0).br.apply(lambda x: (1 + x).prod() - 1)
    wh = D.groupby(level=0).hr.apply(lambda x: (1 + x).prod() - 1)
    out["window_book_vs_hold"] = pd.DataFrame({"book": wl, "hold": wh}).loc[wo]
    return out
