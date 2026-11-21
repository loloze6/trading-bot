def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 72
    hs = [6, 18, 36, 72, 144]
    # normal drift per coin per horizon from non-overlapping returns
    drift = {}; usual = {}
    for c, ws in bars.items():
        for h in hs:
            rs = []
            for w, b in ws.items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
            usual[(c, h)] = np.std(rs) if rs else np.nan
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            fc = b["forecast"].fillna(0).values
            n = len(cl)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            # prior 7-day return, 2-day range relative to 30-day avg of 2-day range
            ret42 = pd.Series(cl).pct_change(42).values
            rng12 = (pd.Series(hi).rolling(12).max() - pd.Series(lo).rolling(12).min()) / pd.Series(cl)
            rng_rel = (rng12.shift(1) / rng12.shift(1).rolling(180, min_periods=60).mean()).values
            trend360 = pd.Series(cl).pct_change(360).values
            lastmin = 0.0; prev_case_cell = -1
            for t in range(n):
                cell = t // H
                if fc[t] - lastmin >= 2 and cell != prev_case_cell:
                    prev_case_cell = cell
                    rec = dict(coin=c, win=w, year=yr[t], fc=fc[t], r42=ret42[t],
                               rngrel=rng_rel[t], tr=trend360[t])
                    for h in hs:
                        if t + h < n:
                            rec["u%d" % h] = cl[t + h] / cl[t] - 1 - drift[(c, h)]
                            rec["s%d" % h] = rec["u%d" % h] / usual[(c, h)]
                    rows.append(rec)
                    lastmin = fc[t]
                if fc[t] == 0:
                    lastmin = 0.0
                else:
                    lastmin = min(lastmin, fc[t])
    df = pd.DataFrame(rows)
    def summ(g, col="u72"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["overall_by_h"] = pd.DataFrame({h: summ(df, "u%d" % h) for h in hs}).T
    out["strength_by_h"] = pd.DataFrame({h: summ(df, "s%d" % h) for h in hs}).T
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    df["fq"] = pd.qcut(df["fc"].rank(method="first"), 5, labels=False)
    out["by_fc_quint"] = df.groupby("fq").apply(summ)
    df["rq"] = pd.qcut(df["r42"].rank(method="first"), 5, labels=False)
    out["by_r42_quint"] = df.groupby("rq").apply(summ)
    d2 = df.dropna(subset=["rngrel"]).copy()
    d2["qq"] = pd.qcut(d2["rngrel"].rank(method="first"), 5, labels=False)
    out["by_quiet_quint(0=narrow)"] = d2.groupby("qq").apply(summ)
    d3 = df.dropna(subset=["tr"]).copy()
    d3["tq"] = pd.qcut(d3["tr"].rank(method="first"), 5, labels=False)
    out["by_60d_trend_quint"] = d3.groupby("tq").apply(summ)
    out["fc_quint_by_h"] = pd.DataFrame({h: df.groupby("fq")["u%d" % h].mean() for h in hs})
    return out
