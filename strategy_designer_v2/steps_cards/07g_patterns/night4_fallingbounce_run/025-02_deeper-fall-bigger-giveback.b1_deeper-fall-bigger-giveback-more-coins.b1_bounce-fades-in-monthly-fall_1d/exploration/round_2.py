def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allc = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            allc.append(c.pct_change().dropna())
        drift = pd.concat(allc).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            n = len(c)
            df = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "pos_in_w": np.arange(n),
                               "z": r / vol, "r30": c / c.shift(30) - 1, "vol": vol,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday})
            for h in [1, 3, 7]:
                df["f%d" % h] = c.shift(-h) / c - 1 - h * drift
            df["vol30"] = vol * np.sqrt(30)
            df["s30"] = df["r30"] / df["vol30"]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["half"] = np.where(d["wn"] <= 12, "early", "late")
    out = {}

    def summ(x):
        x = x.dropna(); n = len(x)
        if n < 3: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})

    # 1) up jumps: graded on r30 scaled, by half, f1 and f3 (jump events are sparse; each event once)
    up = d[(d["z"] >= 2)].dropna(subset=["s30", "f3"]).copy()
    up["q"] = pd.qcut(up["s30"], 4, labels=False)
    out["up jumps f3 by s30 quartile x half"] = up.groupby(["half", "q"])["f3"].apply(summ).unstack()
    out["up jumps f1 by s30 quartile x half"] = up.groupby(["half", "q"])["f1"].apply(summ).unstack()
    rr = []
    for h in ["f1", "f3", "f7"]:
        u = up.dropna(subset=[h])
        rho, p = stats.spearmanr(u["s30"], u[h])
        rr.append(pd.Series({"h": h, "n": len(u), "spearman": rho, "p": p}))
    out["up jumps spearman s30 vs fwd"] = pd.DataFrame(rr)
    # 2) down jumps: graded on s30
    dn = d[(d["z"] <= -2)].dropna(subset=["s30", "f3"]).copy()
    dn["q"] = pd.qcut(dn["s30"], 4, labels=False)
    out["down jumps f3 by s30 quartile x half"] = dn.groupby(["half", "q"])["f3"].apply(summ).unstack()
    rr = []
    for h in ["f1", "f3", "f7"]:
        u = dn.dropna(subset=[h])
        rho, p = stats.spearmanr(u["s30"], u[h])
        rr.append(pd.Series({"h": h, "n": len(u), "spearman": rho, "p": p}))
    out["down jumps spearman s30 vs fwd"] = pd.DataFrame(rr)
    # 3) plain 30-day momentum, non-overlapping 7-day grid
    g7 = d[(d["pos_in_w"] % 7 == 0)].dropna(subset=["s30", "f7"]).copy()
    g7["q"] = g7.groupby("coin")["s30"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["7d grid f7 by s30 quintile x half"] = g7.groupby(["half", "q"])["f7"].apply(summ).unstack()
    g3 = d[(d["pos_in_w"] % 3 == 0)].dropna(subset=["s30", "f3"]).copy()
    g3["q"] = g3.groupby("coin")["s30"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["3d grid f3 by s30 quintile x half"] = g3.groupby(["half", "q"])["f3"].apply(summ).unstack()
    # 4) weekday by half
    out["weekday f1 by half"] = d.dropna(subset=["f1"]).groupby(["half", "wd"])["f1"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x)))).unstack()
    # 5) book: days with largest book gains/losses
    bd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            bd.append(t[["book_return", "coin_return"]].assign(coin=coin))
    bd = pd.concat(bd).dropna()
    act = bd[bd["book_return"].abs() > 1e-9]
    out["book active days"] = pd.Series({"n": len(act), "mean": act["book_return"].mean(),
                                         "corr_with_coin": act["book_return"].corr(act["coin_return"]),
                                         "top5pct_share_of_sum": act["book_return"].nlargest(max(1, len(act)//20)).sum() / act["book_return"].sum()})
    return out
