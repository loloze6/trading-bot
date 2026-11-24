def explore(data):
    import numpy as np, pandas as pd
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rets = {3: []}
        frames = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l)
            mr20 = rng.rolling(20, min_periods=20).mean()
            r1 = c / c.shift(1) - 1
            vol20 = r1.rolling(20, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos": np.arange(len(b)),
                "rr": rng / mr20,
                "flat": 1 - (c - o).abs() / rng.replace(0, np.nan),
                "rise6": c / c.shift(6) - 1,
                "rise20": c / c.shift(20) - 1,
                "vol20": vol20,
                "volu": b["volume"] / b["volume"].rolling(20, min_periods=20).mean(),
                "f3": c.shift(-3) / c - 1,
            })
            df["z6"] = df["rise6"] / (vol20 * np.sqrt(6))
            g = c.iloc[::3]
            rets[3] += list((g.shift(-1) / g - 1).dropna())
            frames.append(df)
        drift[coin] = (np.mean(rets[3]), np.std(rets[3], ddof=1))
        rows.append(pd.concat(frames))
    A = pd.concat(rows, ignore_index=True)
    A["u3"] = A["f3"] - A["coin"].map(lambda k: drift[k][0])
    A["s3"] = A["u3"] / A["coin"].map(lambda k: drift[k][1])
    A["year"] = A["day"].dt.year
    A["volq"] = A.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))

    def stat(mask, dedup=True):
        d = A[mask & A["u3"].notna()].copy()
        if dedup:
            d["cell"] = d["pos"] // 3
            d = d.drop_duplicates(["coin", "win", "cell"])
        if len(d) < 5:
            return pd.Series({"n": len(d)})
        u = d["u3"]; m = u.mean()
        g = (u - m).groupby(d["day"]).sum(); D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / len(u)
        return pd.Series({"n": len(d), "days": D, "mean_unusual": m, "t": m / se,
                          "strength": d["s3"].mean(), "hit": (u > 0).mean()})
    out = {}
    grid = A["pos"] % 3 == 0
    # momentum on all days vs wide days, z6 bins
    zb = [(-99, -1.5), (-1.5, -.5), (-.5, .5), (.5, 1.5), (1.5, 2.5), (2.5, 99)]
    out["1 z6 bins, all grid days"] = pd.DataFrame({f"z6_{a}-{b}": stat(grid & (A["z6"] >= a) & (A["z6"] < b), False) for a, b in zb}).T
    out["2 z6 bins, wide days rr>=1.5"] = pd.DataFrame({f"z6_{a}-{b}": stat((A["rr"] >= 1.5) & (A["z6"] >= a) & (A["z6"] < b)) for a, b in zb}).T
    out["3 z6 bins, narrow days rr<1"] = pd.DataFrame({f"z6_{a}-{b}": stat((A["rr"] < 1) & (A["z6"] >= a) & (A["z6"] < b)) for a, b in zb}).T
    # rr graded within up-runs z6>0.5
    up = A["z6"] >= 0.5
    out["4 rr bins, up-run z6>=0.5"] = pd.DataFrame({f"rr{a}-{b}": stat(up & (A["rr"] >= a) & (A["rr"] < b)) for a, b in [(0, .8), (.8, 1.2), (1.2, 1.7), (1.7, 2.5), (2.5, 99)]}).T
    out["5 rr bins, down-run z6<=-0.5"] = pd.DataFrame({f"rr{a}-{b}": stat((A["z6"] <= -.5) & (A["rr"] >= a) & (A["rr"] < b)) for a, b in [(0, .8), (.8, 1.2), (1.2, 1.7), (1.7, 2.5), (2.5, 99)]}).T
    # volume ratio within up-runs
    out["6 volume ratio bins, up-run"] = pd.DataFrame({f"vol{a}-{b}": stat(up & (A["volu"] >= a) & (A["volu"] < b)) for a, b in [(0, .8), (.8, 1.2), (1.2, 2), (2, 99)]}).T
    # stability by year: wide & up-run
    wu = (A["rr"] >= 1.5) & up
    out["7 wide up-run by year"] = pd.DataFrame({str(y): stat(wu & (A["year"] == y)) for y in sorted(A["year"].unique())}).T
    out["8 wide up-run by vol tercile"] = pd.DataFrame({f"volq{q}": stat(wu & (A["volq"] == q)) for q in range(3)}).T
    # by coin count of positive
    pc = {k: stat(wu & (A["coin"] == k)) for k in A["coin"].unique()}
    pc = pd.DataFrame(pc).T
    out["9 wide up-run by coin"] = pc
    # rise20 context
    out["10 wide up-run by rise20"] = pd.DataFrame({f"r20_{a}-{b}": stat(wu & (A["rise20"] >= a) & (A["rise20"] < b)) for a, b in [(-9, 0), (0, .2), (.2, .5), (.5, 99)]}).T
    return out
