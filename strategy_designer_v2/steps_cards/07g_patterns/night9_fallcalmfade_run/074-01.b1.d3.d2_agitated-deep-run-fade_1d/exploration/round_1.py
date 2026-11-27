def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            dn = (r < 0).astype(int)
            run = np.zeros(len(b)); cnt = 0
            for i in range(len(b)):
                if i == 0 or np.isnan(r.iloc[i]):
                    cnt = 0; run[i] = 0; continue
                if r.iloc[i] < 0:
                    cnt += 1; run[i] = 0
                else:
                    run[i] = cnt; cnt = 0
            # run before an up day; for down days record current down count
            dcount = np.zeros(len(b)); k = 0
            for i in range(len(b)):
                if not np.isnan(r.iloc[i]) and r.iloc[i] < 0: k += 1
                else: k = 0
                dcount[i] = k
            vol30 = r.abs().rolling(30, min_periods=20).mean()
            ret20 = c / c.shift(20) - 1
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "r": r, "nxt": nxt, "runbrk": run,
                              "dcount": dcount, "vol30": vol30, "ret20": ret20,
                              "inprof": (b["regime"] != "chop").values,
                              "regime": b["regime"].values,
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "wd": ts.dt.weekday, "year": ts.dt.year,
                              "rz": r / vol30, "range": (b["high"] - b["low"]) / c,
                              "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["nxt", "r"])
    mu = D.groupby("coin")["nxt"].mean()
    D["unx"] = D["nxt"] - D["coin"].map(mu)
    def summ(g):
        x = g["unx"]
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    D["upday"] = D["r"] > 0
    brk = D[D["upday"]].copy()
    brk["runc"] = brk["runbrk"].clip(upper=5)
    out["upday next by run len x inprof"] = brk.groupby(["inprof", "runc"]).apply(summ)
    out["share in profile"] = D["inprof"].mean()
    # after large standardized moves, in vs out of profile
    D["rzq"] = pd.qcut(D["rz"], 7, labels=False, duplicates="drop")
    out["next by today's z-move x inprof"] = D.groupby(["inprof", "rzq"]).apply(summ)
    # down-day streak continuation
    dd = D[D["r"] < 0].copy(); dd["dc"] = dd["dcount"].clip(upper=5)
    out["after down day by streak x inprof"] = dd.groupby(["inprof", "dc"]).apply(summ)
    # weekday in profile
    out["weekday inprof"] = D[D["inprof"]].groupby("wd").apply(summ)
    out["weekday out"] = D[~D["inprof"]].groupby("wd").apply(summ)
    # close position in range, in profile
    D["clq"] = pd.qcut(D["clpos"], 5, labels=False, duplicates="drop")
    out["next by close pos x inprof"] = D.groupby(["inprof", "clq"]).apply(summ)
    # by 20d return quintile overall
    D["r20q"] = pd.qcut(D["ret20"], 5, labels=False, duplicates="drop")
    out["next by 20d ret quintile x inprof"] = D.groupby(["inprof", "r20q"]).apply(summ)
    # book trades
    held = D[D["alloc"] < 0]
    out["book held: by year"] = held.groupby("year").apply(summ)
    out["book held: by coin"] = held.groupby("coin").apply(summ)
    return out
