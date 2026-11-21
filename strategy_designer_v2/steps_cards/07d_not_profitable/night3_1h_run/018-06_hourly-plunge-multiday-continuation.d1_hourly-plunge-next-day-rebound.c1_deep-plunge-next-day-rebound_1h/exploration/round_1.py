def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- book daily returns, combined across coins
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["window", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
    B["wn"] = B["window"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna()
    eq = (1 + B["book"]).cumprod().values
    peak = np.maximum.accumulate(eq)
    dd_ = eq / peak - 1
    B["dd"] = dd_
    i_min = int(np.argmin(dd_)); i_peak = int(np.argmax(eq[: i_min + 1]))
    out["deepest_fall"] = pd.Series({"depth": dd_[i_min], "days": i_min - i_peak,
                                     "win_start": B["wn"].iloc[i_peak], "win_end": B["wn"].iloc[i_min],
                                     "book_sum_in_fall": B["book"].iloc[i_peak:i_min + 1].sum(),
                                     "hold_sum_in_fall": B["hold"].iloc[i_peak:i_min + 1].sum()})
    pw = B.groupby("wn").agg(book_mean=("book", "mean"), hold_mean=("hold", "mean"),
                             book_sd=("book", "std"), hold_sd=("hold", "std"), mindd=("dd", "min"), n=("book", "size"))
    out["per_window"] = pw.round(5)
    # ---- per-coin bars: position, market gain vs timing, and cases
    cases = []; posrows = []
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            r24 = cl[24::24] / cl[:-24:24] - 1 if len(cl) > 48 else np.array([])
            allr.append(r24)
        allr = np.concatenate(allr); drift = allr.mean(); usual = allr.std()
        for w, b in ws.items():
            cl = b["close"].astype(float).reset_index(drop=True)
            n = len(cl)
            r1 = cl.pct_change(); fwd1 = cl.shift(-1) / cl - 1
            pos = b["postRebalance_current_allocation"].astype(float).reset_index(drop=True)
            posrows.append(pd.DataFrame({"coin": c, "pos": pos, "fwd1": fwd1}))
            r24b = cl / cl.shift(24) - 1
            absmean = r24b.abs().rolling(720, min_periods=120).mean().shift(1)
            mult = -r24b / absmean
            r7d = cl / cl.shift(168) - 1
            r30d = cl / cl.shift(720) - 1
            vol_ratio = r24b.abs().rolling(168).mean() / absmean
            f24 = cl.shift(-24) / cl - 1
            f72 = cl.shift(-72) / cl - 1
            fc = b["forecast"].astype(float).reset_index(drop=True)
            idx = np.arange(0, n, 24)
            for s in idx:
                e = min(s + 24, n)
                seg = fc.iloc[s:e]
                hit = seg[seg >= 2]
                if len(hit) == 0: continue
                t = hit.index[0]
                cases.append(dict(coin=c, wn=int(w[1:]), mult=mult.iloc[t], r7d=r7d.iloc[t], r30d=r30d.iloc[t],
                                  vr=vol_ratio.iloc[t], ex24=f24.iloc[t] - drift, ex72=f72.iloc[t] - 3 * drift,
                                  st=(f24.iloc[t] - drift) / usual, fc=fc.iloc[t]))
    C = pd.DataFrame(cases).dropna(subset=["ex24"])
    def summ(g):
        x = g["ex24"]; y = g["ex72"].dropna()
        return pd.Series({"n": len(x), "ex24": x.mean(), "t24": x.mean() / x.std() * np.sqrt(len(x)),
                          "ex72": y.mean(), "t72": y.mean() / y.std() * np.sqrt(len(y))})
    C["multb"] = pd.cut(C["mult"], [0, 1, 1.5, 2, 3, 5, 100])
    out["by_multiple"] = C.groupby("multb", observed=True).apply(summ).round(4)
    C["r30b"] = pd.qcut(C["r30d"], 4, labels=["q1_low", "q2", "q3", "q4_high"])
    out["by_30d_return"] = C.groupby("r30b", observed=True).apply(summ).round(4)
    C["r7b"] = pd.qcut(C["r7d"], 4, labels=["q1_low", "q2", "q3", "q4_high"])
    out["by_7d_return"] = C.groupby("r7b", observed=True).apply(summ).round(4)
    C["vrb"] = pd.qcut(C["vr"], 4, labels=["q1_calm", "q2", "q3", "q4_turbulent"])
    out["by_week_vol_ratio"] = C.groupby("vrb", observed=True).apply(summ).round(4)
    C["deep"] = C["mult"] >= 1.5
    out["deep_by_30d"] = C[C["deep"]].groupby("r30b", observed=True).apply(summ).round(4)
    out["by_coin"] = C.groupby("coin").apply(summ).round(4)
    P = pd.concat(posrows).dropna()
    out["position"] = P.groupby("coin").apply(lambda g: pd.Series({
        "mean_pos": g["pos"].mean(), "share_in": (g["pos"].abs() > 0.01).mean(),
        "gain_per_bar": (g["pos"] * g["fwd1"]).mean(), "market_part": g["pos"].mean() * g["fwd1"].mean()})).round(6)
    return out
