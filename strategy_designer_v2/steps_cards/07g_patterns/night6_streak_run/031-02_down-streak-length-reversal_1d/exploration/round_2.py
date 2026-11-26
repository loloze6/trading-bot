def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sgn = np.sign(c.diff()).fillna(0).values
            st = np.zeros(len(c))
            for i in range(1, len(c)):
                if sgn[i] == 0: st[i] = 0
                elif np.sign(st[i-1]) == sgn[i]: st[i] = st[i-1] + sgn[i]
                else: st[i] = sgn[i]
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(c)),
                               "ts": pd.to_datetime(b["timestamp"]), "streak": st, "r1": r1,
                               "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    A["wd"] = A["ts"].dt.weekday

    def grp(H, key, fcol, absval=False, cond=None):
        G = A[(A["pos"] % H == 0) & A[fcol].notna()].copy()
        if cond is not None: G = G[cond(G)]
        G["ex"] = G[fcol] - G.groupby("coin")[fcol].transform("mean")
        if absval:
            G["ex"] = G[fcol].abs() / G.groupby("coin")[fcol].transform(lambda s: s.abs().mean()) - 1
        out = []
        for k, s in G.groupby(key):
            m = s["ex"].mean()
            dev = s.groupby("day")["ex"].apply(lambda x: (x - m).sum())
            se = np.sqrt((dev ** 2).sum()) / len(s)
            out.append({key: k, "n": len(s), "days": s["day"].nunique(), "mean_%": 100 * m, "t": m / se})
        return pd.DataFrame(out)

    A["abs_streak"] = A["streak"].abs().clip(0, 6)
    A["streak_b"] = A["streak"].clip(-5, 5)
    # weekday halves per coin per year split
    A["year"] = A["ts"].dt.year
    A["wd_grp"] = A["wd"].map({0: "MonTue", 1: "MonTue", 2: "mid", 3: "mid", 4: "mid", 5: "SatSun", 6: "SatSun"})
    wdyear = []
    for (y), s in A[(A["f1"].notna())].groupby("year"):
        s = s.copy(); s["ex"] = s["f1"] - s.groupby("coin")["f1"].transform("mean")
        g = s.groupby("wd_grp")["ex"].mean() * 100
        wdyear.append(g.rename(y))
    wdyear = pd.DataFrame(wdyear)

    return {"f1_by_weekday_all_bars": grp(1, "wd", "f1"),
            "f1_by_wdgroup_by_year_%": wdyear,
            "f1_by_streak": grp(1, "streak_b", "f1"),
            "f3_by_streak": grp(3, "streak_b", "f3"),
            "abs_f5_rel_by_abs_streak": grp(5, "abs_streak", "f5", absval=True),
            "abs_f1_rel_by_abs_streak": grp(1, "abs_streak", "f1", absval=True),
            "alloc_by_streak": A.groupby("streak_b")["alloc"].mean()}
