def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    hs = [2, 4, 6, 24]
    for coin, wins in data["bars"].items():
        # drift per horizon over all windows
        drift = {}
        sd = {}
        for h in hs:
            rr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.append(c[idx + h] / c[idx] - 1)
            rr = np.concatenate(rr)
            drift[h] = rr.mean(); sd[h] = rr.std()
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            v = b["volume"].astype(float).reset_index(drop=True)
            r1 = c.pct_change()
            scale = r1.abs().rolling(720, min_periods=240).mean()
            z = r1 / scale
            vr = v / v.rolling(720, min_periods=240).mean()
            df = pd.DataFrame({"z": z, "vr": vr})
            for h in hs:
                df[f"f{h}"] = (c.shift(-h) / c - 1 - drift[h]) / sd[h]
                df[f"raw{h}"] = c.shift(-h) / c - 1 - drift[h]
            df = df.iloc[::4]  # grid of 4
            df["coin"] = coin; df["w"] = w
            rows.append(df)
    d = pd.concat(rows).dropna()
    d["side"] = np.sign(d["z"])
    d["zb"] = pd.cut(d["z"].abs(), [0, 1, 2, 3, 5, 100])
    d["vb"] = pd.cut(d["vr"], [0, 1, 2, 4, 1000])
    for h in hs:
        d[f"cont{h}"] = d[f"raw{h}"] * d["side"]
    g = d.groupby(["vb", "zb"], observed=True)
    res = pd.DataFrame({"n": g.size()})
    for h in hs:
        res[f"cont{h}_bp"] = g[f"cont{h}"].mean() * 1e4
        res[f"t{h}"] = g[f"cont{h}"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan)
    out["continuation by vol x |z| (bp, signed with hour)"] = res.round(2)
    # rises only vs falls only, heavy volume
    hv = d[(d["vr"] > 2) & (d["z"].abs() > 2)]
    g2 = hv.groupby("side")
    r2 = pd.DataFrame({"n": g2.size()})
    for h in hs:
        r2[f"cont{h}_bp"] = g2[f"cont{h}"].mean() * 1e4
        r2[f"t{h}"] = g2[f"cont{h}"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
    out["heavy vol vr>2 |z|>2 by side"] = r2.round(2)
    # trades
    tr = pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    out["trades"] = pd.Series({
        "n": len(tr),
        "mean gross %": tr["profit_loss_percent"].mean(),
        "mean net %": tr["net_profit_loss_percent"].mean(),
        "median duration h": tr["duration_minutes"].median() / 60,
        "share short": (tr["side"] == "SHORT").mean(),
        "win rate gross": (tr["profit_loss_percent"] > 0).mean(),
    }).round(4)
    # book daily
    dd = pd.concat([x for wins in data["days"].values() for x in wins.values()])
    out["book"] = pd.Series({"mean book ret": dd["book_return"].mean(),
                             "mean coin ret": dd["coin_return"].mean()})
    # time in market
    bb = pd.concat([x for wins in data["bars"].values() for x in wins.values()])
    al = bb["postRebalance_current_allocation"]
    out["exposure"] = pd.Series({"share bars nonzero": (al.abs() > 1e-6).mean(),
                                 "mean |alloc| when in": al[al.abs() > 1e-6].abs().mean(),
                                 "share thin regime": (bb["regime"] == "mean_reversion").mean()})
    return out
