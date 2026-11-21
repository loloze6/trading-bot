def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [6, 12, 18, 36]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # drift per horizon on non-overlapping grid
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            hi, lo, c = df["high"], df["low"], df["close"]
            ph = hi.shift(1).rolling(12).max()
            pl = lo.shift(1).rolling(12).min()
            rng = (ph - pl) / c
            base = ((hi - lo) / c).shift(1).rolling(180, min_periods=45).mean()
            narrow = base / rng  # higher = narrower stretch
            brk = ((c - ph).clip(lower=0) / c * 100)
            mom = c / c.shift(180) - 1
            fc = df["forecast"]
            year = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            cv = c.values
            for start in range(0, n - 18, 18):
                cell = range(start, min(start + 18, n))
                # case: first bar of cell with forecast rising >=2 above previous bar (approx) -> use forecast>0 & previous 0, or breakout
                pick = None
                for t in cell:
                    if fc.iloc[t] >= 2 and (t == 0 or fc.iloc[t - 1] < fc.iloc[t] - 2 + 1e-9):
                        pick = t; break
                if pick is None:
                    continue
                t = pick
                r = {"coin": coin, "w": w, "year": year.iloc[t], "fc": fc.iloc[t],
                     "narrow": narrow.iloc[t], "brk": brk.iloc[t], "mom": mom.iloc[t]}
                for h in H:
                    if t + h < n:
                        r[f"u{h}"] = cv[t + h] / cv[t] - 1 - drift[(coin, h)][0]
                        r[f"s{h}"] = r[f"u{h}"] / drift[(coin, h)][1]
                    else:
                        r[f"u{h}"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean()})
    out = {}
    out["horizons"] = pd.DataFrame({h: summ(d, f"u{h}") for h in H}).T
    out["fc_desc"] = d["fc"].describe().to_frame().T.assign(share_at_max=(d["fc"] >= d["fc"].max() - 1e-9).mean())
    d["nq"] = pd.qcut(d["narrow"].rank(method="first"), 5, labels=False)
    out["by_narrow_q"] = d.groupby("nq").apply(summ).join(d.groupby("nq")["narrow"].median())
    d["bq"] = pd.qcut(d["brk"].rank(method="first"), 5, labels=False)
    out["by_breakout_q"] = d.groupby("bq").apply(summ).join(d.groupby("bq")["brk"].median())
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 5, labels=False)
    out["by_fc_q"] = d.groupby("fq").apply(summ)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["momq"] = pd.qcut(d["mom"].rank(method="first"), 5, labels=False)
    out["by_mom30d_q"] = d.groupby("momq").apply(summ).join(d.groupby("momq")["mom"].median())
    out["by_mom_q_36"] = d.groupby("momq").apply(lambda g: summ(g, "u36"))
    return out
