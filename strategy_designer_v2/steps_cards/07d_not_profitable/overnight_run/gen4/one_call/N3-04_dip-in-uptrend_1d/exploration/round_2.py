def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 70: continue
            v = b["postRebalance_total_value"].astype(float)
            c = b["close"].astype(float)
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "w": w,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            d["next_book"] = v.shift(-1) / v - 1
            d["next_coin"] = c.shift(-1) / c - 1
            d["ret1"] = r
            d["prev_ret1"] = r.shift(1)
            d["ret60"] = c / c.shift(60) - 1
            d["ret20"] = c / c.shift(20) - 1
            d["mad60"] = r.abs().rolling(60, min_periods=20).mean()
            d["z"] = r / d["mad60"]
            d["fc_prev"] = d["fc"].shift(1)
            d["dist_hi20"] = c / c.rolling(20).max() - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["next_book", "next_coin"])
    out = {}
    A = D[D["fc"] > 0].copy()
    def tt(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    # first entry vs continuing (forecast also positive the day before)
    A["cont"] = np.where(A["fc_prev"] > 0, "second_dip", "first_dip")
    out["coin_by_cont"] = A.groupby("cont")["next_coin"].apply(tt).unstack()
    # drop size by z bucket
    A["zb"] = pd.cut(-A["z"], [0, 0.6, 1, 1.5, 2, 3, 100])
    out["coin_by_dropz"] = A.groupby("zb", observed=True)["next_coin"].apply(tt).unstack()
    # trend strength 60d
    A["r60b"] = pd.qcut(A["ret60"], 3, labels=["r60_low", "r60_mid", "r60_high"])
    out["coin_by_r60"] = A.groupby("r60b", observed=True)["next_coin"].apply(tt).unstack()
    # distance from 20d high
    A["dhb"] = pd.qcut(A["dist_hi20"], 3, labels=["far_below_hi", "mid", "near_hi"])
    out["coin_by_disthi"] = A.groupby("dhb", observed=True)["next_coin"].apply(tt).unstack()
    out["coin_by_year"] = A.groupby("year")["next_coin"].apply(tt).unstack()
    # non-overlapping 3-day forward return after first dips
    rows2 = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); f = b["forecast"].astype(float)
            last = -10
            for i in range(len(b) - 3):
                if f.iloc[i] > 0 and i - last >= 3:
                    rows2.append({"r1": c.iloc[i+1]/c.iloc[i]-1, "r2_3": c.iloc[i+3]/c.iloc[i+1]-1})
                    last = i
    R = pd.DataFrame(rows2)
    out["fwd_nonoverlap"] = pd.DataFrame({"day1": tt(R["r1"]), "days2_3": tt(R["r2_3"])})
    # drawdown periods: book return on active days by year, worst days composition
    act = D[D["alloc"] > 0.01]
    worst = act.nsmallest(50, "next_book")
    out["worst50"] = pd.Series({"mean_alloc": worst["alloc"].mean(), "mean_next_coin": worst["next_coin"].mean(),
                                "share_alloc_ge1.5": (worst["alloc"] >= 1.5).mean(),
                                "share_prev_fc_pos": (worst["fc_prev"] > 0).mean(),
                                "mean_z": worst["z"].mean()})
    out["book_by_alloc"] = act.assign(ab=pd.cut(act["alloc"], [0, 0.5, 1.2, 1.8, 2.1])).groupby("ab", observed=True)["next_book"].agg(["size", "mean", "std", "min"])
    return out
