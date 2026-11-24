def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sgn = np.sign(c.diff()).fillna(0).values
            st = np.zeros(len(c))
            for i in range(1, len(c)):
                if sgn[i] == 0:
                    st[i] = 0
                elif np.sign(st[i-1]) == sgn[i]:
                    st[i] = st[i-1] + sgn[i]
                else:
                    st[i] = sgn[i]
            fwd = c.shift(-H) / c - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(c)),
                "ts": pd.to_datetime(b["timestamp"]),
                "streak": st, "r1": r1,
                "r5p": c / c.shift(5) - 1, "r20p": c / c.shift(20) - 1,
                "vol20": r1.rolling(20).std(),
                "rng": (b["high"] - b["low"]) / c,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fwd": fwd})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    G["drift"] = G.groupby("coin")["fwd"].transform("mean")
    G["usual"] = G.groupby("coin")["fwd"].transform("std")
    G["ex"] = G["fwd"] - G["drift"]
    G["z"] = G["ex"] / G["usual"]
    G["day"] = G["ts"].dt.floor("D")
    # within-coin standardised features
    for f in ["r1", "r5p", "r20p", "vol20", "rng"]:
        G[f + "_z"] = G.groupby("coin")[f].transform(lambda s: (s - s.mean()) / s.std())

    def tclust(sub):
        s = sub.groupby("day")["ex"].sum()
        n = len(s)
        if n < 3: return np.nan
        # t of mean per case with day clustering
        m = sub["ex"].mean()
        se = np.sqrt(((sub.groupby("day")["ex"].apply(lambda x: (x - m).sum())) ** 2).sum()) / len(sub)
        return m / se if se > 0 else np.nan

    def table(key):
        out = []
        for k, sub in G.groupby(key):
            out.append({key: k, "n": len(sub), "days": sub["day"].nunique(),
                        "mean_ex_%": 100 * sub["ex"].mean(), "mean_z": sub["z"].mean(),
                        "t": tclust(sub)})
        return pd.DataFrame(out)

    def slope(f):
        sub = G[[f, "ex", "day"]].dropna()
        x = sub[f] - sub[f].mean()
        b = (x * sub["ex"]).sum() / (x ** 2).sum()
        e = sub["ex"] - sub["ex"].mean() - b * x
        sc = (x * e).groupby(sub["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (x ** 2).sum()
        return pd.Series({"slope": b, "t": b / se, "n": len(sub), "days": sub["day"].nunique()})

    G["streak_b"] = G["streak"].clip(-5, 5)
    G["r1_q"] = G.groupby("coin")["r1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    G["r5p_q"] = G.groupby("coin")["r5p"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    G["r20p_q"] = G.groupby("coin")["r20p"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    G["vol_q"] = G.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    G["rng_q"] = G.groupby("coin")["rng"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    G["wd"] = G["ts"].dt.weekday
    G["year"] = G["ts"].dt.year

    slopes = pd.DataFrame({f: slope(f) for f in ["streak", "r1_z", "r5p_z", "r20p_z", "vol20_z", "rng_z"]}).T

    # book: days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    book = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    q = book["book_return"].quantile([0.02, 0.98])
    bigd = pd.DataFrame({
        "book_worst2%_mean": book.loc[book.book_return <= q.iloc[0]].mean(),
        "book_best2%_mean": book.loc[book.book_return >= q.iloc[1]].mean()})
    corr = book.corr().iloc[0, 1]

    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    trades = T.groupby(["coin", "side"]).agg(n=("net_profit_loss_percent", "size"),
                                            mean_net=("net_profit_loss_percent", "mean"),
                                            med_days=("duration_minutes", lambda x: x.median() / 1440)).reset_index()

    return {"slopes_on_grid": slopes,
            "by_streak": table("streak_b"),
            "by_1d_return_quintile": table("r1_q"),
            "by_5d_return_quintile": table("r5p_q"),
            "by_20d_return_quintile": table("r20p_q"),
            "by_vol20_quintile": table("vol_q"),
            "by_range_quintile": table("rng_q"),
            "by_weekday": table("wd"),
            "by_year": table("year"),
            "by_coin": table("coin"),
            "book_extreme_days": bigd,
            "book_vs_hold_daily_corr": corr,
            "trades": trades,
            "mean_alloc": A["alloc"].mean()}
