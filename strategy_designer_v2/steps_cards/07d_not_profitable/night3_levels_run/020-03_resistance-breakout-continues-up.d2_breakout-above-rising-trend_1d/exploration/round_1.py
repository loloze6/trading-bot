def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily
    rows = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    # exposure per bar
    exp = []
    cases = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            a = b["postRebalance_current_allocation"].fillna(0)
            cl = b["close"].values
            r1 = pd.Series(cl).shift(-1) / pd.Series(cl) - 1
            g = a * r1
            exp.append(pd.DataFrame({"coin": c, "w": w, "alloc": a, "gain": g, "r1": r1,
                                     "in": (a.abs() > 1e-6)}))
            f = b["forecast"].fillna(0).values
            md = b.get("debug_info.components.ma_dist.last_history_value")
            n = len(b)
            # entries: forecast from 0 to >0
            for i in range(1, n):
                if f[i] > 0 and f[i-1] <= 0:
                    rec = {"coin": c, "w": w, "alloc": a.iloc[i],
                           "mad": md.iloc[i] if md is not None else np.nan,
                           "fc": f[i], "year": pd.Timestamp(b["timestamp"].iloc[i]).year}
                    for h in [1, 3, 5, 10, 20, 40]:
                        rec[f"r{h}"] = cl[i+h]/cl[i]-1 if i+h < n else np.nan
                    # prior 20d return
                    rec["p20"] = cl[i]/cl[i-20]-1 if i >= 20 else np.nan
                    cases.append(rec)
    E = pd.concat(exp)
    out["exposure"] = pd.Series({
        "share_bars_in": E["in"].mean(),
        "mean_abs_alloc_when_in": E.loc[E["in"], "alloc"].abs().mean(),
        "mean_gain_per_bar_all": E["gain"].mean(),
        "mean_gain_per_bar_in": E.loc[E["in"], "gain"].mean(),
        "coin_mean_r1": E["r1"].mean(),
        "book_mean_daily": D["book_return"].mean(),
        "coin_mean_daily": D["coin_return"].mean(),
    })
    out["by_coin"] = E.groupby("coin").agg(share_in=("in", "mean"), gain=("gain", "mean"),
                                           r1=("r1", "mean"))
    C = pd.DataFrame(cases)
    out["n_entries"] = len(C)
    # drift per coin daily
    drift = E.groupby("coin")["r1"].mean()
    res = {}
    for h in [1, 3, 5, 10, 20, 40]:
        x = C[f"r{h}"] - C["coin"].map(drift) * h
        x = x.dropna()
        res[h] = {"mean_total": C[f"r{h}"].mean(), "mean_excess": x.mean(),
                  "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)}
    out["entry_fwd"] = pd.DataFrame(res).T
    # increments: days 6-10, 11-20, 21-40
    inc = pd.DataFrame({
        "d6_10": (1+C["r10"])/(1+C["r5"])-1,
        "d11_20": (1+C["r20"])/(1+C["r10"])-1,
        "d21_40": (1+C["r40"])/(1+C["r20"])-1})
    out["increments"] = inc.agg(["mean", "count"]).T.assign(
        t=lambda s: inc.mean()/(inc.std()/np.sqrt(inc.count())))
    C["madq"] = pd.qcut(C["mad"], 4, labels=False, duplicates="drop")
    out["by_mad_q"] = C.groupby("madq").agg(mad=("mad", "mean"), r5=("r5", "mean"),
                                            r20=("r20", "mean"), alloc=("alloc", "mean"), n=("r5", "count"))
    C["p20q"] = pd.qcut(C["p20"], 4, labels=False, duplicates="drop")
    out["by_p20_q"] = C.groupby("p20q").agg(p20=("p20", "mean"), r5=("r5", "mean"),
                                            r20=("r20", "mean"), n=("r5", "count"))
    out["by_year"] = C.groupby("year").agg(r5=("r5", "mean"), r20=("r20", "mean"), n=("r5", "count"))
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(),
                               "mean_gross": T["profit_loss_percent"].mean(),
                               "mean_days": T["duration_minutes"].mean()/1440,
                               "win": (T["net_profit_loss_percent"] > 0).mean()})
    return out
