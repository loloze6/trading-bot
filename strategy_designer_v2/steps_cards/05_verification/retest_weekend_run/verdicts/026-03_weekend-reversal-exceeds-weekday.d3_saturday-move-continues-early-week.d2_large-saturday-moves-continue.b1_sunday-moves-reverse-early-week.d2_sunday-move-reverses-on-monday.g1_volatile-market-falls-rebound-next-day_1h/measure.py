import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    RAW = "debug_info.components.fall_vol.last_history_value"

    def tstat(x):
        x = np.asarray(x, dtype=float)
        x = x[np.isfinite(x)]
        n = len(x)
        if n < 2:
            return float(x.mean()) if n else None, None, n
        sd = x.std(ddof=1)
        m = float(x.mean())
        if sd == 0 or not np.isfinite(sd):
            return m, None, n
        return m, float(m / (sd / np.sqrt(n))), n

    # ---------- 1. situation check: forecast active only while the 24h return is a fall, long ----------
    active_total = 0
    active_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).reset_index(drop=True)
            fc = df["forecast"].astype(float).reset_index(drop=True)
            if RAW in df.columns:
                raw = df[RAW].astype(float).reset_index(drop=True)
            else:
                raw = pd.Series(np.nan, index=close.index)
            past_ret = close / close.shift(H) - 1.0  # inside the window only
            # situation: the component's raw value is negative (24h fall); price return if raw missing
            fall = raw < 0
            fall = fall.where(raw.notna(), past_ret < 0)
            act = fc.notna() & (fc != 0)
            active_total += int(act.sum())
            active_agree += int((act & fall.fillna(False).astype(bool) & (fc > 0)).sum())

    agreement = float(active_agree / active_total) if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars where the 24h return "
                           "is a fall with a long (positive) forecast, as the Fidelity's situation and side require."),
            "reading": "The situation is read as the component's raw value (sign of the 24-bar return) being negative, from the 24-bar price return where the raw value is missing.",
        }

    # ---------- 2. grid samples ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            idx = np.arange(0, len(d), H)
            g = pd.DataFrame({
                "coin": coin,
                "fc": d["forecast"].astype(float).values[idx],
                "raw": (d[RAW].astype(float).values[idx] if RAW in d.columns else np.full(len(idx), np.nan)),
                "r": fwd.values[idx],
            })
            rows.append(g)
    grid = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["coin", "fc", "raw", "r"])
    grid = grid[np.isfinite(grid["r"].astype(float))]

    drift = grid.groupby("coin")["r"].mean()
    grid["adj"] = grid["r"] - grid["coin"].map(drift)

    g_main = grid[np.isfinite(grid["fc"].astype(float))]
    vals = (g_main["fc"] / 10.0) * g_main["adj"]
    m_mean, m_t, m_n = tstat(vals.values)
    n_pos = int((g_main["fc"] > 0).sum())

    # supporting check: top fifth of positive raw values per coin, on the grid bars
    sel = []
    for coin, g in grid.groupby("coin"):
        pos = g[(g["raw"] > 0) & np.isfinite(g["raw"])]
        if len(pos) == 0:
            continue
        cut = np.quantile(pos["raw"].values, 0.8)
        sel.append(pos[pos["raw"] >= cut])
    sup = pd.concat(sel) if sel else pd.DataFrame(columns=grid.columns)
    s_mean, s_t, s_n = tstat(sup["adj"].values if len(sup) else [])
    s_fail = s_mean is not None and s_t is not None and s_mean < 0 and s_t <= -2
    s_passed = None if s_mean is None else (not s_fail)

    counts = {"grid bars with forecast > 0": n_pos,
              "grid bars in the main measure": int(m_n),
              "grid bars in the supporting check": int(s_n)}

    if n_pos < 200:
        status = "not observable"
        decided = f"Only {n_pos} grid bars with forecast > 0 across coins and windows, below the plan's minimum of 200."
    elif (m_t is not None and m_t <= -2) or (s_t is not None and s_t <= -2):
        status = "rejected"
        decided = "Reject rule: the main measure's t is at most -2, or the post-rise mean has a t of at most -2."
    elif m_t is not None and m_t >= 2 and s_passed:
        status = "confirmed"
        decided = "Confirm rule: the main measure's t is at least 2 and the supporting check passes."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the main t is between -2 and 2 (or the supporting check did not pass), meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean of (forecast/10) x drift-adjusted 24-bar return on the 24-bar grid, before costs",
            "value": m_mean,
            "statistic": {"name": "t of the mean", "value": m_t} if m_t is not None else None,
            "threshold": "confirm if t >= 2 (with the supporting check passing); reject if t <= -2",
        },
        "supporting_check": {
            "name": "mean drift-adjusted 24-bar return after the top fifth of positive raw values (rises)",
            "value": s_mean,
            "passed": s_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The main mean is over all grid bars (forecast 0 bars contribute 0), the drift is the coin's mean "
                    "grid 24-bar return over all windows, and the top fifth is the 80th percentile of the coin's "
                    "positive raw values on the grid bars; the plan's below-200 'inconclusive' is reported as 'not observable' per the workflow."),
    }
