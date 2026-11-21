import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW = "debug_info.components.grind_residual.last_history_value"

    # ---------- 1. Situation check: active bars must be bars where the coin rose over 72 bars, and long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            past_ret = close / close.shift(H) - 1.0  # within this window only
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            # rise over 72 bars: from prices where the window holds 72 past bars, else from the raw value (>0 only when risen)
            rose = past_ret > 0
            no_hist = past_ret.isna()
            rose = rose.where(~no_hist, raw > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & rose.fillna(False).astype(bool) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean 72-bar forward return, grind group minus jump group"
    threshold = "confirm: difference > 0 with Welch t >= 2; reject: difference < 0 with Welch t <= -2; at least 200 grid cases per group"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the coin rose "
                           "over the past 72 bars, as the plan's situation and side require."),
            "reading": "The 72-bar rise is taken from closes inside the window, and from the raw grind_residual being above 0 on the first 72 bars of a window.",
        }

    # ---------- 2. Criterion ----------
    grind_all = []
    jump_all = []
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0 or RAW not in df.columns:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            raw = pd.to_numeric(d[RAW], errors="coerce").values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = raw[i]
                c0, c1 = close[i], close[i + H]
                if not np.isfinite(r) or r <= 0:
                    continue
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append((r, c1 / c0 - 1.0))
        if not rows:
            continue
        arr = np.array(rows, dtype=float)
        med = np.median(arr[:, 0])
        grind_all.extend(arr[arr[:, 0] > med, 1].tolist())
        jump_all.extend(arr[arr[:, 0] <= med, 1].tolist())

    g = np.array(grind_all, dtype=float)
    j = np.array(jump_all, dtype=float)
    ng, nj = int(len(g)), int(len(j))
    counts = {"grind group grid cases": ng, "jump group grid cases": nj}

    diff = None
    tval = None
    if ng >= 2 and nj >= 2:
        diff = float(np.mean(g) - np.mean(j))
        t = stats.ttest_ind(g, j, equal_var=False).statistic
        tval = float(t) if np.isfinite(t) else None

    reading = ("The sample is the grid bars (positions 0, 72, 144, ... of each window) with raw grind_residual above 0 "
               "and a 72-bar forward return inside the window; the per-coin median is taken over that coin's sample "
               "across all its windows; the plan's 200-case minimum, when not met, is reported as not observable.")

    if ng < 200 or nj < 200:
        status = "not observable"
        decided_by = "Fewer than 200 independent grid cases in at least one group (grind %d, jump %d)." % (ng, nj)
    elif diff is None or tval is None:
        status = "inconclusive"
        decided_by = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif diff > 0 and tval >= 2:
        status = "confirmed"
        decided_by = "The grind-minus-jump difference in mean 72-bar forward return is above 0 with Welch t >= 2."
    elif diff < 0 and tval <= -2:
        status = "rejected"
        decided_by = "The grind-minus-jump difference is below 0 with Welch t <= -2."
    else:
        status = "inconclusive"
        decided_by = "The Welch t is between -2 and 2 (or its sign disagrees with the difference), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": {"name": "Welch t", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
