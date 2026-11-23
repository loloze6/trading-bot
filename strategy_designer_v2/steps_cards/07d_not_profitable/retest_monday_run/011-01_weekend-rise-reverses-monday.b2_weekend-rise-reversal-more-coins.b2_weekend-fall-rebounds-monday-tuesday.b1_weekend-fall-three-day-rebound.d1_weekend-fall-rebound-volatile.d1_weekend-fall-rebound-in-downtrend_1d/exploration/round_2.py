def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for wn, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values; n = len(b)
            s = pd.Series(cl)
            r1 = s.pct_change().values; r20 = s.pct_change(20).values
            lr = np.log(s).diff(); vol20 = lr.rolling(20).std().values; vol60 = lr.rolling(60).std().values
            mx20 = s.rolling(20).max().values
            fc = b["forecast"].values; al = b["postRebalance_current_allocation"].values
            for i in range(0, n-3):
                rows.append(dict(coin=c, wn=int(wn[1:]), pos=i, dow=ts[i].dayofweek, r1=r1[i], r20=r20[i], vol20=vol20[i],
                                 volr=vol20[i]/vol60[i] if vol60[i] else np.nan, dfm=cl[i]/mx20[i]-1,
                                 fwd=cl[i+3]/cl[i]-1, fc=fc[i], alloc=al[i], key=(int(wn[1:]), ts[i].normalize())))
    A = pd.DataFrame(rows)
    # normal drift per coin: non-overlapping 3-bar grid
    grid = A[A["pos"] % 3 == 0]
    drift = grid.groupby("coin")["fwd"].mean(); usual = grid.groupby("coin")["fwd"].std()
    A["unus"] = A["fwd"] - A["coin"].map(drift)
    A["str"] = A["unus"] / A["coin"].map(usual)
    S = A[A["dow"] == 6]
    case = S[S["fc"] > 0].copy()
    def summ(x):
        n = len(x); m = x["unus"].mean(); sd = x["unus"].std()
        return pd.Series(dict(n=n, unus=m, t=m/(sd/np.sqrt(n)) if n > 1 else np.nan, strength=x["str"].mean(),
                              p05=x["fwd"].quantile(.05), alloc=x["alloc"].mean()))
    # condition alone checks (Sunday, weekend rise or flat) vs with weekend fall
    S2 = S.dropna(subset=["dfm","r20","vol20"]).copy()
    S2["wkfall"] = S2["r1"] < 0
    S2["deep"] = S2["dfm"] < -0.2
    S2["vhi"] = S2["vol20"] > S2["vol20"].median()
    S2["vup"] = S2["volr"] > 1.0
    out["deep_x_wkfall"] = S2.groupby(["deep","wkfall"]).apply(summ)
    out["vup_x_wkfall_in_neg20"] = S2[S2["r20"] < 0].groupby(["vup","wkfall"]).apply(summ)
    out["vhi_x_wkfall_in_neg20"] = S2[S2["r20"] < 0].groupby(["vhi","wkfall"]).apply(summ)
    # all days of week: deep drawdown + one-day fall, to see if Sunday matters
    A2 = A.dropna(subset=["dfm"]).copy()
    A2 = A2[(A2["dfm"] < -0.2) & (A2["r1"] < -0.02)]
    out["deep_fall_by_dow"] = A2[A2["pos"] % 3 == 0].groupby("dow").apply(summ)
    # graded: r1 scaled by vol20
    c2 = case.dropna(subset=["vol20"]).copy()
    c2["z1"] = c2["r1"]/c2["vol20"]
    c2["zb"] = pd.qcut(c2["z1"], 4)
    out["by_r1_over_vol"] = c2.groupby("zb", observed=True).apply(summ).reset_index().astype({"zb": str})
    # crowding: number of coins in a case the same Sunday
    cnt = case.groupby("key")["coin"].transform("count") / case.groupby("key")["coin"].transform("size")
    case["ncoins_same"] = case.groupby("key")["coin"].transform("count")
    case["crowd"] = pd.cut(case["ncoins_same"], [0, 3, 7, 12, 30])
    out["by_crowding"] = case.groupby("crowd", observed=True).apply(summ).reset_index().astype({"crowd": str})
    # cases with nan r20 (start of window)
    case["r20nan"] = case["r20"].isna()
    out["r20_missing"] = case.groupby("r20nan").apply(summ)
    # stronger case: deep dfm and big r1
    c3 = case.dropna(subset=["dfm"]).copy()
    c3["strong"] = (c3["dfm"] < -0.2) & (c3["r1"] < -0.02)
    out["strong_vs_rest"] = c3.groupby("strong").apply(summ)
    # by window for strong
    out["strong_by_window_group"] = c3[c3["strong"]].assign(g=lambda x: pd.cut(x["wn"], [0,6,12,18,24])).groupby("g", observed=True).apply(summ).reset_index().astype({"g": str})
    return out
