def explore(data):
    import numpy as np, pandas as pd
    out = {}
    wins = [f"w{i}" for i in range(1, 25)]
    coins = list(data["bars"].keys())
    # drift per coin over 120 bars, non-overlapping, all windows
    drift = {}; usual = {}
    for c in coins:
        rr = []
        for w, b in data["bars"][c].items():
            cl = b["close"].values.astype(float)
            g = cl[::120]
            rr += list(g[1:] / g[:-1] - 1)
        drift[c] = np.mean(rr); usual[c] = np.std(rr)
    # daily exposure and coin-state per coin-day
    D = []
    C = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            cl = b["close"].astype(float)
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["al"] = b["postRebalance_current_allocation"].fillna(0)
            b["r720"] = cl.pct_change(720)
            b["r1440"] = cl.pct_change(1440)
            b["ma"] = cl / cl.rolling(1440, min_periods=500).mean() - 1
            dd_ = b.groupby("day").agg(al=("al", "mean"), r720=("r720", "last"), ma=("ma", "last"))
            dd_["coin"] = c; dd_["w"] = w
            dd_ = dd_.reset_index()
            dd_ = dd_.merge(data["days"][c][w][["day", "book_return", "coin_return"]].assign(day=lambda x: pd.to_datetime(x["day"])), on="day", how="left")
            D.append(dd_)
            # cases: first bar per 120-grid cell with forecast rise >=2 approx: forecast >=2 and prev forecast lower by >=2 from cell low
            f = b["forecast"].fillna(0).values
            r24 = cl.pct_change(24); ratio = (r24 / r24.abs().rolling(720, min_periods=120).mean()).values
            r168 = cl.pct_change(168).values
            clv = cl.values
            n = len(clv)
            low = 0.0
            for s in range(0, n - 120, 120):
                for k in range(s, s + 120):
                    if f[k] - low >= 2:
                        C.append({"coin": c, "w": w, "ex": clv[s + 120 if False else min(k + 120, n - 1)] / clv[k] - 1 - drift[c] if k + 120 < n else np.nan,
                                  "ratio": ratio[k], "r168": r168[k], "r720": b["r720"].values[k], "r1440": b["r1440"].values[k],
                                  "ma": b["ma"].values[k], "f": f[k]})
                        low = f[k]
                        break
                    low = min(low, f[k])
    D = pd.concat(D)
    D["mkt"] = D["al"] * D["coin"].map({c: None for c in coins})
    mdr = D.groupby("coin")["coin_return"].mean()
    D["mkt"] = D["al"] * D["coin"].map(mdr)
    out["decomp_daily"] = pd.Series({"book_mean": D["book_return"].mean(), "market_part": D["mkt"].mean(), "mean_alloc": D["al"].mean()})
    D["ma_q"] = pd.qcut(D["ma"], 5)
    out["coin_day_by_ma60"] = D.dropna(subset=["book_return"]).groupby("ma_q", observed=True).agg(n=("al", "size"), al=("al", "mean"), book=("book_return", "mean"), coin=("coin_return", "mean"), book_sd=("book_return", "std"))
    D["r720_q"] = pd.qcut(D["r720"], 5)
    out["coin_day_by_r30d"] = D.dropna(subset=["book_return"]).groupby("r720_q", observed=True).agg(n=("al", "size"), al=("al", "mean"), book=("book_return", "mean"), coin=("coin_return", "mean"), book_sd=("book_return", "std"))
    C = pd.DataFrame(C).dropna(subset=["ex"])
    out["cases_n_mean"] = pd.Series({"n": len(C), "mean_ex": C["ex"].mean(), "t": C["ex"].mean() / C["ex"].std() * np.sqrt(len(C))})
    tfun = lambda x: x.mean() / (x.std() / np.sqrt(len(x)))
    for fcol in ["ratio", "r168", "r720", "r1440", "ma"]:
        q = pd.qcut(C[fcol], 5, duplicates="drop")
        out["cases_by_" + fcol] = C.groupby(q, observed=True).agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tfun), lt_m10=("ex", lambda x: (x < -0.10).mean()))
    # ratio graded inside positive vs negative 60-day trend
    C["up60"] = np.where(C["ma"] > 0, "above60avg", "below60avg")
    C["rq"] = pd.qcut(C["ratio"], 3, duplicates="drop")
    out["cases_ratio_by_trend60"] = C.groupby(["up60", "rq"], observed=True).agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tfun))
    return out
