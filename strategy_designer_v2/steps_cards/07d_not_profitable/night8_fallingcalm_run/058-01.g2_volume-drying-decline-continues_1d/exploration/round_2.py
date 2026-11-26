def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    feats = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]
            lr = np.log(cl).diff()
            for h in (5, 10):
                b[f"fwd{h}"] = cl.shift(-h) / cl - 1
            b["low30dist"] = cl / cl.rolling(30).min() - 1
            b["low10dist"] = cl / cl.rolling(10).min() - 1
            b["past60"] = cl / cl.shift(60) - 1
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["window"] = w
            b["alloc"] = b["postRebalance_current_allocation"]
            b["pnl_next"] = b["alloc"] * (cl.shift(-1) / cl - 1)
            b["held_lowdist_entry"] = np.nan
            feats.append(b)
    F = pd.concat(feats, ignore_index=True)
    F["wnum"] = F.window.str[1:].astype(int)
    for h in (5, 10):
        g = F[(F.pos % h == 0) & F[f"fwd{h}"].notna()]
        F[f"drift{h}"] = g[f"fwd{h}"].mean()
    out["drifts"] = pd.Series({"d5": F.drift5.iloc[0], "d10": F.drift10.iloc[0]})
    def summ(x, h=5):
        u = -(x[f"fwd{h}"] - x[f"drift{h}"])
        return pd.Series({"n": len(x), "unusual": u.mean(), "total": (-x[f"fwd{h}"]).mean(),
                          "t": stats.ttest_1samp(u, 0).statistic if len(x) > 2 else np.nan})
    G = F[(F.pos % 5 == 0) & F.fwd5.notna()]
    mr = G[G.regime == "mean_reversion"]
    S = mr[mr.forecast < 0]
    NS = mr[mr.forecast >= 0]
    # condition near 30d low: fixed cut values
    for cut in (0.02, 0.05, 0.10):
        out[f"cut_low30_{cut}"] = pd.DataFrame({
            "sig_near": summ(S[S.low30dist <= cut]), "sig_far": summ(S[S.low30dist > cut]),
            "nosig_near": summ(NS[NS.low30dist <= cut]),
            "chop_near_all": summ(G[(G.regime != "mean_reversion") & (G.low30dist <= cut)])})
    # within near-low, graded by forecast
    near = S[S.low30dist <= 0.05]
    out["near_by_forecast"] = near.groupby(pd.qcut(near.forecast, 2, labels=["strong", "weak"])).apply(summ)
    out["near_by_window"] = near.groupby("wnum").apply(summ)
    far = S[S.low30dist > 0.05]
    out["far_by_window"] = far.groupby("wnum").apply(summ)
    # 10-day horizon
    G10 = F[(F.pos % 10 == 0) & F.fwd10.notna()]
    S10 = G10[(G10.regime == "mean_reversion") & (G10.forecast < 0)]
    out["sig_h10_by_low30"] = S10.groupby(S10.low30dist <= 0.05).apply(lambda x: summ(x, 10))
    # rebuilt filtered book: pnl only on bars where held and low30dist<=cut at that bar
    for cut in (0.05, 0.10):
        F["pnl_f"] = np.where(F.low30dist <= cut, F.pnl_next, 0.0)
        port = F.dropna(subset=["pnl_next"]).groupby(["wnum", "timestamp"]).agg(a=("pnl_next", "mean"), f=("pnl_f", "mean")).reset_index().sort_values(["wnum", "timestamp"])
        res = {}
        for col in ("a", "f"):
            r = port[col]
            v = (1 + r).cumprod().values; dd = (v / np.maximum.accumulate(v) - 1).min()
            yr = v[-1] ** (365 / len(r)) - 1
            res[col] = pd.Series({"sharpe": r.mean() / r.std() * np.sqrt(365), "yearly": yr, "maxdd": dd, "calmar": yr / -dd})
        out[f"rebuilt_gross_book_cut{cut}"] = pd.DataFrame(res)
    # what held during w16-18
    P = F[(F.alloc.abs() > 0) & F.pnl_next.notna()]
    out["w16_18_inpos_by_low30"] = P[P.wnum >= 16].groupby(P.low30dist <= 0.05)["pnl_next"].agg(["count", "mean", "sum"])
    out["inpos_by_past60"] = P.groupby(pd.qcut(P.past60, 3))["pnl_next"].agg(["count", "mean", "sum"])
    return out
