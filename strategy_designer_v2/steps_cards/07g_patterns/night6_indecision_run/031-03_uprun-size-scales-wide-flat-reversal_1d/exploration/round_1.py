def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 5
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            for i in range(0, n - H, H):
                grid_rets.append(c[i + H] / c[i] - 1)
            rng = (df["high"] - df["low"])
            mr20 = rng.rolling(20, min_periods=20).mean()
            width = rng / mr20
            body = (df["close"] - df["open"]).abs() / rng.replace(0, np.nan)
            clv = ((df["close"] - df["low"]) / rng.replace(0, np.nan)) * 2 - 1
            prior5 = df["close"] / df["close"].shift(5) - 1
            prior20 = df["close"] / df["close"].shift(20) - 1
            r1 = df["close"].pct_change()
            vol20 = r1.rolling(20, min_periods=20).std()
            vol60m = vol20.rolling(120, min_periods=40).median()
            fwd = df["close"].shift(-H) / df["close"] - 1
            fwd1 = df["close"].shift(-1) / df["close"] - 1
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                "width": width, "body": body, "clv": clv, "prior5": prior5,
                "prior20": prior20, "fwd": fwd, "fwd1": fwd1, "r1": r1,
                "volratio": vol20 / vol60m, "vol20": vol20,
                "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
            })
            rows.append(d)
        g = np.array(grid_rets)
        drift[coin] = g.mean(); usual[coin] = g.std()
    D = pd.concat(rows, ignore_index=True)
    D["drift"] = D["coin"].map(drift); D["usual"] = D["coin"].map(usual)
    D["unus"] = D["fwd"] - D["drift"]
    D["cell"] = D["pos"] // H

    def ct(sub, col="unus"):
        sub = sub.dropna(subset=[col])
        if len(sub) < 3: return (len(sub), np.nan, np.nan, np.nan)
        m = sub[col].mean()
        dev = (sub[col] - m).groupby(sub["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / len(sub)
        return (len(sub), G, m, m / se if se > 0 else np.nan)

    def first_per_cell(sub):
        return sub.sort_values("pos").groupby(["coin", "win", "cell"]).head(1)

    out = {}
    # 1. wide flat days by prior5 sign/terciles
    wf = first_per_cell(D[(D.width >= 1.5) & (D.body <= 0.1)])
    nf = first_per_cell(D[(D.width <= 0.7) & (D.body <= 0.1)])
    res = []
    for name, S in [("wideflat", wf), ("narrowflat", nf)]:
        for lab, m in [("prior_up", S.prior5 > 0), ("prior_down", S.prior5 <= 0)]:
            n, G, mu, t = ct(S[m]); res.append([name, lab, n, G, mu, t])
    out["flat_days_long_unusual_fwd5"] = pd.DataFrame(res, columns=["set", "prior", "n", "days", "mean_unus", "t"])
    # 2. wide days (any body) by close location: graded
    wd = first_per_cell(D[D.width >= 1.5]).copy()
    wd["clvq"] = pd.qcut(wd["clv"], 5, labels=False, duplicates="drop")
    res = []
    for q, S in wd.groupby("clvq"):
        n, G, mu, t = ct(S); res.append([q, S.clv.mean(), n, G, mu, t])
    out["wide_days_by_close_location"] = pd.DataFrame(res, columns=["q", "clv", "n", "days", "mean_unus", "t"])
    # 3. grid points: fwd5 by prior5 standardized quintile
    G0 = D[(D.pos % H == 0)].dropna(subset=["prior5", "fwd", "vol20"]).copy()
    G0["z5"] = G0.prior5 / (G0.vol20 * np.sqrt(5))
    G0["zq"] = pd.qcut(G0.z5, 5, labels=False)
    res = []
    for q, S in G0.groupby("zq"):
        n, Gd, mu, t = ct(S); res.append([q, S.z5.mean(), n, Gd, mu, t])
    out["grid_fwd5_by_prior5_z"] = pd.DataFrame(res, columns=["q", "z5", "n", "days", "mean_unus", "t"])
    # 4. by vol ratio
    G1 = G0.dropna(subset=["volratio"]).copy()
    G1["vq"] = pd.qcut(G1.volratio, 4, labels=False)
    res = []
    for q, S in G1.groupby("vq"):
        n, Gd, mu, t = ct(S); res.append([q, S.volratio.mean(), n, Gd, mu, t])
    out["grid_fwd5_by_volratio"] = pd.DataFrame(res, columns=["q", "vr", "n", "days", "mean_unus", "t"])
    # 5. prior20 quintile
    G2 = G0.dropna(subset=["prior20"]).copy()
    G2["z20"] = G2.prior20 / (G2.vol20 * np.sqrt(20))
    G2["q"] = pd.qcut(G2.z20, 5, labels=False)
    res = []
    for q, S in G2.groupby("q"):
        n, Gd, mu, t = ct(S); res.append([q, S.z20.mean(), n, Gd, mu, t])
    out["grid_fwd5_by_prior20_z"] = pd.DataFrame(res, columns=["q", "z20", "n", "days", "mean_unus", "t"])
    # 6. weekday 1-day returns
    D["u1"] = D["r1"] - D.groupby("coin")["r1"].transform("mean")
    res = []
    for wdy, S in D.groupby("wd"):
        n, Gd, mu, t = ct(S, "u1"); res.append([wdy, n, mu, t])
    out["weekday_r1"] = pd.DataFrame(res, columns=["wd", "n", "mean_unus1", "t"])
    # 7. wide days by body direction & prior sign: fwd in direction of today's body
    wd2 = first_per_cell(D[(D.width >= 1.5) & (D.body >= 0.5)]).copy()
    wd2["dirn"] = np.sign(wd2.clv)
    wd2["dunus"] = wd2.unus * wd2.dirn
    out["wide_strong_body_fwd_in_body_dir"] = pd.Series(ct(wd2, "dunus"), index=["n", "days", "mean", "t"])
    out["drift_usual"] = pd.DataFrame({"drift": drift, "usual": usual})
    return out
