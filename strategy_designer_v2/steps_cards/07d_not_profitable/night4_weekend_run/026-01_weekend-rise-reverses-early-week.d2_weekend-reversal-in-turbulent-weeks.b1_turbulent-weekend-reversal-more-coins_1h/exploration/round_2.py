def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []; leak = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            a = b["postRebalance_current_allocation"].fillna(0).values
            r = np.append(cl[1:] / cl[:-1] - 1, np.nan)
            g = a * r
            f = b["forecast"].fillna(0).values
            mon = ((ts + pd.Timedelta(hours=1)).dt.weekday == 0) & ((ts + pd.Timedelta(hours=1)).dt.hour == 0)
            inpos = np.zeros(len(b), bool)
            for i in np.where(mon.values)[0]:
                if i + 48 >= len(b): continue
                wk = b["debug_info.components.weekend_move.last_history_value"].iloc[i] if "debug_info.components.weekend_move.last_history_value" in b else np.nan
                ret48 = cl[i + 48] / cl[i] - 1
                ret24 = cl[i + 24] / cl[i] - 1
                ret_wk = cl[i] / cl[i - 48] - 1 if i >= 48 else np.nan
                gs = np.nansum(g[i:i + 48])
                rows.append({"coin": c, "window": w, "year": ts.iloc[i].year, "f": f[i], "regime": b["regime"].iloc[i],
                             "a0": a[i], "a_mean": a[i:i + 48].mean(), "ret48": ret48, "ret24": ret24, "ret_d2": cl[i+48]/cl[i+24]-1,
                             "wk": ret_wk, "book48": gs})
                inpos[i:i + 48] = True
            leak.append({"coin": c, "window": w, "out_bars_nonzero": (a[~inpos] != 0).sum(), "out_gain": np.nansum(g[~inpos]),
                         "in_gain": np.nansum(g[inpos]), "n": len(b)})
    R = pd.DataFrame(rows)
    L = pd.DataFrame(leak)
    out["leak_totals"] = L[["out_bars_nonzero", "out_gain", "in_gain", "n"]].sum()
    S = R[R["f"] < 0].copy()
    S["short48"] = -S["ret48"]
    S["short24"] = -S["ret24"]; S["short_d2"] = -S["ret_d2"]
    def ag(g):
        n = len(g)
        return pd.Series({"n": n, "short48": g["short48"].mean(), "t48": g["short48"].mean()/(g["short48"].std()/np.sqrt(n)) if n>1 else np.nan,
                          "short24": g["short24"].mean(), "short_d2": g["short_d2"].mean(),
                          "a0": g["a0"].mean(), "book48": g["book48"].mean(), "wk": g["wk"].mean()})
    out["short_cases_all"] = ag(S).to_frame().T
    out["short_by_fbin"] = S.groupby(pd.cut(S["f"].abs(), [0, 2, 4, 8, 21])).apply(ag)
    out["short_by_year"] = S.groupby("year").apply(ag)
    out["short_by_window"] = S.groupby("window").apply(ag)
    # all Monday bars (any regime) by weekend move tercile within coin
    R["wk_q"] = R.groupby("coin")["wk"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    R["fwd48"] = R["ret48"]
    out["all_mondays_by_wk_quintile"] = R.groupby("wk_q").agg(n=("fwd48", "size"), wk=("wk", "mean"), fwd48=("fwd48", "mean"), fwd24=("ret24","mean"))
    out["regime_counts"] = R["regime"].value_counts()
    out["alloc_sign_check"] = pd.Series({"a0_neg_share_when_f_neg": (S["a0"] < 0).mean(), "a0_zero_share": (S["a0"] == 0).mean(),
                                         "corr_book48_short48": S[["book48", "short48"]].corr().iloc[0, 1]})
    return out
