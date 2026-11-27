def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 5, 10]
    drift = {}
    for c in bars:
        for h in H:
            rr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                for i in range(0, len(cl) - h, h):
                    rr.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = (np.mean(rr), np.std(rr))
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            ret = cl.pct_change()
            sma = cl.rolling(20).mean()
            sd = ret.rolling(20).std()
            st = (cl - sma) / sma / sd
            tr = (cl / cl.shift(60) - 1) * 100
            agit = b["regime"] != "chop"
            yr = pd.to_datetime(b["timestamp"]).dt.year
            n = len(b)
            for i in range(0, n - 5, 5):
                d = dict(coin=c, win=w, year=yr.iloc[i], st=st.iloc[i], tr=tr.iloc[i], agit=bool(agit.iloc[i]))
                for h in H:
                    if i + h < n:
                        r = cl.iloc[i + h] / cl.iloc[i] - 1
                        d[f"u{h}"] = r - drift[(c, h)][0]
                        d[f"z{h}"] = d[f"u{h}"] / drift[(c, h)][1]
                rows.append(d)
    df = pd.DataFrame(rows)
    df = df[df.st.notna() & df.tr.notna()]
    out = {}
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "st": g.st.mean()})
    df["prof"] = np.where(df.tr > 10, "rising", np.where(df.tr < -10, "falling", "choppy"))
    out["n_by_prof"] = df.groupby(["prof"]).size()
    for p in ["choppy", "rising", "falling"]:
        P = df[df.prof == p].copy()
        P["q"] = pd.qcut(P.st, 5, labels=False)
        for h in [5, 10]:
            out[f"{p}_quintile_u{h}"] = P.groupby("q").apply(lambda g: summ(g, f"u{h}"))
    C = df[df.prof == "choppy"].copy()
    C["q"] = pd.qcut(C.st, 5, labels=False)
    out["choppy_calm_quintile_u5"] = C[~C.agit].groupby("q").apply(summ)
    out["choppy_agit_quintile_u5"] = C[C.agit].groupby("q").apply(summ)
    for side, S in [("below", C[C.st < 0]), ("above", C[C.st > 0])]:
        out[f"choppy_{side}_spearman"] = pd.DataFrame({f"h{h}": [stats.spearmanr(S.st, S[f"u{h}"], nan_policy="omit")[0], stats.spearmanr(S.st, S[f"u{h}"], nan_policy="omit")[1], S[f"u{h}"].notna().sum()] for h in H}, index=["rho", "p", "n"])
    C["top_minus_bot"] = 0
    g = C.groupby("year").apply(lambda g: pd.Series({"q4": g[g.q == 4].u5.mean(), "q0": g[g.q == 0].u5.mean(), "n": len(g)}))
    out["choppy_q4_q0_by_year"] = g
    out["choppy_slope_z5_on_st"] = pd.Series(dict(zip(["slope", "intercept", "r", "p", "se"], stats.linregress(C.dropna(subset=["z5"]).st, C.dropna(subset=["z5"]).z5))))
    return out
