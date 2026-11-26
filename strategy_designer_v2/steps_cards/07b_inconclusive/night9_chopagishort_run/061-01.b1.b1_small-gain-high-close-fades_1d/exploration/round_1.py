def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in (1, 2, 3, 5, 10):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            rng = hi - lo
            cl = np.where(rng > 0, (c - lo) / np.where(rng > 0, rng, 1), np.nan)
            ret1 = pd.Series(c).pct_change().values
            mabs = pd.Series(np.abs(ret1)).rolling(30).mean().shift(0).values
            for i in range(len(df)):
                reg = df["regime"].iloc[i]
                if reg not in ("mean_reversion", "unknown"):
                    continue
                r = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "i": i, "cl": cl[i], "gain": ret1[i],
                     "gain_s": ret1[i] / mabs[i] if mabs[i] and not np.isnan(mabs[i]) else np.nan,
                     "fc": df["forecast"].iloc[i], "reg": reg,
                     "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date())}
                for h in (1, 2, 3, 5, 10):
                    r[f"ok{h}"] = (i % h == 0) and (i + h < len(df))
                    if i + h < len(df):
                        m, s = drift[(coin, h)]
                        r[f"u{h}"] = -(c[i + h] / c[i] - 1 - m)  # short direction
                        r[f"z{h}"] = r[f"u{h}"] / s
                    else:
                        r[f"u{h}"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    out = {}
    def summ(g, h):
        g = g[g[f"ok{h}"]].dropna(subset=[f"u{h}"])
        if len(g) < 3:
            return pd.Series({"n": len(g), "mean": np.nan, "t": np.nan})
        pd_ = g.groupby("day")[f"u{h}"].sum()
        mu = g[f"u{h}"].mean()
        D = len(pd_)
        se = np.sqrt((pd_ - pd_.mean() * 0).pow(2).sum() / len(g) ** 2 * D / (D - 1)) if D > 1 else np.nan
        dev = g.groupby("day")[f"u{h}"].apply(lambda x: (x - mu).sum())
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(g)
        return pd.Series({"n": len(g), "days": D, "mean": mu, "t": mu / se, "strength": g[f"z{h}"].mean()})
    d["clb"] = pd.cut(d["cl"], [-0.01, 0.2, 0.4, 0.6, 0.8, 0.9, 1.01])
    for h in (1, 2, 3, 5, 10):
        out[f"in-profile by close loc, h{h}"] = d.groupby("clb").apply(lambda g: summ(g, h))
    top = d[d["cl"] >= 0.8].copy()
    top["gb"] = pd.cut(top["gain_s"], [-99, -1, 0, 0.5, 1, 2, 99])
    for h in (2, 5):
        out[f"cl>=0.8 by gain_s, h{h}"] = top.groupby("gb").apply(lambda g: summ(g, h))
    out["cl>=0.8 by coin h5"] = top.groupby("coin").apply(lambda g: summ(g, 5))
    out["cl>=0.8 by year h5"] = top.groupby("year").apply(lambda g: summ(g, 5))
    out["cl>=0.8 by year h2"] = top.groupby("year").apply(lambda g: summ(g, 2))
    out["in-profile cl<0.8 vs >=0.8 h5"] = d.groupby(d["cl"] >= 0.8).apply(lambda g: summ(g, 5))
    sub = top[top["ok5"]].dropna(subset=["u5", "gain_s"])
    out["corr gain_s vs u5 (cl>=0.8)"] = pd.Series(stats.spearmanr(sub["gain_s"], sub["u5"]), index=["rho", "p"])
    sub2 = d[d["ok5"]].dropna(subset=["u5", "cl"])
    out["corr cl vs u5 (in profile)"] = pd.Series(stats.spearmanr(sub2["cl"], sub2["u5"]), index=["rho", "p"])
    return out
