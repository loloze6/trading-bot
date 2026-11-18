def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r1 = c.shift(-1) / c - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            ma100 = c.rolling(100, min_periods=40).mean()
            ret60 = c / c.shift(60) - 1
            ret5 = c / c.shift(5) - 1
            ret3 = c / c.shift(3) - 1
            high30 = c.rolling(30, min_periods=10).max()
            dd = c / high30 - 1
            vol20 = r1.shift(1).rolling(20, min_periods=10).std()
            r10 = c.shift(-10) / c - 1
            grid = (np.arange(len(b)) % 10 == 0)
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": pos, "r1": r1, "gain": pos * r1,
                                      "trend": c / ma100 - 1, "ret60": ret60, "ret5": ret5, "ret3": ret3,
                                      "dd": dd, "vol20": vol20, "r10": r10, "grid": grid,
                                      "active": pos != 0}))
    A = pd.concat(rows)
    act = A[A.active & A.r1.notna()].copy()
    def g(df, col):
        return df.groupby(col, observed=True).agg(n=("gain", "size"), gain=("gain", "mean"),
                                                  r1=("r1", "mean"), r10=("r10", "mean"),
                                                  t_gain=("gain", lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    act["trend_q"] = pd.qcut(act.trend, 4, labels=["far_below_ma100", "q2", "q3", "near_ma100"])
    out["by_trend_ma100"] = g(act, "trend_q")
    act["ret60_q"] = pd.qcut(act.ret60, 4, labels=["r60_lowest", "q2", "q3", "r60_highest"])
    out["by_ret60"] = g(act, "ret60_q")
    act["ret5_q"] = pd.qcut(act.ret5, 4, labels=["r5_lowest", "q2", "q3", "r5_highest"])
    out["by_ret5"] = g(act, "ret5_q")
    act["vol_q"] = pd.qcut(act.vol20, 3, labels=["lowvol", "mid", "highvol"])
    out["by_vol20"] = g(act, "vol_q")
    # dd relative to vol: decline in vol units
    act["ddv"] = act.dd / (act.vol20 * np.sqrt(30))
    act["ddv_q"] = pd.qcut(act.ddv, 4, labels=["deep_v", "q2", "q3", "mild_v"])
    out["by_dd_in_vol"] = g(act, "ddv_q")
    # combos: dd half x trend half
    act["dd_h"] = np.where(act.dd > act.dd.median(), "mild", "deep")
    act["tr_h"] = np.where(act.trend > act.trend.median(), "nearMA", "farMA")
    out["dd_x_trend"] = g(act, ["dd_h", "tr_h"])
    # correlations of gain with features
    out["spearman_with_r1"] = pd.Series({k: stats.spearmanr(act[k], act.r1, nan_policy="omit")[0]
                                         for k in ["trend", "ret60", "ret5", "ret3", "dd", "vol20", "ddv"]})
    # book daily: share days active, and the overall holding daily mean
    D = pd.concat([d.assign(coin=c) for c, ws in data["days"].items() for d in ws.values()])
    out["days"] = pd.Series({"book_mean": D.book_return.mean(), "coin_mean": D.coin_return.mean(),
                             "book_std": D.book_return.std(), "coin_std": D.coin_return.std(),
                             "share_active_bars": A.active.mean(), "mean_abs_pos_active": act.pos.abs().mean()})
    # non-overlapping grid on all bars: r10 by dd quartile, regardless of new low (new-low cases included)
    gr = A[A.grid & A.r10.notna() & A.dd.notna()].copy()
    gr["dd_q"] = pd.qcut(gr.dd, 5, labels=["deepest", "q2", "q3", "q4", "at_high"])
    out["grid_r10_by_dd_allbars"] = gr.groupby("dd_q", observed=True).r10.agg(["size", "mean"])
    return out
