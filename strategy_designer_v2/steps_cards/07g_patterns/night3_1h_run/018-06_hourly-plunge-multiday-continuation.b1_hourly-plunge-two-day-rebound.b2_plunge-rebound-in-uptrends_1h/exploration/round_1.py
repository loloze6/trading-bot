def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            if len(c) < 900: continue
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=360).mean()
            z = r24 / mabs
            r30 = c / c.shift(720) - 1
            vol = c.pct_change().rolling(720, min_periods=360).std()
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            f = b["forecast"].astype(float).reset_index(drop=True)
            for h in (24, 96, 192):
                idx = np.arange(0, len(c) - h, h)
                fr = (c.shift(-h) / c - 1).iloc[idx]
                df = pd.DataFrame({"coin": coin, "win": w, "h": h, "fwd": fr.values,
                                   "z": z.iloc[idx].values, "r30": r30.iloc[idx].values,
                                   "vol": vol.iloc[idx].values, "fc": f.iloc[idx].values,
                                   "hour": ts.iloc[idx].dt.hour.values, "wd": ts.iloc[idx].dt.weekday.values})
                rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby(["coin", "h"])["fwd"].transform("mean")
    A["unus"] = A["fwd"] - drift
    A = A.dropna(subset=["z", "r30", "unus"])
    def summ(g):
        x = g["unus"]
        return pd.Series({"n": len(x), "mean_bps": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    for h in (24, 96, 192):
        S = A[A.h == h].copy()
        S["zb"] = pd.cut(S["z"], [-np.inf, -3, -2, -1, -0.3, 0.3, 1, 2, 3, np.inf])
        S["up"] = np.where(S["r30"] > 0, "r30+", "r30-")
        out[f"z_by_trend_h{h}"] = S.groupby(["zb", "up"], observed=True).apply(summ).round(2)
    S = A[A.h == 96].copy()
    S["r30q"] = pd.qcut(S["r30"], 5, labels=False)
    out["r30_quintile_h96"] = S.groupby("r30q").apply(summ).round(2)
    S["volq"] = pd.qcut(S["vol"], 4, labels=False)
    S["zb"] = pd.cut(S["z"], [-np.inf, -1.5, 1.5, np.inf])
    out["vol_x_z_h96"] = S.groupby(["volq", "zb"], observed=True).apply(summ).round(2)
    S24 = A[A.h == 24]
    out["weekday_h24"] = S24.groupby("wd").apply(summ).round(2)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = coin; t["win"] = w; tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["efq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_entry_fc_q"] = T.groupby("efq").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), med_fc=("entry_forecast", "median"),
        dur_h=("duration_minutes", lambda x: x.mean() / 60)).round(3)
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean())).round(3)
    return out
