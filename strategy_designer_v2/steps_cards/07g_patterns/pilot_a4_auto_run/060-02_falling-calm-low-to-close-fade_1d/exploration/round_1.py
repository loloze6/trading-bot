def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "infc": (b["regime"] != "chop").astype(int),
                "ret": r1, "ret_z": r1 / vol30,
                "rng_z": (h - l) / c / vol30,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "lift_z": (c - l) / c / vol30,
                "drop_z": (h - c) / c / vol30,
                "ret5_z": (c / c.shift(5) - 1) / (vol30 * np.sqrt(5)),
                "ret20_z": (c / c.shift(20) - 1) / (vol30 * np.sqrt(20)),
                "volu_z": np.log(b["volume"].replace(0, np.nan)) - np.log(b["volume"].replace(0, np.nan)).rolling(30, min_periods=20).mean(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
                "vol30": vol30,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per coin
    drift = {}
    for hh in [1, 3, 5]:
        g = D[D["pos"] % hh == 0]
        drift[hh] = g.groupby("coin")["f%d" % hh].mean()
    for hh in [1, 3, 5]:
        D["u%d" % hh] = D["f%d" % hh] - D["coin"].map(drift[hh])
    F = D[D["infc"] == 1]
    out["share_in_profile_by_coin"] = D.groupby("coin")["infc"].agg(["mean", "sum"])
    def tab(feat, hh, q=4):
        g = F[(F["pos"] % hh == 0)].dropna(subset=[feat, "u%d" % hh])
        g = g.assign(b=pd.qcut(g[feat], q, labels=False, duplicates="drop"))
        t = g.groupby("b")["u%d" % hh].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["feat_mid"] = g.groupby("b")[feat].median()
        return t.drop(columns="std")
    for feat in ["ret_z", "rng_z", "clv", "lift_z", "drop_z", "ret5_z", "ret20_z", "volu_z"]:
        for hh in [1, 3, 5]:
            out[f"{feat}_h{hh}"] = tab(feat, hh)
    g = F.dropna(subset=["u1"])
    t = g.groupby("wd")["u1"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["weekday_h1"] = t.drop(columns="std")
    # profile vs outside, total
    for hh in [1, 3, 5]:
        g = D[D["pos"] % hh == 0].dropna(subset=["u%d" % hh])
        t = g.groupby("infc")["u%d" % hh].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        out[f"in_vs_out_h{hh}"] = t.drop(columns="std")
    return out
