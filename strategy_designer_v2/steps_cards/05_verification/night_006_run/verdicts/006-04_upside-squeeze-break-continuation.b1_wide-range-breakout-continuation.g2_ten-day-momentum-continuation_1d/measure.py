import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_CASES = 300
    RET = "debug_info.components.ret10.last_history_value"
    DIST = "debug_info.components.near_top20.last_history_value"
    RET_PP = "debug_info.components.ret10.post_pipeline_value"
    DIST_PP = "debug_info.components.near_top20.post_pipeline_value"

    def standardise_in_window(raw, fallback, window=60, min_periods=20):
        # value(t) * 10 / mean(|last `window` raw values, t excluded|), capped at +-20.
        # The warm-up history is not recorded, so bars with fewer than min_periods
        # in-window past values use the recorded post-pipeline value.
        raw = pd.to_numeric(raw, errors="coerce")
        denom = raw.abs().shift(1).rolling(window, min_periods=min_periods).mean()
        out = (raw * 10.0 / denom).clip(-20, 20)
        out = out.where(denom.notna() & (denom != 0))
        if fallback is not None:
            fb = pd.to_numeric(fallback, errors="coerce")
            out = out.where(out.notna(), fb)
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RET not in df.columns or DIST not in df.columns:
                active = fc.notna() & (fc != 0)
                n_active += int(active.sum())
                continue
            r = standardise_in_window(df[RET], df[RET_PP] if RET_PP in df.columns else None)
            d = standardise_in_window(df[DIST], df[DIST_PP] if DIST_PP in df.columns else None)
            # graded situation: stronger 10-day return and close nearer the prior 20-day top
            # than usual (distance centred by the +10 offset); the expected side is long
            # when this score is positive (and, as a graded relation, short when negative).
            score = (r + d + 10.0) / 3.0
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & score.notna() & (np.sign(score) == np.sign(fc)) & (score != 0)
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "t of the pooled OLS slope of excess 10-bar forward return on forecast"
    threshold = "confirm: t >= 2 with top-minus-bottom quintile > 0; reject: t <= -2; else inconclusive"
    sup_name = "top minus bottom forecast quintile mean excess 10-bar return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent grid cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have a forecast sign matching the plan's graded "
                           "situation (standardised 10-bar return plus standardised distance from the prior "
                           "20-bar high, centred by +10), long when positive."),
            "reading": ("The situation is read as the sign of the rebuilt (ret10 + distance + 10)/3 score, "
                        "standardised from in-window raw values (post-pipeline values for the first bars)."),
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[j]) and np.isfinite(fc[i])) or close[i] == 0:
                    continue
                rows.append((coin, w, fc[i], close[j] / close[i] - 1.0))

    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "fwd"])
    n_cases = int(len(g))
    counts = {"independent grid cases": n_cases}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} independent grid cases, below the plan's minimum of 300.",
            "reading": ("Grid at positions 0,10,20,... of each window; excess over each coin's mean grid 10-bar "
                        "return across all windows; quintiles of the pooled grid forecasts."),
        }

    g["excess"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    x = g["forecast"].to_numpy(float)
    y = g["excess"].to_numpy(float)

    slope = None
    t_slope = None
    if np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else None

    ranks = g["forecast"].rank(method="first")
    q = pd.qcut(ranks, 5, labels=False)
    top = g.loc[q == 4, "excess"].mean()
    bot = g.loc[q == 0, "excess"].mean()
    qdiff = float(top - bot) if np.isfinite(top) and np.isfinite(bot) else None
    sup_pass = bool(qdiff is not None and qdiff > 0)

    if t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no variation in the forecast), so neither rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule met: slope t is 2 or more and the top-minus-bottom quintile difference is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Reject rule met: the slope t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule: slope t is 2 or more but the quintile difference is 0 or below."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope t lies between -2 and 2."

    counts["top quintile cases"] = int((q == 4).sum())
    counts["bottom quintile cases"] = int((q == 0).sum())

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": qdiff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid at positions 0,10,20,... of each window with forward return close[t+10]/close[t]-1 inside "
                    "the window; excess over each coin's mean grid 10-bar return across all its windows; quintiles "
                    "are of the pooled grid forecasts (ties broken by order)."),
    }
