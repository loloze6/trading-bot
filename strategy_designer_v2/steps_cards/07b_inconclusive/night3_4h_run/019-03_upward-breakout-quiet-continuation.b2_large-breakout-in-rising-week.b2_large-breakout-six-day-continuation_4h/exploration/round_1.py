def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 36
    rows = []
    drift = {}
    usual = {}
    # drift per coin and horizon
    for coin, ws in bars.items():
        for h in [6, 12, 18, 36, 72]:
            rr = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rr)
            usual[(coin, h)] = np.std(rr)
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(c)
            ph = pd.Series(hi).shift(1).rolling(12).max().values
            rng = pd.Series(hi - lo).rolling(180, min_periods=45).mean().values
            r42 = pd.Series(c).pct_change(42).values
            # quietness: last 12-bar mean range over 180-bar mean range (before the bar)
            q = (pd.Series(hi - lo).shift(1).rolling(12).mean() / pd.Series(hi - lo).shift(1).rolling(180, min_periods=45).mean()).values
            brk = (c - ph) / rng
            fc = df["forecast"].values
            sig = (brk > 0) & (r42 > 0)
            sig = np.where(np.isnan(brk) | np.isnan(r42), False, sig)
            cell = np.arange(n) // H
            seen = set()
            for t in np.where(sig)[0]:
                if cell[t] in seen: continue
                seen.add(cell[t])
                rec = {"coin": coin, "win": int(w[1:]), "brk": brk[t], "r42": r42[t], "q": q[t], "fc": fc[t],
                       "hour": pd.Timestamp(df["timestamp"].iloc[t]).hour,
                       "year": pd.Timestamp(df["timestamp"].iloc[t]).year}
                for h in [6, 12, 18, 36, 72]:
                    rec[f"u{h}"] = (c[t + h] / c[t] - 1 - drift[(coin, h)]) if t + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="u36"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["overall_by_horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in [6, 12, 18, 36, 72]}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["bq"] = pd.qcut(d["brk"], 4, labels=False, duplicates="drop")
    out["by_break_quartile"] = d.groupby("bq").apply(lambda g: pd.concat([summ(g), pd.Series({"brk_med": g.brk.median()})]))
    d["qq"] = pd.qcut(d["q"], 4, labels=False, duplicates="drop")
    out["by_quietness_quartile(0=narrowest)"] = d.groupby("qq").apply(lambda g: pd.concat([summ(g), pd.Series({"q_med": g.q.median()}), summ(g,"u72").rename(lambda s: s+"72")]))
    d["rq"] = pd.qcut(d["r42"], 4, labels=False, duplicates="drop")
    out["by_r42_quartile"] = d.groupby("rq").apply(summ)
    out["forecast_desc"] = d["fc"].describe()
    out["fc_share_at_cap"] = float((d["fc"] >= 19.99).mean())
    out["fc_share_zero"] = float((d["fc"] == 0).mean())
    out["spearman_brk_u36"] = str(stats.spearmanr(d["brk"], d["u36"], nan_policy="omit"))
    out["spearman_q_u36"] = str(stats.spearmanr(d["q"], d["u36"], nan_policy="omit"))
    return out
