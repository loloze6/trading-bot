import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            n = len(d)
            if n < 40: continue
            c, h, l = d["close"], d["high"], d["low"]
            L30 = l.shift(1).rolling(30, min_periods=30).min()
            H30 = h.shift(1).rolling(30, min_periods=30).max()
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            vol_med = vol30.expanding(min_periods=30).median()
            ret60 = c / c.shift(60) - 1
            ret30 = c / c.shift(30) - 1
            fwd5 = c.shift(-5) / c - 1
            fwd3 = c.shift(-3) / c - 1
            fwd10 = c.shift(-10) / c - 1
            ts = pd.to_datetime(d["timestamp"])
            dfo = pd.DataFrame({
                "coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(n),
                "day": ts.dt.floor("D"), "year": ts.dt.year,
                "fa": d["regime"].isin(["trending", "unknown"]).astype(int),
                "pierce_lo": np.where((l < L30) & (c >= L30), (L30 - l) / L30 * 100, 0.0),
                "pierce_hi": np.where((h > H30) & (c <= H30), (h - H30) / H30 * 100, 0.0),
                "break_hi": np.where(c > H30, (c - H30) / H30 * 100, 0.0),
                "ret60": ret60, "ret30": ret30, "agit": (vol30 > vol_med).astype(float).where(vol_med.notna()),
                "fwd3": fwd3, "fwd5": fwd5, "fwd10": fwd10, "valid30": L30.notna().astype(int)})
            rows.append(dfo)
    A = pd.concat(rows, ignore_index=True)
    A = A[A.valid30 == 1].copy()
    for hcol, hh in [("fwd5", 5), ("fwd3", 3), ("fwd10", 10)]:
        dr = A[A.pos % hh == 0].groupby("coin")[hcol].mean()
        A["u" + hcol[3:]] = A[hcol] - A["coin"].map(dr)

    def summ(sub, col="u5"):
        s = sub.dropna(subset=[col])
        if len(s) < 3: return pd.Series({"n": len(s), "days": 0, "mean%": np.nan, "t": np.nan})
        m = s[col].mean()
        dev = s.assign(dv=s[col] - m).groupby("day")["dv"].sum()
        G = len(dev)
        se = np.sqrt((dev**2).sum() * G / max(G - 1, 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean%": 100 * m, "t": m / se if se > 0 else np.nan})

    def trend(r):
        if pd.isna(r): return "na"
        return "rising" if r > 0.10 else ("falling" if r < -0.10 else "choppy")
    A["trend"] = A["ret60"].map(trend)
    A["trend30"] = A["ret30"].map(trend)
    out = {}
    eh = A[A.pierce_hi > 0].copy()
    el = A[A.pierce_lo > 0].copy()
    bh = A[A.break_hi > 0].copy()
    out["pierce_hi_by_trend60"] = eh.groupby("trend").apply(summ).reset_index()
    out["pierce_hi_by_agit"] = eh.groupby("agit").apply(summ).reset_index()
    out["pierce_hi_by_trend_agit"] = eh.groupby(["trend", "agit"]).apply(summ).reset_index()
    eh["dq"] = pd.qcut(eh.pierce_hi, 3, labels=False)
    out["pierce_hi_by_depth_tercile"] = eh.groupby("dq").apply(summ).reset_index()
    out["pierce_hi_by_window_half"] = eh.groupby(eh.wn > 12).apply(summ).reset_index()
    out["pierce_hi_by_year"] = eh.groupby("year").apply(summ).reset_index()
    out["pierce_hi_by_coin"] = eh.groupby("coin").apply(summ).reset_index()
    out["pierce_hi_h3_h10"] = pd.DataFrame({"h3": summ(eh, "u3"), "h10": summ(eh, "u10")}).T
    bh["dq"] = pd.qcut(bh.break_hi, 3, labels=False)
    out["break_hi_by_depth_tercile"] = bh.groupby("dq").apply(summ).reset_index()
    out["break_hi_by_trend60"] = bh.groupby("trend").apply(summ).reset_index()
    out["pierce_lo_by_trend60"] = el.groupby("trend").apply(summ).reset_index()
    out["pierce_lo_by_trend_agit"] = el.groupby(["trend", "agit"]).apply(summ).reset_index()
    el["dq"] = pd.qcut(el.pierce_lo, 3, labels=False)
    out["pierce_lo_by_depth_tercile"] = el.groupby("dq").apply(summ).reset_index()
    out["pierce_lo_by_window_half"] = el.groupby(el.wn > 12).apply(summ).reset_index()
    out["pierce_lo_h3_h10"] = pd.DataFrame({"h3": summ(el, "u3"), "h10": summ(el, "u10")}).T
    G5 = A[A.pos % 5 == 0]
    out["grid_by_trend_agit"] = G5.groupby(["trend", "agit"]).apply(summ).reset_index()
    return out
