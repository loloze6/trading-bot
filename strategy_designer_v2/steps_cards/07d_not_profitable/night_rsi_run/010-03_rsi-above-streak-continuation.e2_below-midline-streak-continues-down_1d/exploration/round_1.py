def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    comp = "debug_info.components.rsi_below_age.last_history_value"
    # book by window
    rows = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            br = d["book_return"].dropna(); cr = d["coin_return"].dropna()
            rows.append({"coin": coin, "w": w, "book_mean": br.mean(), "coin_mean": cr.mean(),
                         "book_sum": br.sum(), "coin_sum": cr.sum(), "n": len(br)})
    bw = pd.DataFrame(rows)
    out["by_window"] = bw.groupby("w")[["book_sum", "coin_sum"]].mean().round(4)
    out["by_coin"] = bw.groupby("coin")[["book_mean", "coin_mean"]].mean()
    # position gain by run-length bucket, and by past 30d return
    recs = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["fwd1"] = b["close"].shift(-1) / b["close"] - 1
            b["gain"] = b["postRebalance_current_allocation"] * b["fwd1"]
            b["run"] = -b[comp] if comp in b else np.nan
            b["ret30"] = b["close"] / b["close"].shift(30) - 1
            b["ret7p"] = b["close"] / b["close"].shift(7) - 1
            b["fwd7"] = b["close"].shift(-7) / b["close"] - 1
            # RSI recompute
            dlt = b["close"].diff()
            up = dlt.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
            dn = (-dlt.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
            b["rsi"] = 100 - 100 / (1 + up / dn)
            b["coin"] = coin; b["w"] = w
            b["pos"] = np.arange(len(b))
            recs.append(b[["coin", "w", "pos", "fwd1", "fwd7", "gain", "run", "ret30", "ret7p", "rsi",
                           "forecast", "postRebalance_current_allocation"]])
    B = pd.concat(recs)
    mean7 = B[B.pos % 7 == 0].groupby("coin")["fwd7"].mean()
    B["ex7"] = B["fwd7"] - B["coin"].map(mean7)
    act = B[B.forecast < 0].copy()
    act["runb"] = pd.cut(act["run"], [0, 3, 7, 14, 30, 61])
    out["gain_by_run"] = act.groupby("runb").agg(n=("gain", "size"), gain=("gain", "mean"),
                                                fwd1=("fwd1", "mean"), alloc=("postRebalance_current_allocation", "mean"))
    g = act[act.pos % 7 == 0]
    g["runb"] = pd.cut(g["run"], [0, 3, 7, 14, 30, 61])
    out["ex7_by_run_grid"] = g.groupby("runb")["ex7"].agg(["size", "mean", "std"])
    g["r30q"] = pd.qcut(g["ret30"], 4)
    out["ex7_by_ret30_grid"] = g.groupby("r30q")["ex7"].agg(["size", "mean", "std"])
    g["rsiq"] = pd.qcut(g["rsi"], 4)
    out["ex7_by_rsi_grid"] = g.groupby("rsiq")["ex7"].agg(["size", "mean", "std"])
    # all grid bars by rsi quintile (overall)
    G = B[(B.pos % 7 == 0)].dropna(subset=["ex7", "rsi"])
    G["rsiq"] = pd.qcut(G["rsi"], 5)
    out["ex7_by_rsi_all"] = G.groupby("rsiq")["ex7"].agg(["size", "mean", "std"])
    out["share_time_short"] = (B.forecast < 0).mean()
    out["gain_short_vs_flat"] = B.groupby(B.forecast < 0)["fwd1"].mean()
    # worst windows' gain split
    out["book_gain_by_year_like_window"] = act.groupby("w")["gain"].sum().round(3)
    return out
