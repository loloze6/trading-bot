def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            n = len(df)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n)})
            d["fwd"] = c.shift(-H) / c - 1
            d["r1"] = c.pct_change()
            d["vol20"] = d["r1"].rolling(20).std()
            d["sig"] = d["r1"] / d["vol20"]
            hi = c.shift(1).rolling(20).max()
            lo = c.shift(1).rolling(20).min()
            d["dhi"] = c / hi - 1
            d["brk"] = c > hi
            d["brk_sig"] = (c / hi - 1) / d["vol20"]
            d["newbrk"] = d["brk"] & ~d["brk"].shift(1, fill_value=False).astype(bool)
            d["rng_pos"] = (c - lo) / (hi - lo)
            d["volr"] = v / v.rolling(20).mean()
            d["r20p"] = c / c.shift(20) - 1
            d["year"] = pd.to_datetime(df["timestamp"]).dt.year
            d["wd"] = pd.to_datetime(df["timestamp"]).dt.weekday
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G0 = A[A["pos"] % H == 0].dropna(subset=["fwd"])
    st = G0.groupby("coin")["fwd"].agg(["mean", "std"])
    A = A.join(st, on="coin")
    A["z"] = (A["fwd"] - A["mean"]) / A["std"]
    A["um"] = A["fwd"] - A["mean"]
    A["cell"] = A["pos"] // H
    G = A[A["pos"] % H == 0].dropna(subset=["fwd"])

    def summ(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    def cases(mask):
        s = A[mask & A["fwd"].notna()].sort_values("pos")
        return s.groupby(["coin", "win", "cell"]).head(1).copy()

    out = {}
    bc = cases(A["brk"])
    out["brk_um_pct"] = summ(bc["um"] * 100)
    out["brk_total_pct"] = summ(bc["fwd"] * 100)
    out["brk_by_coin"] = bc.groupby("coin")["z"].apply(summ).unstack()
    out["brk_by_year"] = bc.groupby("year")["z"].apply(summ).unstack()
    bc["bq"] = pd.qcut(bc["brk_sig"], 3, labels=["small", "mid", "large"])
    out["brk_by_margin_sigma"] = bc.groupby("bq")["z"].apply(summ).unstack()
    out["brk_margin_spearman"] = stats.spearmanr(bc["brk_sig"], bc["z"], nan_policy="omit").correlation
    nb = cases(A["newbrk"])
    out["newbrk"] = summ(nb["z"])
    # grid: graded by position in 20-day range
    g = G.dropna(subset=["rng_pos"]).copy()
    g["rq"] = pd.cut(g["rng_pos"], [-np.inf, 0.2, 0.4, 0.6, 0.8, 1.0, np.inf])
    out["grid_by_range_pos"] = g.groupby("rq")["z"].apply(summ).unstack()
    out["grid_spearman_rngpos"] = stats.spearmanr(g["rng_pos"], g["z"]).correlation
    g = G.dropna(subset=["sig"]).copy()
    out["grid_spearman_sig"] = stats.spearmanr(g["sig"], g["z"]).correlation
    g["up"] = g["sig"].clip(lower=0)
    out["sig_up_spearman_pos"] = stats.spearmanr(g.loc[g.sig > 0, "sig"], g.loc[g.sig > 0, "z"]).correlation
    out["n_up"] = int((g.sig > 0).sum())
    # up-day by year half split
    g["half"] = np.where(g["year"] <= 2021, "2018-21", "2022-25")
    g["sb"] = pd.cut(g["sig"], [-np.inf, 0, 1, np.inf])
    out["sig_by_half"] = g.groupby(["half", "sb"])["z"].apply(summ).unstack()
    # weekday by half
    G2 = G.copy(); G2["half"] = np.where(G2["year"] <= 2021, "a", "b")
    out["wd_by_half"] = G2.groupby(["wd", "half"])["z"].mean().unstack()
    # book: days around largest book gains / losses
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; dd.append(x)
    D = pd.concat(dd)
    D = D[D["book_return"].abs() > 0]
    out["book_active_days"] = len(D)
    out["book_mean_active"] = D["book_return"].mean()
    out["book_coin_corr_active"] = D[["book_return", "coin_return"]].corr().iloc[0, 1]
    top = D["book_return"].quantile([0.05, 0.95])
    out["book_tail_q"] = top
    return out
