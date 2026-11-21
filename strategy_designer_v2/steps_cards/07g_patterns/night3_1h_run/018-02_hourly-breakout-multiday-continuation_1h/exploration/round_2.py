def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [24, 120, 240, 480]
    grids = {h: [] for h in H}; ev = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            v = b["volume"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            ph = hi.shift(1).rolling(480).max(); pl = lo.shift(1).rolling(480).min()
            a24 = (c / c.shift(24) - 1).abs().rolling(720, min_periods=240).mean()
            for h in H:
                f = (c.shift(-h) / c - 1).iloc[::h].dropna()
                grids[h].append(pd.DataFrame({"coin": coin, "f": f.values}))
            above = c > ph
            first = above & ~above.shift(1, fill_value=False)
            # next daily close: last bar of the current UTC day
            day = ts.dt.floor("D")
            lastidx = pd.Series(np.arange(len(b))).groupby(day.values).transform("max").values
            nd = pd.Series(c.values[lastidx], index=b.index)
            hrs_to_close = lastidx - np.arange(len(b))
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "brk": (c / ph - 1) / a24,
                "width": (ph / pl - 1) / a24,
                "r30": (c / c.shift(720) - 1) / a24,
                "r1": (c / c.shift(1) - 1) / a24,
                "vrel": v / v.rolling(720, min_periods=240).mean(),
                "hour": ts.dt.hour, "wd": ts.dt.weekday,
                "to_close": (nd / c - 1), "htc": hrs_to_close,
            })
            for h in H:
                df[f"f{h}"] = c.shift(-h) / c - 1
            # from next daily close over 120h
            nc = pd.Series(lastidx, index=b.index)
            tgt = nc + 120
            ok = tgt < len(b)
            df["fdc120"] = np.where(ok, c.values[np.minimum(tgt, len(b) - 1)] / nd.values - 1, np.nan)
            e = df[first].copy()
            e["cell"] = e["pos"] // 120
            e = e.groupby("cell").head(1)
            ev.append(e)
    drift = {h: pd.concat(grids[h]).groupby("coin")["f"].mean() for h in H}
    E = pd.concat(ev).dropna(subset=["brk", "f120"])
    for h in H:
        E[f"u{h}"] = E[f"f{h}"] - E["coin"].map(drift[h])
    E["udc120"] = E["fdc120"] - E["coin"].map(drift[120])
    def summ(df, key, col="u120"):
        x = df.groupby(key, observed=True)[col].agg(["mean", "std", "count"])
        x["t"] = x["mean"] / (x["std"] / np.sqrt(x["count"]))
        return x.drop(columns="std")
    def tq(df, col, ycol="u120", q=4):
        d = df.dropna(subset=[col, ycol]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = summ(d, "q", ycol)
        rho, p = stats.spearmanr(d[col], d[ycol])
        r.loc["spearman"] = [rho, len(d), p]
        return r
    out = {}
    out["events dedup: unusual by horizon"] = pd.DataFrame({h: [E[f"u{h}"].mean(), E[f"u{h}"].count(),
        E[f"u{h}"].mean() / (E[f"u{h}"].std() / np.sqrt(E[f"u{h}"].count()))] for h in H},
        index=["mean", "n", "t"]).T
    d = E.dropna(subset=["udc120"])
    diff = d["u120"] - d["udc120"]
    out["event entry vs next daily close entry (120h)"] = pd.Series({
        "u_event": d["u120"].mean(), "u_dailyclose": d["udc120"].mean(),
        "event_to_close_raw": d["to_close"].mean(),
        "t_to_close": d["to_close"].mean() / (d["to_close"].std() / np.sqrt(len(d))), "n": len(d),
        "mean_hours_to_close": d["htc"].mean()})
    out["to-close move by hours left in day"] = summ(E.assign(hb=pd.cut(E["htc"], [-1, 3, 8, 14, 24])), "hb", "to_close")
    out["by volume of breakout hour (coin quartiles)"] = tq(E, "vrel")
    out["by width of 20d range (compression)"] = tq(E, "width")
    out["by 30d prior return"] = tq(E, "r30")
    out["by breakout hour's own return"] = tq(E, "r1")
    out["by break size, 480h"] = tq(E, "brk", "u480")
    out["by width, 480h"] = tq(E, "width", "u480")
    out["by coin, 120h"] = summ(E, "coin")
    # book
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["db"] = pd.cut(T["dur_d"], [0, 5.5, 10, 20, 1000])
    out["trades by duration (days)"] = T.groupby("db", observed=True)["net_profit_loss_percent"].agg(["mean", "median", "count"])
    return out
