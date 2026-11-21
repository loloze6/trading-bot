def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; coins = list(bars.keys())
    out = {}
    def cells(h):
        rows = []
        for c in coins:
            for w, b in bars[c].items():
                cl = b["close"].values; fc = b["forecast"].values
                r30 = b["close"].pct_change(720).values
                r7 = b["close"].pct_change(168).values
                lr = np.log(b["close"]).diff()
                vol = (lr.rolling(720).std() * np.sqrt(24)).values
                yr = pd.to_datetime(b["timestamp"]).dt.year.values
                for i in range(0, len(cl) - h, h):
                    rows.append((c, w, yr[i], cl[i + h] / cl[i] - 1, fc[i], r30[i], r7[i], vol[i]))
        C = pd.DataFrame(rows, columns=["coin", "w", "year", "r", "fc", "r30", "r7", "vol"])
        C["ex"] = C["r"] - C.groupby("coin")["r"].transform("mean")
        C["usual"] = C.groupby("coin")["r"].transform("std")
        C["str"] = C["ex"] / C["usual"]
        return C
    for h in [72, 168]:
        C = cells(h)
        P = C[C.fc > 0]
        pc = P.groupby("coin")["ex"].agg(["mean", "count", "std"])
        pc["t"] = pc["mean"] / (pc["std"] / np.sqrt(pc["count"]))
        pc["strength"] = P.groupby("coin")["str"].mean()
        out[f"coin_h{h}"] = pc.drop(columns="std")
        py = P.groupby("year")["ex"].agg(["mean", "count"])
        out[f"year_h{h}"] = py
        D = C.dropna(subset=["r30"]).copy()
        D["z"] = D.groupby("coin")["r30"].transform(lambda s: s / s.std())
        D["q"] = D.groupby("coin")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False))
        g = D.groupby("q")[["ex", "str"]].mean(); g["n"] = D.groupby("q").size()
        out[f"r30_quint_h{h}"] = g
        sl = stats.linregress(D.z, D.str)
        out[f"slope_all_h{h}"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(D)})
        # 7-day return grading
        E = C.dropna(subset=["r7"]).copy()
        E["q"] = E.groupby("coin")["r7"].transform(lambda s: pd.qcut(s, 5, labels=False))
        out[f"r7_quint_h{h}"] = E.groupby("q")[["ex", "str"]].mean()
        # by vol regime among positive
        P2 = D[D.fc > 0].copy()
        P2["vq"] = P2.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
        out[f"vol_terc_pos_h{h}"] = P2.groupby("vq")["ex"].agg(["mean", "count"])
    # trades: concentration by coin and by top trades excluded
    tr = []
    for c in coins:
        for w, t in data["trades"][c].items():
            if len(t): x = t.copy(); x["coin"] = c; x["w"] = w; tr.append(x)
    T = pd.concat(tr)
    T["days"] = T.duration_minutes / 1440
    T["dq"] = pd.cut(T.days, [0, 1, 7, 14, 30, 90, 2000])
    g = T.groupby("dq", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    out["trades_by_duration"] = g.reset_index().astype({"dq": str})
    return out
