def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []; leak = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            t1 = ts + pd.Timedelta(hours=1)
            cl = b["close"].values
            a = b["postRebalance_current_allocation"].fillna(0).values
            r = np.append(cl[1:] / cl[:-1] - 1, np.nan)
            g = a * r
            f = b["forecast"].fillna(0).values
            lr = np.log(cl[1:] / cl[:-1])
            mon = ((t1.dt.weekday == 0) & (t1.dt.hour == 0)).values
            inpos = np.zeros(len(b), bool)
            for i in np.where(mon)[0]:
                inpos[i:i + 48] = True
                if i + 48 >= len(b) or i < 720 or f[i] >= 0: continue
                vol = lr[i - 720:i].std()
                wk = cl[i] / cl[i - 48] - 1
                rows.append({"year": ts.iloc[i].year, "f": f[i], "short48": -(cl[i + 48] / cl[i] - 1),
                             "short24": -(cl[i + 24] / cl[i] - 1),
                             "wkz": wk / (vol * np.sqrt(48)), "ret30": cl[i] / cl[i - 720] - 1,
                             "ret7": cl[i - 48] / cl[i - 216] - 1, "vol": vol})
            ob = ~inpos
            leak.append({"out_short_bars": ((a < 0) & ob).sum(), "out_long_bars": ((a > 0) & ob).sum(),
                         "out_gain_short": np.nansum(g[ob & (a < 0)]), "out_gain_long": np.nansum(g[ob & (a > 0)]),
                         "out_wd_mode": pd.Series(t1.dt.weekday[ob & (a != 0)]).mode().iloc[0] if (ob & (a != 0)).any() else -1})
    S = pd.DataFrame(rows)
    L = pd.DataFrame(leak)
    out["leak"] = L[["out_short_bars", "out_long_bars", "out_gain_short", "out_gain_long"]].sum()
    out["leak_weekday_mode"] = L["out_wd_mode"].value_counts()
    def ag(g):
        n = len(g); m = g["short48"].mean()
        return pd.Series({"n": n, "short48": m, "t": m / (g["short48"].std() / np.sqrt(n)) if n > 1 else np.nan,
                          "short24": g["short24"].mean(), "absf": g["f"].abs().mean()})
    out["n_cases"] = len(S)
    out["by_wkz_quint"] = S.groupby(pd.qcut(S["wkz"], 5)).apply(ag)
    out["by_ret30_quint"] = S.groupby(pd.qcut(S["ret30"], 5)).apply(ag)
    out["by_ret7_quint"] = S.groupby(pd.qcut(S["ret7"], 5)).apply(ag)
    out["by_vol_quint"] = S.groupby(pd.qcut(S["vol"], 5)).apply(ag)
    out["corr"] = pd.Series({"wkz_short48": S[["wkz", "short48"]].corr().iloc[0, 1],
                             "ret30_short48": S[["ret30", "short48"]].corr().iloc[0, 1],
                             "absf_short48": S[["f", "short48"]].corr().iloc[0, 1] * -1})
    return out
