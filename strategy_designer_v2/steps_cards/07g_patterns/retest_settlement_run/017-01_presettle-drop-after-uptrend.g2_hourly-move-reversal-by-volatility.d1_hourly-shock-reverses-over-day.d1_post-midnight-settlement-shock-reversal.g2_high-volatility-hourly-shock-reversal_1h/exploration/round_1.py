def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    drift = {}
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            c = b["close"].astype(float).reset_index(drop=True)
            v = b["volume"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            vol24 = r1.rolling(24).std()
            vol720 = r1.rolling(720, min_periods=240).std()
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "z1": r1 / vol24,
                "z4": (c / c.shift(4) - 1) / (vol24 * 2),
                "z24": (c / c.shift(24) - 1) / (vol720 * np.sqrt(24)),
                "vr": vol24 / vol720,
                "vrel": v / v.rolling(24).mean(),
                "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                "pos": np.arange(len(c)),
            })
            for h in (1, 4, 24, 72):
                df[f"f{h}"] = c.shift(-h) / c - 1
            recs.append(df)
    D = pd.concat(recs, ignore_index=True)
    for h in (1, 4, 24, 72):
        g = D[D["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    def table(sig, h, bins, cond=None, label=None):
        g = D[(D["pos"] % h == 0)].copy()
        if cond is not None:
            g = g[cond(g)]
        g = g.dropna(subset=[sig, f"f{h}"])
        g["ex"] = g[f"f{h}"] - g["coin"].map(drift[h])
        g["fade"] = -np.sign(g[sig]) * g["ex"]
        g["b"] = pd.cut(g[sig].abs(), bins)
        t = g.groupby("b", observed=True)["fade"].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["mean_pct"] = t["mean"] * 100
        return t[["count", "mean_pct", "t"]]
    zb = [0, 1, 2, 3, 5, 100]
    out["z1 fade by |z|, h1"] = table("z1", 1, zb)
    out["z1 fade by |z|, h4"] = table("z1", 4, zb)
    out["z1 fade by |z|, h24, vr>1"] = table("z1", 24, zb, lambda g: g["vr"] > 1)
    out["z1 fade by |z|, h24, all"] = table("z1", 24, zb)
    out["z4 fade by |z|, h24"] = table("z4", 24, zb)
    out["z24 fade by |z|, h24"] = table("z24", 24, [0, 0.5, 1, 2, 3, 100])
    out["z24 fade by |z|, h72"] = table("z24", 72, [0, 0.5, 1, 2, 3, 100])
    out["z24 fade by |z|, h72, vr>1.5"] = table("z24", 72, [0, 0.5, 1, 2, 3, 100], lambda g: g["vr"] > 1.5)
    # shock with volume
    out["z1|>2 fade h24 by volume rel"] = table("vrel", 24, [0, 0.5, 1, 2, 4, 100], lambda g: g["z1"].abs() > 2) \
        if False else None
    g = D[(D["pos"] % 24 == 0)].dropna(subset=["z1", "f24", "vrel"]).copy()
    g["ex"] = g["f24"] - g["coin"].map(drift[24]); g["fade"] = -np.sign(g["z1"]) * g["ex"]
    g = g[g["z1"].abs() > 1.5]
    g["vb"] = pd.cut(g["vrel"], [0, 0.7, 1, 1.5, 2.5, 1000])
    t = g.groupby("vb", observed=True)["fade"].agg(["count", "mean", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"])); t["mean"] *= 100
    out["|z1|>1.5 fade h24 by volume rel"] = t[["count", "mean", "t"]]
    # by hour of z1 shocks, h4
    g = D[(D["pos"] % 4 == 0)].dropna(subset=["z1", "f4"]).copy()
    g["ex"] = g["f4"] - g["coin"].map(drift[4]); g["fade"] = -np.sign(g["z1"]) * g["ex"] * g["z1"].abs().clip(upper=5)
    t = g.groupby("hour")["fade"].agg(["count", "mean", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"])); t["mean"] *= 100
    out["z1-weighted fade h4 by hour"] = t[["count", "mean", "t"]]
    # coin-level z24 h72 slope t
    g = D[(D["pos"] % 72 == 0)].dropna(subset=["z24", "f72"]).copy()
    g["ex"] = g["f72"] - g["coin"].map(drift[72])
    res = {}
    for coin, gg in g.groupby("coin"):
        s = stats.linregress(gg["z24"].clip(-5, 5), gg["ex"])
        res[coin] = {"n": len(gg), "slope_pct": s.slope * 100, "t": s.slope / s.stderr}
    out["z24 -> f72 slope by coin"] = pd.DataFrame(res).T
    # book
    days = pd.concat([d.assign(coin=c, w=w) for c, ws in data["days"].items() for w, d in ws.items()])
    days["year"] = pd.to_datetime(days["day"]).dt.year
    out["book daily mean % by year"] = days.groupby("year")[["book_return", "coin_return"]].mean() * 100
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    out["trades gross vs net by side"] = tr.groupby("side")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"])
    out = {k: v for k, v in out.items() if v is not None}
    return out
