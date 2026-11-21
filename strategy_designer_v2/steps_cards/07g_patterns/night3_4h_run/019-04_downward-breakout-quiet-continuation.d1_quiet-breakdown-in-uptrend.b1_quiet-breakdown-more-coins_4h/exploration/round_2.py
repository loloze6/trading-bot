def explore(data):
    import numpy as np, pandas as pd
    H = 18
    grid_rows, ev_rows = [], []
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets.extend(list(c[idx + H] / c[idx] - 1))
        rets = np.array(rets)
        if len(rets) < 20:
            continue
        drift, sd = rets.mean(), rets.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, hi, lo = b["close"], b["high"], b["low"]
            n = len(b)
            if n < 200:
                continue
            rng = (hi - lo) / c
            mbr = rng.rolling(180).mean().shift(1)
            span = (hi.rolling(12).max().shift(1) - lo.rolling(12).min().shift(1)) / c
            width = span / (12 * mbr)
            dn = c < lo.rolling(12).min().shift(1)
            up = c > hi.rolling(12).max().shift(1)
            r30 = c / c.shift(180) - 1
            r1 = c / c.shift(6) - 1
            r2 = c / c.shift(12) - 1
            lr = np.log(c).diff()
            vol30 = lr.rolling(180).std()
            vratio = lr.rolling(30).std() / vol30
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-6) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "fwd": fwd, "width": width, "dn": dn, "up": up,
                               "r30": r30, "r1z": r1 / (vol30 * np.sqrt(6)), "r2z": r2 / (vol30 * np.sqrt(12)),
                               "vratio": vratio, "year": ts.dt.year})
            df["u"] = df["fwd"] - drift
            df["s"] = df["u"] / sd
            df["u1"] = fwd1
            df["cell"] = np.arange(n) // H
            df = df[df["cell"] < (n - 1) // H].dropna(subset=["fwd"])
            grid_rows.append(df.iloc[::H])
            e = df[df["dn"]].dropna(subset=["width", "r30", "r2z"]).groupby("cell").head(1).copy()
            ev_rows.append(e)
    G = pd.concat(grid_rows).dropna(subset=["width", "r30", "r1z", "vratio"])
    E = pd.concat(ev_rows)
    def summ(d, by):
        f = d.groupby(by, observed=True)
        out = f["s"].agg(["mean", "count"])
        out["u_mean_pct"] = f["u"].mean() * 100
        out["t"] = f["s"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan)
        out["coins_pos"] = f.apply(lambda x: (x.groupby("coin")["s"].mean() > 0).sum())
        out["coins"] = f["coin"].nunique()
        return out
    E["wd10"] = pd.qcut(E["width"], 10, labels=False)
    E["trend"] = np.where(E["r30"] > 0, "r30+", "r30-")
    E["wq"] = pd.qcut(E["width"], 4, labels=["narrow", "q2", "q3", "wide"])
    E["era"] = pd.cut(E["year"], [2000, 2020, 2022, 2030], labels=["<=2020", "2021-22", "2023+"])
    E["r2q"] = pd.qcut(E["r2z"], 4, labels=False)
    G["r1d10"] = pd.qcut(G["r1z"], 10, labels=False)
    G["r1q"] = pd.qcut(G["r1z"], 5, labels=False)
    G["vq"] = pd.qcut(G["vratio"], 5, labels=False)
    G["trend"] = np.where(G["r30"] > 0, "r30+", "r30-")
    G["era"] = pd.cut(G["year"], [2000, 2020, 2022, 2030], labels=["<=2020", "2021-22", "2023+"])
    low1 = G[G["r1q"] == 0]
    return {
        "dn events by width decile": summ(E, "wd10"),
        "dn events width quartile x trend": summ(E, ["wq", "trend"]),
        "dn events width quartile x era": summ(E, ["wq", "era"]),
        "dn events width quartile x past-2d move quartile": summ(E, ["wq", "r2q"]),
        "grid by 1d return z decile": summ(G, "r1d10"),
        "grid lowest 1d quintile by trend": summ(low1, "trend"),
        "grid lowest 1d quintile by era": summ(low1, "era"),
        "grid 1d quintile x vol ratio top/other": summ(G.assign(vt=(G["vq"] == 4)), ["r1q", "vt"]),
    }
