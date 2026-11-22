def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    hours = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float); hi = d["high"].astype(float); lo = d["low"].astype(float)
            r1 = np.log(c).diff()
            ret6 = c / c.shift(6) - 1
            ret42 = c / c.shift(42) - 1
            ret180 = c / c.shift(180) - 1
            rng6 = hi.rolling(6).max() / lo.rolling(6).min() - 1
            rmult = rng6 / rng6.rolling(180).mean()
            v42 = r1.rolling(42).std(); v360 = r1.rolling(360).std()
            vratio = v42 / v360
            fc = d["forecast"].astype(float)
            ts = pd.to_datetime(d["timestamp"])
            base = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(d)), "ret6": ret6, "ret42": ret42,
                                 "ret180": ret180, "rmult": rmult, "vratio": vratio, "v42": v42, "fc": fc,
                                 "close_pos": (c - lo.rolling(6).min()) / (hi.rolling(6).max() - lo.rolling(6).min())})
            for h in (6, 18, 42, 84):
                f = c.shift(-h) / c - 1
                g = base[(base["pos"] % h == 0)].copy()
                g["h"] = h; g["fwd"] = f[g.index].values
                rows.append(g)
            hr = pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday, "r": c.shift(-1) / c - 1})
            hours.append(hr)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    st = A.groupby(["coin", "h"])["fwd"].agg(["mean", "std"]).rename(columns={"mean": "drift", "std": "sd"})
    A = A.join(st, on=["coin", "h"])
    A["s"] = (A["fwd"] - A["drift"]) / A["sd"]
    def tab(feat, h, q=5, sub=None):
        B = A[(A["h"] == h)].dropna(subset=[feat])
        if sub is not None: B = B[sub(B)]
        B = B.copy()
        B["q"] = B.groupby("coin")[feat].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        g = B.groupby("q")["s"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["fmean"] = B.groupby("q")[feat].mean()
        return g.drop(columns="std").round(4)
    for h in (6, 18, 42, 84):
        out[f"ret6 quintile -> strength h{h}"] = tab("ret6", h)
    for h in (18, 84):
        out[f"rmult quintile h{h} (falls only)"] = tab("rmult", h, sub=lambda B: B["ret6"] < 0)
        out[f"ret42 quintile h{h}"] = tab("ret42", h)
        out[f"ret180 quintile h{h}"] = tab("ret180", h)
        out[f"vratio quintile h{h}"] = tab("vratio", h)
        out[f"close_pos quintile h{h}"] = tab("close_pos", h)
    H = pd.concat(hours).dropna()
    hh = H.groupby("hour")["r"].agg(["mean", "count", "std"]); hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    out["next-bar return by hour"] = hh.drop(columns="std").round(5)
    ww = H.groupby("wd")["r"].agg(["mean", "count", "std"]); ww["t"] = ww["mean"] / (ww["std"] / np.sqrt(ww["count"]))
    out["next-bar return by weekday"] = ww.drop(columns="std").round(5)
    # book by window
    days = data["days"]
    D = []
    for coin, wins in days.items():
        for w, df in wins.items():
            x = df[["day", "book_return", "coin_return"]].copy(); x["win"] = w; x["coin"] = coin; D.append(x)
    D = pd.concat(D)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bw = bk.groupby("win").agg(book=("book_return", "sum"), coin=("coin_return", "sum"), n=("day", "count"))
    out["book vs coins summed daily by window"] = bw.round(4)
    return out
