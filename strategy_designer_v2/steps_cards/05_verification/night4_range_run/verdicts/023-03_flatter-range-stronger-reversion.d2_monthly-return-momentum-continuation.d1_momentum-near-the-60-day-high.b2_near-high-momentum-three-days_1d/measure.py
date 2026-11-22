import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.hpm.last_history_value"
    MIN_CASES = 300

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is the 30-day return, and a larger one means a larger rise.
    # So the expected side is the sign of the 30-day return.
    # The raw component (30d return x positive proximity weight) has that sign.
    # standardise only scales it, so the forecast's sign should be the sign of the raw value.
    active = 0
    agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Where the raw value is missing, recompute the 30-day return from prices inside the window.
            ret30 = close / close.shift(30) - 1.0
            side_src = raw.where(raw.notna(), ret30)
            mask = fc.notna() & (fc != 0)
            active += int(mask.sum())
            s_exp = np.sign(side_src[mask])
            s_fc = np.sign(fc[mask])
            agree += int(((s_exp == s_fc) & (s_exp != 0)).sum())
    agreement = float(agree / active) if active > 0 else 0.0
    passed = bool(active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of next-3-bar excess return (vs coin mean 3-bar return) on forecast"
    threshold = "confirm: slope > 0 with t >= 2.0; reject: slope < 0 with t <= -2.0; at least 300 nonzero-forecast grid cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active)},
            "decided_by": "fewer than 90% of nonzero-forecast bars have the sign of the coin's 30-day return (raw hpm value), the side the Fidelity's situation and outcome expect",
            "reading": "the expected side on each bar is the sign of the raw hpm value (30-day return), recomputed from closes where it is missing",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                rows.append((coin, r, fc[i]))
    d = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    d = d.replace([np.inf, -np.inf], np.nan).dropna(subset=["ret"])
    coin_mean = d.groupby("coin")["ret"].mean()
    d["excess"] = d["ret"] - d["coin"].map(coin_mean)
    d = d.dropna(subset=["excess", "fc"])

    n_nonzero = int((d["fc"] != 0).sum())
    n_cases = int(len(d))
    counts = {"grid cases with a nonzero forecast": n_nonzero, "grid cases in regression": n_cases}

    slope = None
    tval = None
    if n_cases >= 3 and d["fc"].nunique() > 1:
        x = d["fc"].values.astype(float)
        y = d["excess"].values.astype(float)
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    reading = ("the regression is OLS with an intercept on all grid cases with a valid next-3-bar return "
               "(zero forecasts included); the coin's mean 3-bar return is the mean of its grid returns over all windows; "
               "a shortfall of the plan's 300-case minimum is reported as 'not observable' per the workflow")

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold}

    if n_nonzero < MIN_CASES:
        status = "not observable"
        decided = f"only {n_nonzero} grid cases with a nonzero forecast, below the plan's minimum of 300"
    elif tval is None:
        status = "inconclusive"
        decided = "the slope's t could not be computed, which meets neither the confirm nor the reject rule"
    elif slope > 0 and tval >= 2.0:
        status = "confirmed"
        decided = "the slope is positive with t >= 2.0 on at least 300 nonzero-forecast grid cases (confirm rule)"
    elif slope < 0 and tval <= -2.0:
        status = "rejected"
        decided = "the slope is negative with t <= -2.0 on at least 300 nonzero-forecast grid cases (reject rule)"
    else:
        status = "inconclusive"
        decided = "the slope's t lies between -2.0 and 2.0 (inconclusive rule)"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
