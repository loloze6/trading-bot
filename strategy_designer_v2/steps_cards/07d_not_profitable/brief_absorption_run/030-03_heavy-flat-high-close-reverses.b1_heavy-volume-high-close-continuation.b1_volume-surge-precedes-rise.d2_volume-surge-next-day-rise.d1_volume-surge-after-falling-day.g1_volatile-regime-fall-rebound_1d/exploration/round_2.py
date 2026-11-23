def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            r = b["close"].pct_change()
            sd20 = r.rolling(20).std()
            b["z"] = r / sd20
            b["vr"] = sd20 / sd20.rolling(120, min_periods=40).mean()
            b["fwd"] = b["close"].shift(-1) / b["close"] - 1
            b["alloc"] = b["postRebalance_current_allocation"]
            b["coin"] = c; b["win"] = w; b["pos"] = np.arange(len(b))
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b[["coin","win","pos","day","forecast","alloc","z","vr","fwd"]])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["fwd"].mean()
    B["ex"] = B["fwd"] - B["coin"].map(mu)
    B["sig"] = B["forecast"] > 0
    # per-coin vr tercile (expanding not available; use pooled per-coin quantiles as description)
    B["vrq"] = B.groupby("coin")["vr"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    B["zq"] = pd.qcut(B["z"].where(B["sig"]), 3, labels=False)
    def summ(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s)))})
    out["ex_sig_by_vr_tercile_x_z_tercile(0=deepest)"] = B[B["sig"]].groupby(["vrq","zq"])["ex"].apply(summ).unstack()
    out["ex_nosig_by_vr_tercile"] = B[~B["sig"]].groupby("vrq")["ex"].apply(summ).unstack()
    out["vr_threshold_cuts_mean"] = B.groupby("vrq")["vr"].agg(["min","max","mean"])
    # simulated books: alloc kept vs zeroed when vr below thresholds; cost 0.19% per round trip (0.095% per side of change)
    cost = 0.00095
    def book(mask_keep, scale=None):
        a = B["alloc"].where(mask_keep, 0.0)
        if scale is not None: a = a * scale
        g = B.assign(a=a)
        g["prev"] = g.groupby(["coin","win"])["a"].shift(1).fillna(0)
        g["ret"] = g["a"] * g["fwd"].fillna(0) - (g["a"] - g["prev"]).abs() * cost
        d = g.groupby(["win","day"])["ret"].mean().reset_index()
        d["wn"] = d["win"].str[1:].astype(int)
        d = d.sort_values(["wn","day"])
        v = (1 + d["ret"]).cumprod()
        mdd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365/len(d)) - 1
        sh = d["ret"].mean()/d["ret"].std()*np.sqrt(365)
        held = (a.abs() > 0).mean()
        return pd.Series({"sharpe": sh, "yearly": yr, "maxdd": mdd, "calmar": yr/abs(mdd), "held": held})
    res = {}
    res["as_is"] = book(B["alloc"].notna())
    for th in [0.9, 1.0, 1.1, 1.2]:
        res[f"out_when_vr<{th}"] = book(B["vr"] >= th)
    res["scale_vr"] = book(B["alloc"].notna(), scale=B["vr"].clip(0, 2).fillna(1))
    res["scale_vr_sq"] = book(B["alloc"].notna(), scale=(B["vr"]**2).clip(0, 2.5).fillna(1))
    out["sim_books"] = pd.DataFrame(res).T
    # gain on held bars by vr quartile (actual)
    H = B[B["alloc"].abs() > 0]
    out["held_gain_by_vr_bin"] = H.assign(q=pd.cut(H["vr"], [0,0.8,0.9,1.0,1.1,1.2,1.4,10])).groupby("q")["ex"].apply(summ).unstack()
    out["nosig_ex_vr_ge_1.1"] = summ(B.loc[(~B["sig"]) & (B["vr"] >= 1.1), "ex"])
    out["sig_ex_vr_ge_1.1"] = summ(B.loc[(B["sig"]) & (B["vr"] >= 1.1), "ex"])
    out["sig_ex_vr_lt_1.1"] = summ(B.loc[(B["sig"]) & (B["vr"] < 1.1), "ex"])
    return out
