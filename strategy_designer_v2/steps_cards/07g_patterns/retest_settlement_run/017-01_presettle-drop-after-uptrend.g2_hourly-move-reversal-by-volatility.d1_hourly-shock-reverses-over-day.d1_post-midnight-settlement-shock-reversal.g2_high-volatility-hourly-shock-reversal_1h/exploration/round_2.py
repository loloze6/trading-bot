def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            vol720 = r1.rolling(720, min_periods=240).std()
            vol24 = r1.rolling(24).std()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(c)),
                               "year": ts.dt.year, "hour": ts.dt.hour,
                               "r24": c / c.shift(24) - 1,
                               "z24": (c / c.shift(24) - 1) / (vol720 * np.sqrt(24)),
                               "vr": vol24 / vol720})
            for h in (12, 24, 48):
                df[f"f{h}"] = c.shift(-h) / c - 1
            recs.append(df)
    D = pd.concat(recs, ignore_index=True)
    def grid(h):
        g = D[D["pos"] % h == 0].dropna(subset=["z24", f"f{h}"]).copy()
        dr = g.groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g["coin"].map(dr)
        g["fade"] = -np.sign(g["z24"]) * g["ex"]
        return g
    zb = [0, 0.5, 1, 2, 3, 100]
    for h in (12, 24, 48):
        g = grid(h)
        g["b"] = pd.cut(g["z24"].abs(), zb)
        t = g.groupby("b", observed=True)["fade"].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"])); t["mean"] *= 100
        out[f"z24 fade by |z| h{h}"] = t[["count", "mean", "t"]]
    g = grid(24)
    res = {}
    for coin, gg in g.groupby("coin"):
        s = stats.linregress(gg["z24"].clip(-5, 5), gg["ex"])
        m = gg[gg["z24"].abs() > 1]["fade"]
        res[coin] = {"n": len(gg), "slope_pct": s.slope * 100, "t": s.slope / s.stderr,
                     "n_big": len(m), "fade_big_pct": m.mean() * 100,
                     "t_big": m.mean() / (m.std() / np.sqrt(len(m)))}
    out["z24->f24 by coin"] = pd.DataFrame(res).T
    res = {}
    for y, gg in g.groupby("year"):
        s = stats.linregress(gg["z24"].clip(-5, 5), gg["ex"])
        res[y] = {"n": len(gg), "slope_pct": s.slope * 100, "t": s.slope / s.stderr}
    out["z24->f24 by year"] = pd.DataFrame(res).T
    gb = g[g["z24"].abs() > 1].copy()
    gb["side"] = np.where(gb["z24"] > 0, "after rise", "after drop")
    gb["vrb"] = pd.cut(gb["vr"], [0, 0.8, 1.2, 2, 100])
    t = gb.groupby("side")["fade"].agg(["count", "mean", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"])); t["mean"] *= 100
    out["|z24|>1 fade h24 by side"] = t[["count", "mean", "t"]]
    t = gb.groupby("vrb", observed=True)["fade"].agg(["count", "mean", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"])); t["mean"] *= 100
    out["|z24|>1 fade h24 by vol ratio"] = t[["count", "mean", "t"]]
    s = stats.linregress(g["z24"].clip(-5, 5), g["ex"])
    out["pooled z24 slope h24"] = pd.Series({"n": len(g), "slope_pct": s.slope * 100, "t": s.slope / s.stderr})
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    tr["dur_h"] = tr["duration_minutes"] / 60
    out["trades by side"] = tr.groupby("side").agg(n=("dur_h", "size"), dur_h_med=("dur_h", "median"),
        dur_h_mean=("dur_h", "mean"), pl_med=("profit_loss_percent", "median"),
        pl_mean=("profit_loss_percent", "mean"), win=("profit_loss_percent", lambda x: (x > 0).mean()))
    tr["db"] = pd.cut(tr["dur_h"], [0, 24, 48, 168, 1e6])
    out["trades pl by side and duration"] = tr.groupby(["side", "db"], observed=True)["profit_loss_percent"].agg(["count", "mean"])
    return out
