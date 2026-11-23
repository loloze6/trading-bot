def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day", "book_return", "coin_return"]].copy()
            t["w"] = w; t["coin"] = c
            rows.append(t)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index().sort_values(["wn", "day"])
    val = (1 + B["book_return"]).cumprod()
    dd = val / val.cummax() - 1
    B["dd"] = dd.values
    B["val"] = val.values
    out["max_dd"] = float(dd.min())
    # drawdown by window: book and hold return per window, worst dd within window
    g = B.groupby("wn")
    W = pd.DataFrame({
        "book_ret": g["book_return"].apply(lambda x: (1 + x).prod() - 1),
        "hold_ret": g["coin_return"].apply(lambda x: (1 + x).prod() - 1),
        "book_mindd_in_w": g["book_return"].apply(lambda x: ((1 + x).cumprod() / (1 + x).cumprod().cummax() - 1).min()),
        "days": g.size()})
    out["by_window"] = W.round(4)
    # bars: allocation and forecast
    br = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["coin"] = c; b["w"] = w
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["ret60"] = b["close"] / b["close"].shift(60) - 1
            b["fwd10"] = b["close"].shift(-10) / b["close"] - 1
            b["pos"] = np.arange(len(b))
            br.append(b)
    A = pd.concat(br, ignore_index=True)
    al = A["postRebalance_current_allocation"]
    fc = A["forecast"]
    out["alloc_forecast_stats"] = pd.Series({
        "mean_alloc": al.mean(), "share_alloc_gt0.05": (al > 0.05).mean(),
        "share_alloc_gt0.5": (al > 0.5).mean(), "mean_fc": fc.mean(),
        "share_fc_ge10": (fc >= 10).mean(), "share_fc_lt1": (fc < 1).mean(),
        "share_fc_0": (fc == 0).mean()})
    A["fcb"] = pd.cut(fc, [-0.01, 0.5, 2, 5, 10, 20.01])
    A["gain"] = al * A["r1"]
    out["alloc_by_fc_bucket"] = A.groupby("fcb", observed=True).agg(
        n=("r1", "size"), mean_alloc=("postRebalance_current_allocation", "mean"),
        mean_r1=("r1", "mean"), mean_gain=("gain", "mean"))
    # grid analysis
    drift = A.groupby("coin").apply(lambda x: x.loc[x["pos"] % 10 == 0, "fwd10"].mean())
    G = A[(A["pos"] % 10 == 0)].dropna(subset=["fwd10", "ret60"]).copy()
    G["ex"] = G["fwd10"] - G["coin"].map(drift)
    G["sig"] = np.where(G["forecast"] >= 10, "fc>=10", np.where(G["forecast"] >= 2, "fc2-10", "fc<2"))
    G["trend60"] = np.where(G["ret60"] > 0, "up60", "down60")
    G["trend20"] = np.where(G["ret20"] > 0, "up20", "down20")
    def summ(x):
        return pd.Series({"n": len(x), "mean_ex": x["ex"].mean(), "mean_tot": x["fwd10"].mean(),
                          "t": x["ex"].mean() / (x["ex"].std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["grid_sig_x_trend60"] = G.groupby(["sig", "trend60"]).apply(summ).round(4)
    out["grid_sig_x_trend20"] = G.groupby(["sig", "trend20"]).apply(summ).round(4)
    # daily gain by trend state (book attribution)
    A["trend60"] = np.where(A["ret60"] > 0, "up60", np.where(A["ret60"].isna(), "na", "down60"))
    out["gain_by_trend60"] = A.groupby("trend60").agg(n=("gain", "size"), mean_alloc=("postRebalance_current_allocation", "mean"),
                                                      mean_gain=("gain", "mean"), sum_gain=("gain", "sum"), mean_r1=("r1", "mean"))
    return out
