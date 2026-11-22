import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    P = 30
    RAW = "debug_info.components.flat_range_rev.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: close off the middle with some flatness (raw != 0); expected side: opposite sign of raw
            ok = active & raw.notna() & (raw != 0) & (np.sign(fc) == -np.sign(raw))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x (5-day return minus coin's normal drift) on the 5-bar grid"
    main_thr = "confirm: mean > 0 with t >= 2 (and supporting difference > 0); reject: mean < 0 with t <= -2"
    sup_name = "flatter-half minus less-flat-half mean reversion return per unit distance"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars have a forecast whose sign is opposite to the raw "
                          "flatness-weighted range position (short above the middle, long below), as the Fidelity requires.",
            "reading": "Situation taken as raw component value nonzero, expected side as the sign opposite to the raw value.",
        }

    # ---------- 2. grid samples ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").values.astype(float)
            n = len(d)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                pos_term = np.nan
                flat = np.nan
                if t >= P:
                    win = close[t - P + 1: t + 1]
                    if np.all(np.isfinite(win)) and np.isfinite(close[t - P]):
                        hi, lo = win.max(), win.min()
                        if hi > lo:
                            pos = (c0 - lo) / (hi - lo)
                            pos_term = 2.0 * pos - 1.0
                            flat = 1.0 - abs(c0 - close[t - P]) / (hi - lo)
                rows.append((coin, fc[t], r, pos_term, flat))
    g = pd.DataFrame(rows, columns=["coin", "fc", "r", "pt", "flat"])

    # normal drift per coin: mean 5-day grid return over all its windows
    drift = g.groupby("coin")["r"].mean()
    m = g[g["fc"].notna()].copy()
    m["prod"] = m["fc"] / 10.0 * (m["r"] - m["coin"].map(drift))
    n_main = int(len(m))
    n_nonzero = int((m["fc"] != 0).sum())
    if n_main > 1:
        main_mean = float(m["prod"].mean())
        sd = float(m["prod"].std(ddof=1))
        main_t = float(main_mean / (sd / np.sqrt(n_main))) if sd > 0 else 0.0
    else:
        main_mean, main_t = None, None

    # supporting check
    s = g[g["pt"].notna() & g["flat"].notna() & (g["pt"] != 0)].copy()
    s["rev"] = s["r"] * (-np.sign(s["pt"])) / s["pt"].abs()
    diff, welch_t, n_flat, n_less = None, None, 0, 0
    if len(s) > 0:
        med = s["flat"].median()
        a = s.loc[s["flat"] > med, "rev"]
        b = s.loc[s["flat"] <= med, "rev"]
        n_flat, n_less = int(len(a)), int(len(b))
        if n_flat > 0 and n_less > 0:
            diff = float(a.mean() - b.mean())
            if n_flat > 1 and n_less > 1:
                tt = stats.ttest_ind(a.values, b.values, equal_var=False)
                welch_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {
        "grid cases with a nonzero forecast": n_nonzero,
        "grid cases in main measure": n_main,
        "supporting flatter half": n_flat,
        "supporting less-flat half": n_less,
    }

    # ---------- 3. decision ----------
    if n_nonzero < 300 or main_mean is None:
        status = "not observable"
        decided = f"Only {n_nonzero} grid cases with a nonzero forecast, below the plan's minimum of 300."
    elif main_mean > 0 and main_t >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = "Main mean is positive with t >= 2 and the supporting flatter-minus-less-flat difference is positive."
    elif (main_mean < 0 and main_t <= -2) or (diff is not None and diff < 0 and welch_t is not None and welch_t <= -2):
        status = "rejected"
        if main_mean < 0 and main_t <= -2:
            decided = "Main mean is negative with t <= -2."
        else:
            decided = "Supporting difference is negative with Welch t <= -2."
    else:
        status = "inconclusive"
        decided = "The numbers meet neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": main_mean,
            "statistic": None if main_t is None else {"name": "t of the mean", "value": main_t},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name,
            "value": diff,
            "passed": sup_passed,
            "welch_t": welch_t,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Main mean is over all grid bars (zero forecasts contribute zero) with drift as the coin's mean grid "
                   "5-day return over all windows; the supporting check recomputes pos and flatness from prices "
                   "(range of closes t-29..t, net move close[t]-close[t-30]), so grid bars with fewer than 30 prior "
                   "bars in the window or at the exact middle are left out, and the flatter half is flatness above "
                   "the median, the less-flat half at or below it.",
    }
