import numpy as np
import pandas as pd


def measure(bars):
    H = 120
    BAND = 2.0
    FD_RAW = "debug_info.components.fall_depth.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    used_regime_fallback = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # surge: 24h return over the mean absolute 24h return of the last 720 bars
            r24 = close / close.shift(24) - 1.0
            mad = r24.abs().rolling(720, min_periods=720).mean()
            surge = r24 / mad.replace(0, np.nan)
            # prior week: recorded raw value, else sign of the lagged 168-bar return
            if FD_RAW in df.columns:
                pw = pd.to_numeric(df[FD_RAW], errors="coerce")
            else:
                pw = pd.Series(np.nan, index=df.index)
            pw_fb = close.shift(24) / close.shift(24 + 168) - 1.0
            pw = pw.where(pw.notna(), pw_fb)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)

            active = fc.notna() & (fc != 0)
            for i in np.flatnonzero(active.values):
                n_active += 1
                s = surge.iat[i]
                if np.isfinite(s):
                    surge_ok = s >= 3.0 - 1e-9
                else:
                    used_regime_fallback += 1
                    surge_ok = regime.iat[i] == "mean_reversion"
                p = pw.iat[i]
                pw_ok = np.isfinite(p) and p < 0
                side_ok = fc.iat[i] < 0
                if surge_ok and pw_ok and side_ok:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Surge recomputed as the 24h return over the mean absolute 24h return of the last 720 bars "
               "(the recorded regime label stands in where a window lacks 744 bars of history), prior week from "
               "fall_depth's raw value; one case per 120-bar grid cell = the first short bet in that cell; "
               "the depth halves are the top and bottom n//2 cases by |forecast| (the middle case dropped when n is odd).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean drift-removed 120-bar short-side move per case",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are bars where the 24h return is at least 3 usual daily "
                           "moves after a negative prior 7-day return with a short forecast."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_vals = []
    case_depth = []
    for coin, wins in bars.items():
        # coin drift: mean non-overlapping 120-bar return over all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(c)
            base = 0.0
            prev_side = 0
            seen_cells = set()
            for i in range(n):
                f = fc[i]
                side = -1 if f < 0 else (1 if f > 0 else 0)
                if side != -1:
                    base = 0.0
                    prev_side = side
                    continue
                if prev_side != -1:
                    base = 0.0
                m = -f
                if m - base >= BAND:
                    base = m
                    cell = i // H
                    if cell not in seen_cells:
                        seen_cells.add(cell)
                        if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                            r = c[i + H] / c[i] - 1.0
                            case_vals.append(-(r - drift))
                            case_depth.append(abs(f))
                else:
                    base = min(base, m)
                prev_side = -1

    vals = np.array(case_vals, dtype=float)
    depth = np.array(case_depth, dtype=float)
    n_cases = int(len(vals))

    mean = float(np.mean(vals)) if n_cases > 0 else None
    tstat = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        tstat = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    check_passed = None
    n_half = n_cases // 2
    if n_half >= 1:
        order = np.argsort(-depth, kind="mergesort")
        deep = vals[order[:n_half]]
        shallow = vals[order[n_cases - n_half:]]
        diff = float(np.mean(deep) - np.mean(shallow))
        check_passed = bool(diff > 0)

    main = {"name": "mean drift-removed 120-bar short-side move per case",
            "value": mean,
            "statistic": {"name": "t of the mean", "value": tstat} if tstat is not None else None,
            "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"}
    supp = {"name": "deeper-half minus shallower-half mean move (by |forecast|)",
            "value": diff, "passed": check_passed}
    counts = {"independent cases": n_cases}

    if n_cases < 30 or tstat is None:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, below the plan's minimum of 30."
    elif mean > 0 and tstat >= 2:
        if check_passed:
            status = "confirmed"
            decided = "Main mean above 0 with t >= 2 and the deeper half's mean move exceeds the shallower half's."
        else:
            status = "inconclusive"
            decided = "Main t >= 2 but the depth check fails, which the plan calls inconclusive."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Main mean below 0 with t <= -2: the price rose more than usual after these surges."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
