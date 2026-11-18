def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    dd_rows = []
    for coin in data["bars"]:
        cr = pd.concat([data["days"][coin][w]["coin_return"] for w in data["days"][coin]]).dropna()
        mu = cr.mean()
        for w, b in data["bars"][coin].items():
            c = b["close"]
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = c.shift(-1) / c - 1
            fwd3 = c.shift(-3) / c - 1
            ret5 = c / c.shift(5) - 1
            ret30 = c / c.shift(30) - 1
            ret60 = c / c.shift(60) - 1
            vr = np.log(b["volume"].rolling(5).mean() / b["volume"].rolling(30).mean())
            i = np.arange(len(b))
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": pos, "r1": r1, "g": pos * r1, "fc": b["forecast"],
                                      "ret5": ret5, "ret30": ret30, "ret60": ret60, "vr": vr, "fwd3": fwd3,
                                      "ex3": fwd3 - 3 * mu, "grid": (i % 3 == 0), "mu": mu}))
            d = data["days"][coin][w].dropna(subset=["book_return"])
            if len(d) > 5:
                v = (1 + d.book_return).cumprod()
                ddv = v / v.cummax() - 1
                dd_rows.append({"coin": coin, "w": w, "maxdd": ddv.min(), "book_tot": v.iloc[-1] - 1,
                                "hold_tot": (1 + d.coin_return).prod() - 1})
    A = pd.concat(rows)
    DD = pd.DataFrame(dd_rows)
    out["worst_dd_windows"] = DD.sort_values("maxdd").head(12).drop(columns="w").reset_index(drop=True)
    out["dd_vs_hold_corr"] = pd.Series({"corr_maxdd_holdtot": DD.maxdd.corr(DD.hold_tot),
                                        "share_windows_book_neg": (DD.book_tot < 0).mean(),
                                        "mean_book_tot_when_hold_up20": DD.book_tot[DD.hold_tot > 0.2].mean(),
                                        "n_hold_up20": (DD.hold_tot > 0.2).sum()})
    G = A[A.grid & (A.ret5 < 0)].dropna(subset=["ex3", "vr", "ret30"])
    G["vrq"] = pd.qcut(G.vr, 5)
    G["t30"] = np.where(G.ret30 > 0, "up30", "down30")
    out["ex3_by_vr_trend30"] = G.groupby(["t30", "vrq"], observed=True).ex3.agg(["size", "mean"]).unstack(0)
    G["r5q"] = pd.qcut(G.ret5, 4)
    out["ex3_by_ret5q_vr_sign"] = G.groupby(["r5q", np.sign(G.vr)], observed=True).ex3.agg(["size", "mean"]).unstack(1)
    # losing days of the book: what is held and the trend
    B = A.dropna(subset=["r1", "ret30"])
    B["loss_bin"] = pd.qcut(B.g, 20, labels=False, duplicates="drop")
    worst = B[B.g <= B.g.quantile(0.03)]
    out["worst3pct_bars"] = pd.Series({"n": len(worst), "share_short": (worst.pos < 0).mean(),
                                       "mean_r1": worst.r1.mean(), "share_up30": (worst.ret30 > 0).mean(),
                                       "share_vr_neg": (worst.vr < 0).mean(), "mean_ret5": worst.ret5.mean(),
                                       "all_share_up30": (B.ret30 > 0).mean()})
    # short gain by trend 60
    S = B[B.pos != 0].copy()
    S["t60"] = pd.qcut(S.ret60, 4)
    out["gain_by_ret60q_side"] = S.groupby(["t60", np.sign(S.pos)], observed=True).agg(n=("g", "size"), gain=("g", "mean"), r1=("r1", "mean")).unstack(1)
    return out
