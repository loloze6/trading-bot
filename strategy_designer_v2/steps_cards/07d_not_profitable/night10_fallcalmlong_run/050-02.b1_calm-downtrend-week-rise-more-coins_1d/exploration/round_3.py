def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    tr = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]; r = cl.pct_change()
            b["r7"] = cl / cl.shift(7) - 1
            b["sd30"] = r.rolling(30).std()
            b["z7"] = b["r7"] / (b["sd30"] * np.sqrt(7))
            b["dh"] = cl / cl.rolling(30).max() - 1
            b["inprof"] = b["regime"] == "unknown"
            b["sig"] = b["forecast"] > 0
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * (cl.shift(-1) / cl - 1)
            b["f3"] = cl.shift(-3) / cl - 1
            b["f7"] = cl.shift(-7) / cl - 1
            b["coin"] = c; b["w"] = w; b["i"] = np.arange(len(b))
            # entry-bar features carried through each holding stretch
            start = (b.pos != 0) & (b.pos.shift(1).fillna(0) == 0)
            b["sid"] = start.cumsum().where(b.pos != 0)
            b["edh"] = b["dh"].where(start).ffill().where(b.pos != 0)
            b["ez7"] = b["z7"].where(start).ffill().where(b.pos != 0)
            tr.append(b)
    A = pd.concat(tr, ignore_index=True)
    for h in [3, 7]:
        g = A[(A.i % h) == 0].dropna(subset=[f"f{h}", "dh"])
        drift = g.groupby("coin")[f"f{h}"].mean()
        g = g.assign(u=g[f"f{h}"] - g.coin.map(drift))
        gi = g[g.inprof].copy()
        gi["dhb"] = pd.cut(gi.dh, [-1, -0.15, -0.05, 0.001])
        out[f"h{h}_sig_by_dh"] = gi.groupby(["sig", "dhb"]).u.agg(["mean", "count"])
        S = gi[gi.sig]
        far = S[S.dh <= -0.05]; near = S[S.dh > -0.05]
        out[f"h{h}_far_vs_near"] = pd.Series({"far_u": far.u.mean(), "near_u": near.u.mean(),
            "t_welch": stats.ttest_ind(far.u, near.u, equal_var=False).statistic,
            "n_far": len(far), "n_near": len(near),
            "far_t1": stats.ttest_1samp(far.u, 0).statistic})
        far2 = far[far.z7 > 0.4]
        out[f"h{h}_far_and_z7gt04"] = pd.Series({"u": far2.u.mean(), "n": len(far2),
            "t": stats.ttest_1samp(far2.u, 0).statistic if len(far2) > 2 else np.nan})
    H = A[A.pos != 0].copy()
    H["edhb"] = pd.cut(H.edh, [-1, -0.15, -0.05, 0.001])
    out["held_gain_by_entry_dh"] = H.groupby("edhb").gain.agg(["sum", "mean", "count"])
    H["wb"] = H.w
    out["held_gain_by_window_entry_near"] = H.groupby(["wb", H.edh > -0.05]).gain.sum().unstack()
    # book chain with near-high entries removed (bar gains, coins averaged per day approx by timestamp)
    A["gain_f"] = np.where((A.pos != 0) & (A.edh > -0.05), 0.0, A.gain)
    A["wn"] = A.w.str[1:].astype(int)
    res = {}
    for col in ["gain", "gain_f"]:
        d = A.groupby(["wn", "timestamp"])[col].mean().fillna(0).sort_index()
        v = (1 + d).cumprod(); dd = (v / v.cummax() - 1).min()
        yrs = len(d) / 365
        yr = v.iloc[-1] ** (1 / yrs) - 1
        res[col] = {"yearly": yr, "maxdd": dd, "calmar": yr / -dd, "sharpe": d.mean() / d.std() * np.sqrt(365)}
    out["book_filter"] = pd.DataFrame(res)
    return out
