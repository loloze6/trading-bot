import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.vsr10.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Where the component is not recorded, rebuild the sign of the
            # volatility-scaled 10-day return from the 10-day price return.
            ret10 = close / close.shift(10) - 1.0
            raw = raw.where(raw.notna(), ret10)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # The situation is an advance (raw > 0) and the expected side is long.
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where "
                           "the 10-day volatility-scaled return is positive, as the plan's situation requires."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1, f = close[i], close[i + H], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                rows.append((coin, w, f, c1 / c0 - 1.0))

    grid = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    if len(grid) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": "mean excess 3-bar return of the top-20% forecast grid bars",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"grid bars in the top group": 0},
            "decided_by": "No grid bars with a 3-bar return: the minimum of 100 top-group grid bars is not reached.",
            "reading": "none",
        }

    grid["coin_mean"] = grid.groupby("coin")["ret"].transform("mean")
    grid["excess"] = grid["ret"] - grid["coin_mean"]

    pos = grid[grid["forecast"] > 0]
    if len(pos) > 0:
        q = float(np.quantile(pos["forecast"].to_numpy(), 0.8))
        top = pos[pos["forecast"] >= q]
    else:
        q = None
        top = pos
    zero = grid[grid["forecast"] == 0]

    n_top = int(len(top))
    n_pos = int(len(pos))
    n_zero = int(len(zero))

    mean_top = float(top["excess"].mean()) if n_top > 0 else None
    t_top = None
    if n_top >= 2:
        sd = float(top["excess"].std(ddof=1))
        if sd > 0:
            t_top = float(mean_top / (sd / np.sqrt(n_top)))

    diff = None
    if n_top > 0 and n_zero > 0:
        diff = float(mean_top - zero["excess"].mean())
    sup_passed = (diff > 0) if diff is not None else None

    reading = ("The top group is the grid bars with forecast > 0 (and a valid 3-bar return) whose forecast is at or "
               "above the 80th percentile of those bars pooled over coins, ties at the cut-off included; the coin's mean "
               "3-bar return is the mean over its non-overlapping grid returns across all windows; the plan's "
               "'fewer than 100 top-group bars' case is reported as not observable.")

    main = {
        "name": "mean excess 3-bar return of the top-20% forecast grid bars",
        "value": mean_top,
        "statistic": {"name": "one-group t", "value": t_top} if t_top is not None else None,
        "threshold": "mean > 0 with t >= 2 (and supporting difference > 0) confirms; mean < 0 with t <= -2 rejects",
    }
    supporting = {
        "name": "top-group mean excess minus forecast-0 mean excess",
        "value": diff,
        "passed": sup_passed,
    }
    counts = {
        "grid bars in the top group": n_top,
        "grid bars with forecast > 0": n_pos,
        "grid bars with forecast 0": n_zero,
    }

    if n_top < 100:
        status = "not observable"
        decided = f"Only {n_top} grid bars in the top group, below the plan's minimum of 100."
    elif t_top is None:
        status = "inconclusive"
        decided = "The t of the top-group mean cannot be computed (zero dispersion), so neither rule is met."
    elif mean_top > 0 and t_top >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "The top-group mean excess return is above 0 with t >= 2 and the supporting difference is above 0."
    elif mean_top < 0 and t_top <= -2:
        status = "rejected"
        decided = "The top-group mean excess return is below 0 with t <= -2."
    elif t_top >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting difference is 0 or less (or not measurable), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the top-group mean excess return lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
