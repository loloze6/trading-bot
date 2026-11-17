import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_CASES = 300
    DIST = "debug_info.components.dist_high.last_history_value"
    DIST_PP = "debug_info.components.dist_high.post_pipeline_value"
    OFF = "debug_info.components.offset.last_history_value"
    OFF_PP = "debug_info.components.offset.post_pipeline_value"
    STD_WIN, STD_MINP = 60, 20

    def standardise_series(raw, fallback):
        # value(t) = raw(t) * 10 / mean(|raw| over last `window` values, t excluded), capped +-20.
        # Rebuilt exactly only when the full 60-value history sits inside the window
        # (warm-up bars are not recorded); otherwise the recorded post-pipeline value is used.
        raw = pd.to_numeric(raw, errors="coerce").to_numpy(dtype=float)
        fb = pd.to_numeric(fallback, errors="coerce").to_numpy(dtype=float) if fallback is not None \
            else np.full(len(raw), np.nan)
        out = np.full(len(raw), np.nan)
        for t in range(len(raw)):
            if t >= STD_WIN:
                past = raw[t - STD_WIN:t]
                past = past[~np.isnan(past)]
                if np.isnan(raw[t]) or len(past) < STD_MINP:
                    out[t] = fb[t]
                    continue
                m = np.mean(np.abs(past))
                out[t] = 0.0 if m == 0 else float(np.clip(raw[t] * 10.0 / m, -20, 20))
            else:
                out[t] = fb[t]
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            d_raw = df[DIST] if DIST in df.columns else pd.Series(np.nan, index=df.index)
            d_pp = df[DIST_PP] if DIST_PP in df.columns else None
            o_raw = df[OFF] if OFF in df.columns else pd.Series(np.nan, index=df.index)
            o_pp = df[OFF_PP] if OFF_PP in df.columns else None
            d_std = standardise_series(d_raw, d_pp)
            o_std = standardise_series(o_raw, o_pp)
            # Situation: close nearer the 30-day high than its usual distance (or through it)
            # -> long; further below than usual -> short.  Graded: sign of (dist_std + offset_std).
            expected = np.sign(d_std + o_std)
            for t in range(len(df)):
                if np.isnan(fc[t]) or fc[t] == 0:
                    continue
                n_active += 1
                e = expected[t]
                if not np.isnan(e) and e != 0 and np.sign(fc[t]) == e:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of slope of excess 10-bar forward return on forecast (pooled, non-overlapping)"
    main_thr = "confirm if t >= 2 with positive top-minus-bottom quintile difference; reject if t <= -2"
    sup_name = "top-minus-bottom forecast quintile mean excess 10-bar return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active forecast bars have the sign of the plan's graded situation "
                          "(long when the close is nearer the 30-day high than usual, short when further below).",
            "reading": "Expected side rebuilt from standardised dist_high plus standardised offset; post-pipeline "
                       "values used where the 60-bar history is not inside the window.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            for t in range(0, len(df), H):
                if t + H >= len(df):
                    break
                r = close[t + H] / close[t] - 1.0
                if np.isnan(r) or np.isnan(fc[t]) or not np.isfinite(r):
                    continue
                rows.append((coin, w, fc[t], r))
    samp = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    n_cases = int(len(samp))

    slope = None
    t_slope = None
    q_diff = None
    if n_cases >= 3:
        samp["excess"] = samp["ret"] - samp.groupby("coin")["ret"].transform("mean")
        x = samp["forecast"].to_numpy(dtype=float)
        y = samp["excess"].to_numpy(dtype=float)
        if np.var(x) > 0:
            res = stats.linregress(x, y)
            slope = float(res.slope)
            t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None
        if n_cases >= 5:
            ranks = samp["forecast"].rank(method="first")
            samp["q"] = pd.qcut(ranks, 5, labels=False)
            top = samp.loc[samp["q"] == 4, "excess"].mean()
            bot = samp.loc[samp["q"] == 0, "excess"].mean()
            q_diff = float(top - bot)

    sup_pass = None if q_diff is None else bool(q_diff > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent 10-bar cases, fewer than the plan's minimum of 300."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-minus-bottom quintile difference is positive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-minus-bottom quintile difference is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": q_diff, "passed": sup_pass},
        "counts": {"independent 10-bar cases": n_cases},
        "decided_by": decided,
        "reading": "Samples at positions 0,10,20,... of each window with a full 10-bar return inside it, the coin's "
                   "mean 10-bar return taken over those pooled samples, OLS with intercept on the recorded forecast, "
                   "quintiles by pooled forecast rank, and fewer than 300 cases reported as 'not observable' per the "
                   "workflow's minimum-count rule.",
    }
