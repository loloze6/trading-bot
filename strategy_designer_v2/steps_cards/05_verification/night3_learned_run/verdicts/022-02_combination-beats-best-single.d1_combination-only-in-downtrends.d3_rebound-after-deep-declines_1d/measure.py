import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    LOOK = 90
    DEPTH_RAW = "debug_info.components.depth.last_history_value"
    DEPTH_POST = "debug_info.components.depth.post_pipeline_value"

    # ---------- 1. Situation check ----------
    # Situation: 90-bar return below 0. The expected side is long.
    # Where the window holds 90 earlier closes, ret90 is recomputed from the prices.
    # Earlier in the window, the regime detector's own decision for that rule is used.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns or "close" not in df.columns:
                continue
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            if DEPTH_RAW in df.columns:
                depth_raw = pd.to_numeric(df[DEPTH_RAW], errors="coerce").values
            else:
                depth_raw = np.full(len(df), np.nan)
            for i in range(len(df)):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if i >= LOOK and np.isfinite(close[i]) and np.isfinite(close[i - LOOK]) and close[i - LOOK] > 0:
                    in_regime = (close[i] / close[i - LOOK] - 1.0) < 0.0
                else:
                    in_regime = reg[i] == "mean_reversion"
                d = depth_raw[i]
                below_high = (not np.isfinite(d)) or d <= 0.0
                if in_regime and below_high and f > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of excess 5-bar forward return on depth forecast, mean_reversion grid bars"
    threshold = ("confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; "
                 "at least 100 grid cases")
    reading = ("The situation is ret90 < 0, recomputed from the closes where 90 prior bars exist in the window "
               "and otherwise taken from the recorded regime, together with depth <= 0 and forecast > 0; "
               "the normal drift is each coin's mean 5-bar return over all grid bars of all its windows; "
               "the regression is one OLS of excess return on post_pipeline_value pooled over all coins; "
               "fewer than 100 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's situation "
                           "(90-bar return below 0, close below its 90-bar high)."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # Normal drift: the mean of the 5-bar grid returns over all windows of the coin.
        all_rets = []
        cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            if DEPTH_POST in df.columns:
                post = pd.to_numeric(df[DEPTH_POST], errors="coerce").values
            else:
                post = np.full(len(df), np.nan)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if reg[i] == "mean_reversion" and np.isfinite(post[i]):
                    cases.append((post[i], r))
        if len(all_rets) == 0:
            continue
        drift = float(np.mean(all_rets))
        for x, r in cases:
            xs.append(float(x))
            ys.append(r - drift)

    n = len(xs)
    counts = {"grid cases": int(n)}
    slope = None
    tval = None
    if n >= 3:
        x = np.asarray(xs)
        y = np.asarray(ys)
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
                tval = float(lr.slope / lr.stderr)

    stat = {"name": "OLS slope t", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": threshold}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} grid cases in the mean_reversion regime, fewer than the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t cannot be computed, so the numbers meet neither the confirm rule nor the reject rule."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 over at least 100 grid cases (the confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 over at least 100 grid cases (the reject rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (the inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
