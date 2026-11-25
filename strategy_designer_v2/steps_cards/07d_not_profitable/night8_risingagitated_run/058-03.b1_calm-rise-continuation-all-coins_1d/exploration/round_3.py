def explore(data):
    import numpy as np, pandas as pd
    out = {}
    wn = lambda w: int(w[1:])
    feats = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            f = pd.DataFrame({
                "coin": c, "window": w, "wn": wn(w),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos": b["postRebalance_current_allocation"].fillna(0),
                "fc": b["forecast"].fillna(0),
                "dist": cl / cl.rolling(20).mean() - 1,
                "ret60": cl / cl.shift(60) - 1,
                "vr": r1.rolling(10).std() / r1.rolling(60).std(),
                "nxt": cl.shift(-1) / cl - 1,
                "fwd5": cl.shift(-5) / cl - 1,
                "grid": (np.arange(len(b)) % 5 == 0),
                "inprof": b["regime"] == "unknown",
            })
            f["gain"] = (f["pos"] * f["nxt"]).fillna(0)
            feats.append(f)
    F = pd.concat(feats, ignore_index=True)
    def book(mask):
        g = F["gain"].where(mask, 0)
        d = F.assign(g=g).groupby(["wn", "day"])["g"].mean().sort_index()
        v = (1 + d).cumprod(); mdd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(d)) - 1
        return pd.Series({"yearly": yr, "maxdd": mdd, "calmar": yr / -mdd,
                          "sharpe": d.mean() / d.std() * np.sqrt(365)})
    allm = pd.Series(True, index=F.index)
    out["variants"] = pd.DataFrame({
        "base": book(allm),
        "no_dist_gt25": book(~(F.dist > 0.25)),
        "no_dist_gt20": book(~(F.dist > 0.20)),
        "no_ret60_gt60": book(~(F.ret60 > 0.6)),
        "no_vr_gt12": book(~(F.vr > 1.2)),
        "no_dist25_or_vr12": book(~((F.dist > 0.25) | (F.vr > 1.2))),
    }).T
    H = F[F.pos > 0]
    out["w11_w12_gain_by_dist"] = H[H.window.isin(["w11", "w12"])].groupby(
        pd.cut(H.dist, [-1, 0, 0.1, 0.25, 5]), observed=True)["gain"].agg(["size", "mean", "sum"])
    out["w11_w12_gain_by_vr"] = H[H.window.isin(["w11", "w12"])].groupby(
        pd.cut(H.vr, [0, 0.9, 1.2, 5]), observed=True)["gain"].agg(["size", "mean", "sum"])
    # condition-alone check for vr>1.2: forward 5 excess on grid bars without the signal
    drift5 = F[F.grid].groupby("coin")["fwd5"].mean()
    F["ex5"] = F["fwd5"] - F["coin"].map(drift5)
    G = F[F.grid & F.ex5.notna() & F.vr.notna()]
    def s(x): return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["vr_cond_check"] = pd.DataFrame({
        "nosig_vr_hi": s(G[(G.fc == 0) & (G.vr > 1.2)].ex5),
        "nosig_vr_lo": s(G[(G.fc == 0) & (G.vr <= 1.2)].ex5),
        "sig_vr_hi": s(G[(G.fc > 0) & (G.vr > 1.2)].ex5),
        "sig_vr_lo": s(G[(G.fc > 0) & (G.vr <= 1.2)].ex5),
        "nosig_dist_gt25": s(G[(G.fc == 0) & (G.dist > 0.25)].ex5),
        "sig_dist_gt25": s(G[(G.fc > 0) & (G.dist > 0.25)].ex5),
        "sig_dist_le25": s(G[(G.fc > 0) & (G.dist <= 0.25)].ex5),
    }).T
    return out
