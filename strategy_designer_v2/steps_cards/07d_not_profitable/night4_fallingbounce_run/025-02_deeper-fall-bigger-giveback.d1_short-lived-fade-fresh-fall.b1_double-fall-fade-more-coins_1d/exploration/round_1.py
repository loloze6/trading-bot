def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    # trades
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["win"] = w
            T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440.0
    T["et"] = pd.to_datetime(T["entry_time"]); T["year"] = T["et"].dt.year
    out["trades_summary"] = pd.DataFrame({
        "n": [len(T)], "short_share": [(T.side == "SHORT").mean()],
        "pnl_before": [T.profit_loss_percent.mean()], "pnl_after": [T.net_profit_loss_percent.mean()],
        "t_before": [stats.ttest_1samp(T.profit_loss_percent.dropna(), 0).statistic],
        "dur_mean_d": [T.dur_d.mean()], "dur_median_d": [T.dur_d.median()]})
    T["durb"] = pd.cut(T.dur_d, [0, 1.5, 2.5, 3.5, 5.5, 10.5, 1e9])
    out["trades_by_duration"] = T.groupby("durb", observed=True).agg(n=("dur_d", "size"), before=("profit_loss_percent", "mean"), after=("net_profit_loss_percent", "mean"))
    out["trades_by_year"] = T.groupby("year").agg(n=("dur_d", "size"), before=("profit_loss_percent", "mean"), after=("net_profit_loss_percent", "mean"), dur=("dur_d", "mean"))
    # entry bars: forward returns per day after entry, by bounce size
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(b)
            r1 = pd.Series(cl).pct_change()
            vol20 = r1.rolling(20).std()
            z = (r1 / vol20).values
            r90 = pd.Series(cl).pct_change(90).values
            r30 = pd.Series(cl).pct_change(30).values
            r7 = pd.Series(cl).pct_change(7).values
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            prev = b["previous_allocation"].fillna(0).values
            for i in range(n):
                if alloc[i] < -1e-6 and prev[i] > -1e-6:
                    d = {"coin": c, "win": w, "z": z[i], "r30": r30[i], "r90": r90[i], "r7": r7[i], "r1": r1.values[i], "fc": b["forecast"].values[i]}
                    for h in [1, 2, 3, 5]:
                        d[f"f{h}"] = -(cl[i + h] / cl[i] - 1) if i + h < n else np.nan
                    d["d2only"] = -(cl[i + 2] / cl[i + 1] - 1) if i + 2 < n else np.nan
                    d["year"] = pd.to_datetime(b["timestamp"].iloc[i]).year
                    rows.append(d)
    E = pd.DataFrame(rows)
    out["entries_n"] = len(E)
    out["entry_fwd_means"] = E[["f1", "d2only", "f2", "f3", "f5"]].agg(["mean", "count"]).T.assign(t=lambda x: [stats.ttest_1samp(E[k].dropna(), 0).statistic for k in ["f1", "d2only", "f2", "f3", "f5"]])
    E["zq"] = pd.qcut(E["z"], 4, duplicates="drop")
    out["fwd_by_z_quartile"] = E.groupby("zq", observed=True)[["f1", "f2", "f3", "r1"]].agg(["mean", "count"]).round(4)
    E["r30q"] = pd.qcut(E["r30"], 4, duplicates="drop")
    out["fwd_by_r30_quartile"] = E.groupby("r30q", observed=True)[["f1", "f2", "f3"]].mean().round(4)
    E["r7q"] = pd.qcut(E["r7"], 4, duplicates="drop")
    out["fwd_by_r7_quartile"] = E.groupby("r7q", observed=True)[["f1", "f2", "f3"]].agg(["mean", "count"]).round(4)
    E["r90q"] = pd.qcut(E["r90"], 4, duplicates="drop")
    out["fwd_by_r90_quartile"] = E.groupby("r90q", observed=True)[["f1", "f2", "f3"]].agg(["mean", "count"]).round(4)
    out["fwd_by_year"] = E.groupby("year")[["f1", "f2", "f3"]].agg(["mean", "count"]).round(4)
    # book: in-position vs flat days, exposure
    D = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w]
            a = b.set_index(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"]
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"])
            dd["alloc_prev"] = dd["day"].map(a.shift(1).to_dict())
            D.append(dd)
    D = pd.concat(D)
    D["inpos"] = D["alloc_prev"].fillna(0).abs() > 1e-6
    out["book_by_inpos"] = D.groupby("inpos")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["mean_abs_alloc_inpos"] = float(D.loc[D.inpos, "alloc_prev"].abs().mean())
    return out
