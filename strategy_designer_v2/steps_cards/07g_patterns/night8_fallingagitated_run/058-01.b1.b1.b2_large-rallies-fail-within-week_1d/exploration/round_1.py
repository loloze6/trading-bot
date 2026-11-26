def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ret3 = c / c.shift(3) - 1
            ret10 = c / c.shift(10) - 1
            for h in (1, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["s3"] = ret3 / (sd30 * np.sqrt(3))
            df["s10"] = ret10 / (sd30 * np.sqrt(10))
            df["s1"] = r1 / sd30
            df["sd30"] = sd30
            rng = (df["high"] - df["low"]) / c
            df["clpos"] = (c - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            df["rng_s"] = rng / sd30
            df["coin"] = coin; df["win"] = w
            df["pos"] = np.arange(len(df))
            df["wd"] = pd.to_datetime(df["timestamp"]).dt.weekday
            df["yr"] = pd.to_datetime(df["timestamp"]).dt.year
            df["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")
            df["fa"] = (df["regime"] == "unknown").astype(int)
            rows.append(df[["coin","win","pos","f1","f5","s1","s3","s10","sd30","clpos","rng_s","wd","yr","day","fa","forecast","postRebalance_current_allocation"]])
    A = pd.concat(rows, ignore_index=True)
    drift5 = A[A.pos % 5 == 0].groupby("coin")["f5"].mean()
    drift1 = A.groupby("coin")["f1"].mean()
    A["x5"] = A["f5"] - A["coin"].map(drift5)
    A["x1"] = A["f1"] - A["coin"].map(drift1)
    G5 = A[(A.pos % 5 == 0)].dropna(subset=["x5"])
    out = {}
    out["share_fa_bars"] = float(A.fa.mean())
    def tab(df, col, ycol, q=5):
        d = df.dropna(subset=[col, ycol]).copy()
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        g = d.groupby("b")[ycol].agg(["count","mean","std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["xmean"] = d.groupby("b")[col].mean()
        return g.round(4)
    for reg in (1, 0):
        sub = G5[G5.fa == reg]
        out[f"x5_by_s3_fa{reg}"] = tab(sub, "s3", "x5")
        out[f"x5_by_s10_fa{reg}"] = tab(sub, "s10", "x5")
        out[f"x5_by_rng_fa{reg}"] = tab(sub, "rng_s", "x5")
        out[f"x5_by_clpos_fa{reg}"] = tab(sub, "clpos", "x5")
    G1 = A.dropna(subset=["x1"])
    out["x1_by_s1_fa1"] = tab(G1[G1.fa == 1], "s1", "x1")
    out["x1_by_s1_fa0"] = tab(G1[G1.fa == 0], "s1", "x1")
    wd = G1.groupby(["fa","wd"])["x1"].agg(["count","mean","std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["x1_weekday"] = wd.round(4)
    # book: daily returns
    dr = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dr.append(d)
    D = pd.concat(dr)
    bk = D.groupby("day")["book_return"].mean().dropna()
    out["book_mean_std_n"] = pd.Series({"mean": bk.mean(), "std": bk.std(), "n": len(bk)})
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): t = t.copy(); t["coin"] = coin; t["win"] = w; tr.append(t)
    T = pd.concat(tr)
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"]).round(3)
    T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades_by_year"] = T.groupby("yr")["net_profit_loss_percent"].agg(["count","mean","median"]).round(3)
    T["fb"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_entry_forecast_q"] = T.groupby("fb").agg(n=("net_profit_loss_percent","count"), pl=("net_profit_loss_percent","mean"), fc=("entry_forecast","mean"), dur=("dur_d","mean")).round(3)
    return out
