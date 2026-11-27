def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    H = [1, 3, 5, 10, 20]
    # coin drift over all windows (non-overlapping) for each horizon
    for c in bars:
        for h in H:
            rr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                for i in range(0, len(cl) - h, h):
                    rr.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = (np.mean(rr), np.std(rr)) if rr else (np.nan, np.nan)
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            ret = cl.pct_change()
            sma = cl.rolling(20).mean()
            sd = ret.rolling(20).std()
            stretch = (cl - sma) / sma / sd
            inprof = b["regime"] != "chop"
            fc = b["forecast"]
            yr = pd.to_datetime(b["timestamp"]).dt.year
            n = len(b)
            for i in range(0, n - 5, 5):
                d = dict(coin=c, win=w, year=yr.iloc[i], inprof=bool(inprof.iloc[i]),
                         fc=fc.iloc[i], st=stretch.iloc[i], pos=i)
                for h in H:
                    if i + h < n:
                        r = cl.iloc[i + h] / cl.iloc[i] - 1
                        d[f"u{h}"] = r - drift[(c, h)][0]
                        d[f"z{h}"] = (r - drift[(c, h)][0]) / drift[(c, h)][1]
                rows.append(d)
    df = pd.DataFrame(rows)
    out = {}
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    P = df[df.inprof & df.st.notna()].copy()
    # unusual move in UP direction (positive = coin rises more than drift); short cases want negative
    P["stq"] = pd.qcut(P.st, 5, labels=False)
    out["inprof_by_stretch_quintile_u5"] = P.groupby("stq").apply(lambda g: pd.concat([summ(g), pd.Series({"st_mean": g.st.mean()})]))
    for h in H:
        out[f"inprof_below_vs_above_u{h}"] = P.groupby(P.st < 0).apply(lambda g: summ(g, f"u{h}"))
    S = P[P.st < 0]
    out["below_corr_st_vs_u_by_h"] = pd.DataFrame({f"h{h}": [stats.spearmanr(S.st, S[f"u{h}"], nan_policy="omit")[0], S[f"u{h}"].notna().sum()] for h in H}, index=["spearman", "n"])
    A = P[P.st > 0]
    out["above_corr_st_vs_u_by_h"] = pd.DataFrame({f"h{h}": [stats.spearmanr(A.st, A[f"u{h}"], nan_policy="omit")[0], A[f"u{h}"].notna().sum()] for h in H}, index=["spearman", "n"])
    out["below_by_coin_u5"] = S.groupby("coin").apply(summ)
    out["below_by_year_u5"] = S.groupby("year").apply(summ)
    out["below_by_window_u5"] = S.groupby("win").apply(summ)
    # out of profile, all chop
    O = df[(~df.inprof) & df.st.notna()].copy()
    O["stq"] = pd.qcut(O.st, 5, labels=False)
    out["outprof_by_stretch_quintile_u5"] = O.groupby("stq").apply(lambda g: pd.concat([summ(g), pd.Series({"st_mean": g.st.mean()})]))
    out["share_inprof"] = df.inprof.mean()
    return out
