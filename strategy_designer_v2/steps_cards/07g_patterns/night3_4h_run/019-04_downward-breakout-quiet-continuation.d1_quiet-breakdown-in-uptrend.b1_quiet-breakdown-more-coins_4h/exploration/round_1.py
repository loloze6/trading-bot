def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    grid_rows, ev_rows = [], []
    for coin, wins in data["bars"].items():
        # coin drift and usual move on grid
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
            up = c > hi.rolling(12).max().shift(1)
            dn = c < lo.rolling(12).min().shift(1)
            r30 = c / c.shift(180) - 1
            r3 = c / c.shift(18) - 1
            r1 = c / c.shift(6) - 1
            lr = np.log(c).diff()
            vol5 = lr.rolling(30).std()
            vol30 = lr.rolling(180).std()
            vratio = vol5 / vol30
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "fwd": fwd, "width": width, "up": up, "dn": dn,
                               "r30": r30, "r3z": r3 / (vol30 * np.sqrt(18)), "r1z": r1 / (vol30 * np.sqrt(6)),
                               "vratio": vratio, "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year})
            df["u"] = (df["fwd"] - drift)
            df["s"] = df["u"] / sd
            df["cell"] = np.arange(n) // H
            df = df[df["cell"] < (n - 1) // H]
            df = df.dropna(subset=["fwd"])
            g = df.iloc[::H]
            grid_rows.append(g)
            for side in ["up", "dn"]:
                e = df[df[side]].dropna(subset=["width", "r30"]).groupby("cell").head(1).copy()
                e["side"] = side
                ev_rows.append(e)
    G = pd.concat(grid_rows).dropna(subset=["width", "r30"])
    E = pd.concat(ev_rows)
    def summ(d, by):
        f = d.groupby(by, observed=True)
        out = f["s"].agg(["mean", "count"])
        out["u_mean_pct"] = f["u"].mean() * 100
        out["t"] = f["s"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan)
        out["coins_pos"] = f.apply(lambda x: (x.groupby("coin")["s"].mean() > 0).sum())
        out["coins"] = f["coin"].nunique()
        return out
    E["trend"] = np.where(E["r30"] > 0, "r30+", "r30-")
    E["wq"] = pd.qcut(E["width"], 4, labels=["narrow", "q2", "q3", "wide"])
    G["wq"] = pd.qcut(G["width"], 5, labels=False)
    G["absmove"] = G["fwd"].abs()
    absw = G.groupby("wq").agg(width_mean=("width", "mean"), absfwd_pct=("absmove", lambda x: x.mean() * 100), n=("absmove", "count"))
    G["r3q"] = pd.qcut(G["r3z"], 5, labels=False)
    G["r1q"] = pd.qcut(G["r1z"], 5, labels=False)
    G["vq"] = pd.qcut(G["vratio"], 5, labels=False)
    G["trend"] = np.where(G["r30"] > 0, "r30+", "r30-")
    G["r30q"] = pd.qcut(G["r30"], 5, labels=False)
    return {
        "events side x trend": summ(E, ["side", "trend"]),
        "events side x width quartile": summ(E, ["side", "wq"]),
        "grid abs move by width quintile": absw,
        "grid by past 3d return z quintile": summ(G, "r3q"),
        "grid by past 1d return z quintile": summ(G, "r1q"),
        "grid by vol ratio quintile": summ(G, "vq"),
        "grid by 30d return quintile": summ(G, "r30q"),
        "grid by weekday": summ(G, "wd"),
        "grid by year": summ(G, "year"),
    }
