def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days, bars, trades = data["days"], data["bars"], data["trades"]
    # book vs holding by coin
    rows = []
    for c in days:
        b = pd.concat([days[c][w]["book_return"] for w in days[c]]).dropna()
        h = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        tr = pd.concat([trades[c][w] for w in trades[c]]) if len(trades[c]) else pd.DataFrame()
        rows.append({"coin": c, "book_mean": b.mean(), "book_sh": b.mean()/b.std()*np.sqrt(365),
                     "hold_mean": h.mean(), "hold_sh": h.mean()/h.std()*np.sqrt(365),
                     "n_trades": len(tr),
                     "gross_pl_mean": tr["profit_loss_percent"].mean() if len(tr) else np.nan,
                     "net_pl_mean": tr["net_profit_loss_percent"].mean() if len(tr) else np.nan})
    out["by_coin"] = pd.DataFrame(rows)
    # book by window (pooled coins)
    wr = []
    for w in days[list(days)[0]]:
        b = pd.concat([days[c][w].set_index("day")["book_return"] for c in days if w in days[c]], axis=1).mean(axis=1).dropna()
        h = pd.concat([days[c][w].set_index("day")["coin_return"] for c in days if w in days[c]], axis=1).mean(axis=1).dropna()
        wr.append({"w": w, "book_mean": b.mean(), "book_sum": b.sum(), "hold_sum": h.sum(),
                   "exposure": np.nanmean([bars[c][w]["postRebalance_current_allocation"].abs().mean() for c in bars if w in bars[c]])})
    out["by_window"] = pd.DataFrame(wr)
    # grid cases: excess 5d return by market state
    recs = []
    for c in bars:
        allg = []
        for w in bars[c]:
            df = bars[c][w].reset_index(drop=True)
            cl = df["close"].values; v = df["volume"].values
            n = len(df)
            r30 = pd.Series(cl).pct_change(30).values
            r5p = pd.Series(cl).pct_change(5).values
            vol20 = pd.Series(cl).pct_change().rolling(20).std().values
            ma = pd.Series(cl).rolling(50).mean().values
            for i in range(0, n-5, 5):
                allg.append({"coin": c, "w": w, "fwd": cl[i+5]/cl[i]-1, "fc": df["forecast"].iloc[i],
                             "r1": cl[i]/cl[i-1]-1 if i > 0 else np.nan, "r30": r30[i], "r5p": r5p[i],
                             "vol20": vol20[i], "abovema": (cl[i] > ma[i]) if not np.isnan(ma[i]) else np.nan})
        g = pd.DataFrame(allg)
        g["ex"] = g["fwd"] - g["fwd"].mean()
        recs.append(g)
    G = pd.concat(recs)
    A = G[G["fc"] > 0].copy()
    def summ(s):
        return pd.Series({"n": len(s), "mean_ex": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    A["r30q"] = pd.qcut(A["r30"], 4, labels=False)
    out["active_by_r30_quartile"] = A.groupby("r30q")["ex"].apply(summ).unstack()
    out["active_by_abovema50"] = A.groupby("abovema")["ex"].apply(summ).unstack()
    A["volq"] = pd.qcut(A["vol20"], 4, labels=False)
    out["active_by_vol20_quartile"] = A.groupby("volq")["ex"].apply(summ).unstack()
    A["fcq"] = pd.qcut(A["fc"].rank(method="first"), 4, labels=False)
    out["active_by_fc_quartile"] = A.groupby("fcq")["ex"].apply(summ).unstack()
    A["r5q"] = pd.qcut(A["r5p"], 4, labels=False)
    out["active_by_prior5d_quartile"] = A.groupby("r5q")["ex"].apply(summ).unstack()
    # all grid bars (not only active), above/below ma, for contrast
    out["all_by_abovema50"] = G.groupby("abovema")["ex"].apply(summ).unstack()
    out["share_active"] = float((G["fc"] > 0).mean())
    return out
