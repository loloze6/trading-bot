def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            # down run before today and up run
            down = (r < 0).astype(int); up = (r > 0).astype(int)
            drun = np.zeros(len(b)); urun = np.zeros(len(b))
            for i in range(1, len(b)):
                drun[i] = drun[i-1] + 1 if down[i] else 0
                urun[i] = urun[i-1] + 1 if up[i] else 0
            prev_drun = pd.Series(drun).shift(1)
            prev_urun = pd.Series(urun).shift(1)
            vol20 = r.rolling(20).std()
            ts = pd.to_datetime(b["timestamp"])
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"])
            ret5 = c / c.shift(5) - 1
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "nxt": nxt,
                               "drun": drun, "urun": urun, "pdrun": prev_drun, "purun": prev_urun,
                               "vol20": vol20, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "infc": (b["regime"] != "chop").values, "regime": b["regime"].values,
                               "alloc": b["postRebalance_current_allocation"], "rng": rng, "clpos": clpos,
                               "ret5": ret5, "day": ts.dt.floor("D")})
            df["z"] = df["r"] / df["vol20"]
            df["z5"] = df["ret5"] / (df["vol20"] * np.sqrt(5))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "r"])
    cm = A.groupby("coin")["nxt"].transform("mean")
    A["un"] = A["nxt"] - cm
    def summ(g):
        x = g["un"]
        return pd.Series({"n": len(x), "mean_un%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["profile share"] = A.groupby("regime").size()
    # run-break up days by prior down-run, in vs out of falling calm
    rb = A[(A["r"] > 0) & (A["pdrun"] >= 1)].copy()
    rb["runb"] = rb["pdrun"].clip(upper=5)
    out["run-break nxt by run, in falling calm"] = rb[rb["infc"]].groupby("runb").apply(summ)
    out["run-break nxt by run, outside"] = rb[~rb["infc"]].groupby("runb").apply(summ)
    # continuation of down runs: on a down day, by current run length
    dd = A[A["r"] < 0].copy(); dd["runb"] = dd["drun"].clip(upper=6)
    out["down day nxt by down run length, all"] = dd.groupby("runb").apply(summ)
    uu = A[A["r"] > 0].copy(); uu["runb"] = uu["urun"].clip(upper=6)
    out["up day nxt by up run length, all"] = uu.groupby("runb").apply(summ)
    # z-score buckets
    A["zq"] = pd.qcut(A["z"], 10, labels=False, duplicates="drop")
    out["nxt by z decile, all"] = A.groupby("zq").apply(summ)
    out["nxt by z decile, in falling calm"] = A[A["infc"]].groupby("zq").apply(summ)
    A["z5q"] = pd.qcut(A["z5"], 5, labels=False, duplicates="drop")
    out["nxt by 5d z quintile"] = A.groupby("z5q").apply(summ)
    out["nxt by weekday"] = A.groupby("wd").apply(summ)
    A["vq"] = A.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["nxt by vol quartile"] = A.groupby("vq").apply(summ)
    A["cq"] = pd.qcut(A["clpos"], 5, labels=False, duplicates="drop")
    out["nxt by close position quintile"] = A.groupby("cq").apply(summ)
    out["nxt by close pos, falling calm"] = A[A["infc"]].groupby("cq").apply(summ)
    # book daily: largest gains/losses
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D)
    bk = D.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(["count", "mean", "std"])
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin, w=w))
    T = pd.concat(T)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "std"])
    return out
