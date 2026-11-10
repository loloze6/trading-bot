import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    all_rets = []
    short_rets = []
    short_fc = []

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window].reset_index(drop=True)
            if "close" not in df.columns:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = (pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
                  if "forecast" in df.columns else np.full(len(df), np.nan))
            n = len(df)
            # non-overlapping sampling: every 20 bars from the window's first bar, return kept inside the window
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    short_rets.append(r)
                    short_fc.append(fc[t])

    all_rets = np.asarray(all_rets, dtype=float)
    short_rets = np.asarray(short_rets, dtype=float)
    short_fc = np.asarray(short_fc, dtype=float)
    n_short = int(len(short_rets))

    diff_pp = None
    t_stat = None
    hit_short = None
    hit_all = None
    hit_excess_pp = None
    tertile_mean = None

    if len(all_rets) > 0 and n_short > 0:
        mean_all = float(np.mean(all_rets))
        mean_short = float(np.mean(short_rets))
        diff_pp = (mean_short - mean_all) * 100.0
        if n_short >= 2:
            sd = float(np.std(short_rets, ddof=1))
            if sd > 0:
                t_stat = (mean_short - mean_all) / (sd / np.sqrt(n_short))
        hit_short = float(np.mean(short_rets < 0))
        hit_all = float(np.mean(all_rets < 0))
        hit_excess_pp = (hit_short - hit_all) * 100.0
        cut = np.quantile(short_fc, 1.0 / 3.0)
        top = short_rets[short_fc <= cut]
        if len(top) > 0:
            tertile_mean = float(np.mean(top))

    supp_passed = None if hit_excess_pp is None else bool(hit_excess_pp >= 10.0)

    if n_short < 15 or diff_pp is None:
        status = "inconclusive"
        decided_by = ("Fewer than 15 non-overlapping short cases pooled across windows, "
                      "so the run is inconclusive whatever the numbers show.")
    else:
        reject_diff = diff_pp >= 0
        reject_hit = hit_excess_pp <= 0
        reject_tert = tertile_mean is not None and tertile_mean > 0
        confirm = (diff_pp <= -2.0 and t_stat is not None and t_stat <= -2.0
                   and hit_excess_pp >= 10.0)
        if reject_diff or reject_hit or reject_tert:
            status = "rejected"
            parts = []
            if reject_diff:
                parts.append("the difference is 0 or positive")
            if reject_hit:
                parts.append("the short-bar hit rate is not above the unconditional share")
            if reject_tert:
                parts.append("mean forward return after the largest-tertile shorts is positive")
            decided_by = "Reject: " + "; ".join(parts) + "."
        elif confirm:
            status = "confirmed"
            decided_by = ("Confirm: the difference is at most -2 percentage points with t-stat at or below -2, "
                          "and the short-bar hit rate exceeds the unconditional share by at least 10 points.")
        else:
            status = "inconclusive"
            decided_by = "The result lies between the confirm and reject lines, so it is inconclusive."

    def _f(x):
        return None if x is None else float(x)

    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar forward return on short bars minus on all bars (pp)",
            "value": _f(diff_pp),
            "threshold": "confirm at or below -2 percentage points with t-stat at or below -2; reject at 0 or above",
        },
        "supporting_check": {
            "name": "short-bar negative-return hit rate minus unconditional share (pp)",
            "value": _f(hit_excess_pp),
            "passed": supp_passed,
        },
        "cases": n_short,
        "decided_by": decided_by,
        "reading": ("Bars are sampled at every 20th row from each window's first row (only where the return fits in the window). "
                    "The t-stat is the one-sample t of short-bar returns against the pooled all-bar mean. "
                    "The largest-tertile shorts are the sampled short bars with forecast at or below the 1/3 quantile of short forecasts. "
                    "Any reject condition takes precedence over confirm."),
        "details": {
            "t_stat": _f(t_stat),
            "hit_rate_short": _f(hit_short),
            "hit_rate_all": _f(hit_all),
            "largest_tertile_short_mean_return": _f(tertile_mean),
            "n_all_cases": int(len(all_rets)),
        },
    }
