import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.vol_ratio.last_history_value"
    H = 7
    MIN_CASES = 300

    # ---------- 1. Situation check ----------
    # Fidelity: situation = 5-day mean volume vs 30-day mean volume, higher or lower.
    # Outcome: a higher ratio means a higher return, so long when the ratio is above the norm
    # (log ratio > 0) and short when it is below (log ratio < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            # Recompute the log ratio from volume where the raw value is missing.
            m5 = vol.rolling(5, min_periods=5).mean()
            m30 = vol.rolling(30, min_periods=30).mean()
            with np.errstate(divide="ignore", invalid="ignore"):
                recomputed = np.log(m5 / m30)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            expected = np.sign(raw)
            agree = active & raw.notna() & (expected != 0) & (np.sign(fc) == expected)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "pooled OLS slope of 7-bar excess forward return on forecast"
    threshold = "confirm if t >= 2 with top-minus-bottom tercile > 0; reject if t <= -2"
    sup_name = "top-minus-bottom forecast tercile mean excess 7-bar return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars have a forecast sign equal to the sign of the "
                           "log 5/30-day volume ratio (long above the norm, short below), as the Fidelity requires."),
            "reading": "The expected side is the sign of the raw log volume ratio, recomputed from volume where the raw value is missing.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, f = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, f))

    samp = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    n_cases = int(len(samp))
    counts = {"independent non-overlapping cases": n_cases}

    reading = ("The coin's mean 7-bar return is taken over its non-overlapping samples from all windows. "
               "The OLS includes an intercept and uses the ordinary OLS standard error. "
               "Terciles are cut at the pooled 1/3 and 2/3 forecast quantiles (bottom <= q1/3, top >= q2/3).")

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} independent non-overlapping cases, below the plan's minimum of 300.",
            "reading": reading,
        }

    samp["excess"] = samp["ret"] - samp.groupby("coin")["ret"].transform("mean")
    x = samp["fc"].values.astype(float)
    y = samp["excess"].values.astype(float)

    slope = None
    t_stat = None
    if np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_stat = float(res.slope / res.stderr) if res.stderr > 0 else None

    q1, q2 = np.quantile(x, [1 / 3, 2 / 3])
    top = y[x >= q2]
    bot = y[x <= q1]
    diff = float(np.mean(top) - np.mean(bot)) if len(top) > 0 and len(bot) > 0 else None
    sup_pass = bool(diff is not None and diff > 0)
    counts["top tercile cases"] = int(len(top))
    counts["bottom tercile cases"] = int(len(bot))

    if t_stat is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no forecast variation), so it meets neither the confirm nor the reject rule."
    elif t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope t is >= 2 and the top-minus-bottom tercile difference is above 0 (confirm rule)."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The slope t is <= -2 (reject rule)."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "The slope t is >= 2 but the tercile difference is 0 or below (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_stat} if t_stat is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
