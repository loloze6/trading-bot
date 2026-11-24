def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd60 = r.rolling(60, min_periods=30).std()
            sd10 = r.rolling(10, min_periods=8).std()
            z = r / sd60
            # streak: signed count of consecutive same-direction closes
            s = np.sign(r.fillna(0)).values
            st = np.zeros(len(s))
            for i in range(len(s)):
                if s[i] == 0: st[i] = 0
                elif i > 0 and np.sign(st[i-1]) == s[i]: st[i] = st[i-1] + s[i]
                else: st[i] = s[i]
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "z": z, "ratio": sd10 / sd60, "streak": st,
                "r5z": r5 / (sd60 * np.sqrt(5)), "r20z": r20 / (sd60 * np.sqrt(20)),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f5": c.shift(-5) / c - 1,
                "fc": b["forecast"].astype(float), "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "ts": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 2, 5]:
        A[f"x{h}"] = A[f"f{h}"] - A.groupby("coin")[f"f{h}"].transform(
            lambda s: s[A.loc[s.index, "pos"] % h == 0].mean())
    def tab(df, key, h):
        g = df[df.pos % h == 0].dropna(subset=[key, f"x{h}"])
        res = g.groupby(key)[f"x{h}"].agg(["mean", "count", "std"])
        res["t"] = res["mean"] / (res["std"] / np.sqrt(res["count"]))
        return res.drop(columns="std")
    A["zq"] = pd.cut(A["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    for h in [1, 2, 5]:
        out[f"excess {h}d by day z"] = tab(A, "zq", h)
    A["rq"] = pd.qcut(A["ratio"], 4, labels=["lowvol", "q2", "q3", "hivol"])
    sub = A[A.z > 1]
    out["after up day z>1, 2d excess by volratio"] = tab(sub, "rq", 2)
    sub = A[A.z < -1]
    out["after down day z<-1, 2d excess by volratio"] = tab(sub, "rq", 2)
    A["stc"] = A["streak"].clip(-5, 5)
    out["2d excess by streak"] = tab(A, "stc", 2)
    out["5d excess by streak"] = tab(A, "stc", 5)
    A["r5q"] = pd.cut(A["r5z"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["2d excess by 5d return z"] = tab(A, "r5q", 2)
    out["5d excess by 5d return z"] = tab(A, "r5q", 5)
    A["r20q"] = pd.cut(A["r20z"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["5d excess by 20d return z"] = tab(A, "r20q", 5)
    out["1d excess by weekday"] = tab(A, "wd", 1)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    out["book daily corr with coin avg"] = float(bk.corr().iloc[0, 1])
    bk["yr"] = pd.to_datetime(bk.index).year
    out["book vs hold by year mean daily"] = bk.groupby("yr")[["book_return", "coin_return"]].mean()
    q = bk["book_return"].quantile([0.02, 0.98])
    out["coin avg on book worst 2% / best 2% days"] = pd.Series({
        "worst_book": bk.loc[bk.book_return <= q.iloc[0], "book_return"].mean(),
        "coin_on_worst": bk.loc[bk.book_return <= q.iloc[0], "coin_return"].mean(),
        "best_book": bk.loc[bk.book_return >= q.iloc[1], "book_return"].mean(),
        "coin_on_best": bk.loc[bk.book_return >= q.iloc[1], "coin_return"].mean()})
    A["fcq"] = pd.cut(A["fc"], [-1, 0, 5, 10, 15, 21])
    out["2d excess by forecast"] = tab(A, "fcq", 2)
    out["2d excess by coin, z<-1"] = tab(A[A.z < -1], "coin", 2)
    out["2d excess by coin, z>1"] = tab(A[A.z > 1], "coin", 2)
    return out
