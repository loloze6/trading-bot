def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            z = r24 / mabs
            r720 = c / c.shift(720) - 1
            r168 = c / c.shift(168) - 1
            hi = c.rolling(720, min_periods=120).max()
            dd = c / hi - 1
            for h in (24, 72, 120, 240):
                idx = np.arange(0, len(c) - h, h)
                fwd = (c.shift(-h) / c - 1).iloc[idx]
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "z": z.iloc[idx].values,
                    "r720": r720.iloc[idx].values, "r168": r168.iloc[idx].values, "dd": dd.iloc[idx].values,
                    "fwd": fwd.values}))
    df = pd.concat(rows).dropna(subset=["fwd"])
    g = df.groupby(["coin", "h"])["fwd"]
    df["drift"] = g.transform("mean"); df["sd"] = g.transform("std")
    df["ex"] = df["fwd"] - df["drift"]; df["st"] = df["ex"] / df["sd"]
    d = df.dropna(subset=["z"])
    d["zb"] = pd.cut(d["z"], [-99, -3, -2, -1.5, -1, 0, 1, 1.5, 2, 3, 99])
    def summ(x):
        return pd.Series({"n": len(x), "mean_ex_pct": 100*x["ex"].mean(), "mean_tot_pct": 100*x["fwd"].mean(),
                          "strength": x["st"].mean(), "t": stats.ttest_1samp(x["st"], 0).statistic if len(x) > 2 else np.nan})
    out["by_zbin_h"] = d.groupby(["h", "zb"]).apply(summ).reset_index()
    big = d[d["z"] <= -1.5].copy()
    big["trend30"] = np.where(big["r720"] > 0, "up30", "down30")
    big["trend7"] = np.where(big["r168"] > 0, "up7", "down7")
    big["ddb"] = pd.cut(big["dd"], [-1, -0.3, -0.15, -0.05, 0.01])
    out["plunge_by_trend30"] = big.groupby(["h", "trend30"]).apply(summ).reset_index()
    out["plunge_by_dd"] = big.groupby(["h", "ddb"]).apply(summ).reset_index()
    big120 = big[big.h == 120]
    out["plunge120_by_coin"] = big120.groupby("coin").apply(summ)
    upb = d[(d["z"] >= 1.5)].copy(); upb["trend30"] = np.where(upb["r720"] > 0, "up30", "down30")
    out["surge_by_trend30"] = upb.groupby(["h", "trend30"]).apply(summ).reset_index()
    # book
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bd.append(x.assign(coin=coin, w=w))
    bd = pd.concat(bd)
    out["book_by_coin"] = bd.groupby("coin")[["book_return", "coin_return"]].mean() * 100
    out["book_by_window"] = bd.groupby("w")[["book_return", "coin_return"]].mean().mul(100).round(3)
    tr = []
    for coin, wins in data["trades"].items():
        for w, x in wins.items():
            tr.append(x.assign(coin=coin))
    tr = pd.concat(tr)
    out["trades"] = tr.groupby("side")[["profit_loss_percent", "net_profit_loss_percent", "duration_minutes"]].agg(["mean", "count"])
    return out
