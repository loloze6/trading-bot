import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.support_cluster.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan situation: a past swing low sits at or above the close
    # (raw count x nearness > 0). Expected side: short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw > 0) & (fc < 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.90)

    main_name = "OLS slope of 5-bar excess return on short size (-forecast/10), non-overlapping grid, pooled"
    main_thr = "confirm: slope < 0 with t <= -2 (and largest-third mean < 0); reject: slope > 0 with t >= +2"
    sup_name = "mean 5-bar excess return in the largest third of short sizes"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": (f"Only {agreement:.1%} of the non-zero-forecast bars are short bars with a past swing low "
                           f"at or above the close (raw component > 0), below the 90 % required."),
            "reading": "The situation is taken as a raw component value above zero (a swing low at or above the close) and the side as forecast below zero.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float) if "forecast" in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                coin_rows.append((coin, w, c1 / c0 - 1.0, fc[p]))
        if not coin_rows:
            continue
        rets = np.array([r[2] for r in coin_rows])
        coin_mean = float(np.mean(rets))
        for (c, w, r, f) in coin_rows:
            rows.append((c, w, r - coin_mean, f))

    if rows:
        ex = np.array([r[2] for r in rows], dtype=float)
        fcv = np.array([r[3] for r in rows], dtype=float)
    else:
        ex = np.array([], dtype=float)
        fcv = np.array([], dtype=float)

    ok = np.isfinite(ex) & np.isfinite(fcv)
    ex, fcv = ex[ok], fcv[ok]
    size = -fcv / 10.0

    nz = fcv != 0
    n_nonzero = int(nz.sum())
    ex_nz, size_nz = ex[nz], size[nz]
    n_top = n_nonzero // 3
    if n_top > 0:
        order = np.argsort(-size_nz, kind="mergesort")
        top_ex = ex_nz[order[:n_top]]
        top_mean = float(np.mean(top_ex))
    else:
        top_mean = None

    slope = None
    tval = None
    if len(ex) >= 3 and np.std(size) > 0:
        lr = stats.linregress(size, ex)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_passed = None if top_mean is None else bool(top_mean < 0)

    counts = {
        "non-zero-forecast grid cases": n_nonzero,
        "largest-third cases": int(n_top),
        "grid cases in regression": int(len(ex)),
    }

    if n_nonzero < 100:
        status = "not observable"
        decided = f"Only {n_nonzero} non-zero-forecast grid cases, fewer than the plan's minimum of 100."
    elif n_top < 30:
        status = "not observable"
        decided = f"Only {n_top} cases in the largest third, fewer than the plan's minimum of 30."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope < 0 and tval <= -2:
        if sup_passed:
            status = "confirmed"
            decided = "The slope is negative with t <= -2 and the largest-third mean excess return is below zero."
        else:
            status = "inconclusive"
            decided = "The slope is negative with t <= -2 but the largest-third mean excess return is at or above zero."
    elif slope > 0 and tval >= 2:
        status = "rejected"
        decided = "The slope is positive with t >= +2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": top_mean, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The regression uses every grid bar (zero-forecast bars at short size 0) with the coin's mean "
                    "taken over all its non-overlapping grid returns, and the largest third is the top floor(n/3) "
                    "non-zero-forecast grid cases ranked by short size."),
    }
