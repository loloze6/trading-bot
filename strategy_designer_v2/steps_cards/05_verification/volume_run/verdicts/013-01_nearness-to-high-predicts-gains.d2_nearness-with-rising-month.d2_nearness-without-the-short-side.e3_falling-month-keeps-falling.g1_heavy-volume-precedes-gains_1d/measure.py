import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_CASES = 300
    VR_RAW = "debug_info.components.vol_ratio.last_history_value"
    VR_PP = "debug_info.components.vol_ratio.post_pipeline_value"
    OF_RAW = "debug_info.components.offset.last_history_value"
    OF_PP = "debug_info.components.offset.post_pipeline_value"
    STD_WIN, STD_MINP = 60, 20
    EPS = 1e-6

    def standardise_full(raw):
        """Standardise only where the full 60-value past window is inside the record; else NaN."""
        raw = np.asarray(raw, dtype=float)
        out = np.full(len(raw), np.nan)
        for t in range(len(raw)):
            if t < STD_WIN:
                continue
            past = raw[t - STD_WIN:t]
            past = past[~np.isnan(past)]
            if len(past) < STD_MINP or np.isnan(raw[t]):
                continue
            m = np.mean(np.abs(past))
            out[t] = 0.0 if m == 0 else float(np.clip(raw[t] * 10.0 / m, -20, 20))
        return out

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            vr_raw = pd.to_numeric(df[VR_RAW], errors="coerce").to_numpy(dtype=float) if VR_RAW in df.columns else np.full(len(df), np.nan)
            of_raw = pd.to_numeric(df[OF_RAW], errors="coerce").to_numpy(dtype=float) if OF_RAW in df.columns else np.full(len(df), np.nan)
            vr_pp = pd.to_numeric(df[VR_PP], errors="coerce").to_numpy(dtype=float) if VR_PP in df.columns else np.full(len(df), np.nan)
            of_pp = pd.to_numeric(df[OF_PP], errors="coerce").to_numpy(dtype=float) if OF_PP in df.columns else np.full(len(df), np.nan)

            s_vr = standardise_full(vr_raw)
            s_of = -standardise_full(of_raw)  # negate
            # Fallback to recorded transformed values where the 60-bar history is not in the record
            s_vr = np.where(np.isnan(s_vr), vr_pp, s_vr)
            s_of = np.where(np.isnan(s_of), of_pp, s_of)
            expected = np.clip((s_vr + s_of) / 2.0, -20, 20)

            for t in range(len(df)):
                if np.isnan(fc[t]) or fc[t] == 0:
                    continue
                n_active += 1
                e = expected[t]
                if np.isnan(e):
                    continue
                if abs(e) < EPS or np.sign(e) == np.sign(fc[t]):
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of coin-demeaned 3-bar forward return on forecast (non-overlapping grid, pooled)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive; at least 300 non-overlapping cases"
    reading = ("The coin's mean 3-bar return is taken over that coin's non-overlapping grid samples pooled over all its windows, "
               "the regression is OLS with an intercept, the 300-case minimum counts the pooled grid cases with a forecast and a return, "
               "and the situation check rebuilds standardise from raw values where the full 60-bar history is inside the window and uses the recorded post-pipeline values before that.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping cases": None},
            "decided_by": "Fewer than 90% of active bars have the forecast sign the plan's situation implies (long when the volume ratio is above its usual size, short when below).",
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        c_f, c_r = [], []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            for t in range(0, len(df) - H, H):
                r = close[t + H] / close[t] - 1.0
                if np.isnan(r) or np.isnan(fc[t]) or not np.isfinite(r):
                    continue
                c_f.append(fc[t])
                c_r.append(r)
        if len(c_r) == 0:
            continue
        mu = float(np.mean(c_r))
        xs.extend(c_f)
        ys.extend([r - mu for r in c_r])

    n = len(ys)
    counts = {"non-overlapping cases": int(n), "active bars": int(n_active)}

    if n < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n} non-overlapping cases, below the plan's minimum of 300.",
            "reading": reading,
        }

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    if np.var(x) == 0:
        return {
            "status": "inconclusive",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The forecast does not vary, so the slope cannot be estimated; no confirm or reject rule is met.",
            "reading": reading,
        }
    res = stats.linregress(x, y)
    slope = float(res.slope)
    t_stat = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else 0.0

    if slope > 0 and t_stat >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {t_stat:.2f} >= 2 over {n} cases (confirm rule)."
    elif slope < 0 and t_stat <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {t_stat:.2f} <= -2 over {n} cases (reject rule)."
    else:
        status = "inconclusive"
        decided = f"t = {t_stat:.2f} lies between -2 and 2 over {n} cases (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": t_stat},
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
