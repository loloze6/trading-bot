def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 5
    rows = []
    daily = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); hi = df["high"].astype(float); lo = df["low"].astype(float)
            hh = hi.shift(1).rolling(20).max(); ll = lo.shift(1).rolling(20).min()
            rp = (c - ll) / (hh - ll)
            dhi = c / hh - 1; dlo = c / ll - 1
            r1 = c.pct_change()
            r5p = c / c.shift(5) - 1
            r20p = c / c.shift(20) - 1
            vol20 = r1.rolling(20).std()
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)), "day": ts.dt.floor("D"),
                              "year": ts.dt.year, "wd": ts.dt.weekday, "rp": rp, "dhi": dhi, "dlo": dlo,
                              "r1": r1, "r5p": r5p, "r20p": r20p, "vol20": vol20, "fwd": fwd, "fwd1": fwd1,
                              "alloc": df["postRebalance_current_allocation"].astype(float),
                              "fc": df["forecast"].astype(float)})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % H == 0].dropna(subset=["fwd"]).copy()
    drift = G.groupby("coin")["fwd"].mean(); sd = G.groupby("coin")["fwd"].std()
    G["u"] = G["fwd"] - G["coin"].map(drift)
    G["vol20r"] = G.groupby("coin")["vol20"].rank(pct=True)
    A["u1"] = A["fwd1"] - A["coin"].map(A.groupby("coin")["fwd1"].mean())

    def tab(df, key, col="u"):
        out = []
        for k, g in df.dropna(subset=[key, col]).groupby(key, observed=True):
            s = g.groupby("day")[col].sum()
            n = len(s)
            t = s.mean() / (s.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
            # proper: mean per case, t from day sums
            out.append({key: str(k), "n": len(g), "days": n, "mean_u%": 100 * g[col].mean(), "t_day": t})
        return pd.DataFrame(out)

    G["rp_bin"] = pd.cut(G["rp"], [-np.inf, 0, .2, .4, .6, .8, 1, np.inf])
    res = {}
    res["rangepos_5d"] = tab(G, "rp_bin")
    G["r1q"] = pd.qcut(G["r1"], 5, labels=False)
    res["prev1d_quintile_5d"] = tab(G, "r1q")
    G["r5q"] = pd.qcut(G["r5p"], 5, labels=False)
    res["prev5d_quintile_5d"] = tab(G, "r5q")
    G["r20q"] = pd.qcut(G["r20p"], 5, labels=False)
    res["prev20d_quintile_5d"] = tab(G, "r20q")
    G["volq"] = pd.cut(G["vol20r"], [0, 1/3, 2/3, 1])
    res["vol_tercile_5d"] = tab(G, "volq")
    lowbr = G[G["dlo"] < 0].copy()
    lowbr["q"] = pd.qcut(lowbr["dlo"], 3, labels=["deep", "mid", "shallow"])
    res["below_20d_low_5d"] = tab(lowbr, "q")
    hibr = G[G["dhi"] > 0].copy()
    hibr["q"] = pd.qcut(hibr["dhi"], 3, labels=["small", "mid", "big"])
    res["above_20d_high_5d"] = tab(hibr, "q")
    hibr["vq"] = pd.cut(hibr["vol20r"], [0, 1/3, 2/3, 1])
    res["above_high_by_vol"] = tab(hibr, "vq")
    res["weekday_1d"] = tab(A.dropna(subset=["u1"]), "wd", "u1")
    res["coin_drift5_sd5"] = pd.DataFrame({"drift%": 100 * drift, "sd%": 100 * sd})
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    T["dur_d"] = T["duration_minutes"] / 1440
    res["trades_by_year"] = T.groupby("year").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean()),
        dur=("dur_d", "mean"))
    T["fcq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    res["trades_by_entry_fc"] = T.groupby("fcq", observed=True).agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"))
    res["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"))
    return res
