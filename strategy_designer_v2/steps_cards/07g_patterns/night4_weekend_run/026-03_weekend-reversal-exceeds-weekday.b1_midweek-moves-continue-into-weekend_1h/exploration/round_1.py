def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    # --- per-start-weekday 48h back -> 48h forward, one per week per coin-window
    rows = []
    hrs = []
    volrows = []
    for coin, wins in bars.items():
        # usual 48h move: std of non-overlapping 48h returns over all windows
        r48 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            r48.extend(c[idx + 48] / c[idx] - 1)
        usual = np.std(r48); drift = np.mean(r48)
        for w, df in wins.items():
            d = df[["timestamp", "close"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"])
            d = d.reset_index(drop=True)
            c = d["close"].values
            n = len(c)
            ts = d["timestamp"]
            wd = ts.dt.weekday.values; hr = ts.dt.hour.values
            # hour-of-day 1h returns (non-overlapping by nature)
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            hrs.append(pd.DataFrame({"coin": coin, "hr": hr, "wd": wd, "r": r1}))
            # trailing 30-day vol of hourly returns, relative
            lr = pd.Series(np.log(c)).diff()
            vol = lr.rolling(720, min_periods=240).std().values
            sel = np.where(hr == 23)[0]
            for i in sel:
                if i - 48 < 0 or i + 48 >= n:
                    continue
                back = c[i] / c[i - 48] - 1
                fwd = c[i + 48] / c[i] - 1
                fwd24 = c[i + 24] / c[i] - 1
                rows.append((coin, w, (wd[i] + 1) % 7, back / usual, (fwd - drift) / usual, fwd - drift, fwd24, vol[i]))
    R = pd.DataFrame(rows, columns=["coin", "w", "startwd", "zb", "zf", "uf", "f24", "vol"])
    # per start weekday regression of forward on back (standardised)
    res = []
    for s, g in R.groupby("startwd"):
        sl = stats.linregress(g["zb"], g["zf"])
        dirm = (np.sign(g["zb"]) * g["uf"]).mean()
        res.append((s, len(g), sl.slope, sl.slope / sl.stderr, dirm))
    out["by_start_weekday_0Mon"] = pd.DataFrame(res, columns=["startwd", "n", "slope", "t", "dir_unusual_mean"])
    # Thursday-start case (Friday start=4) by vol tercile within coin
    F = R[R.startwd == 4].dropna(subset=["vol"]).copy()
    F["vq"] = F.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    res = []
    for q, g in F.groupby("vq"):
        sl = stats.linregress(g["zb"], g["zf"])
        res.append((q, len(g), sl.slope, sl.slope / sl.stderr, (np.sign(g["zb"]) * g["uf"]).mean()))
    out["fri_start_by_vol_tercile"] = pd.DataFrame(res, columns=["vq", "n", "slope", "t", "dir_mean"])
    res = []
    for cn, g in F.groupby("coin"):
        sl = stats.linregress(g["zb"], g["zf"])
        res.append((cn, len(g), sl.slope, sl.slope / sl.stderr))
    out["fri_start_by_coin"] = pd.DataFrame(res, columns=["coin", "n", "slope", "t"])
    # weekend (Sat+Sun) -> Mon+Tue: start Mon (0)
    # hour of day
    H = pd.concat(hrs).dropna()
    hg = H.groupby("hr")["r"].agg(["mean", "std", "count"])
    hg["t"] = hg["mean"] / (hg["std"] / np.sqrt(hg["count"]))
    out["hour_of_day"] = hg[["mean", "t", "count"]]
    wg = H.groupby("wd")["r"].agg(["mean", "std", "count"])
    wg["t"] = wg["mean"] / (wg["std"] / np.sqrt(wg["count"]))
    out["weekday_hourly"] = wg[["mean", "t", "count"]]
    # book: days
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["wd"] = pd.to_datetime(x["day"]).dt.weekday; x["coin"] = coin
            D.append(x)
    D = pd.concat(D).dropna(subset=["book_return"])
    bg = D.groupby("wd")[["book_return", "coin_return"]].mean()
    out["book_by_weekday"] = bg
    # trades
    T = pd.concat([df.assign(coin=c) for c, ws in data["trades"].items() for w, df in ws.items()])
    T["absf"] = T["entry_forecast"].abs()
    T["fq"] = pd.qcut(T["absf"], 4, labels=False, duplicates="drop")
    out["trades_by_absforecast_q"] = T.groupby("fq")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["mean", "count"])
    out["trades_by_side"] = T.groupby("side")[["profit_loss_percent", "net_profit_loss_percent"]].mean()
    return out
