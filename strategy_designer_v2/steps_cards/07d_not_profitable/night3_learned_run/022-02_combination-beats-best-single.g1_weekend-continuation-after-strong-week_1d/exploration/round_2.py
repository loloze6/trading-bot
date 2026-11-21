def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            allr.append(pd.Series(b["close"].astype(float).values).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in ws.items():
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            c = b["close"].astype(float).reset_index(drop=True)
            o = b["open"].astype(float).reset_index(drop=True)
            d = pd.DataFrame({"nwd": (ts + pd.Timedelta(days=1)).dt.weekday})
            d["r7"] = c / c.shift(7) - 1
            d["r3"] = c / c.shift(3) - 1
            d["r28"] = c / c.shift(28) - 1
            d["r1"] = c / c.shift(1) - 1
            d["vol"] = c.pct_change().rolling(30).std()
            d["n1"] = c.shift(-1) / c - 1 - mu
            d["coin"] = coin
            d["alloc"] = b["postRebalance_current_allocation"].astype(float).values
            d["chg"] = (b["postRebalance_current_allocation"].astype(float) - b["previous_allocation"].astype(float)).abs().values
            rows.append(d)
    df = pd.concat(rows, ignore_index=True).dropna(subset=["r7", "r3", "r28", "n1", "vol"])
    for k in ["r1", "r3", "r7", "r28"]:
        df["z" + k] = df[k] / (df["vol"] * np.sqrt({"r1": 1, "r3": 3, "r7": 7, "r28": 28}[k]))
    df["comb"] = df[["zr3", "zr7", "zr28"]].mean(axis=1)
    res = []
    for wd, s in df.groupby("nwd"):
        res.append([wd] + [s[k].corr(s["n1"]) for k in ["zr1", "zr3", "zr7", "zr28", "comb"]] + [len(s)])
    out["corr_by_nwd"] = pd.DataFrame(res, columns=["nwd", "r1", "r3", "r7", "r28", "comb", "n"])
    for wd in [5, 6, 1]:
        s = df[df["nwd"] == wd].copy()
        s["q"] = s.groupby("coin")["comb"].transform(lambda x: pd.qcut(x, 5, labels=False))
        g = s.groupby("q")["n1"].agg(["mean", "std", "count"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        out["comb_quintile_nwd%d" % wd] = g
    # Saturday by vol regime
    s = df[(df["nwd"] == 5) & (df["r7"] > 0)].copy()
    s["vq"] = s.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["sat_pos_by_volterc"] = s.groupby("vq")["n1"].agg(["mean", "count"])
    out["sat_corr_by_volterc"] = s.groupby("vq").apply(lambda x: x["r7"].corr(x["n1"]))
    out["turnover_per_active_bar"] = float(df.loc[df["alloc"] > 1e-9, "chg"].mean())
    return out
