def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); v = df["volume"].astype(float)
            n = len(df)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n)})
            d["fwd"] = c.shift(-H) / c - 1
            d["r1"] = c.pct_change()
            d["r5p"] = c / c.shift(5) - 1
            d["r20p"] = c / c.shift(20) - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["volr"] = v / v.rolling(20).mean()
            hi = c.shift(1).rolling(20).max()
            d["dhi"] = c / hi - 1
            brk = (c > hi)
            d["brk"] = brk
            # failed breakout: a breakout 1..3 days ago and close now below that breakout's old high
            fail = pd.Series(False, index=df.index)
            depth = pd.Series(np.nan, index=df.index)
            for k in (1, 2, 3):
                b = brk.shift(k, fill_value=False).astype(bool)
                oh = hi.shift(k)
                f = b & (c < oh)
                depth = depth.where(~(f & depth.isna()), c / oh - 1)
                fail = fail | f
            d["fail"] = fail; d["fdepth"] = depth
            d["wd"] = pd.to_datetime(df["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(df["timestamp"]).dt.year
            d["fc"] = df["forecast"].astype(float)
            d["alloc"] = df["postRebalance_current_allocation"].astype(float)
            d["absr1"] = d["r1"].abs()
            d["absr1_rel"] = d["absr1"] / d["vol20"]
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    grid = A[A["pos"] % H == 0].dropna(subset=["fwd"])
    st = grid.groupby("coin")["fwd"].agg(["mean", "std"])
    A = A.join(st, on="coin")
    A["z"] = (A["fwd"] - A["mean"]) / A["std"]
    A["cell"] = A["pos"] // H
    G = A[(A["pos"] % H == 0)].dropna(subset=["fwd"])

    def summ(x):
        x = x.dropna()
        n = len(x)
        return pd.Series({"n": n, "mean_z": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    def cases(mask):
        s = A[mask & A["fwd"].notna()]
        s = s.sort_values("pos").groupby(["coin", "win", "cell"]).head(1)
        return s

    out = {}
    out["drift_sd"] = st
    # failed breakouts any volume, by volume ratio tercile
    fc = cases(A["fail"])
    out["fail_all"] = summ(fc["z"])
    fc = fc.copy()
    fc["vq"] = pd.qcut(fc["volr"], 3, labels=["low", "mid", "high"])
    out["fail_by_volr"] = fc.groupby("vq")["z"].apply(summ).unstack()
    fc["dq"] = pd.qcut(fc["fdepth"], 3, labels=["deep", "mid", "shallow"])
    out["fail_by_depth"] = fc.groupby("dq")["z"].apply(summ).unstack()
    bc = cases(A["brk"])
    out["breakout_all"] = summ(bc["z"])
    bc = bc.copy(); bc["vq"] = pd.qcut(bc["volr"], 3, labels=["low", "mid", "high"])
    out["breakout_by_volr"] = bc.groupby("vq")["z"].apply(summ).unstack()
    # grid quintiles
    for col in ["r5p", "r20p", "vol20", "volr", "dhi", "absr1_rel"]:
        g = G.dropna(subset=[col]).copy()
        g["q"] = g.groupby("coin")[col].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out["q_" + col] = g.groupby("q")["z"].apply(summ).unstack()
    # big down day / big up day
    g = G.dropna(subset=["r1", "vol20"]).copy()
    g["sig"] = g["r1"] / g["vol20"]
    g["sb"] = pd.cut(g["sig"], [-np.inf, -2, -1, 1, 2, np.inf])
    out["by_last_day_sigma"] = g.groupby("sb")["z"].apply(summ).unstack()
    out["by_weekday"] = G.groupby("wd")["z"].apply(summ).unstack()
    out["by_year"] = G.groupby("year")["z"].apply(summ).unstack()
    out["by_coin_failcases"] = fc.groupby("coin")["z"].apply(summ).unstack()
    # book: active share
    act = A[A["alloc"].abs() > 1e-6]
    out["active_bars"] = len(act)
    out["active_mean_alloc"] = act["alloc"].mean()
    return out
