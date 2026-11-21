def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["wn"] = int(w[1:])
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), n=("coin", "count")).reset_index().sort_values(["wn", "day"]).dropna(subset=["br"])
    B["eq"] = (1 + B["br"]).cumprod(); B["dd"] = B["eq"] / B["eq"].cummax() - 1
    # exposure per day: mean allocation over coins at last bar of day
    ex = []
    T = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            alloc = b["postRebalance_current_allocation"].fillna(0)
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            e = pd.DataFrame({"day": day, "alloc": alloc, "wn": int(w[1:]), "coin": c}).groupby(["wn", "day"]).last().reset_index()
            ex.append(e)
            r60 = cl / cl.shift(60) - 1; r10 = cl / cl.shift(10) - 1
            vol20 = r1.rolling(20).std()
            hi90 = cl.rolling(90).max()
            r30 = cl / cl.shift(30) - 1
            prev = alloc.shift(1).fillna(0)
            for i in b.index[(alloc > 0) & (prev <= 0)]:
                j = i
                while j + 1 < len(b) and alloc.iloc[j + 1] > 0: j += 1
                k = min(j + 1, len(b) - 1)
                ret = cl.iloc[k] / cl.iloc[i] - 1
                T.append({"coin": c, "wn": int(w[1:]), "r60": r60.iloc[i], "r10": r10.iloc[i], "r30": r30.iloc[i],
                          "z10": r10.iloc[i] / (vol20.iloc[i] * np.sqrt(10)) if vol20.iloc[i] else np.nan,
                          "vol20": vol20.iloc[i], "alloc": alloc.iloc[i], "hold": j - i + 1, "ret": ret, "pnl": ret * alloc.iloc[i],
                          "day": day.iloc[i], "mdd_in": (cl.iloc[i:k + 1] / cl.iloc[i]).min() - 1})
    EX = pd.concat(ex)
    G = EX.groupby(["wn", "day"]).agg(expo=("alloc", "sum"), ncoins=("alloc", lambda s: (s > 0).sum())).reset_index()
    B = B.merge(G, on=["wn", "day"], how="left")
    B["indd"] = (B["dd"] < -0.15)
    out["exposure_vs_dd"] = B.groupby("indd").agg(days=("br", "size"), br=("br", "mean"), sd=("br", "std"), expo=("expo", "mean"), ncoins=("ncoins", "mean"), cr=("cr", "mean"))
    # day loss tail vs number of coins held
    B["nq"] = pd.cut(B["ncoins"], [-1, 0, 1, 2, 4, 100])
    out["day_by_ncoins"] = B.groupby("nq").agg(days=("br", "size"), br=("br", "mean"), sd=("br", "std"), p2=("br", lambda s: s.quantile(0.02)), cr=("cr", "mean"))
    # worst 20 days: how many coins held
    w20 = B.nsmallest(30, "br")
    out["worst30_days"] = pd.Series({"br_mean": w20["br"].mean(), "ncoins_mean": w20["ncoins"].mean(), "expo_mean": w20["expo"].mean(), "cr_mean": w20["cr"].mean(), "all_ncoins_mean": B["ncoins"].mean()})
    T = pd.DataFrame(T)
    # number of coins entering in same 5-day span (crowding)
    T["wk"] = T["day"].dt.floor("5D")
    T["crowd"] = T.groupby(["wn", "wk"])["coin"].transform("count")
    for f in ["crowd", "z10", "r30", "vol20", "r60"]:
        x = T.dropna(subset=[f, "ret"]).copy()
        x["q"] = pd.qcut(x[f].rank(method="first"), 5, labels=False)
        out["by_" + f] = x.groupby("q").agg(n=("ret", "size"), fmean=(f, "mean"), ret=("ret", "mean"), pnl=("pnl", "mean"), sd=("pnl", "std"), mdd=("mdd_in", "mean"), share_neg=("ret", lambda s: (s < 0).mean()))
    # trades in deep-dd periods vs others
    T = T.merge(B[["wn", "day", "dd"]], on=["wn", "day"], how="left")
    T["deep"] = T["dd"] < -0.15
    out["trades_deep_vs_not"] = T.groupby("deep").agg(n=("ret", "size"), ret=("ret", "mean"), pnl=("pnl", "mean"), r60=("r60", "median"), z10=("z10", "median"), crowd=("crowd", "mean"), vol20=("vol20", "median"))
    return out
