def explore(data):
    import numpy as np, pandas as pd
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 40: continue
            c, o, hi, lo = b["close"], b["open"], b["high"], b["low"]
            rng = (hi - lo)
            r = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            r["pos"] = np.arange(len(b))
            r["ret5"] = c / c.shift(6) - 1
            r["ret20"] = c / c.shift(20) - 1
            r["width"] = rng / rng.rolling(20).mean()
            r["flat"] = 1 - (c - o).abs() / rng.replace(0, np.nan)
            r["vol20"] = np.log(c).diff().rolling(20).std()
            r["ret1"] = c / c.shift(1) - 1
            r["fwd"] = c.shift(-H) / c - 1
            r["fwd1"] = c.shift(-1) / c - 1
            r["cell"] = r["pos"] // H
            rows.append(r)
    A = pd.concat(rows, ignore_index=True)
    grid = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    drift = grid.groupby("coin")["fwd"].mean()
    usual = grid.groupby("coin")["fwd"].std()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    A["str"] = A["ex"] / A["coin"].map(usual)
    A["day"] = A["ts"].dt.floor("D")

    def pooled(df, col="ex"):
        df = df.dropna(subset=[col])
        n = len(df)
        if n < 5: return pd.Series({"n": n, "mean": df[col].mean() if n else np.nan, "t": np.nan, "days": n})
        m = df[col].mean()
        d = (df[col] - m).groupby(df["day"]).sum()
        D = len(d)
        se = np.sqrt(D / (D - 1) * (d ** 2).sum()) / n
        return pd.Series({"n": n, "mean": m, "t": m / se, "days": D, "strength": df["str"].mean() if col=="ex" else np.nan})

    def first_per_cell(mask):
        s = A[mask & A["fwd"].notna()]
        return s.groupby(["coin", "win", "cell"]).head(1)

    out = {}
    wide = A["width"] >= 1.5
    flat = A["flat"] >= 0.9
    narrow = A["width"] <= 0.7
    up = A["ret5"] > 0; dn = A["ret5"] < 0
    conds = {
        "wideflat_up": wide & flat & up, "wideflat_dn": wide & flat & dn,
        "wideflat_any": wide & flat, "narrowflat_up": narrow & flat & up,
        "narrowflat_dn": narrow & flat & dn, "wide_any": wide,
        "wide_up_bigbody": wide & up & (A["flat"] < 0.5),
        "wide_dn_bigbody": wide & dn & (A["flat"] < 0.5),
    }
    out["conditions_fwd10_excess"] = pd.DataFrame({k: pooled(first_per_cell(v)) for k, v in conds.items()}).T

    g = grid.copy(); g["ex"] = A.loc[g.index, "ex"]; g["str"] = A.loc[g.index, "str"]; g["day"] = A.loc[g.index, "day"]
    for f in ["ret5", "ret20", "width", "flat", "vol20", "ret1"]:
        gg = g.dropna(subset=[f]).copy()
        gg["q"] = gg.groupby("coin")[f].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        out["q_" + f] = gg.groupby("q").apply(pooled)
    # weekday next-day return
    d1 = A.dropna(subset=["fwd1"]).copy()
    d1["wd"] = d1["ts"].dt.weekday
    out["weekday_next_day"] = d1.groupby("wd")["fwd1"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # after large 1-day moves: next 1 and 10 day
    A["z1"] = A["ret1"] / A["vol20"]
    big = A.dropna(subset=["z1"])
    big = big.assign(zb=pd.cut(big["z1"], [-99, -2.5, -1.5, 1.5, 2.5, 99]))
    out["after_1day_z_fwd10"] = big[big["fwd"].notna()].groupby(["zb", "coin", "win", "cell"]).head(1).groupby("zb").apply(pooled)
    out["by_year_wideflat_up"] = first_per_cell(conds["wideflat_up"]).assign(y=lambda x: x["ts"].dt.year).groupby("y").apply(pooled)
    return out
