def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [6, 24, 48, 96, 168]
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        # drift per horizon: grid returns over all windows
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
            # bet bars
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
                else:
                    low = min(low, f[i]) if low > 0 else low
            seen = set()
            r720 = pd.Series(c).pct_change(720).values
            r24 = pd.Series(c).pct_change(24).values
            for i in bets:
                cell = i // 48
                if cell in seen:
                    continue
                if i + 48 >= n:
                    continue
                seen.add(cell)
                d = {"coin": coin, "win": int(w[1:]), "year": ts.iloc[i].year,
                     "hour": ts.iloc[i].hour, "fc": f[i], "r720": r720[i], "r24": r24[i]}
                for h in H:
                    d[f"x{h}"] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < n else np.nan
                d["tot48"] = c[i + 48] / c[i] - 1
                rows.append(d)
    df = pd.DataFrame(rows)
    def summ(g, col="x48"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(df, f"x{h}") for h in H}).T
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    df["fcb"] = pd.cut(df["fc"], [0, 2.5, 5, 10, 19.99, 20.01])
    out["by_fc"] = df.groupby("fcb").apply(summ)
    out["by_fc_h168"] = df.groupby("fcb").apply(lambda g: summ(g, "x168"))
    df["trend"] = pd.qcut(df["r720"], 4, labels=["q1down", "q2", "q3", "q4up"])
    out["by_30d_trend"] = df.groupby("trend").apply(summ)
    out["by_30d_trend_h168"] = df.groupby("trend").apply(lambda g: summ(g, "x168"))
    out["by_r24_quint"] = df.groupby(pd.qcut(df["r24"], 5)).apply(summ)
    out["spearman_fc_h"] = pd.Series({h: stats.spearmanr(df["fc"], df[f"x{h}"], nan_policy="omit")[0] for h in H})
    out["fc_share_capped"] = (df["fc"] >= 19.99).mean()
    out["window_means_pos_share"] = (df.groupby(["coin", "win"])["x48"].mean() > 0).mean()
    return out
