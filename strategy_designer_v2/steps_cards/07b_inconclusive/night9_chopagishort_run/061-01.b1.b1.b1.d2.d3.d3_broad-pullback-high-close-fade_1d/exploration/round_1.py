def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    hs = [1, 2, 3, 5, 10]
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            n = len(df)
            rng = h - l
            loc = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            r1 = pd.Series(c).pct_change().values
            mad = pd.Series(np.abs(r1)).rolling(20).mean().shift(0).values
            prior = np.full(n, np.nan)
            prior[6:] = c[5:-1] / c[:-6] - 1
            tr60 = np.full(n, np.nan)
            tr60[60:] = c[60:] / c[:-60] - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(n):
                fwd = {}
                for hh in hs:
                    fwd[hh] = c[i + hh] / c[i] - 1 if i + hh < n else np.nan
                rows.append(dict(coin=coin, w=w, i=i, day=ts.iloc[i].floor("D"), year=ts.iloc[i].year,
                                 loc=loc[i], r1=r1[i], mad=mad[i], prior=prior[i], tr60=tr60[i],
                                 fc=df["forecast"].iloc[i], **{f"f{hh}": fwd[hh] for hh in hs}))
    A = pd.DataFrame(rows)
    # drift per coin and horizon: non-overlapping grid
    drift = {}
    for hh in hs:
        g = A[A["i"] % hh == 0].groupby("coin")[f"f{hh}"].mean()
        drift[hh] = g
    for hh in hs:
        A[f"u{hh}"] = -(A[f"f{hh}"] - A["coin"].map(drift[hh]))
    A["sit"] = (A["loc"] >= 0.75) & (A["r1"] > 0) & (A["prior"] < 0)
    A["sit_nofall"] = (A["loc"] >= 0.75) & (A["r1"] > 0)
    A["gain_mult"] = A["r1"] / A["mad"]

    def cases(mask, hh):
        S = A[mask].copy()
        S["cell"] = S["i"] // hh
        S = S.sort_values("i").groupby(["coin", "w", "cell"]).head(1)
        return S

    def ct(S, col):
        S = S.dropna(subset=[col])
        if len(S) < 5:
            return pd.Series(dict(n=len(S), days=0, mean=np.nan, t=np.nan))
        d = S.groupby("day")[col].apply(lambda x: (x - S[col].mean()).sum())
        m = S[col].mean()
        se = np.sqrt((d ** 2).sum()) / len(S)
        return pd.Series(dict(n=len(S), days=S["day"].nunique(), mean=m, t=m / se if se > 0 else np.nan))

    out = {}
    hz = pd.DataFrame({f"h{hh}": ct(cases(A["sit"], hh), f"u{hh}") for hh in hs}).T
    out["by horizon, situation"] = hz
    hz2 = pd.DataFrame({f"h{hh}": ct(cases(A["sit_nofall"], hh), f"u{hh}") for hh in hs}).T
    out["by horizon, no prior-fall condition"] = hz2
    S5 = cases(A["sit"], 5)
    out["by coin h5"] = S5.groupby("coin").apply(lambda g: ct(g, "u5"))
    out["by window h5"] = S5.groupby("w").apply(lambda g: ct(g, "u5"))
    out["by year h5"] = S5.groupby("year").apply(lambda g: ct(g, "u5"))
    S5["trend"] = pd.cut(S5["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["by trend h5"] = S5.groupby("trend").apply(lambda g: ct(g, "u5"))
    S2 = cases(A["sit"], 2)
    S2["trend"] = pd.cut(S2["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["by trend h2"] = S2.groupby("trend").apply(lambda g: ct(g, "u2"))
    S5["gq"] = pd.qcut(S5["gain_mult"], 4, labels=["g1small", "g2", "g3", "g4large"])
    out["by gain quartile h5"] = S5.groupby("gq").apply(lambda g: ct(g, "u5"))
    S5["pq"] = pd.qcut(S5["prior"], 4, labels=["p1deepfall", "p2", "p3", "p4shallow"])
    out["by prior fall quartile h5"] = S5.groupby("pq").apply(lambda g: ct(g, "u5"))
    S5["lq"] = pd.cut(S5["loc"], [0.74, 0.85, 0.95, 1.01], labels=["0.75-0.85", "0.85-0.95", "0.95-1"])
    out["by close loc h5"] = S5.groupby("lq").apply(lambda g: ct(g, "u5"))
    S5["traded"] = S5["fc"] < 0
    out["by forecast<0 h5"] = S5.groupby("traded").apply(lambda g: ct(g, "u5"))
    return out
