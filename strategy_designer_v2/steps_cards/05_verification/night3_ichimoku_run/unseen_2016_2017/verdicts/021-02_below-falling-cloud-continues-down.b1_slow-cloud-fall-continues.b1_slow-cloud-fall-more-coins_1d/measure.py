import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 26
    FC = "forecast"
    SF = "debug_info.components.slow_fall.last_history_value"

    def _ichimoku_situation(df):
        """Recompute cloud position (nearest edge, close base) and the cloud mid's 26-bar
        percent slope from the window's own prices; NaN where history is insufficient."""
        high = df["high"].astype(float)
        low = df["low"].astype(float)
        close = df["close"].astype(float)
        tenkan = (high.rolling(9, min_periods=9).max() + low.rolling(9, min_periods=9).min()) / 2.0
        kijun = (high.rolling(26, min_periods=26).max() + low.rolling(26, min_periods=26).min()) / 2.0
        span_a = ((tenkan + kijun) / 2.0).shift(26)
        span_b = ((high.rolling(52, min_periods=52).max() + low.rolling(52, min_periods=52).min()) / 2.0).shift(26)
        lower = np.minimum(span_a, span_b)
        valid_cloud = span_a.notna() & span_b.notna()
        below = close < lower
        mid = (span_a + span_b) / 2.0
        slope = mid / mid.shift(H) - 1.0
        valid_slope = slope.notna()
        computable = valid_cloud & valid_slope
        situation = below & (slope < 0)
        return situation.values, computable.values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_recomputed = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            sit, comp = _ichimoku_situation(df)
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            active = fc != 0
            for i in np.where(active)[0]:
                n_active += 1
                if comp[i]:
                    n_recomputed += 1
                    in_sit = bool(sit[i])
                else:
                    in_sit = reg[i] == "trending"
                if in_sit and fc[i] < 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean of forecast/10 x (26-bar forward return - coin's 26-bar drift) on trending grid bars"
    main_thr = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2"
    sup_name = "slow-fall half minus fast-fall half excess 26-bar return (split at median slow_fall), Welch t"
    reading = ("Situation recomputed from each window's own prices (Ichimoku 9/26/52/26, close below the lower cloud "
               "edge and cloud mid 26-bar percent slope < 0) where enough history exists, and taken from the recorded "
               "regime 'trending' (the detector's rule of those two conditions) on bars where it cannot be recomputed; "
               "the slower-fall half is slow_fall above its median (larger 1/(1+fall%)), the faster half at or below it; "
               "drift is the coin's mean non-overlapping 26-bar return over all its windows; the plan's 'fewer than "
               "30 cases or 15 per half' is treated as the minimum-count rule giving 'not observable'.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"independent grid cases in the regime": 0, "slow-fall half": 0, "fast-fall half": 0},
            "decided_by": "No bar has a non-zero forecast, so the idea could not be observed.",
            "reading": reading,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation and short": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars where the close is "
                           "below a falling Ichimoku cloud, so the config does not do what the plan's situation says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # drift per coin: mean non-overlapping 26-bar return over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).reset_index(drop=True).values
            for i in range(0, len(c), H):
                if i + H < len(c) and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    main_vals = []
    sup_rows = []
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            reg = df["regime"].astype(str).values
            sf = pd.to_numeric(df[SF], errors="coerce").values if SF in df.columns else np.full(len(df), np.nan)
            for i in range(0, len(df), H):
                if reg[i] != "trending":
                    continue
                if i + H >= len(df) or not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                if not np.isfinite(fc[i]):
                    continue
                r = c[i + H] / c[i] - 1.0
                ex = r - d
                main_vals.append(fc[i] / 10.0 * ex)
                if np.isfinite(sf[i]):
                    sup_rows.append((sf[i], ex))

    n_cases = len(main_vals)
    slow, fast = [], []
    if sup_rows:
        sfv = np.array([s for s, _ in sup_rows])
        exv = np.array([e for _, e in sup_rows])
        med = np.median(sfv)
        slow = exv[sfv > med]
        fast = exv[sfv <= med]
    n_slow, n_fast = len(slow), len(fast)

    def _t_mean(x):
        x = np.asarray(x, float)
        if len(x) < 2:
            return np.nan
        sd = x.std(ddof=1)
        if sd == 0:
            return np.nan
        return float(x.mean() / (sd / np.sqrt(len(x))))

    main_mean = float(np.mean(main_vals)) if n_cases else None
    main_t = _t_mean(main_vals) if n_cases else np.nan
    diff = float(np.mean(slow) - np.mean(fast)) if (n_slow and n_fast) else None
    diff_t = np.nan
    if n_slow >= 2 and n_fast >= 2:
        diff_t = float(stats.ttest_ind(slow, fast, equal_var=False).statistic)

    counts = {"independent grid cases in the regime": int(n_cases),
              "slow-fall half": int(n_slow), "fast-fall half": int(n_fast)}

    def _num(x):
        return None if x is None or not np.isfinite(x) else float(x)

    sup_pass = None
    if diff is not None and np.isfinite(diff_t):
        sup_pass = bool(diff < 0 and diff_t <= -1)

    out = {
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": _num(main_mean),
                         "statistic": {"name": "t of the mean", "value": _num(main_t)} if np.isfinite(main_t) else None,
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": _num(diff), "passed": sup_pass,
                             "welch_t": _num(diff_t)},
        "counts": counts,
        "reading": reading,
    }

    if n_cases < 30 or n_slow < 15 or n_fast < 15:
        out["status"] = "not observable"
        out["decided_by"] = ("A minimum count is not reached: the plan needs at least 30 independent grid cases in the "
                             "regime and at least 15 per half.")
        return out

    reject_main = main_mean is not None and np.isfinite(main_t) and main_mean < 0 and main_t <= -2
    reject_sup = diff is not None and np.isfinite(diff_t) and diff > 0 and diff_t >= 2
    confirm_main = main_mean is not None and np.isfinite(main_t) and main_mean > 0 and main_t >= 2

    if reject_main or reject_sup:
        out["status"] = "rejected"
        out["decided_by"] = ("Reject rule met: " +
                             ("the main mean is below 0 with t <= -2" if reject_main else "") +
                             (" and " if reject_main and reject_sup else "") +
                             ("the slow-minus-fast difference is above 0 with t >= +2" if reject_sup else "") + ".")
    elif confirm_main and sup_pass:
        out["status"] = "confirmed"
        out["decided_by"] = ("Confirm rule met: the main mean is above 0 with t >= 2 and the slow-minus-fast "
                             "difference is below 0 with t <= -1.")
    else:
        out["status"] = "inconclusive"
        if confirm_main:
            out["decided_by"] = ("The main mean meets the confirm rule but the slow-minus-fast check fails without "
                                 "reaching t >= +2, which the plan calls inconclusive.")
        else:
            out["decided_by"] = ("Neither the confirm nor the reject rule is met (main t between -2 and 2 or "
                                 "otherwise short of both rules), which the plan calls inconclusive.")
    return out
