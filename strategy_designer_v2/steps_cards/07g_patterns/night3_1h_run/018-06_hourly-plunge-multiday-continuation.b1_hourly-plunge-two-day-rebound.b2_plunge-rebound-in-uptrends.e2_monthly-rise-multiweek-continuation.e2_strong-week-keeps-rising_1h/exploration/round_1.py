import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    def fwd_cases(H, feat_fn, nb=5):
        rows = []
        for c, ws in bars.items():
            rets = []
            per = {}
            for w, df in ws.items():
                cl = df["close"].reset_index(drop=True).astype(float)
                f = feat_fn(df.reset_index(drop=True), cl)
                idx = np.arange(0, len(cl) - H, H)
                r = cl.values[idx + H] / cl.values[idx] - 1
                rets.extend(r.tolist())
                per[w] = (r, f.values[idx] if f is not None else None)
            mu, sd = np.mean(rets), np.std(rets)
            for w, (r, fv) in per.items():
                for a, b in zip(r, fv):
                    rows.append((c, w, a - mu, (a - mu) / sd, b))
        d = pd.DataFrame(rows, columns=["coin", "w", "unus", "str", "feat"]).dropna()
        d["q"] = d.groupby("coin")["feat"].transform(lambda s: pd.qcut(s.rank(method="first"), nb, labels=False))
        g = d.groupby("q").agg(n=("str", "size"), unus=("unus", "mean"), strength=("str", "mean"), sd=("str", "std"), feat=("feat", "mean"))
        g["t"] = g["strength"] / (g["sd"] / np.sqrt(g["n"]))
        return g.drop(columns="sd")
    ret = lambda k: (lambda df, cl: cl / cl.shift(k) - 1)
    out["fwd7d_by_past7d"] = fwd_cases(168, ret(168))
    out["fwd7d_by_past30d"] = fwd_cases(168, ret(720))
    out["fwd1d_by_past1d"] = fwd_cases(24, ret(24))
    out["fwd3d_by_past1d"] = fwd_cases(72, ret(24))
    out["fwd1d_by_past4h"] = fwd_cases(24, ret(4))
    vol = lambda df, cl: np.log(cl).diff().rolling(168).std()
    out["fwd7d_by_vol7d"] = fwd_cases(168, vol)
    hi = lambda df, cl: cl / df["high"].astype(float).rolling(720).max() - 1
    out["fwd7d_by_dist30dhigh"] = fwd_cases(168, hi)
    out["fwd3d_by_dist30dhigh"] = fwd_cases(72, hi)
    volchg = lambda df, cl: df["volume"].astype(float).rolling(24).sum() / df["volume"].astype(float).rolling(720).sum() * 30
    out["fwd3d_by_volume_surge"] = fwd_cases(72, volchg)
    # hour of day, weekday
    hr = []
    for c, ws in bars.items():
        for w, df in ws.items():
            ts = pd.to_datetime(df["timestamp"]); cl = df["close"].astype(float)
            r = (cl.shift(-1) / cl - 1)
            s = r.std()
            hr.append(pd.DataFrame({"h": ts.dt.hour.values, "wd": ts.dt.weekday.values, "z": (r / s).values}))
    hr = pd.concat(hr).dropna()
    gh = hr.groupby("h")["z"].agg(["mean", "std", "size"]); gh["t"] = gh["mean"] / (gh["std"] / np.sqrt(gh["size"]))
    out["hour_next1h_z"] = gh[["mean", "t"]]
    gw = hr.groupby("wd")["z"].agg(["mean", "std", "size"]); gw["t"] = gw["mean"] / (gw["std"] / np.sqrt(gw["size"]))
    out["weekday_next1h_z"] = gw[["mean", "t"]]
    # book by year, window
    bk = []
    for c, ws in days.items():
        for w, df in ws.items():
            d = df.copy(); d["w"] = w; d["yr"] = pd.to_datetime(d["day"]).dt.year; bk.append(d)
    bk = pd.concat(bk).dropna(subset=["book_return"])
    out["book_by_year"] = bk.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    worst = bk.nsmallest(int(len(bk) * 0.01), "book_return")
    out["worst1pct_days_coin_ret_mean"] = float(worst["coin_return"].mean())
    out["worst1pct_by_year"] = worst.groupby("yr").size()
    return out
