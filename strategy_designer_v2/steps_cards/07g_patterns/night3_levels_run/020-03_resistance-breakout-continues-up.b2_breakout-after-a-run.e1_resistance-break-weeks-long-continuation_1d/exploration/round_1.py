def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rc = "debug_info.components.res_break.last_history_value"
    out = {}
    H = 20
    rows = []
    for coin, wins in bars.items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            f = c.shift(-H) / c - 1
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": np.arange(len(b)),
                "f20": f, "f5": f5, "f1": f1,
                "r1": c.pct_change(),
                "r20": c / c.shift(20) - 1,
                "r90": c / c.shift(90) - 1,
                "vol20": lr.rolling(20).std(),
                "near90": c / c.rolling(90, min_periods=60).max() - 1,
                "low90": c / c.rolling(90, min_periods=60).min() - 1,
                "raw": b[rc].astype(float) if rc in b else np.nan,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            recs.append(df)
        d = pd.concat(recs)
        g = d[d["pos"] % H == 0].dropna(subset=["f20"])
        drift = g["f20"].mean(); sd = g["f20"].std()
        d["drift"] = drift; d["usd"] = sd
        d["ex20"] = d["f20"] - drift
        d["str20"] = d["ex20"] / sd
        rows.append(d)
    D = pd.concat(rows)
    G = D[D["pos"] % H == 0].dropna(subset=["ex20"])

    def tab(df, col, q=5, val="str20"):
        x = df.dropna(subset=[col, val]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = x.groupby("q")[val].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["ex20_mean"] = x.groupby("q")["ex20"].mean()
        return t.drop(columns="std")

    out["grid_by_r20_quint"] = tab(G, "r20")
    out["grid_by_r90_quint"] = tab(G, "r90")
    out["grid_by_vol20_quint"] = tab(G, "vol20")
    out["grid_by_near90high_quint"] = tab(G, "near90")
    out["grid_by_above90low_quint"] = tab(G, "low90")
    # rank correlations per coin, grid
    cor = []
    for coin, x in G.groupby("coin"):
        r = {"coin": coin}
        for col in ["r20", "r90", "vol20", "near90", "low90"]:
            y = x.dropna(subset=[col])
            r[col] = stats.spearmanr(y[col], y["ex20"])[0]
        r["n"] = len(x)
        cor.append(r)
    out["grid_spearman_by_coin"] = pd.DataFrame(cor)
    # breakout bars: raw>0
    B = D[(D["raw"] > 0)].dropna(subset=["ex20"]).copy()
    B["g"] = B.groupby(["coin", "win"])["pos"].transform(lambda p: p // H)
    Bc = B.groupby(["coin", "win", "g"]).first().reset_index()
    out["breakout_cases_by_raw_quint"] = tab(Bc, "raw", 4)
    out["breakout_cases_by_r20_quint"] = tab(Bc, "r20", 4)
    out["breakout_cases_by_vol_quint"] = tab(Bc, "vol20", 4)
    # daily returns after large moves
    E = D.dropna(subset=["r1", "f1", "f5"]).copy()
    E["z"] = E["r1"] / E.groupby("coin")["vol20"].shift(0)
    E["f5ex"] = E["f5"] - E.groupby("coin")["f5"].transform("mean")
    E["f1ex"] = E["f1"] - E.groupby("coin")["f1"].transform("mean")
    E5 = E[E["pos"] % 5 == 0]
    zq = E5.dropna(subset=["z"]).copy()
    zq["q"] = pd.qcut(zq["z"], 5, labels=False)
    t = zq.groupby("q")["f5ex"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["f5ex_by_todays_move_z_quint(5d grid)"] = t.drop(columns="std")
    t = E.groupby("wd")["f1ex"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["next_day_excess_by_weekday"] = t.drop(columns="std")
    # book daily returns: biggest losses context
    dd = []
    for coin, wins in days.items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd).dropna(subset=["book_return"])
    out["book_by_window"] = DD.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    out["book_by_coin"] = DD.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), sd=("book_return", "std"))
    out["share_days_invested"] = float((D["alloc"].abs() > 0.01).mean())
    return out
