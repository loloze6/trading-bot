import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    COL_RAW = "debug_info.components.fall_depth.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # 90-bar return: recorded raw value where present, else from prices (inside window)
            ret90_px = close / close.shift(90) - 1.0
            if COL_RAW in df.columns:
                ret90 = pd.to_numeric(df[COL_RAW], errors="coerce")
                ret90 = ret90.where(ret90.notna(), ret90_px)
            else:
                ret90 = ret90_px
            # 1-bar return over the 20-bar std of daily returns
            r1 = close.pct_change()
            vol = r1.rolling(20).std()
            vol = vol.where(vol > 0)
            jump = r1 / vol
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            computable = ret90.notna() & jump.notna()
            sit_calc = (ret90 < 0) & (jump >= 2.0)
            sit_fallback = regime == "mean_reversion"
            situation = np.where(computable, sit_calc, sit_fallback)
            active = (fc != 0).values
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0).values).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "t of the slope of drift-adjusted 5-bar forward return on the case's forecast, pooled over coins"
    threshold = "confirm: slope > 0 with t >= 2 (and supporting check passes); reject: slope < 0 with t <= -2; at least 30 cases"
    reading = ("Situation bars are recomputed from prices (90-bar return from the recorded fall_depth raw value where present, "
               "1-bar return over the rolling 20-bar std of daily returns including the bar), falling back to the recorded regime "
               "'mean_reversion' where the window lacks the history; a case is the first short bet (forecast fall of >= 2 points from "
               "its least negative level since the last bet, from 0 after a flat) in each 5-bar grid cell of a window with a full "
               "5-bar forward return in that window; the minimum of 30 cases is treated as a minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars where the 90-bar return is "
                           "negative and the 1-bar return is at least 2 usual moves (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # normal 5-bar drift of the coin over all windows (non-overlapping grid)
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a != 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(f)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            side = 0
            for i in range(n):
                fi = f[i]
                s = 1 if fi > 0 else (-1 if fi < 0 else 0)
                if s == 0:
                    side, ref = 0, 0.0
                    continue
                if s != side:
                    side, ref = s, 0.0
                if s < 0:
                    if ref - fi >= 2.0 - 1e-12:
                        bet[i] = True
                        ref = fi
                    else:
                        ref = max(ref, fi)
                else:
                    ref = min(ref, fi) if ref > 0 else ref
                    if fi - ref >= 2.0 - 1e-12:
                        ref = fi
            for p in range(0, n, H):
                idx = [i for i in range(p, min(p + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                a, b = c[i], c[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a != 0):
                    continue
                xs.append(float(f[i]))
                ys.append(float(b / a - 1.0 - drift))

    n_cases = len(xs)
    x = np.array(xs)
    y = np.array(ys)
    sup_val = float(np.mean(-y)) if n_cases > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    slope, tval = None, None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            tval = float(lr.slope / lr.stderr)

    counts = {"cases": int(n_cases)}
    stat = {"name": "OLS slope t", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": tval, "statistic": stat, "threshold": threshold}
    sup = {"name": "mean unusual 5-bar move in the short direction", "value": sup_val, "passed": sup_pass}

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than 30 cases (%d), the plan's minimum count, so the data could not show the idea." % n_cases
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the cases' forecasts), so neither rule is met."
    elif tval >= 2 and slope > 0:
        if sup_pass:
            status = "confirmed"
            decided = "Confirm: the slope is positive with t >= 2 and the mean unusual move in the short direction is above 0."
        else:
            status = "inconclusive"
            decided = "Inconclusive: a confirming slope (t >= 2) with a mean unusual move in the short direction of 0 or below."
    elif tval <= -2 and slope < 0:
        status = "rejected"
        decided = "Reject: the slope is negative with t <= -2, deeper falls are followed by smaller falls or rises."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
