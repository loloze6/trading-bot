def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        g = {h: [] for h in (1, 2)}
        for w, b in wins.items():
            c = b["close"].astype(float).values
            for h in g:
                idx = np.arange(0, len(c) - h, h)
                g[h] += list(c[idx + h] / c[idx] - 1)
        drift = {h: np.mean(v) for h, v in g.items()}
        usual = {h: np.std(v, ddof=1) for h, v in g.items()}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            z = r / r.rolling(20).std()
            r60 = c / c.shift(60) - 1
            r40 = c / c.shift(40) - 1
            r20 = c / c.shift(20) - 1
            ma = c / c.rolling(50).mean() - 1
            seen = set()
            for t in range(len(b)):
                if not (z.iloc[t] <= -2):
                    continue
                cell = t // 2
                if cell in seen:
                    continue
                seen.add(cell)
                d = {"coin": coin, "win": w, "z": z.iloc[t], "r60": r60.iloc[t], "r40": r40.iloc[t],
                     "r20": r20.iloc[t], "ma50": ma.iloc[t], "day": str(b["timestamp"].iloc[t])[:10]}
                for h in (1, 2):
                    if t + h < len(b):
                        d[f"x{h}"] = c.iloc[t + h] / c.iloc[t] - 1 - drift[h]
                        d[f"s{h}"] = d[f"x{h}"] / usual[h]
                rows.append(d)
    df = pd.DataFrame(rows)

    def ct(s, days):
        m = pd.DataFrame({"v": s, "d": days}).dropna()
        n = len(m)
        if n < 3:
            return pd.Series({"n": n, "days": np.nan, "mean": np.nan, "t_cl": np.nan})
        mu = m["v"].mean()
        dev = (m["v"] - mu).groupby(m["d"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / n
        return pd.Series({"n": n, "days": D, "mean": mu, "t_cl": mu / se})

    out = {}
    out["all_cl"] = pd.DataFrame({h: ct(df[f"x{h}"], df["day"]) for h in (1, 2)}).T
    out["by_win_x2"] = df.groupby("win").apply(lambda g: ct(g["x2"], g["day"]))
    for col in ("r60", "r40", "ma50"):
        sub = df.dropna(subset=[col])
        lab = np.where(sub[col] > 0, "up", "down")
        res = sub.groupby(lab).apply(lambda g: ct(g["x2"], g["day"]))
        sl = {}
        for k, g in sub.groupby(lab):
            g2 = g.dropna(subset=["x2"])
            if len(g2) > 5:
                L = stats.linregress(-g2["z"], g2["x2"])
                sl[k] = L.slope / L.stderr
        res["t_slope_negz"] = pd.Series(sl)
        out[f"by_{col}_sign_x2"] = res
    sub = df.dropna(subset=["ma50", "x2"])
    sub = sub.assign(mb=pd.qcut(sub["ma50"], 4, labels=["q1", "q2", "q3", "q4"]))
    out["by_ma50_quart_x2"] = sub.groupby("mb").apply(lambda g: ct(g["x2"], g["day"]))
    sub = df.dropna(subset=["x2"]).assign(deep=lambda d: np.where(d["z"] <= -3, "z<=-3", "-3<z<=-2"))
    out["by_depth_x1x2"] = pd.concat([sub.groupby("deep").apply(lambda g: ct(g["x1"], g["day"])).add_prefix("h1_"),
                                      sub.groupby("deep").apply(lambda g: ct(g["x2"], g["day"])).add_prefix("h2_")], axis=1)
    return out
