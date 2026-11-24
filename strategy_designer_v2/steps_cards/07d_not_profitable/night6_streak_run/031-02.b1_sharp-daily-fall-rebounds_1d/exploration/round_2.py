def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]
    feats = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            r = b["close"].pct_change()
            vol = r.rolling(60, min_periods=20).std()
            b["r"] = r
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["fall"] = (-r / vol).clip(lower=0)
            b["vol"] = vol
            b["volratio"] = r.rolling(10).std() / vol
            b["fwd2"] = b["close"].shift(-2) / b["close"] - 1
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["wn"] = int(w[1:])
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["alloc"] = b["postRebalance_current_allocation"]
            b["bgain"] = b["alloc"] * b["r1"]
            feats.append(b)
    F = pd.concat(feats, ignore_index=True)
    drift = F[F["pos"] % 2 == 0].groupby("coin")["fwd2"].mean()
    F["ex2"] = F["fwd2"] - F["coin"].map(drift)
    vq = F["volratio"].quantile(2/3)
    G = F[(F["pos"] % 2 == 0)].dropna(subset=["fwd2", "volratio", "fall"])
    sig = G["fall"] > 0
    # graded within volratio quintiles
    G["vrq"] = pd.qcut(G["volratio"], 5, labels=False)
    res = {}
    for qn in range(5):
        s = G[sig & (G["vrq"] == qn)]; ns = G[~sig & (G["vrq"] == qn)]
        big = s[s["fall"] > 1]["ex2"]
        res[qn] = pd.Series({"n_sig": len(s), "sig_ex2": s["ex2"].mean(),
                             "t_sig": s["ex2"].mean() / s["ex2"].std() * np.sqrt(len(s)),
                             "bigfall_ex2": big.mean(), "n_big": len(big),
                             "slope": np.polyfit(s["fall"], s["ex2"], 1)[0],
                             "nosig_ex2": ns["ex2"].mean()})
    out["volratio_quintile"] = pd.DataFrame(res).T
    # day-clustered t of highvol signal
    hv = G[sig & (G["volratio"] > vq)]
    dsum = hv.groupby("day")["ex2"].sum()
    out["highvol_sig_dayclustered_t"] = float(dsum.mean() / dsum.std() * np.sqrt(len(dsum)) )
    out["highvol_sig_days"] = len(dsum)
    out["highvol_sig_ex2_by_year"] = hv.groupby(pd.to_datetime(hv["day"]).dt.year)["ex2"].agg(["count", "mean"]).round(4)

    # simulated books: long after signal, held 2 days, vol-target size
    def book(cond, graded=False):
        parts = []
        for (c, wn), b in F.groupby(["coin", "wn"]):
            b = b.sort_values("pos")
            size = (0.382099 / (b["vol"] * np.sqrt(365))).clip(upper=2).fillna(0)
            if graded:
                size = size * (b["fall"].clip(upper=3) / 1.0)
                size = size.clip(upper=2)
            entry = np.where(cond.loc[b.index], size, 0.0)
            e = pd.Series(entry, index=b.index)
            p = np.maximum(e, e.shift(1).fillna(0))
            p = pd.Series(p, index=b.index)
            fee = (p - p.shift(1).fillna(0)).abs() * 0.00095
            ret = p * b["r1"].fillna(0) - fee
            parts.append(pd.DataFrame({"wn": wn, "day": b["day"], "ret": ret, "held": p > 0}))
        P = pd.concat(parts)
        D = P.groupby(["wn", "day"]).agg(ret=("ret", "mean")).reset_index().sort_values(["wn", "day"])
        v = (1 + D["ret"]).cumprod()
        mdd = (v / v.cummax() - 1).min()
        yrs = len(D) / 365
        yr = v.iloc[-1] ** (1 / yrs) - 1
        return pd.Series({"sharpe": D["ret"].mean() / D["ret"].std() * np.sqrt(365),
                          "yearly": yr, "maxdd": mdd, "calmar": yr / -mdd,
                          "held_share": P["held"].mean()})
    f = F["fall"].fillna(0); vr = F["volratio"].fillna(0)
    res = {}
    res["all_falls"] = book(f > 0)
    res["all_graded"] = book(f > 0, graded=True)
    res["fall>0.5"] = book(f > 0.5)
    res["highvol"] = book((f > 0) & (vr > vq))
    res["highvol_graded"] = book((f > 0) & (vr > vq), graded=True)
    res["highvol_fall>0.5"] = book((f > 0.5) & (vr > vq))
    res["notlowvol_graded"] = book((f > 0) & (vr > F["volratio"].quantile(1/3)), graded=True)
    out["sim_books"] = pd.DataFrame(res).T.round(3)
    # actual book: where losses in deepest drawdown came from
    F["fcpos"] = F["forecast"] > 0
    F["vrhi"] = F["volratio"] > vq
    out["actual_gain_by_vr_fc"] = F.groupby(["vrhi", "fcpos"])["bgain"].agg(["mean", "count"])
    return out
