def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            pos = b["postRebalance_current_allocation"]
            nxt = c.shift(-1) / c - 1
            ret30 = c / c.shift(30) - 1
            lhv = b.get("debug_info.components.hpm.last_history_value")
            W = lhv / ret30 if lhv is not None else np.nan
            fwd30 = c.shift(-30) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "pos": pos, "nxt": nxt,
                               "gain": pos * nxt, "ret30": ret30, "W": W, "fwd30": fwd30,
                               "fc": b["forecast"], "vol": b["volume"],
                               "ret90": c / c.shift(90) - 1})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["year"] = None
    coin_mean = A.groupby("coin")["nxt"].mean()
    A["cm"] = A["coin"].map(coin_mean)
    A["side"] = np.sign(A["pos"]).map({1: "long", -1: "short", 0: "flat"})
    g = A.dropna(subset=["gain"])
    out["by_side"] = g.groupby("side").agg(n=("gain", "size"), mean_gain=("gain", "mean"), sum_gain=("gain", "sum"),
                                          mean_nxt=("nxt", "mean"), mean_abs_pos=("pos", lambda x: x.abs().mean()))
    out["by_coin_side"] = g.groupby(["coin", "side"])["gain"].agg(["size", "mean", "sum"]).unstack()
    # market part vs timing
    g2 = g.assign(mkt=g["pos"] * g["cm"])
    out["market_vs_timing"] = pd.Series({"mean_gain": g2["gain"].mean(), "market_part": g2["mkt"].mean(),
                                         "timing": g2["gain"].mean() - g2["mkt"].mean()})
    # by proximity W quintile
    gw = g.dropna(subset=["W"]).copy()
    gw = gw[np.isfinite(gw["W"])]
    gw["Wq"] = pd.qcut(gw["W"], 5, labels=False, duplicates="drop")
    out["by_W_q"] = gw.groupby(["Wq", "side"]).agg(n=("gain", "size"), mean_gain=("gain", "mean"),
                                                  mean_nxt=("nxt", "mean"), Wmean=("W", "mean")).unstack()
    # by ret30 quintile
    gr = g.dropna(subset=["ret30"]).copy()
    gr["rq"] = pd.qcut(gr["ret30"], 5, labels=False)
    out["by_ret30_q"] = gr.groupby("rq").agg(n=("gain", "size"), mean_gain=("gain", "mean"),
                                            mean_nxt=("nxt", "mean"), mean_pos=("pos", "mean"), r=("ret30", "mean"))
    # forward 30 non-overlapping by ret30 sign x W half
    grid = A[(A["i"] % 30 == 0)].dropna(subset=["fwd30", "ret30", "W"]).copy()
    grid = grid[np.isfinite(grid["W"])]
    grid["near"] = grid["W"] > grid["W"].median()
    grid["up"] = grid["ret30"] > 0
    out["grid_fwd30"] = grid.groupby(["near", "up"])["fwd30"].agg(["size", "mean", "std"])
    # book daily: mean across coins per window/day
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["w"] = w; dd["coin"] = coin
            dl.append(dd)
    D = pd.concat(dl)
    D["wn"] = D["w"].str[1:].astype(int)
    bk = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    bk = bk.dropna()
    eq = (1 + bk["book_return"]).cumprod()
    dd_ = eq / eq.cummax() - 1
    bk["dd"] = dd_.values
    out["book_stats"] = pd.Series({"mean": bk["book_return"].mean(), "hold_mean": bk["coin_return"].mean(),
                                   "maxdd": dd_.min(), "sharpe": bk["book_return"].mean() / bk["book_return"].std() * np.sqrt(365)})
    out["by_window"] = bk.groupby("wn").agg(book=("book_return", "sum"), hold=("coin_return", "sum"),
                                           mindd=("dd", "min"), n=("book_return", "size"))
    # identify deepest fall period: peak to trough
    trough = int(np.argmin(dd_.values)); peak = int(np.argmax(eq.values[:trough + 1]))
    seg = bk.iloc[peak:trough + 1]
    out["deep_fall_windows"] = seg.groupby("wn").agg(book=("book_return", "sum"), hold=("coin_return", "sum"), n=("book_return", "size"))
    # trade count / fees
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
                                          net=("net_profit_loss_percent", "mean"), comm=("total_commission", "sum"),
                                          dur_days=("duration_minutes", lambda x: x.mean() / 1440))
    return out
