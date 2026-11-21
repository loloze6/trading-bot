def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 72
    rows = []
    hour_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r24 = c / c.shift(24) - 1
            scale = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            ratio = r24 / scale
            r720 = c / c.shift(720) - 1
            r72p = c / c.shift(72) - 1
            r168 = c / c.shift(168) - 1
            lr = np.log(c).diff()
            vol24 = lr.rolling(24).std()
            vol720 = lr.rolling(720, min_periods=240).std()
            volratio = vol24 / vol720
            fwd = c.shift(-H) / c - 1
            idx = np.arange(0, len(b), H)
            g = pd.DataFrame({"coin": coin, "win": w, "ratio": ratio.iloc[idx].values,
                              "r720": r720.iloc[idx].values, "r72p": r72p.iloc[idx].values,
                              "r168": r168.iloc[idx].values, "volratio": volratio.iloc[idx].values,
                              "fwd": fwd.iloc[idx].values,
                              "fc": b["forecast"].iloc[idx].values,
                              "pos": b["postRebalance_current_allocation"].iloc[idx].values})
            rows.append(g)
            ts = pd.to_datetime(b["timestamp"])
            f1 = c.shift(-1) / c - 1
            hour_rows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values,
                                           "wd": ts.dt.weekday.values, "f1": f1.values,
                                           "ratio": ratio.values}))
    G = pd.concat(rows).dropna(subset=["fwd"])
    G["drift"] = G.groupby("coin")["fwd"].transform("mean")
    G["usual"] = G.groupby("coin")["fwd"].transform("std")
    G["un"] = G["fwd"] - G["drift"]
    G["str"] = G["un"] / G["usual"]

    def summ(df, key):
        out = df.groupby(key, observed=True).agg(n=("un", "size"), un=("un", "mean"),
                                                 sd=("un", "std"), strength=("str", "mean"),
                                                 tot=("fwd", "mean"))
        out["t"] = out["un"] / (out["sd"] / np.sqrt(out["n"]))
        return out.drop(columns="sd").round(5)

    res = {}
    rb = [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf]
    G["ratio_b"] = pd.cut(G["ratio"], rb)
    G["up30"] = np.where(G["r720"] > 0, "up", "down")
    d = G.dropna(subset=["ratio", "r720"])
    res["ratio_by_trend"] = summ(d, ["up30", "ratio_b"])
    for col in ["r72p", "r168", "r720", "volratio"]:
        dd = G.dropna(subset=[col]).copy()
        dd["q"] = dd.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        res[col + "_quint"] = summ(dd, "q")
    # 3-day past return quintile within uptrend vs downtrend
    dd = G.dropna(subset=["r72p", "r720"]).copy()
    dd["q"] = dd.groupby("coin")["r72p"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    res["r72p_by_trend"] = summ(dd, ["up30", "q"])
    res["by_coin"] = summ(G, "coin")
    res["by_window_r720up"] = summ(d[d.up30 == "up"], "win")
    Hh = pd.concat(hour_rows).dropna(subset=["f1"])
    Hh["f1"] = Hh["f1"] - Hh.groupby("coin")["f1"].transform("mean")
    hh = Hh.groupby("hour")["f1"].agg(["mean", "std", "size"])
    hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["size"]))
    res["hour_1h_unusual"] = hh[["mean", "t", "size"]]
    wd = Hh.groupby("wd")["f1"].agg(["mean", "std", "size"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    res["wd_1h_unusual"] = wd[["mean", "t", "size"]]
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    T["eh"] = pd.to_datetime(T["entry_time"]).dt.hour
    T["fcb"] = pd.cut(T["entry_forecast"], [-0.1, 2, 5, 10, 15, 20.1])
    res["trades_by_fc"] = T.groupby("fcb", observed=True)["net_profit_loss_percent"].agg(["size", "mean", "median"])
    res["trades_dur_h"] = (T["duration_minutes"] / 60).describe()
    # book days
    D = pd.concat([x.assign(coin=c) for c, ws in data["days"].items() for x in ws.values()]).dropna(subset=["book_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    res["book_by_wd"] = D.groupby("wd")[["book_return", "coin_return"]].mean()
    return res
