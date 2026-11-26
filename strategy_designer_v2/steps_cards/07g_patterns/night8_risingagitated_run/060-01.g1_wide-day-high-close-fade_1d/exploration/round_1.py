def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 30: continue
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "cl": (c - l) / rng,
                "rr": (h - l) / (h - l).rolling(20, min_periods=20).mean(),
                "ret": c.pct_change(),
                "ret5": c / c.shift(5) - 1,
                "vol20": c.pct_change().rolling(20).std(),
                "nxt": c.shift(-1) / c - 1,
                "nxt3": c.shift(-3) / c - 1,
                "inprof": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"],
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    drift = df.groupby("coin")["nxt"].transform("mean")
    sd = df.groupby("coin")["nxt"].transform("std")
    df["u"] = df["nxt"] - drift
    df["z"] = df["u"] / sd
    df["day"] = df["ts"].dt.floor("D")
    df = df.dropna(subset=["nxt"])
    def summ(g):
        n = len(g); m = g["u"].mean(); s = g["u"].std()
        dd = g.groupby("day")["u"].sum()
        tday = dd.mean() / (dd.std() / np.sqrt(len(dd))) * 1 if len(dd) > 2 else np.nan
        return pd.Series({"n": n, "mean_u%": 100 * m, "z": g["z"].mean(), "t": m / (s / np.sqrt(n)) if n > 2 else np.nan})
    df["clq"] = pd.cut(df["cl"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["q1", "q2", "q3", "q4"])
    df["rrq"] = pd.cut(df["rr"], [0, 0.7, 1.0, 1.5, 2.2, 99], labels=["<0.7", "0.7-1", "1-1.5", "1.5-2.2", ">2.2"])
    out = {}
    out["cl_by_profile"] = df.groupby(["inprof", "clq"]).apply(summ)
    out["rr_by_profile_highclose"] = df[df["cl"] >= 0.75].groupby(["inprof", "rrq"]).apply(summ)
    out["rr_by_profile_lowclose"] = df[df["cl"] <= 0.25].groupby(["inprof", "rrq"]).apply(summ)
    df["retq"] = pd.qcut(df["ret"] / df["vol20"], 5, labels=False)
    out["scaled_ret_quintile_by_profile"] = df.dropna(subset=["retq"]).groupby(["inprof", "retq"]).apply(summ)
    df["r5q"] = pd.qcut(df["ret5"] / (df["vol20"] * np.sqrt(5)), 5, labels=False)
    out["ret5_quintile_by_profile"] = df.dropna(subset=["r5q"]).groupby(["inprof", "r5q"]).apply(summ)
    out["weekday_inprof"] = df[df["inprof"] == 1].groupby(df["ts"].dt.weekday).apply(summ)
    out["weekday_all"] = df.groupby(df["ts"].dt.weekday).apply(summ)
    out["year_cases"] = df[df["fc"] < 0].groupby(df["ts"].dt.year).apply(summ)
    out["coin_cases"] = df[df["fc"] < 0].groupby("coin").apply(summ)
    out["share_inprof"] = df["inprof"].mean()
    return out
