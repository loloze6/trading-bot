def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 10
    # Bar-level: book return per coin-bar, split by whether the forecast is > 0 at entry of the bar
    R = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            f = pd.DataFrame({"coin": c, "w": w, "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"]})
            f["nxt"] = cl.shift(-1) / cl - 1
            f["gain"] = f["alloc"] * f["nxt"]
            f["fwd"] = cl.shift(-H) / cl - 1
            f["ma100"] = cl / cl.rolling(100, min_periods=60).mean() - 1
            f["r30"] = cl / cl.shift(30) - 1
            f["fc_max10"] = f["fc"].rolling(10, min_periods=1).max()
            f["pos"] = np.arange(len(b))
            R.append(f)
    R = pd.concat(R, ignore_index=True).dropna(subset=["nxt"])
    R["fcpos"] = R["fc"] > 0
    R["recent_sig"] = R["fc_max10"] > 0
    out["gain_by_fc_state"] = R.groupby("fcpos").agg(n=("gain", "size"), mean_alloc=("alloc", "mean"),
                                                     share_alloc_pos=("alloc", lambda x: (x > 0).mean()),
                                                     mean_gain=("gain", "mean"), coin_mean=("nxt", "mean"),
                                                     gain_sd=("gain", "std"))
    R["state"] = np.where(R["ma100"] > 0, "above_ma100", "below_ma100")
    R.loc[R["ma100"].isna(), "state"] = "na"
    out["gain_by_trend_state"] = R.groupby(["state", "fcpos"]).agg(n=("gain", "size"), mean_alloc=("alloc", "mean"),
                                                                   mean_gain=("gain", "mean"), coin_mean=("nxt", "mean"),
                                                                   worst_gain_q05=("gain", lambda x: x.quantile(0.05)))
    # share of total loss days where forecast was 0
    R["loss"] = R["gain"] < 0
    out["loss_share"] = pd.Series({"share_of_negative_gain_sum_fc0": R.loc[~R.fcpos & R.loss, "gain"].sum() / R.loc[R.loss, "gain"].sum(),
                                   "share_bars_fc0": (~R.fcpos).mean(),
                                   "gain_sum_fc0": R.loc[~R.fcpos, "gain"].sum(), "gain_sum_fcpos": R.loc[R.fcpos, "gain"].sum()})
    # Grid: streak strength x trend, conditional alone check
    g = R[R.pos % H == 0].dropna(subset=["fwd"]).copy()
    drift = g.groupby("coin")["fwd"].mean()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    g["fcb"] = pd.cut(g["fc"], [-0.1, 0, 4, 21], labels=["0", "1day", "2+day"])
    def summ(x):
        return pd.Series({"n": len(x), "fwd": x["fwd"].mean(), "ex": x["ex"].mean(),
                          "t_ex": x["ex"].mean() / (x["ex"].std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "q10": x["fwd"].quantile(0.1)})
    gg = g.dropna(subset=["ma100"])
    out["grid_fcb_x_trend"] = gg.groupby(["state", "fcb"]).apply(summ)
    gr = g.dropna(subset=["r30"]).copy()
    gr["r30s"] = np.where(gr["r30"] > 0, "r30_up", "r30_down")
    out["grid_fcb_x_r30"] = gr.groupby(["r30s", "fcb"]).apply(summ)
    # slope of ex on fc among fc>0 within above-trend
    a = gg[(gg.state == "above_ma100") & (gg.fc > 0)]
    sl = np.polyfit(a["fc"], a["ex"], 1)[0]
    res = a["ex"] - np.polyval(np.polyfit(a["fc"], a["ex"], 1), a["fc"])
    se = np.sqrt((res**2).sum() / (len(a) - 2) / ((a["fc"] - a["fc"].mean())**2).sum())
    out["slope_above_trend_fcpos"] = pd.Series({"slope": sl, "t": sl / se, "n": len(a)})
    return out
