def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        mu = pd.concat([b["close"].astype(float).pct_change().dropna() for b in wins.values()]).mean()
        mus = {}
        for h in [1, 2, 3, 5]:
            vals = []
            for b in wins.values():
                c = b["close"].astype(float).reset_index(drop=True)
                idx = np.arange(0, len(c) - h, h)
                vals.append((c.values[idx + h] / c.values[idx] - 1))
            mus[h] = np.concatenate(vals).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(c)), "r": r, "z": r / sd,
                               "z2": (c / c.shift(2) - 1) / (sd * np.sqrt(2)),
                               "z3": (c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                               "tr60": c / c.shift(60) - 1,
                               "sdrank": sd.rolling(60, min_periods=30).rank(pct=True),
                               "fa": (b["regime"] == "unknown"),
                               "rng": (b["high"] - b["low"]) / c / sd,
                               "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                               "vol_rel": b["volume"] / b["volume"].rolling(20, min_periods=10).mean().shift(1)})
            for h in [1, 2, 3, 5]:
                df[f"f{h}"] = c.shift(-h) / c - 1 - mus[h]
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["z"])
    out = {}
    def reg(s, x, y):
        s = s.dropna(subset=[x, y])
        if len(s) < 10: return {"slope": np.nan, "t": np.nan, "n": len(s)}
        l = stats.linregress(s[x], s[y]); return {"slope": l.slope, "t": l.slope / l.stderr, "n": len(s), "mean_y": s[y].mean(),
                                                    "t_mean": s[y].mean() / (s[y].std() / np.sqrt(len(s)))}
    # horizons on non-overlapping grid, FA falls
    res = {}
    for h in [1, 2, 3, 5]:
        s = d[(d.pos % h == 0) & d.fa & (d.z < 0)].copy(); s["mz"] = -s.z
        res[f"FA h{h}"] = reg(s, "mz", f"f{h}")
        s = d[(d.pos % h == 0) & (~d.fa) & (d.tr60.abs() <= 0.10) & (d.z < 0)].copy(); s["mz"] = -s.z
        res[f"chop h{h}"] = reg(s, "mz", f"f{h}")
    out["slope by horizon, nonoverlap"] = pd.DataFrame(res).T
    # chop split by in-window vol rank
    ch = d[(~d.fa) & (d.tr60.abs() <= 0.10) & (d.z < 0)].copy(); ch["mz"] = -ch.z
    ch["ag"] = ch.sdrank > 0.5
    out["chop falls by agitation proxy"] = pd.DataFrame({k: reg(s, "mz", "f1") for k, s in ch.groupby("ag")}).T
    # all profiles: agitated proxy vs calm, falls
    al = d[d.z < 0].copy(); al["mz"] = -al.z; al["ag"] = al.sdrank > 0.5
    al["tr"] = np.where(al.tr60 > 0.1, "rise", np.where(al.tr60 < -0.1, "fall", "chop"))
    out["falls slope by trend x agitation proxy"] = pd.DataFrame({f"{a}_{b}": reg(s, "mz", "f1") for (a, b), s in al.groupby(["tr", "ag"])}).T
    # FA: multi-day falls
    fa = d[d.fa].copy()
    res = {}
    for x in ["z", "z2", "z3"]:
        s = fa[fa[x] < 0].copy(); s["mx"] = -s[x]; res[x] = reg(s, "mx", "f1")
    out["FA: 1d vs 2d vs 3d scaled fall, next day"] = pd.DataFrame(res).T
    # FA falls: residual drivers - range, close position, volume
    s = fa[fa.z < 0].copy(); s["mz"] = -s.z
    X = s[["mz", "rng", "clpos", "vol_rel"]].dropna(); y = s.loc[X.index, "f1"]
    ok = y.notna(); X = X[ok]; y = y[ok]
    A = np.column_stack([np.ones(len(X)), X.values]); beta, *_ = np.linalg.lstsq(A, y.values, rcond=None)
    resid = y.values - A @ beta; s2 = resid @ resid / (len(y) - A.shape[1]); se = np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A)))
    out["FA falls multiple reg next day"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "mz", "rng", "clpos", "vol_rel"])
    # by year
    ts = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ts.append(pd.to_datetime(b["timestamp"]).dt.year.values)
    d["yr"] = np.concatenate(ts)[d.index if False else np.arange(len(d))] if False else np.nan
    # book largest days
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items(): bd.append(x.assign(coin=coin, w=w))
    bd = pd.concat(bd).dropna(subset=["book_return"])
    book = bd.groupby(["w", "day"]).book_return.mean().sort_values()
    out["book: share of total gain from top 10 days"] = pd.Series({"total": book.sum(), "top10": book.tail(10).sum(), "bottom10": book.head(10).sum(), "days_nonzero": (book != 0).sum()})
    return out
