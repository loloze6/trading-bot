def explore(data):
    import numpy as np, pandas as pd
    out = {}
    def ct(dev, day):
        d = pd.DataFrame({"d": dev.values, "day": day.values}).groupby("day")["d"].sum()
        D = len(d)
        if D < 3: return np.nan, D
        se = np.sqrt((d ** 2).sum() * D / (D - 1)) / len(dev)
        return dev.mean() / se, D
    allg = {}
    for H in [5, 10, 20]:
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.sort_values("timestamp").reset_index(drop=True)
                c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
                rng = (hi - lo) / c
                f = pd.DataFrame({"coin": coin, "win": w,
                    "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                    "mr": (b["regime"] == "mean_reversion"),
                    "fc": b["forecast"].astype(float),
                    "depth": b.get("debug_info.components.depth.last_history_value"),
                    "dhi20": c / hi.shift(1).rolling(20).max() - 1,
                    "dlo20": c / lo.shift(1).rolling(20).min() - 1,
                    "r20": c / c.shift(20) - 1,
                    "rng1": rng / rng.rolling(20).mean(),
                    "r1": c.pct_change(),
                    "fwd": c.shift(-H) / c - 1})
                f["mr_any"] = f["mr"].rolling(H, min_periods=1).max().astype(bool)
                f["pos"] = np.arange(len(f))
                rows.append(f[f["pos"] % H == 0])
        g = pd.concat(rows).dropna(subset=["fwd"])
        g["dev"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        allg[H] = g
        res = {}
        for name, m in [("mr_bar", g["mr"]), ("mr_in_cell", g["mr_any"]), ("fc_pos", g["fc"] > 0), ("all", g["fwd"].notna())]:
            x = g[m]
            t, D = ct(x["dev"], x["day"])
            res[name] = {"n": len(x), "days": D, "mean_dev": x["dev"].mean(), "mean_tot": x["fwd"].mean(), "t_day": t}
        out[f"regime_H{H}"] = pd.DataFrame(res).T
        for ft in ["dhi20", "dlo20", "r20", "rng1", "r1"]:
            x = g.dropna(subset=[ft]).copy()
            x["q"] = x.groupby("coin")[ft].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
            rr = {}
            for q, y in x.groupby("q"):
                t, D = ct(y["dev"], y["day"])
                rr[q] = {"n": len(y), "days": D, "mean_dev": y["dev"].mean(), "t_day": t}
            out[f"q_{ft}_H{H}"] = pd.DataFrame(rr).T
    # depth gradient inside regime, all regime bars (overlapping, informative) at H=10,20
    for H in [5, 10, 20]:
        g = allg[H]; x = g[g["mr"]].dropna(subset=["dlo20"])
        if len(x) > 5:
            out[f"mr_slope_dlo20_H{H}"] = pd.Series({"n": len(x), "corr": np.corrcoef(x["dlo20"], x["dev"])[0, 1]})
    # trades: by duration and by window
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin, win=w))
    T = pd.concat(tr)
    T["days"] = T["duration_minutes"] / 1440
    T["dq"] = pd.cut(T["days"], [0, 5.5, 10.5, 20.5, 1000])
    out["trades_by_dur"] = T.groupby("dq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_by_win"] = T.groupby("win")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
