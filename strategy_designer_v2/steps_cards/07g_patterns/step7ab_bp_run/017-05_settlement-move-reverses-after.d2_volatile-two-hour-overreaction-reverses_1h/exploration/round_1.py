def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd24 = r1.rolling(24).std()
            usual = sd24.rolling(720, min_periods=240).mean() * np.sqrt(2)
            z = (c / c.shift(2) - 1) / usual
            vr = sd24 / sd24.rolling(720, min_periods=240).mean()
            r24 = c / c.shift(24) - 1
            hour = pd.to_datetime(b["timestamp"]).dt.hour
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr, "r24p": r24 / (usual / np.sqrt(2) * np.sqrt(24)),
                               "hour": hour, "pos": np.arange(len(b))})
            for h in (8, 24, 48):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # drift per coin per h
    res = []
    for h in (8, 24, 48):
        g = d[d["pos"] % h == 0].copy()
        drift = g.groupby("coin")[f"f{h}"].transform("mean")
        usualh = g.groupby("coin")[f"f{h}"].transform("std")
        g["u"] = -np.sign(g["z"]) * (g[f"f{h}"] - drift)
        g["s"] = g["u"] / usualh
        g = g.dropna(subset=["u", "z", "vr"])
        g["zb"] = pd.cut(g["z"].abs(), [0, 1, 2, 3, 4, 100])
        g["vb"] = pd.cut(g["vr"], [0, 0.8, 1.0, 1.5, 2.5, 100])
        for (zb), gg in g[g["vr"] >= 1].groupby("zb"):
            t = gg["u"].mean() / (gg["u"].std() / np.sqrt(len(gg)))
            res.append(("hi-vol", h, str(zb), len(gg), gg["u"].mean() * 1e4, t, gg["s"].mean()))
        for (zb), gg in g[g["vr"] < 1].groupby("zb"):
            t = gg["u"].mean() / (gg["u"].std() / np.sqrt(len(gg)))
            res.append(("lo-vol", h, str(zb), len(gg), gg["u"].mean() * 1e4, t, gg["s"].mean()))
        if h == 24:
            gz = g[g["z"].abs() >= 2]
            vt = gz.groupby("vb")["u"].agg(["count", "mean", "std"])
            vt["bps"] = vt["mean"] * 1e4; vt["t"] = vt["mean"] / (vt["std"] / np.sqrt(vt["count"]))
            out["24h |z|>=2 by volratio"] = vt[["count", "bps", "t"]]
            ht = gz.groupby(gz["hour"] // 4 * 4)["u"].agg(["count", "mean", "std"])
            ht["bps"] = ht["mean"] * 1e4; ht["t"] = ht["mean"] / (ht["std"] / np.sqrt(ht["count"]))
            out["24h |z|>=2 by hour block"] = ht[["count", "bps", "t"]]
            ct = gz.groupby("coin")["u"].agg(["count", "mean", "std"])
            ct["bps"] = ct["mean"] * 1e4; ct["t"] = ct["mean"] / (ct["std"] / np.sqrt(ct["count"]))
            out["24h |z|>=2 by coin"] = ct[["count", "bps", "t"]]
            # 24h move (longer-period) reversal / continuation: signed by -sign(r24p)
            g["u24"] = -np.sign(g["r24p"]) * (g[f"f{h}"] - drift)
            g["rb"] = pd.cut(g["r24p"].abs(), [0, 1, 2, 3, 100])
            rt = g.groupby("rb")["u24"].agg(["count", "mean", "std"])
            rt["bps"] = rt["mean"] * 1e4; rt["t"] = rt["mean"] / (rt["std"] / np.sqrt(rt["count"]))
            out["next24h vs prior 24h move (contrarian sign)"] = rt[["count", "bps", "t"]]
    out["contrarian unusual move by |z2h|, h, vol"] = pd.DataFrame(res, columns=["vol", "h", "absz", "n", "bps", "t", "strength"])
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    tr["hrs"] = tr["duration_minutes"] / 60
    tr["hb"] = pd.cut(tr["hrs"], [0, 8, 9, 16, 48, 1e5])
    tt = tr.groupby("hb").agg(n=("hrs", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    out["trades by duration"] = tt
    out["trades overall"] = tr[["profit_loss_percent", "net_profit_loss_percent"]].mean()
    return out
