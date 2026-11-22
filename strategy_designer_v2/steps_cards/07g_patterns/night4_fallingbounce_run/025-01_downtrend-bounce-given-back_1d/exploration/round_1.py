import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=20).std()
            z = r / sd
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            # past 5-day and 20-day return
            p5 = c / c.shift(5) - 1
            p20 = c / c.shift(20) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n), "z": z, "r": r, "sd": sd,
                               "f5": f5, "f1": f1, "p5": p5, "p20": p20,
                               "falling": (b["regime"] == "mean_reversion").values,
                               "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    grid = d[d["pos"] % 5 == 0].copy()
    drift = grid.groupby("coin")["f5"].mean()
    sd5 = grid.groupby("coin")["f5"].std()
    grid["u5"] = grid["f5"] - grid["coin"].map(drift)
    grid["s5"] = grid["u5"] / grid["coin"].map(sd5)
    g = grid.dropna(subset=["z", "u5"])
    g["zb"] = pd.cut(g["z"], [-np.inf, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, np.inf])
    def summ(x):
        return pd.Series({"n": len(x), "mean_u5": x["u5"].mean(), "mean_s5": x["s5"].mean(),
                          "t": x["u5"].mean() / (x["u5"].std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["z_by_regime"] = g.groupby(["falling", "zb"]).apply(summ)
    # past 20-day return quintile (trend continuation/reversal) by regime
    g2 = g.dropna(subset=["p20"]).copy()
    g2["p20q"] = g2.groupby("coin")["p20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["p20q_by_regime"] = g2.groupby(["falling", "p20q"]).apply(summ)
    g3 = g.copy()
    g3["p5q"] = g3.groupby("coin")["p5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["p5q_by_regime"] = g3.groupby(["falling", "p5q"]).apply(summ)
    # vol level
    g4 = g.copy()
    g4["sdq"] = g4.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["volq"] = g4.groupby(["falling", "sdq"]).apply(summ)
    # per-coin z slope, correlation z vs s5 by regime
    cc = []
    for (coin, fl), x in g.groupby(["coin", "falling"]):
        rr, p = stats.spearmanr(x["z"], x["s5"])
        cc.append({"coin": coin, "falling": fl, "n": len(x), "rho": rr, "p": p})
    out["coin_rho_z"] = pd.DataFrame(cc)
    # weekday daily returns
    dd = d.dropna(subset=["f1"]).copy()
    dd["u1"] = dd["f1"] - dd.groupby("coin")["f1"].transform("mean")
    out["weekday_next1"] = dd.groupby((dd["wd"] + 1) % 7).apply(lambda x: pd.Series({"n": len(x), "mean": x["u1"].mean(), "t": x["u1"].mean() / (x["u1"].std() / np.sqrt(len(x)))}))
    # book: days
    bk = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; bk.append(x)
    bk = pd.concat(bk)
    bd = bk.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bd.groupby(level=0).agg(["mean", "count"]).iloc[:, [0, 2, 3]]
    # book: by year
    bk["yr"] = pd.to_datetime(bk["day"]).dt.year
    out["book_by_year"] = bk.groupby("yr")[["book_return", "coin_return"]].mean()
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades"] = tr.groupby("coin").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), mean_gross=("profit_loss_percent", "mean"), dur_days=("duration_minutes", lambda s: s.mean() / 1440))
    return out
