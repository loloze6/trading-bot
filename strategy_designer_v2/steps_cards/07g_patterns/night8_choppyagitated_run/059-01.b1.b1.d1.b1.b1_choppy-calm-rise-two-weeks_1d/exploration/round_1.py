def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for coin, wd in bars.items():
        for w, b in wd.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            r7 = c / c.shift(7) - 1
            mabs = r7.abs().rolling(30, min_periods=20).mean()
            s7 = r7 / mabs
            sd30 = r1.rolling(30, min_periods=20).std()
            z1 = r1 / sd30.shift(1)
            n = len(b)
            for h in (3, 7, 14):
                f = c.shift(-h) / c - 1
                b[f"f{h}"] = f
            f1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n), "regime": b["regime"],
                               "inprof": (b["regime"] == "unknown").astype(int),
                               "fc": b["forecast"].astype(float), "s7": s7, "z1": z1, "r1": r1,
                               "f1": f1, "f3": b["f3"], "f7": b["f7"], "f14": b["f14"],
                               "clv": clv, "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # drift per coin for 14 and 3
    for h in (1, 3, 7, 14):
        g = D[D.pos % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        D[f"u{h}"] = D[f"f{h}"] - D.coin.map(dr)
    out["regime share"] = D.regime.value_counts(normalize=True)
    def tab(sub, key, h, q=5):
        g = sub[(sub.pos % h == 0)].dropna(subset=[key, f"u{h}"]).copy()
        g["b"] = pd.qcut(g[key], q, labels=False, duplicates="drop")
        a = g.groupby("b").agg(lo=(key, "min"), hi=(key, "max"), n=(f"u{h}", "size"),
                               mean=(f"u{h}", "mean"), sd=(f"u{h}", "std"))
        a["t"] = a["mean"] / (a["sd"] / np.sqrt(a["n"]))
        return a.drop(columns="sd")
    ip = D[D.inprof == 1]; op = D[D.inprof == 0]
    out["inprof s7 -> u14"] = tab(ip, "s7", 14)
    out["outprof s7 -> u14"] = tab(op, "s7", 14)
    out["inprof s7 -> u3"] = tab(ip, "s7", 3)
    out["outprof s7 -> u3"] = tab(op, "s7", 3)
    out["all z1 -> u1"] = tab(D, "z1", 1)
    out["all z1 -> u3"] = tab(D, "z1", 3)
    out["inprof z1 -> u3"] = tab(ip, "z1", 3)
    out["all clv -> u1"] = tab(D, "clv", 1)
    wdg = D.dropna(subset=["u1"]).groupby("wd")["u1"].agg(["size", "mean", "std"])
    wdg["t"] = wdg["mean"] / (wdg["std"] / np.sqrt(wdg["size"]))
    out["weekday u1"] = wdg.drop(columns="std")
    # forecast buckets in profile
    out["fc>0 -> u14"] = tab(ip[ip.fc > 0], "fc", 14, 4)
    # book days
    dd = []
    for coin, wd in days.items():
        for w, d in wd.items():
            dd.append(d.assign(coin=coin, w=w))
    DD = pd.concat(dd, ignore_index=True)
    book = DD.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book by window"] = book.groupby(level=0).agg(["size", "mean", "std"])
    yrs = pd.to_datetime(book.index.get_level_values(1)).year
    out["book by year"] = book.groupby(yrs).agg(["size", "mean", "sum"])
    return out
