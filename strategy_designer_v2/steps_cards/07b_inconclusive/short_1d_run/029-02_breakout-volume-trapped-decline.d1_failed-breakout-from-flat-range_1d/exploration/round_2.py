def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1, 2, 3, 5, 10]
    drift = {}
    rows = []
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"]).dt.year.values
            for t in range(24, n):
                j = None
                for k in (1, 2, 3):
                    jj = t - k
                    if jj - 20 < 0: continue
                    ph = c[jj-20:jj].max()
                    if c[jj] > ph:
                        j = jj; hi = ph; break
                if j is None or not (c[t] < hi): continue
                if t - 1 > j and c[t-1] < hi: continue
                pre = c[j-1] / c[j-21] - 1 if j - 21 >= 0 else np.nan
                depth = hi / c[t] - 1
                drop = c[j] / c[t] - 1  # fall from breakout close
                r = {"coin": coin, "w": w, "t": t, "year": ts[t], "pre": pre,
                     "depth": depth, "drop": drop}
                for h in H:
                    if t + h < n:
                        m, s = drift[(coin, h)]
                        r[f"long_u{h}"] = (c[t+h] / c[t] - 1) - m
                        r[f"str{h}"] = r[f"long_u{h}"] / s
                    else:
                        r[f"long_u{h}"] = np.nan; r[f"str{h}"] = np.nan
                rows.append(r)
    E = pd.DataFrame(rows)
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    E1 = E.drop_duplicates(["coin", "w", "t"])
    out["long_u_by_h"] = pd.DataFrame({f"h{h}": tt(E.assign(cell=E.t // h).drop_duplicates(["coin","w","cell"])[f"long_u{h}"]) for h in H}).T
    out["strength_by_h"] = pd.DataFrame({f"h{h}": tt(E.assign(cell=E.t // h).drop_duplicates(["coin","w","cell"])[f"str{h}"]) for h in H}).T
    E1 = E1.copy()
    E1["depth_q"] = pd.qcut(E1["depth"], 4, labels=False, duplicates="drop")
    E1["drop_q"] = pd.qcut(E1["drop"], 4, labels=False, duplicates="drop")
    E1["pre_q"] = pd.qcut(E1["pre"], 4, labels=False, duplicates="drop")
    out["h1_by_depth_q"] = E1.groupby("depth_q")["long_u1"].apply(tt).unstack()
    out["h1_by_drop_q"] = E1.groupby("drop_q")["long_u1"].apply(tt).unstack()
    out["h1_by_pre_q"] = E1.groupby("pre_q")["long_u1"].apply(tt).unstack()
    out["h1_by_coin"] = E1.groupby("coin")["long_u1"].apply(tt).unstack()
    out["h1_by_year"] = E1.groupby("year")["long_u1"].apply(tt).unstack()
    x = E1[["depth", "long_u1"]].dropna()
    b = np.polyfit(x.depth, x.long_u1, 1)[0]
    res = x.long_u1 - np.polyval(np.polyfit(x.depth, x.long_u1, 1), x.depth)
    se = np.sqrt((res**2).sum() / (len(x)-2) / ((x.depth - x.depth.mean())**2).sum())
    out["slope_h1_on_depth"] = pd.Series({"slope": b, "t": b / se, "n": len(x)})
    return out
