def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # coin drift (5-bar non-overlapping) and daily mean
    drift5 = {}; dmean = {}
    for c in bars:
        r5 = []; rd = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 5, 5)
            r5 += list(cl[idx + 5] / cl[idx] - 1)
            rd += list(cl[1:] / cl[:-1] - 1)
        drift5[c] = np.mean(r5); dmean[c] = np.mean(rd)
    # book decomposition daily
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values
            pos = b["postRebalance_current_allocation"].fillna(0).values
            g = pos[:-1] * (cl[1:] / cl[:-1] - 1)
            mk = pos[:-1] * dmean[c]
            v = b["postRebalance_total_value"].values
            br = v[1:] / v[:-1] - 1
            recs.append(pd.DataFrame({"coin": c, "w": w, "gross": g, "market": mk, "book": br, "pos": pos[:-1],
                                      "yr": pd.to_datetime(b["timestamp"]).dt.year.values[1:]}))
    D = pd.concat(recs)
    D["fees"] = D["gross"] - D["book"]
    D["timing"] = D["gross"] - D["market"]
    out["decomp_mean_per_bar"] = D[["book", "gross", "market", "timing", "fees"]].mean().to_frame("mean")
    out["exposure_share_short"] = float((D["pos"] < 0).mean())
    out["mean_pos_when_short"] = float(D.loc[D.pos < 0, "pos"].mean())
    out["by_year"] = D.groupby("yr")[["book", "gross", "market", "timing", "fees"]].mean()
    # cases: bars by z-score bins
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"]
            r1 = cl.pct_change()
            vol = r1.rolling(20).std()
            z = r1 / vol
            r30 = cl / cl.shift(30) - 1
            f5 = cl.shift(-5) / cl - 1
            rv = vol / r1.rolling(60, min_periods=40).std()
            n = len(cl)
            grid = np.zeros(n, bool); grid[np.arange(0, n, 5)] = True
            df = pd.DataFrame({"z": z, "f5": f5, "r30": r30, "reg": b["regime"].values, "fc": b["forecast"].values,
                               "grid": grid, "vol": vol, "rv": rv, "coin": c, "w": w})
            rows.append(df)
    A = pd.concat(rows).dropna(subset=["z", "f5"])
    A["drift"] = A["coin"].map(drift5)
    A["tot_short"] = -A["f5"]; A["unus_short"] = -(A["f5"] - A["drift"])
    G = A[A.grid]
    fall = G[G.reg == "mean_reversion"]; rise = G[G.reg != "mean_reversion"]
    def tab(df, col):
        g = df.groupby(col)
        return pd.DataFrame({"n": g.size(), "tot_short": g["tot_short"].mean(), "unus_short": g["unus_short"].mean(),
                             "t_unus": g["unus_short"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))})
    bins = [-np.inf, 0, 0.5, 1, 1.5, 2, 3, np.inf]
    fall = fall.assign(zb=pd.cut(fall.z, bins)); rise = rise.assign(zb=pd.cut(rise.z, bins))
    out["falling_by_z"] = tab(fall, "zb")
    out["rising_by_z"] = tab(rise, "zb")
    up = fall[fall.z > 1]
    up = up.assign(r30b=pd.qcut(up.r30, 4), rvb=pd.qcut(up.rv, 3))
    out["falling_z>1_by_r30"] = tab(up, "r30b")
    out["falling_z>1_by_relvol"] = tab(up, "rvb")
    # trades
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    out["trades"] = pd.DataFrame({"n": [len(T)], "gross": [T.profit_loss_percent.mean()], "net": [T.net_profit_loss_percent.mean()],
                                  "win": [(T.net_profit_loss_percent > 0).mean()], "dur_days": [T.duration_minutes.mean() / 1440]})
    T["fcb"] = pd.cut(T.entry_forecast, [-21, -15, -10, -5, -2, 0])
    out["trades_by_entry_fc"] = T.groupby("fcb")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["mean", "count"])
    return out
