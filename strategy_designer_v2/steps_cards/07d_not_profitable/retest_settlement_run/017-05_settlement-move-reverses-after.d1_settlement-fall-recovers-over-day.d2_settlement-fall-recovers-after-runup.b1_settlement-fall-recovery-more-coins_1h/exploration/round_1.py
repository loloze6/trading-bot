def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # ---- book daily series
    wins = sorted({w for c in days for w in days[c]}, key=lambda s: int(s[1:]))
    rows = []
    for w in wins:
        frames = []
        for c in days:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                b = bars[c][w]
                ts = pd.to_datetime(b["timestamp"])
                al = b["postRebalance_current_allocation"].abs().groupby(ts.dt.floor("D")).mean()
                d["alloc"] = pd.to_datetime(d["day"]).dt.floor("D").map(al).values
                frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), alloc=("alloc", "mean")).reset_index()
        g["win"] = w
        rows.append(g.sort_values("day"))
    B = pd.concat(rows).dropna(subset=["book"]).reset_index(drop=True)
    v = (1 + B["book"]).cumprod(); dd = v / v.cummax() - 1
    B["dd"] = dd
    # episodes
    eps = []
    peak = 0
    i = 0
    vals = v.values
    runmax = np.maximum.accumulate(vals)
    in_dd = False
    for k in range(len(vals)):
        if vals[k] < runmax[k] and not in_dd:
            in_dd = True; start = k - 1 if k > 0 else 0
        if in_dd and vals[k] >= runmax[k]:
            seg = B.iloc[start:k]
            t = seg["dd"].idxmin()
            eps.append((start, t, B["dd"].min() if False else seg["dd"].min()))
            in_dd = False
    if in_dd:
        seg = B.iloc[start:]
        eps.append((start, seg["dd"].idxmin(), seg["dd"].min()))
    eps = sorted(eps, key=lambda e: e[2])[:6]
    er = []
    for s, t, m in eps:
        seg = B.iloc[s:t + 1]
        er.append({"win": B.loc[s, "win"] + "-" + B.loc[t, "win"], "year": str(pd.to_datetime(B.loc[t, "day"]).year),
                   "depth": m, "days_to_trough": t - s, "book_sum": seg["book"].sum(), "coin_mean_sum": seg["coin"].sum(),
                   "mean_alloc": seg["alloc"].mean(), "alloc_all": B["alloc"].mean()})
    out["deepest_falls"] = pd.DataFrame(er)
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["book_by_year"] = B.groupby("year").agg(book_mean=("book", "mean"), coin_mean=("coin", "mean"), mindd=("dd", "min"), n=("book", "size"))
    # ---- cases
    cr = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values; n = len(cl)
            ts = pd.to_datetime(b["timestamp"])
            hr = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            s = pd.Series(cl)
            r24 = s.shift(-24) / s - 1
            r168 = s / s.shift(168) - 1
            r720 = s / s.shift(720) - 1
            r2 = s / s.shift(2) - 1
            lr = np.log(s).diff()
            vol24 = lr.rolling(24).std(); vol720 = lr.rolling(720).std()
            r24p = s / s.shift(24) - 1
            pos = np.arange(n)
            f = b["forecast"].fillna(0).values
            settle = np.isin(hr, [0, 16])
            df = pd.DataFrame({"coin": c, "win": w, "f": f, "settle": settle, "cell": pos // 24, "r24": r24, "r168": r168,
                               "r720": r720, "r2": r2, "vr": vol24 / vol720, "r24p": r24p, "year": ts.dt.year,
                               "hr": hr})
            df = df[df["settle"]].dropna(subset=["r24", "r168"])
            cr.append(df)
    C = pd.concat(cr)
    drift = {}
    for c in bars:
        vals_ = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 24, 24)
            vals_.append(cl[idx + 24] / cl[idx] - 1)
        drift[c] = np.concatenate(vals_).mean()
    C["x"] = C["r24"] - C["coin"].map(drift)
    sig = C[C["f"] > 0].groupby(["coin", "win", "cell"]).head(1).copy()
    def summ(g):
        return pd.Series({"n": len(g), "mean_r24": g["r24"].mean(), "mean_x": g["x"].mean(),
                          "t_x": g["x"].mean() / (g["x"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "win_share": (g["r24"] > 0.0022).mean()})
    out["sig_all"] = summ(sig).to_frame().T
    for col, q in [("r168", 5), ("r720", 5), ("vr", 5), ("r24p", 5), ("f", 5)]:
        sig["q"] = pd.qcut(sig[col].rank(method="first"), q, labels=False)
        t = sig.groupby("q").apply(summ)
        t["lo"] = sig.groupby("q")[col].min(); t["hi"] = sig.groupby("q")[col].max()
        out["sig_by_" + col] = t
    out["sig_by_year"] = sig.groupby("year").apply(summ)
    out["sig_by_hour"] = sig.groupby("hr").apply(summ)
    # condition alone: settlement bars with run-up but no fall (no signal) by r720 sign
    nos = C[(C["f"] <= 0) & (C["r168"] > 0)].groupby(["coin", "win", "cell"]).head(1).copy()
    nos["r720pos"] = nos["r720"] > 0; sig["r720pos"] = sig["r720"] > 0
    out["cond_runup_nofall_by_r720pos"] = nos.groupby("r720pos").apply(summ)
    out["sig_by_r720pos"] = sig.groupby("r720pos").apply(summ)
    sig["vrhi"] = sig["vr"] > 1.3; nos["vrhi"] = nos["vr"] > 1.3
    out["sig_by_vrhi"] = sig.groupby("vrhi").apply(summ)
    out["cond_nofall_by_vrhi"] = nos.groupby("vrhi").apply(summ)
    return out
