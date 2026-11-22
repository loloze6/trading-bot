import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = {"1d":6, "3d":18, "7d":42, "14d":84}
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r6 = c / c.shift(6) - 1
            usual = r6.abs().rolling(180, min_periods=45).mean()
            z = r6 / usual
            rng = (hi.rolling(6).max() - lo.rolling(6).min()) / c.shift(6)
            rr = rng / rng.rolling(180, min_periods=45).mean()
            r42p = c / c.shift(42) - 1
            vlong = r6.abs().rolling(540, min_periods=180).mean()
            vr = usual / vlong
            r1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            hourly.append(pd.DataFrame({"hour": ts.dt.hour, "wd": ts.dt.weekday, "r1": r1, "z": z, "coin": coin}))
            for hn, h in H.items():
                idx = np.arange(0, len(b) - h, h)
                fwd = (c.shift(-h) / c - 1).iloc[idx]
                rows.append(pd.DataFrame({"coin": coin, "win": w, "h": hn, "fwd": fwd.values,
                    "z": z.iloc[idx].values, "rr": rr.iloc[idx].values, "prior7": r42p.iloc[idx].values,
                    "vr": vr.iloc[idx].values}))
    d = pd.concat(rows, ignore_index=True)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["sd"] = d.groupby(["coin", "h"])["fwd"].transform("std")
    d["ex"] = d["fwd"] - d["drift"]; d["str"] = d["ex"] / d["sd"]
    d = d.dropna(subset=["z"])
    d["zbin"] = pd.cut(d["z"], [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf])
    def agg(g):
        n = len(g); m = g["str"].mean(); s = g["str"].std()
        return pd.Series({"n": n, "ex_mean": g["ex"].mean(), "strength": m, "t": m / (s / np.sqrt(n)) if n > 1 else np.nan})
    out = {}
    out["by_z_horizon"] = d.groupby(["h", "zbin"], observed=True).apply(agg).unstack(0)[["strength", "t", "n"]].round(3)
    d["panic"] = np.where((d["z"] < -1.5) & (d["rr"] > 1.8), "panic", np.where(d["z"] < -1.5, "fall_norange", "other"))
    out["panic_vs"] = d.groupby(["h", "panic"]).apply(agg).round(3)
    d["rrbin"] = pd.qcut(d["rr"], 5, labels=False, duplicates="drop")
    out["by_rangeratio"] = d.groupby(["h", "rrbin"]).apply(agg)[["strength", "t", "n"]].unstack(0).round(3)
    d["vrbin"] = pd.qcut(d["vr"], 5, labels=False, duplicates="drop")
    out["by_volratio"] = d.groupby(["h", "vrbin"]).apply(agg)[["strength", "t", "n"]].unstack(0).round(3)
    d["p7bin"] = pd.qcut(d["prior7"], 5, labels=False)
    out["by_prior7d"] = d.groupby(["h", "p7bin"]).apply(agg)[["strength", "t", "n"]].unstack(0).round(3)
    corr = {}
    for hn in H:
        g = d[d.h == hn].dropna(subset=["z", "str"])
        r, p = stats.pearsonr(g["z"].clip(-6, 6), g["str"]); corr[hn] = (round(r, 4), round(p, 4), len(g))
    out["corr_z_str"] = pd.DataFrame(corr, index=["r", "p", "n"])
    hh = pd.concat(hourly).dropna(subset=["r1"])
    def tt(g):
        return pd.Series({"mean_bp": g["r1"].mean() * 1e4, "t": g["r1"].mean() / (g["r1"].std() / np.sqrt(len(g))), "n": len(g)})
    out["by_hour"] = hh.groupby("hour").apply(tt).round(2)
    out["by_weekday"] = hh.groupby("wd").apply(tt).round(2)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; x["prev_coin"] = x["coin_return"].shift(1); dd.append(x)
    dd = pd.concat(dd).dropna(subset=["book_return"])
    q = dd["book_return"].quantile([0.02, 0.98])
    out["book_tails"] = pd.DataFrame({
        "worst2pct": dd[dd.book_return <= q.iloc[0]][["book_return", "coin_return", "prev_coin"]].mean(),
        "best2pct": dd[dd.book_return >= q.iloc[1]][["book_return", "coin_return", "prev_coin"]].mean(),
        "all": dd[["book_return", "coin_return", "prev_coin"]].mean()})
    alloc = pd.concat([b[["postRebalance_current_allocation"]].assign(coin=c) for c, ws in data["bars"].items() for b in ws.values()])
    out["mean_alloc_by_coin"] = alloc.groupby("coin")["postRebalance_current_allocation"].agg(["mean", lambda s: (s.abs() > 0.01).mean()]).round(3)
    out["book_by_coin"] = dd.groupby("coin")[["book_return", "coin_return"]].mean().round(5)
    return out
