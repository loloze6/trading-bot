def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 36
    hs = [18, 36, 72]
    drift = {}
    for coin, ws in bars.items():
        for h in hs:
            rr = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rr)
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(c)
            ph = pd.Series(hi).shift(1).rolling(12).max().values
            rng = pd.Series(hi - lo).rolling(180, min_periods=45).mean().values
            r42 = pd.Series(c).pct_change(42).values
            r180 = pd.Series(c).pct_change(180).values
            vol42 = pd.Series(c).pct_change().rolling(42).std().values * np.sqrt(42)
            brk = (c - ph) / rng
            sig = (brk > 0) & (r42 > 0)
            sig = np.where(np.isnan(brk) | np.isnan(r42), False, sig)
            cell = np.arange(n) // H
            seen = set()
            for t in np.where(sig)[0]:
                if cell[t] in seen: continue
                seen.add(cell[t])
                rec = {"coin": coin, "brk": brk[t], "r42": r42[t], "r42v": r42[t] / vol42[t] if vol42[t] > 0 else np.nan,
                       "r180": r180[t], "year": pd.Timestamp(df["timestamp"].iloc[t]).year}
                for h in hs:
                    rec[f"u{h}"] = (c[t + h] / c[t] - 1 - drift[(coin, h)]) if t + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="u36"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    d["rq"] = pd.qcut(d["r42"], 4, labels=False)
    d["bq"] = pd.qcut(d["brk"], 4, labels=False)
    d["vq"] = pd.qcut(d["r42v"], 4, labels=False)
    out["r42_quartile_bounds"] = d.groupby("rq")["r42"].agg(["min", "median", "max"])
    out["r42_vol_scaled_quartile"] = d.groupby("vq").apply(lambda g: pd.concat([summ(g), summ(g, "u72").rename(lambda s: s + "72"), pd.Series({"med": g.r42v.median()})]))
    out["r42q_x_bq_mean"] = d.pivot_table(index="rq", columns="bq", values="u36", aggfunc="mean")
    out["r42q_x_bq_n"] = d.pivot_table(index="rq", columns="bq", values="u36", aggfunc="count")
    top = d[d.rq == 3]
    out["topR42_by_year"] = top.groupby("year").apply(summ)
    out["topR42_by_coin"] = top.groupby("coin").apply(summ)
    out["by_r180_sign"] = d.groupby(d.r180 > 0).apply(lambda g: pd.concat([summ(g), summ(g, "u72").rename(lambda s: s + "72")]))
    out["spearman_r42_u36"] = str(stats.spearmanr(d["r42"], d["u36"], nan_policy="omit"))
    out["spearman_r42v_u36"] = str(stats.spearmanr(d["r42v"], d["u36"], nan_policy="omit"))
    out["spearman_r42_u72"] = str(stats.spearmanr(d["r42"], d["u72"], nan_policy="omit"))
    out["topR42_horizons"] = pd.DataFrame({h: summ(top, f"u{h}") for h in hs}).T
    return out
