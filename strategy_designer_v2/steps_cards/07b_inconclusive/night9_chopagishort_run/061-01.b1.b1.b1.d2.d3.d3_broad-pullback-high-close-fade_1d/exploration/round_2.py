def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    hs = [1, 2, 3, 5]
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            n = len(df)
            rng = h - l
            loc = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            r1 = pd.Series(c).pct_change().values
            sd30 = pd.Series(r1).rolling(30).std()
            agi = sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True).values
            mad = pd.Series(np.abs(r1)).rolling(20).mean().values
            prior = np.full(n, np.nan)
            prior[6:] = c[5:-1] / c[:-6] - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(n):
                d = dict(coin=coin, w=w, i=i, day=ts.iloc[i].floor("D"), year=ts.iloc[i].year,
                         loc=loc[i], r1=r1[i], mad=mad[i], prior=prior[i], agi=agi[i])
                for hh in hs:
                    d[f"f{hh}"] = c[i + hh] / c[i] - 1 if i + hh < n else np.nan
                rows.append(d)
    A = pd.DataFrame(rows)
    for hh in hs:
        dr = A[A["i"] % hh == 0].groupby("coin")[f"f{hh}"].mean()
        A[f"u{hh}"] = -(A[f"f{hh}"] - A["coin"].map(dr))
    A["pm"] = A["prior"] / (A["mad"] * np.sqrt(5))  # prior fall in usual moves
    A["sit"] = (A["loc"] >= 0.75) & (A["r1"] > 0) & (A["prior"] < 0)
    A["base"] = (A["r1"] > 0) & (A["prior"] < 0)  # up day after fall, any close location

    def cases(mask, hh):
        S = A[mask].copy(); S["cell"] = S["i"] // hh
        return S.sort_values("i").groupby(["coin", "w", "cell"]).head(1)

    def ct(S, col):
        S = S.dropna(subset=[col])
        if len(S) < 5:
            return pd.Series(dict(n=len(S), days=0, mean=np.nan, t=np.nan))
        m = S[col].mean()
        d = S.groupby("day")[col].apply(lambda x: (x - m).sum())
        se = np.sqrt((d ** 2).sum()) / len(S)
        return pd.Series(dict(n=len(S), days=S["day"].nunique(), mean=m, t=m / se))

    out = {}
    S5 = cases(A["sit"], 5)
    S5["pq"] = pd.qcut(S5["pm"], 5, labels=["q1deep", "q2", "q3", "q4", "q5shallow"])
    out["sit h5 by prior fall in usual moves, quintile"] = S5.groupby("pq").apply(lambda g: ct(g, "u5"))
    out["sit h5 corr prior-fall size vs unusual move"] = pd.Series(dict(
        spearman=S5[["pm", "u5"]].dropna().corr("spearman").iloc[0, 1],
        n=len(S5[["pm", "u5"]].dropna())))
    S5["deep"] = S5["pm"] <= S5["pm"].median()
    out["sit h5 deep half by year"] = S5[S5["deep"]].groupby("year").apply(lambda g: ct(g, "u5"))
    out["sit h5 shallow half by year"] = S5[~S5["deep"]].groupby("year").apply(lambda g: ct(g, "u5"))
    out["sit h5 deep half by coin"] = S5[S5["deep"]].groupby("coin").apply(lambda g: ct(g, "u5"))
    S5["ag"] = np.where(S5["agi"] > 0.5, "agitated", np.where(S5["agi"].notna(), "calm", "na"))
    out["sit h5 deep half by agitation"] = S5[S5["deep"]].groupby("ag").apply(lambda g: ct(g, "u5"))
    for hh in [1, 2, 3]:
        S = cases(A["sit"], hh)
        S["pq"] = pd.qcut(S["pm"], 5, labels=["q1deep", "q2", "q3", "q4", "q5shallow"])
        out[f"sit h{hh} by prior fall quintile"] = S.groupby("pq").apply(lambda g: ct(g, f"u{hh}"))
    B5 = cases(A["base"], 5)
    B5["pq"] = pd.qcut(B5["pm"], 5, labels=["q1deep", "q2", "q3", "q4", "q5shallow"])
    B5["hi"] = B5["loc"] >= 0.75
    out["up day after fall, any close, h5 by prior quintile x high close"] = B5.groupby(["pq", "hi"]).apply(lambda g: ct(g, "u5"))
    return out
