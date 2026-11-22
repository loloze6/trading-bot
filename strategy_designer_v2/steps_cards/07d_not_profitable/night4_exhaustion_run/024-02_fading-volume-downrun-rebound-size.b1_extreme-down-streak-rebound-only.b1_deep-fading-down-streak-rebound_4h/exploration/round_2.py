def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # cases: grid cells of 18 bars, first bar in the cell where forecast rises >=2 from 0 (approx: forecast>0 and previous ==0)
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float)
            f = b["forecast"].fillna(0).values
            n = len(b)
            lr = np.diff(np.log(cl), prepend=np.nan)
            absr = pd.Series(np.abs(lr)).rolling(180, min_periods=60).mean().values
            hi30 = pd.Series(cl).rolling(180, min_periods=60).max().values
            pos = (f > 0).astype(float)
            active3d = pd.Series(pos).rolling(18, min_periods=1).sum().shift(1).values
            active7d = pd.Series(pos).rolling(42, min_periods=1).sum().shift(1).values
            ma30 = pd.Series(cl).rolling(180, min_periods=60).mean().values
            seen = set()
            for i in range(1, n - 18):
                if f[i] >= 2 and f[i - 1] < 2:
                    cell = i // 18
                    if cell in seen: continue
                    seen.add(cell)
                    rows.append(dict(coin=c, wn=int(w[1:]), fwd=cl[i + 18] / cl[i] - 1,
                        p7=cl[i] / cl[i - 42] - 1 if i >= 42 else np.nan,
                        p30=cl[i] / cl[i - 180] - 1 if i >= 180 else np.nan,
                        offhi=(cl[i] / hi30[i] - 1) / absr[i] if absr[i] > 0 else np.nan,
                        trend=(cl[i] / ma30[i] - 1) / absr[i] if absr[i] > 0 else np.nan,
                        act3=active3d[i], act7=active7d[i], f=f[i]))
    C = pd.DataFrame(rows)
    out["n_cases"] = len(C)
    out["mean_fwd"] = float(C["fwd"].mean())
    def grp(col, q=5):
        s = C.dropna(subset=[col]).copy()
        s["q"] = pd.qcut(s[col].rank(method="first"), q, labels=False)
        a = s.groupby("q").agg(n=("fwd", "size"), lo=(col, "min"), hi=(col, "max"),
                               mean=("fwd", "mean"), sd=("fwd", "std"))
        a["t"] = a["mean"] / (a["sd"] / np.sqrt(a["n"]))
        return a.round(4)
    for col in ["p7", "p30", "offhi", "trend", "act3", "act7"]:
        out["case_by_" + col] = grp(col)
    # rank corr
    out["spearman"] = pd.Series({col: stats.spearmanr(C[col], C["fwd"], nan_policy="omit")[0] for col in ["p7","p30","offhi","trend","act3","act7","f"]}).round(4)
    # book exposure in drawdown days vs not: mean daily allocation
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            a = b.groupby("day").agg(alloc=("postRebalance_current_allocation", "mean"))
            a["coin"] = c; a["wn"] = int(w[1:])
            rows.append(a.reset_index())
    A = pd.concat(rows)
    Dl = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["coin"] = c; x["wn"] = int(w[1:])
            Dl.append(x)
    D = pd.concat(Dl)
    D["day"] = pd.to_datetime(D["day"]).dt.tz_localize(None) if hasattr(pd.to_datetime(D["day"]).dt, "tz") and pd.to_datetime(D["day"]).dt.tz is not None else pd.to_datetime(D["day"])
    A["day"] = pd.to_datetime(A["day"]).dt.tz_localize(None) if A["day"].dt.tz is not None else A["day"]
    M = D.merge(A, on=["coin", "wn", "day"], how="left").dropna(subset=["book_return"])
    # coin's down-trend state per day: coin's 30-day return quintile
    M = M.sort_values(["coin", "wn", "day"])
    M["c30"] = M.groupby(["coin", "wn"])["coin_return"].transform(lambda s: (1 + s).rolling(30, min_periods=10).apply(np.prod, raw=True) - 1).shift(0)
    M["c30"] = M.groupby(["coin", "wn"])["c30"].shift(1)
    M["q"] = pd.qcut(M["c30"].rank(method="first"), 5, labels=False)
    out["book_by_coin_prior30d"] = M.groupby("q").agg(n=("book_return", "size"), c30lo=("c30", "min"), c30hi=("c30", "max"),
        alloc=("alloc", "mean"), book=("book_return", "mean"), coin=("coin_return", "mean"),
        book_sd=("book_return", "std")).round(5)
    out["share_days_invested"] = float((M["alloc"].abs() > 0.01).mean())
    return out
