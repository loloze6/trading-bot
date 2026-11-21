def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        wl = list(wins.keys())
        for wi, (w, b) in enumerate(wins.items()):
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd24 = r1.rolling(24).std()
            m = sd24.rolling(720, min_periods=240).mean()
            df = pd.DataFrame({"coin": coin, "half": "early" if wi < len(wl) / 2 else "late",
                               "z2": (c / c.shift(2) - 1) / (m * np.sqrt(2)),
                               "z24": (c / c.shift(24) - 1) / (m * np.sqrt(24)),
                               "z72": (c / c.shift(72) - 1) / (m * np.sqrt(72)),
                               "vr": sd24 / m, "pos": np.arange(len(b))})
            for h in (24, 72):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    def tab(g, key, val):
        t = g.groupby(key, observed=True)[val].agg(["count", "mean", "std"])
        t["bps"] = t["mean"] * 1e4; t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t[["count", "bps", "t"]]
    for phase in (0, 12):
        g = d[d["pos"] % 24 == phase].copy()
        drift = g.groupby("coin")["f24"].transform("mean")
        g["u24"] = -np.sign(g["z24"]) * (g["f24"] - drift)
        g["u2"] = -np.sign(g["z2"]) * (g["f24"] - drift)
        g = g.dropna(subset=["u24", "vr", "z2"])
        g["rb"] = pd.cut(g["z24"].abs(), [0, 1, 2, 3, 100])
        g["vol"] = np.where(g["vr"] >= 1, "hi", "lo")
        out[f"p{phase} next24 contra prior24 by size x vol"] = tab(g, ["vol", "rb"], "u24")
        gz = g[g["z24"].abs() >= 1]
        out[f"p{phase} prior24 |z|>=1: by coin"] = tab(gz, "coin", "u24")
        out[f"p{phase} prior24 |z|>=1: by half"] = tab(gz, "half", "u24")
        out[f"p{phase} prior24 |z|>=1: by direction of prior move"] = tab(gz.assign(up=np.sign(gz["z24"])), "up", "u24")
        g3 = g[(g["z2"].abs() >= 3) & (g["vr"] >= 1)]
        out[f"p{phase} hi-vol |z2|>=3 next24: by half"] = tab(g3, "half", "u2")
    # 72h reversal of 72h move
    g = d[d["pos"] % 72 == 0].copy()
    drift = g.groupby("coin")["f72"].transform("mean")
    g["u"] = -np.sign(g["z72"]) * (g["f72"] - drift)
    g = g.dropna(subset=["u", "vr"])
    g["rb"] = pd.cut(g["z72"].abs(), [0, 1, 2, 100])
    out["next72 contra prior72 by size"] = tab(g, "rb", "u")
    return out
