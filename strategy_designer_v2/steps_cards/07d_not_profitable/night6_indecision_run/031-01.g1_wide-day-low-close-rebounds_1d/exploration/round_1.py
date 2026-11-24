def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    wins = sorted({w for c in data["days"] for w in data["days"][c]}, key=lambda s: int(s[1:]))
    # book daily
    rows = []
    for w in wins:
        frames = []
        for c in data["days"]:
            if w in data["days"][c]:
                d = data["days"][c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        d = pd.concat(frames)
        g = d.groupby("day")[["book_return", "coin_return"]].mean().reset_index()
        g["w"] = w
        rows.append(g)
    book = pd.concat(rows).dropna(subset=["book_return"]).reset_index(drop=True)
    v = (1 + book["book_return"]).cumprod()
    dd = v / v.cummax() - 1
    book["dd"] = dd
    out["max_dd"] = float(dd.min())
    out["yearly"] = float(v.iloc[-1] ** (365 / len(v)) - 1)
    # per window drawdown/return
    pw = book.groupby("w").agg(ret=("book_return", lambda x: (1 + x).prod() - 1),
                               worst_day=("book_return", "min"), mindd=("dd", "min"))
    out["per_window"] = pw.reindex(wins)
    # worst book days count
    out["worst_days_share"] = pd.Series({
        "n_days": len(book),
        "sum_ret": book["book_return"].sum(),
        "sum_worst10": book["book_return"].nsmallest(10).sum(),
        "sum_best10": book["book_return"].nlargest(10).sum()})
    # cases
    cases = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            rng = h - l
            mr20 = rng.rolling(20).mean()
            mr20p = rng.shift(1).rolling(20).mean()
            df = pd.DataFrame({
                "coin": c, "w": w,
                "fwd1": cl.shift(-1) / cl - 1,
                "fwd3": cl.shift(-3) / cl - 1,
                "ret1": cl / cl.shift(1) - 1,
                "ret5": cl / cl.shift(5) - 1,
                "ret20": cl / cl.shift(20) - 1,
                "body": (cl - o) / rng.replace(0, np.nan),
                "rmult": rng / mr20,
                "cloc": (cl - l) / rng.replace(0, np.nan),
                "vol20": cl.pct_change().rolling(20).std(),
                "vol60": cl.pct_change().rolling(60).std(),
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            df["volr"] = df["vol20"] / df["vol60"]
            df["above_ma50"] = (cl > cl.rolling(50).mean()).astype(float)
            cases.append(df)
    allb = pd.concat(cases, ignore_index=True)
    drift = allb.groupby("coin")["fwd1"].mean()
    allb["ex1"] = allb["fwd1"] - allb["coin"].map(drift)
    sig = allb[allb["fc"] > 0].dropna(subset=["fwd1"]).copy()
    out["n_cases"] = len(sig)
    def summ(g):
        return pd.Series({"n": len(g), "mean_fwd1": g["fwd1"].mean(), "t": stats.ttest_1samp(g["fwd1"], 0).statistic if len(g) > 2 else np.nan,
                          "hit": (g["fwd1"] > 0).mean(), "worst": g["fwd1"].min(), "mean_alloc": g["alloc"].mean()})
    out["by_coin"] = sig.groupby("coin").apply(summ)
    out["by_year"] = sig.groupby("year").apply(summ)
    for col in ["ret1", "ret5", "ret20", "body", "rmult", "volr", "vol20"]:
        q = pd.qcut(sig[col], 4, duplicates="drop")
        out["sig_by_" + col] = sig.groupby(q.cat.codes).apply(summ)
    out["sig_by_ma50"] = sig.groupby("above_ma50").apply(summ)
    # largest losing cases: their features
    lo = sig.nsmallest(30, "fwd1")
    out["worst30_feat_vs_all"] = pd.DataFrame({"worst30": lo[["ret1", "ret5", "ret20", "body", "rmult", "volr", "alloc"]].mean(),
                                               "all": sig[["ret1", "ret5", "ret20", "body", "rmult", "volr", "alloc"]].mean()})
    # pnl contribution: alloc*fwd1
    sig["pnl"] = sig["alloc"] * sig["fwd1"]
    out["pnl_by_ret5_q"] = sig.groupby(pd.qcut(sig["ret5"], 4).cat.codes)["pnl"].agg(["sum", "mean", "std"])
    out["pnl_by_volr_q"] = sig.groupby(pd.qcut(sig["volr"], 4).cat.codes)["pnl"].agg(["sum", "mean", "std"])
    return out
