def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for H in (12, 24):
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values; n = len(c)
                idx = np.arange(0, n - H, H)
                fwd = c[idx + H] / c[idx] - 1
                p72 = np.full(len(idx), np.nan); ok = idx >= 72
                p72[ok] = c[idx[ok]] / c[idx[ok] - 72] - 1
                p168 = np.full(len(idx), np.nan); ok = idx >= 168
                p168[ok] = c[idx[ok]] / c[idx[ok] - 168] - 1
                lr = np.log(c[1:] / c[:-1])
                vol = pd.Series(np.r_[np.nan, lr]).rolling(72).std().values[idx]
                rows.append(pd.DataFrame({"H": H, "coin": coin, "w": w, "fwd": fwd, "p72": p72,
                                          "p168": p168, "vol": vol}))
    g = pd.concat(rows, ignore_index=True)
    g["ex"] = g["fwd"] - g.groupby(["H", "coin"])["fwd"].transform("mean")
    g["z72"] = g["p72"] / (g["vol"] * np.sqrt(72))
    for H in (12, 24):
        for col in ("p72", "p168", "z72"):
            d = g[(g.H == H)].dropna(subset=[col, "ex"]).copy()
            d["q"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x, 5, labels=False))
            t = d.groupby("q")["ex"].agg(["mean", "count", "std"])
            t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
            for cn in d.coin.unique():
                t[cn] = d[d.coin == cn].groupby("q")["ex"].mean()
            out[f"H{H} excess by {col} quintile"] = t.round(5)
            if col == "p72":
                r = stats.spearmanr(d[col], d["ex"])
                out[f"H{H} spearman p72"] = f"rho={r[0]:.4f} p={r[1]:.4f} n={len(d)}"
    d = g[g.H == 12].dropna(subset=["p72", "ex"]).copy()
    d["q"] = d.groupby("coin")["p72"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["H12 p72 Q0 excess by window"] = d[d.q == 0].groupby("w")["ex"].agg(["mean", "count"]).round(5)
    out["H12 p72 Q1 excess by window"] = d[d.q == 1].groupby("w")["ex"].agg(["mean", "count"]).round(5)
    # book: gross vs fee per day
    hh = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            v = b["postRebalance_total_value"].values
            vr = np.r_[v[1:] / v[:-1] - 1, np.nan]
            hh.append(pd.DataFrame({"coin": coin, "gain": b["postRebalance_current_allocation"].values * r1,
                                    "vr": vr, "absch": b["allocation_change"].abs().values}))
    h = pd.concat(hh, ignore_index=True).dropna()
    out["hourly book vs gross"] = pd.Series({"gross gain/h": h.gain.mean(), "book ret/h": h.vr.mean(),
                                             "cost/h": h.gain.mean() - h.vr.mean(),
                                             "mean |alloc change|/h": h.absch.mean()}).round(7)
    T = []
    for coin, wins in data["trades"].items():
        for w, t2 in wins.items():
            T.append(t2)
    T = pd.concat(T, ignore_index=True)
    T["dq"] = pd.qcut(T["duration_minutes"], 4, labels=False, duplicates="drop")
    out["trades by duration quartile"] = T.groupby("dq").agg(n=("profit_loss_percent", "size"),
        mean_pl=("profit_loss_percent", "mean"), win=("profit_loss_percent", lambda x: (x > 0).mean()),
        med_dur=("duration_minutes", "median")).round(4)
    out["trade pl quantiles"] = T["profit_loss_percent"].quantile([.01, .05, .25, .5, .75, .95, .99]).round(3)
    return out
