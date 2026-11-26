def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 20
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rets); usual[coin] = np.std(rets, ddof=1)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            prev = np.r_[0, f[:-1]]
            rise = f - prev
            hi60 = df["high"].shift(1).rolling(60, min_periods=60).max().values
            lo60 = df["low"].shift(1).rolling(60, min_periods=60).min().values
            seen = set()
            for i in np.where(rise >= 2)[0]:
                cell = i // H
                if cell in seen: continue
                seen.add(cell)
                out = {"coin": coin, "win": w, "year": ts[i].year, "day": ts[i].normalize(),
                       "fc": f[i], "brk": c[i] / hi60[i] - 1 if hi60[i] == hi60[i] else np.nan,
                       "rng": hi60[i] / lo60[i] - 1 if lo60[i] == lo60[i] else np.nan}
                for h in [1, 3, 5, 10, 20, 40]:
                    out[f"r{h}"] = c[i + h] / c[i] - 1 - drift[coin] * h / 20 if i + h < len(c) else np.nan
                rows.append(out)
    d = pd.DataFrame(rows)
    def tday(x):
        g = d.assign(v=x).dropna(subset=["v"]).groupby("day")["v"].sum()
        n = d.assign(v=x).dropna(subset=["v"]).shape[0]
        m = g.sum() / n
        se = np.sqrt(((g - m * d.assign(v=x).dropna(subset=["v"]).groupby("day").size()) ** 2).sum()) / n
        return pd.Series({"mean": m, "t": m / se, "n": n, "days": len(g)})
    hz = pd.DataFrame({f"r{h}": tday(d[f"r{h}"]) for h in [1, 3, 5, 10, 20, 40]}).T
    def grp(col):
        return d.groupby(col)["r20"].agg(["mean", "count", lambda s: s.mean() / (s.std(ddof=1) / np.sqrt(s.count())) if s.count() > 1 else np.nan, lambda s: (s > 0).mean()]).rename(columns={"<lambda_0>": "t", "<lambda_1>": "share_pos"})
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    d["bq"] = pd.qcut(d["brk"].rank(method="first"), 4, labels=["b1", "b2", "b3", "b4"])
    d["rq"] = pd.qcut(d["rng"].rank(method="first"), 4, labels=["r1narrow", "r2", "r3", "r4wide"])
    med = d["r20"].median()
    return {"horizons": hz, "by_coin": grp("coin"), "by_year": grp("year"), "by_window": grp("win"),
            "by_forecast_q": grp("fq"), "by_break_q": grp("bq"), "by_range_width_q": grp("rq"),
            "median_r20": med, "usual": pd.Series(usual), "drift": pd.Series(drift),
            "corr_fc_r20": d[["fc", "brk", "rng", "r20"]].corr()["r20"]}
