def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    trows = []
    drift = {}
    H = [1, 2, 4, 8, 12, 24]
    # normal drift per coin per horizon
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = (rs.mean(), rs.std())
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values
            f = b["forecast"].values
            raw = b["debug_info.components.vol_fall.last_history_value"].values
            # 30d vol of hourly returns
            r1 = pd.Series(c).pct_change()
            sd = r1.rolling(720, min_periods=200).std().values
            n = len(c)
            for t in range(0, n - 24, 4):
                # case: forecast positive at grid start (simplified)
                if not (f[t] > 0):
                    continue
                d = {"coin": coin, "w": w, "f": f[t], "raw": raw[t],
                     "ret1": r1.values[t], "sd": sd[t],
                     "hour": pd.Timestamp(b["timestamp"].iloc[t]).hour,
                     "year": pd.Timestamp(b["timestamp"].iloc[t]).year}
                for h in H:
                    d["u%d" % h] = c[t + h] / c[t] - 1 - drift[(coin, h)][0]
                    d["tot%d" % h] = c[t + h] / c[t] - 1
                rows.append(d)
    df = pd.DataFrame(rows)
    out["n_cases"] = len(df)
    def st(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": x.mean() * 100, "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["by_horizon_total"] = pd.DataFrame({h: st(df["tot%d" % h]) for h in H}).T
    df["fq"] = pd.qcut(df["f"].rank(method="first"), 5, labels=False)
    g = df.groupby("fq")
    out["by_forecast_quintile"] = pd.DataFrame({
        "n": g.size(), "f_mean": g["f"].mean(),
        "tot4%": g["tot4"].mean() * 100, "tot12%": g["tot12"].mean() * 100,
        "tot24%": g["tot24"].mean() * 100,
        "t4": g["u4"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))})
    # vol regime: hourly sd vs its median by coin
    df["sdq"] = df.groupby("coin")["sd"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    g = df.groupby("sdq")
    out["by_30d_vol_tercile"] = pd.DataFrame({"n": g.size(), "tot4%": g["tot4"].mean() * 100,
                                             "tot12%": g["tot12"].mean() * 100, "tot24%": g["tot24"].mean() * 100})
    # hour's own fall in sd units
    df["z"] = df["ret1"] / df["sd"]
    df["zq"] = pd.qcut(df["z"].rank(method="first"), 5, labels=False)
    g = df.groupby("zq")
    out["by_hour_fall_z_quintile"] = pd.DataFrame({"n": g.size(), "z": g["z"].mean(),
                                                  "tot4%": g["tot4"].mean() * 100, "tot12%": g["tot12"].mean() * 100,
                                                  "tot24%": g["tot24"].mean() * 100})
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    out["trades"] = pd.DataFrame({"n": [len(tr)], "gross_mean%": [tr["profit_loss_percent"].mean()],
                                  "net_mean%": [tr["net_profit_loss_percent"].mean()],
                                  "dur_h_median": [tr["duration_minutes"].median() / 60],
                                  "share_long": [(tr["side"] == "LONG").mean()]})
    # time in market and allocation
    alloc = pd.concat([b["postRebalance_current_allocation"] for wins in data["bars"].values() for b in wins.values()])
    out["alloc"] = pd.Series({"share_bars_in": (alloc.abs() > 1e-6).mean(), "mean_abs_in": alloc[alloc.abs() > 1e-6].abs().mean()})
    # book by year
    dd = pd.concat([d.assign(coin=c) for c, wins in data["days"].items() for d in wins.values()])
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    out["book_by_year"] = dd.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out
