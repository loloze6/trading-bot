def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [24, 48, 96, 168]
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
        for w, b in wins.items():
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(c)
            low = None
            bets = []
            for i in range(n):
                if f[i] <= 0:
                    low = None
                    continue
                if low is None:
                    low = 0.0
                if f[i] - low >= 2:
                    bets.append(i)
                    low = f[i]
            seen = set()
            s = pd.Series(c)
            r720 = s.pct_change(720).values
            r168 = s.pct_change(168).values
            for i in bets:
                cell = i // 48
                if cell in seen or i + 48 >= n:
                    continue
                seen.add(cell)
                d = {"coin": coin, "win": int(w[1:]), "year": ts.iloc[i].year,
                     "fc": f[i], "r720": r720[i], "r168": r168[i]}
                for h in H:
                    d[f"x{h}"] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows).dropna(subset=["r720"])
    def summ(g, col="x48"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    df["up"] = np.where(df["r720"] > 0, "up30", "down30")
    out["by_sign30_h"] = pd.DataFrame({h: df.groupby("up").apply(lambda g: summ(g, f"x{h}")).stack() for h in H})
    df["dec"] = pd.qcut(df["r720"], 8, labels=False)
    out["by_r720_oct_x48"] = df.groupby("dec").apply(summ)
    out["by_r720_oct_x168"] = df.groupby("dec").apply(lambda g: summ(g, "x168"))
    up = df[df["up"] == "up30"]
    out["up_by_coin_x96"] = up.groupby("coin").apply(lambda g: summ(g, "x96"))
    out["up_by_year_x96"] = up.groupby("year").apply(lambda g: summ(g, "x96"))
    out["up_by_fc_x96"] = up.groupby(pd.cut(up["fc"], [0, 2.5, 5, 10, 19.99, 20.01])).apply(lambda g: summ(g, "x96"))
    out["up_spearman_fc"] = pd.Series({h: stats.spearmanr(up["fc"], up[f"x{h}"], nan_policy="omit")[0] for h in H})
    out["spearman_r720_x"] = pd.Series({h: stats.spearmanr(df["r720"], df[f"x{h}"], nan_policy="omit")[0] for h in H})
    out["by_r168_sign_x48"] = df.groupby(df["r168"] > 0).apply(summ)
    return out
