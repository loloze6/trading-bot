def explore(data):
    import numpy as np, pandas as pd
    out = {}
    tr = pd.concat([t.assign(coin=c, win=w) for c, wins in data["trades"].items() for w, t in wins.items() if len(t)])
    et = pd.to_datetime(tr["entry_time"], utc=True)
    tr["ewd"] = et.dt.weekday; tr["ehr"] = et.dt.hour
    tr["dur_h"] = tr["duration_minutes"] / 60
    out["trades_by_entry_wd"] = tr.groupby("ewd").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), dur=("dur_h", "mean"), comm=("total_commission", "mean"))
    out["trades_by_side"] = tr.groupby("side").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    tr["dur_bin"] = pd.cut(tr["dur_h"], [0, 1.5, 24, 47.5, 48.5, 72, 1e6])
    out["trades_by_duration"] = tr.groupby("dur_bin").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    # book: allocation stats and bar-level gains
    rows = []; pos_stats = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            a = b["postRebalance_current_allocation"].fillna(0).values
            c = b["close"].values
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            ch = np.abs(np.diff(np.r_[0, a]))
            pos_stats.append({"coin": coin, "share_bars_in": (a != 0).mean(), "mean_abs_alloc_when_in": np.abs(a[a != 0]).mean() if (a != 0).any() else np.nan,
                              "n_alloc_changes": (ch > 1e-9).sum(), "turnover": ch.sum(),
                              "gain": np.nansum(a * r1), "long_bars": (a > 0).sum()})
            # weekday-move comparison: 48h move ending at 23:00 each day, next 48h
            for i in np.where(ts.dt.hour == 23)[0]:
                if i < 168 or i + 48 >= len(c): continue
                rows.append({"coin": coin, "wd": ts[i].weekday(), "year": ts[i].year,
                             "past": c[i] / c[i - 48] - 1, "f48": c[i + 48] / c[i] - 1,
                             "prev5": c[i - 48] / c[i - 168] - 1,
                             "vr": b["volume"].values[i - 47:i + 1].mean() / b["volume"].values[i - 167:i - 47].mean()})
    ps = pd.DataFrame(pos_stats)
    out["position_by_coin"] = ps.groupby("coin").agg(share_in=("share_bars_in", "mean"), abs_alloc=("mean_abs_alloc_when_in", "mean"),
        changes=("n_alloc_changes", "sum"), turnover=("turnover", "sum"), gross_gain_sum=("gain", "sum"), long_bars=("long_bars", "sum"))
    df = pd.DataFrame(rows)
    # standardise past by coin std of 48h moves
    sd = df.groupby("coin")["past"].transform("std")
    df["z"] = df["past"] / sd
    dr = df.groupby("coin")["f48"].transform("mean")
    df["unus"] = df["f48"] - dr
    df["rev"] = -np.sign(df["past"]) * df["unus"]
    def s(g):
        x = g["rev"]; return pd.Series({"n": len(x), "rev": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["reversal_by_weekday_end_all_moves(overlapping days)"] = df.groupby("wd").apply(s)
    df["absq"] = df.groupby("wd")["z"].transform(lambda z: pd.qcut(z.abs().rank(method="first"), 3, labels=False))
    out["reversal_sunday_by_abs_move_tercile"] = df[df["wd"] == 6].groupby("absq").apply(s)
    out["reversal_weekdays_by_abs_move_tercile"] = df[df["wd"] < 5].groupby("absq").apply(s)
    sun = df[(df["wd"] == 6) & (df["past"] > 0)].copy()
    sun["against_week"] = np.where(sun["prev5"] < 0, "week_fell", "week_rose")
    out["sun_rise_by_prior_week_and_vol"] = sun.groupby(["against_week", np.where(sun["vr"] < 1, "thin", "thick")]).apply(s)
    sun["q"] = pd.qcut((sun["past"] / sun["prev5"].abs().clip(lower=1e-3)).rank(method="first"), 4, labels=False)
    out["sun_rise_by_rise_over_weekmove_quart"] = sun.groupby("q").apply(s)
    return out
