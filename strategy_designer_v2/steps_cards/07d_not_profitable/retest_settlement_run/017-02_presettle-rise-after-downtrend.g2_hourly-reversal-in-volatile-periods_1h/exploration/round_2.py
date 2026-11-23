def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book gross vs fees, daily
    gross_d, net_d, fee_d = [], [], []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            a = b["postRebalance_current_allocation"].astype(float)
            g = (a * (c.shift(-1) / c - 1)).fillna(0)
            v = b["postRebalance_total_value"].astype(float)
            tv = b["total_portfolio_value"].astype(float)
            fee = ((tv - v) / tv).fillna(0)
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            gross_d.append(g.groupby(day).sum().mean())
            fee_d.append(fee.groupby(day).sum().mean())
    out["book_daily_gross_pct"] = float(np.mean(gross_d) * 100)
    out["book_daily_fee_pct"] = float(np.mean(fee_d) * 100)
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd24 = r1.rolling(24).std()
            usual = sd24.rolling(720, min_periods=120).mean()
            ratio = sd24 / usual
            z = r1 / usual
            n = len(b)
            for H in [4, 12, 24, 48]:
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, n, H)
                d = pd.DataFrame({"z": z.iloc[idx].values, "fwd": fwd.iloc[idx].values,
                                  "ratio": ratio.iloc[idx].values})
                d["coin"] = coin; d["H"] = H; d["w"] = w
                d["year"] = pd.to_datetime(b["timestamp"]).dt.year.iloc[idx].values
                rows.append(d)
    D = pd.concat(rows).dropna()
    drift = D.groupby(["coin", "H"])["fwd"].transform("mean")
    D["fade"] = -np.sign(D["z"]) * (D["fwd"] - drift)
    D["fadetot"] = -np.sign(D["z"]) * D["fwd"]
    D["s"] = D["z"].abs() * D["ratio"]   # strength of situation: move x vol ratio
    D["sbin"] = pd.cut(D["s"], [0, 1, 2, 4, 6, 10, 1000])
    g = D.groupby(["H", "sbin"], observed=True)
    t = g["fade"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    t["mean_pct"] = t["mean"] * 100; t["tot_pct"] = g["fadetot"].mean() * 100
    out["fade_by_H_strength"] = t[["count", "mean_pct", "tot_pct", "t"]].reset_index().round(4)
    # condition-alone check: high vol ratio but small move
    D["vr_hi"] = D["ratio"] >= 1.6
    D["zbig"] = D["z"].abs() >= 2
    g2 = D[D.H.isin([12, 24])].groupby(["H", "vr_hi", "zbig"])["fade"].agg(["count", "mean", "std"])
    g2["t"] = g2["mean"] / (g2["std"] / np.sqrt(g2["count"])); g2["mean_pct"] = g2["mean"] * 100
    out["cond_alone_check"] = g2[["count", "mean_pct", "t"]].reset_index().round(4)
    S = D[(D.H == 24) & (D.s >= 4)].copy()
    S["side"] = np.where(S["z"] < 0, "long_after_down", "short_after_up")
    g3 = S.groupby("side").agg(count=("fade", "count"), mean_pct=("fade", "mean"), tot_pct=("fadetot", "mean"))
    g3["mean_pct"] *= 100; g3["tot_pct"] *= 100
    out["H24_s4_by_side"] = g3.round(4)
    g4 = S.groupby("year").agg(count=("fade", "count"), mean_pct=("fade", "mean"))
    g4["mean_pct"] *= 100
    out["H24_s4_by_year"] = g4.round(4)
    g5 = S.groupby("coin").agg(count=("fade", "count"), mean_pct=("fade", "mean")); g5["mean_pct"] *= 100
    out["H24_s4_by_coin"] = g5.round(4)
    return out
