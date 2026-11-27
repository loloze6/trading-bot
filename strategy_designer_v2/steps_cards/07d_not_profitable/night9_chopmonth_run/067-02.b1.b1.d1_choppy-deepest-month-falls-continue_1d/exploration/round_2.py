import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    out = {}
    cases = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            f = b["forecast"].fillna(0).values
            lr = np.r_[np.nan, np.diff(np.log(cl))]
            vol30 = pd.Series(lr).rolling(30, min_periods=20).std().values
            volrank = pd.Series(vol30).expanding(min_periods=30).apply(lambda s: (s <= s[-1]).mean(), raw=True).values
            r30b = np.r_[[np.nan] * 30, cl[30:] / cl[:-30] - 1]
            r7b = np.r_[[np.nan] * 7, cl[7:] / cl[:-7] - 1]
            reg = b["regime"].values
            for t in range(0, n, 7):
                rec = {"coin": c, "w": w, "f": f[t], "chop": reg[t] == "chop", "volrank": volrank[t],
                       "r30b": r30b[t], "r7b": r7b[t], "day": str(b["timestamp"].iloc[t])[:10]}
                for h in (7, 14, 21):
                    rec[f"fwd{h}"] = cl[t + h] / cl[t] - 1 if t + h < n else np.nan
                cases.append(rec)
    C = pd.DataFrame(cases)
    for h in (7, 14, 21):
        C[f"drift{h}"] = C.groupby("coin")[f"fwd{h}"].transform("mean")
        C[f"ex{h}"] = -(C[f"fwd{h}"] - C[f"drift{h}"])
        C[f"tot{h}"] = -C[f"fwd{h}"]
    def ct(df, col):
        x = df[[col, "day"]].dropna()
        if len(x) < 3: return np.nan, len(x), 0
        m = x[col].mean(); dev = (x[col] - m).groupby(x["day"]).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / len(x)
        return m / se if se > 0 else np.nan, len(x), G
    def summ(df):
        r = {}
        for h in (7, 21):
            for k in ("ex", "tot"):
                t, n, G = ct(df, f"{k}{h}")
                r[f"{k}{h}"] = df[f"{k}{h}"].mean(); r[f"{k}{h}_t"] = t
            r[f"n{h}"] = n; r[f"days{h}"] = G
        return pd.Series(r)
    ch = C[C.chop].copy()
    thr = ch.loc[ch.f < 0, "f"].abs().quantile(2 / 3)
    ch["sig"] = np.where(ch.f.abs() >= thr, "large", np.where(ch.f < 0, "smallmid", "none"))
    ch["agit"] = np.where(ch.volrank > 0.5, "agit", "calm")
    out["chop_sig_x_agit"] = ch.groupby(["agit", "sig"]).apply(summ)
    out["chop_sig_x_last7"] = ch.assign(l7=np.where(ch.r7b < 0, "l7down", "l7up")).groupby(["l7", "sig"]).apply(summ)
    # graded by raw month depth in chop
    neg = ch[ch.r30b < 0].copy()
    neg["depth_q"] = pd.qcut(neg.r30b, 5, labels=["q1deep", "q2", "q3", "q4", "q5shallow"])
    out["chop_depth_quintiles"] = neg.groupby("depth_q").apply(summ)
    out["depth_q_bounds"] = neg.groupby("depth_q")["r30b"].agg(["min", "max"])
    # forecast sextiles
    s = ch[ch.f < 0].copy()
    s["fq"] = pd.qcut(s.f.abs().rank(method="first"), 6, labels=list("123456"))
    out["forecast_sextiles"] = s.groupby("fq").apply(summ)
    # large-signal by window, h21 and h7
    L = ch[ch.sig == "large"]
    out["large_by_window"] = L.groupby("w")[["ex7", "ex21", "tot21"]].agg(["count", "mean"])
    # leave-one-window-out of large ex21 / tot21 mean
    loo = {}
    for w in L.w.unique():
        x = L[L.w != w]
        loo[w] = pd.Series({"ex7": x.ex7.mean(), "ex21": x.ex21.mean(), "tot21": x.tot21.mean()})
    out["large_loo"] = pd.DataFrame(loo).T
    # large & agitated by window
    LA = L[L.agit == "agit"]
    out["large_agit_by_window"] = LA.groupby("w")[["ex7", "ex21", "tot21"]].agg(["count", "mean"])
    return out
