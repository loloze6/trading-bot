def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    out = {}
    # drift per coin (2-bar and 1-bar, non-overlapping, all windows)
    drift2 = {}; drift1 = {}
    for c in bars:
        r2 = []; r1s = []
        for w, b in bars[c].items():
            cl = b["close"].values
            r2 += list(cl[2::2] / cl[:-2:2][:len(cl[2::2])] - 1)
            r1s += list(cl[1:] / cl[:-1] - 1)
        drift2[c] = np.mean(r2); drift1[c] = np.mean(r1s)
    # all candidate bounce bars on 2-bar grid: r90<0, r30<0, z>0.5
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True); cl = pd.Series(b["close"].values); n = len(cl)
            r1 = cl.pct_change(); z = r1 / r1.rolling(20).std()
            r90 = cl.pct_change(90); r30 = cl.pct_change(30); r7 = cl.pct_change(7)
            r7x = cl.shift(1) / cl.shift(8) - 1  # 7-day return before the bounce day
            for i in range(0, n - 2, 2):
                if r90[i] < 0 and r30[i] < 0 and z[i] > 0.5:
                    rows.append({"coin": c, "z": z[i], "r7": r7[i], "r7x": r7x[i], "r30": r30[i],
                                 "s1": -(cl[i+1]/cl[i]-1) + drift1[c],
                                 "s2": -(cl[i+2]/cl[i]-1) + drift2[c],
                                 "s2tot": -(cl[i+2]/cl[i]-1)})
    G = pd.DataFrame(rows).dropna()
    out["grid_cases"] = len(G)
    def tab(col, q=4):
        G["q"] = pd.qcut(G[col], q, duplicates="drop")
        g = G.groupby("q", observed=True)
        return pd.DataFrame({"n": g.size(), "s1": g.s1.mean(), "s2": g.s2.mean(), "s2tot": g.s2tot.mean(),
                             "t_s2": g.s2.apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x))))}).round(4)
    out["grid_by_r7x_before_bounce"] = tab("r7x")
    out["grid_by_r7"] = tab("r7")
    out["grid_by_r30"] = tab("r30")
    out["grid_by_z"] = tab("z")
    # within the most negative half of r7x, grading by z
    H = G[G.r7x < G.r7x.median()].copy()
    H["q"] = pd.qcut(H["z"], 3)
    out["deepweek_by_z"] = H.groupby("q", observed=True).agg(n=("s2", "size"), s2=("s2", "mean"), s2tot=("s2tot", "mean")).round(4)
    out["corr_s2_r7x_spearman"] = float(stats.spearmanr(G.r7x, G.s2).correlation)
    # trades: entry r7 vs duration and pnl
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0: continue
            b = bars[c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = pd.Series(b["close"].values)
            r7 = (cl.pct_change(7)).values
            idx = pd.Series(range(len(b)), index=ts)
            t = t.copy()
            et = pd.to_datetime(t["entry_time"])
            pos = [idx.index.get_indexer([x], method="nearest")[0] for x in et]
            t["r7"] = [r7[p] for p in pos]
            T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["dur_d"] = T.duration_minutes / 1440
    T["long_hold"] = T.dur_d > 2.5
    T["r7q"] = pd.qcut(T.r7, 4, duplicates="drop")
    out["trades_by_entry_r7"] = T.groupby("r7q", observed=True).agg(n=("dur_d", "size"), pnl=("profit_loss_percent", "mean"),
                                                                    share_long_hold=("long_hold", "mean"), dur=("dur_d", "mean")).round(3)
    out["pnl_sum_by_hold"] = T.groupby("long_hold").agg(n=("dur_d", "size"), pnl_sum=("profit_loss_percent", "sum"), pnl_mean=("profit_loss_percent", "mean")).round(2)
    return out
