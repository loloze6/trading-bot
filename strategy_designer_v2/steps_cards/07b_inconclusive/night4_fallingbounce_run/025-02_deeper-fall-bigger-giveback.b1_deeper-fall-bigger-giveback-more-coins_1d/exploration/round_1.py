def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    coinmean = {}
    for coin, wins in bars.items():
        # coin's mean h-day return, non-overlapping grid of all windows
        cm = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                cm[h].extend(list(c[idx + h] / c[idx] - 1))
        coinmean[coin] = {h: np.mean(cm[h]) if cm[h] else np.nan for h in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            bounce = r1 / sd
            r90 = c / c.shift(90) - 1
            fd = df.get("debug_info.components.fall_depth.last_history_value")
            fz = df.get("debug_info.components.fall_depth.post_pipeline_value")
            year = pd.to_datetime(df["timestamp"]).dt.year
            for i in range(len(df)):
                mr = df["regime"].iat[i] == "mean_reversion" and df["forecast"].iat[i] < 0
                rising = (not np.isnan(bounce.iat[i])) and bounce.iat[i] >= 2 and (not np.isnan(r90.iat[i])) and r90.iat[i] > 0
                if not (mr or rising):
                    continue
                rec = dict(coin=coin, window=w, i=i, cell=i // 5, year=year.iat[i],
                           grp="fall" if mr else "rise",
                           depth=(fd.iat[i] if (mr and fd is not None) else r90.iat[i]),
                           z=(fz.iat[i] if (mr and fz is not None) else np.nan),
                           bounce=bounce.iat[i])
                for h in H:
                    if i + h < len(df):
                        rec[f"x{h}"] = c.iat[i + h] / c.iat[i] - 1 - coinmean[coin][h]
                    else:
                        rec[f"x{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    d = d.sort_values(["coin", "window", "i"]).groupby(["grp", "coin", "window", "cell"]).head(1)
    out = {}
    def summ(g):
        res = {"n": len(g)}
        for h in H:
            x = g[f"x{h}"].dropna()
            res[f"mean_x{h}"] = x.mean()
            res[f"t_x{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(res)
    out["by_group_excess_long_dir"] = d.groupby("grp").apply(summ)
    f = d[d.grp == "fall"].copy()
    sl = {}
    for h in H:
        g = f[["depth", f"x{h}"]].dropna()
        if len(g) > 5:
            r = stats.linregress(g["depth"], g[f"x{h}"])
            sl[h] = dict(n=len(g), slope=r.slope, t=r.slope / r.stderr)
    out["fall_slope_by_horizon"] = pd.DataFrame(sl).T
    f["dq"] = pd.qcut(f["depth"], 4, labels=["deepest", "q2", "q3", "shallow"])
    out["fall_by_depth_quartile"] = f.groupby("dq").apply(summ)
    f["bq"] = pd.qcut(f["bounce"], 3, labels=["small", "mid", "large"])
    out["fall_by_bounce_tercile"] = f.groupby("bq").apply(summ)
    out["fall_by_year"] = f.groupby("year").apply(summ)[["n", "mean_x5", "t_x5", "mean_x10", "t_x10"]]
    out["fall_by_coin"] = f.groupby("coin").apply(summ)[["n", "mean_x5", "t_x5", "mean_x10", "t_x10"]]
    out["depth_stats"] = f["depth"].describe()
    return out
