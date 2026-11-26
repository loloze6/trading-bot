def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1)/c - 1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l)
            mr = rng.rolling(20, min_periods=20).mean()
            rm = rng / mr
            clv = ((c - l) / rng.replace(0, np.nan))
            r1 = c.shift(-1)/c - 1
            r3 = c.shift(-3)/c - 1
            past5 = c/c.shift(5) - 1
            tr = c/c.shift(60) - 1
            d = pd.DataFrame({"coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "rm": rm, "clv": clv, "u1": r1 - mu, "u3": r3 - 3*mu, "grid3": (np.arange(len(b)) % 3 == 0),
                              "agit": (b["regime"] != "chop"), "trend": tr, "past5": past5,
                              "dayret": c/o - 1, "fc": b["forecast"]})
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df = df.dropna(subset=["rm", "clv"])
    def stat(g, col="u1"):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series({"n": len(g), "mean%": np.nan, "t_day": np.nan})
        s = g.groupby("day")[col].apply(lambda x: (x - g[col].mean()).sum())
        dd = len(s); se = np.sqrt((s**2).sum() * dd/(dd-1)) / len(g)
        return pd.Series({"n": len(g), "days": dd, "mean%": 100*g[col].mean(), "t_day": g[col].mean()/se})
    df["rmb"] = pd.cut(df["rm"], [0, 0.7, 1.0, 1.5, 2.0, 99], labels=["<0.7","0.7-1","1-1.5","1.5-2",">2"])
    df["clvb"] = pd.cut(df["clv"], [-0.01, 0.33, 0.67, 1.01], labels=["low","mid","high"])
    df["tb"] = pd.cut(df["trend"], [-9, -0.1, 0.1, 99], labels=["falling","choppy","rising"])
    out = {}
    out["u1 by width x close, agitated"] = df[df.agit].groupby(["rmb","clvb"], observed=True).apply(stat)
    out["u1 by width x close, calm"] = df[~df.agit].groupby(["rmb","clvb"], observed=True).apply(stat)
    wide = df[df.rm >= 1.5]
    out["wide days u1 by agit x trend x close"] = wide.groupby(["agit","tb","clvb"], observed=True).apply(stat)
    g3 = df[df.grid3]
    out["u3 grid by width x close, all"] = g3[g3.rm>=1.5].groupby(["agit","clvb"], observed=True).apply(lambda g: stat(g,"u3"))
    out["all days u1 by agit"] = df.groupby("agit").apply(stat)
    return out
