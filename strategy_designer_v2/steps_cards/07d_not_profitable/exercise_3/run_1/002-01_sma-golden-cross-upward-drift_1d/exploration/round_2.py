import pandas as pd, numpy as np

def explore(data):
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]
            raw = b["debug_info.components.sma_cross.last_history_value"]
            b["r20"] = cl / cl.shift(20) - 1
            b["ds"] = raw - raw.shift(10)
            b["dd60"] = cl / cl.rolling(60).max() - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["nxt"] = cl.shift(-1) / cl - 1
            b["gain"] = b["pos"] * b["nxt"]
            b["coin"] = c; b["wn"] = int(w[1:])
            rows.append(b[["coin", "wn", "forecast", "r20", "ds", "dd60", "pos", "nxt", "gain"]])
    X = pd.concat(rows).dropna()
    on = X[X.forecast > 0].copy()
    tot = on.gain.sum()
    def summ(g):
        return pd.Series({"n": len(g), "gain_mean": g.gain.mean(), "share_of_total_gain": g.gain.sum() / tot,
                          "nxt_mean": g.nxt.mean(), "t": g.nxt.mean() / g.nxt.std() * np.sqrt(len(g)),
                          "worst_day_share": (g.nxt < -0.08).mean()})
    on["r20q"] = pd.qcut(on.r20, 4, labels=False)
    out["on_by_r20q_daily"] = on.groupby("r20q").apply(summ)
    on["dsq"] = pd.qcut(on.ds, 4, labels=False)
    out["on_by_dsq_daily"] = on.groupby("dsq").apply(summ)
    on["ddq"] = pd.qcut(on.dd60, 4, labels=False, duplicates="drop")
    out["on_by_dd60q_daily"] = on.groupby("ddq").apply(summ)
    on["state"] = np.where(on.r20 < 0, "r20neg", "r20pos") + "_" + np.where(on.ds < 0, "dsneg", "dspos")
    out["on_by_state"] = on.groupby("state").apply(summ)
    # deepest falls: bad windows, state composition of invested days
    bad = on[on.wn.isin([12, 13, 16, 18])]
    out["bad_windows_state"] = bad.groupby("state").apply(summ)
    out["corr_r20_dd60"] = on[["r20", "dd60", "ds"]].corr()
    return out
