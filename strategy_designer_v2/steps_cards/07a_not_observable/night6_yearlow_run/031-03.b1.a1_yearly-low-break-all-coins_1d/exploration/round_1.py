def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            mr = df["regime"] == "mean_reversion"
            lh = df.get("debug_info.components.break_depth.last_history_value")
            pp = df.get("debug_info.components.break_depth.post_pipeline_value")
            f = df["forecast"]
            yr = pd.to_datetime(df["timestamp"]).dt.year.iloc[0]
            # episodes: entries into regime
            ep = int((mr & ~mr.shift(1, fill_value=False)).sum())
            rows.append(dict(coin=coin, window=w, year=yr, bars=len(df), mr_bars=int(mr.sum()),
                             episodes=ep,
                             pp_notnull=int(pp.notna().sum()) if pp is not None else 0,
                             f_pos=int((f > 0).sum()), f_ge2=int((f >= 2).sum()),
                             alloc_pos=int((df["postRebalance_current_allocation"] > 0).sum()),
                             lh_mean=float(lh[mr].mean()) if lh is not None and mr.any() else np.nan,
                             f_max=float(f.max())))
    t = pd.DataFrame(rows)
    by_coin = t.groupby("coin")[["bars", "mr_bars", "episodes", "pp_notnull", "f_pos", "f_ge2", "alloc_pos"]].sum()
    by_year = t.groupby("year")[["bars", "mr_bars", "episodes", "pp_notnull", "f_pos", "f_ge2", "alloc_pos"]].sum()
    by_win = t.groupby("window")[["bars", "mr_bars", "episodes", "f_pos", "f_ge2"]].sum()
    # forecast distribution on regime bars
    allf = []; alllh = []; allpp = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            mr = df["regime"] == "mean_reversion"
            allf.append(df.loc[mr, "forecast"])
            alllh.append(df.loc[mr, "debug_info.components.break_depth.last_history_value"])
            allpp.append(df.loc[mr, "debug_info.components.break_depth.post_pipeline_value"])
    allf = pd.concat(allf); alllh = pd.concat(alllh); allpp = pd.concat(allpp)
    dist = pd.DataFrame({"forecast": allf.describe(), "raw_depth": alllh.describe(), "post": allpp.describe()})
    fbins = pd.cut(allf, [-0.01, 0, 0.5, 1, 2, 5, 10, 20]).value_counts().sort_index()
    nanpost = pd.Series({"regime bars": len(allf), "post NaN": int(allpp.isna().sum()),
                         "post==0": int((allpp == 0).sum()), "raw NaN": int(alllh.isna().sum())})
    return {"by_coin": by_coin, "by_year": by_year, "by_window": by_win, "dist_on_regime_bars": dist,
            "forecast_bins_regime": fbins, "nan_check": nanpost}
