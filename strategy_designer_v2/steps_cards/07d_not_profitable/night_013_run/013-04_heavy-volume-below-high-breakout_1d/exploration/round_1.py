def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # exposure and book vs hold
    rows = []
    bk, hd = [], []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            a = b["postRebalance_current_allocation"].fillna(0)
            tr = (b["regime"] == "trending")
            d = data["days"][c][w]
            bk.append(d["book_return"].dropna()); hd.append(d["coin_return"].dropna())
            rows.append({"coin": c, "bars": len(b), "trend_share": tr.mean(), "in_share": (a.abs() > 1e-6).mean(),
                         "mean_alloc_when_in": a[a.abs() > 1e-6].mean() if (a.abs() > 1e-6).any() else np.nan,
                         "book_ret": d["book_value"].iloc[-1] / d["book_value"].iloc[0] - 1,
                         "coin_ret": d["close"].iloc[-1] / d["close"].iloc[0] - 1})
    r = pd.DataFrame(rows)
    out["by_coin"] = r.groupby("coin").agg(trend_share=("trend_share", "mean"), in_share=("in_share", "mean"),
                                          alloc_in=("mean_alloc_when_in", "mean"), book=("book_ret", "mean"), coin=("coin_ret", "mean"))
    bk = pd.concat(bk); hd = pd.concat(hd)
    out["book_vs_hold"] = pd.Series({"book_mean": bk.mean(), "book_sd": bk.std(), "hold_mean": hd.mean(), "hold_sd": hd.std(),
                                     "book_sharpe": bk.mean()/bk.std()*np.sqrt(365), "hold_sharpe": hd.mean()/hd.std()*np.sqrt(365)})
    # forward returns from trending bars by run length (days since the run of trending started), and after run end
    recs = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            cl = b["close"].values; tr = (b["regime"] == "trending").values
            fc = b["forecast"].values
            run = np.zeros(len(b), int); since_end = np.full(len(b), -1)
            for i in range(len(b)):
                run[i] = run[i-1] + 1 if (tr[i] and i > 0) else (1 if tr[i] else 0)
            last_tr = -999
            for i in range(len(b)):
                if tr[i]: last_tr = i
                elif last_tr >= 0: since_end[i] = i - last_tr
            for i in range(len(b)):
                rec = {"coin": c, "w": w, "tr": tr[i], "run": run[i], "since_end": since_end[i], "fc": fc[i]}
                for h in (1, 5, 10, 30):
                    rec[f"f{h}"] = cl[i+h]/cl[i]-1 if i+h < len(b) else np.nan
                recs.append(rec)
    R = pd.DataFrame(recs)
    out["mean_fwd_all_bars"] = R[["f1", "f5", "f10", "f30"]].mean()
    R["runb"] = pd.cut(R["run"], [-1, 0, 1, 3, 7, 15, 30, 1000])
    out["fwd_by_trend_runlength"] = R.groupby("runb", observed=True)[["f1", "f5", "f10", "f30"]].agg(["mean", "count"])
    R["endb"] = pd.cut(R["since_end"], [0, 3, 10, 30, 1000])
    out["fwd_after_trend_end"] = R[R.since_end > 0].groupby("endb", observed=True)[["f1", "f5", "f30"]].agg(["mean", "count"])
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values() if len(t)])
    T["dur_d"] = T["duration_minutes"]/1440
    out["trades"] = pd.Series({"n": len(T), "mean_dur_d": T.dur_d.mean(), "med_dur_d": T.dur_d.median(),
                               "mean_pl": T.profit_loss_percent.mean(), "mean_net": T.net_profit_loss_percent.mean(),
                               "win": (T.profit_loss_percent > 0).mean()})
    return out
