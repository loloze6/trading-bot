import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.pre_move.last_history_value"
    H = 2
    SETTLE_HOURS = {0, 8, 16}

    n_active = 0
    n_agree = 0
    case_rows = []  # (coin, forecast, fwd_return)
    drift_by_coin = {}

    for coin, wins in bars.items():
        grid_rets = []
        per_coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            n = len(df)

            # Non-overlapping 2-bar returns on the grid 0, 2, 4, ... for the coin's normal drift
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)

            # Settlement bar: the bar's close (= next bar's start) is 00:00, 08:00 or 16:00 UTC
            close_time = ts + pd.Timedelta(hours=1)
            settle = (close_time.dt.hour.isin(SETTLE_HOURS) & (close_time.dt.minute == 0)).values

            # Raw pre-move: recorded value where present, otherwise rebuilt from prices (2-bar return)
            price_pre = np.full(n, np.nan)
            price_pre[H:] = close[H:] / close[:-H] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
                pre = np.where(np.isfinite(raw), raw, price_pre)
            else:
                pre = price_pre

            # Situation check
            active = fc != 0
            n_active += int(active.sum())
            expected_sign = -np.sign(pre)
            agree = active & settle & np.isfinite(pre) & (np.sign(fc) == expected_sign) & (expected_sign != 0)
            n_agree += int(agree.sum())

            # Cases: settlement bars with nonzero forecast
            idx = np.where(settle & active)[0]
            for i in idx:
                if i + H < n:
                    r = close[i + H] / close[i] - 1.0
                    if np.isfinite(r):
                        per_coin_cases.append((coin, float(fc[i]), float(r)))
        drift = float(np.mean(grid_rets)) if len(grid_rets) else 0.0
        drift_by_coin[coin] = drift
        case_rows.extend(per_coin_cases)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("A settlement bar is a bar whose close (start + 1h) falls at 00:00, 08:00 or 16:00 UTC and the "
               "expected side is opposite to the 2-bar pre-move (recorded raw value, else rebuilt from closes); "
               "the coin's normal 2-bar drift is the mean of non-overlapping 2-bar returns (grid 0,2,4,... per "
               "window, inside windows) pooled over all the coin's windows; thirds are taken over all cases pooled, "
               "sorted by |forecast| (n//3 lowest vs n//3 highest); the plan's 1000-case minimum, when missed, "
               "gives 'not observable' as the workflow requires.")

    main_name = "mean of forecast/10 x drift-removed 2-bar return per case"
    main_thr = "t >= 2 (with supporting check) confirms; t <= -2 rejects; otherwise inconclusive"
    sup_name = "Welch t of top-third minus bottom-third |forecast| drift-removed return in forecast direction"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": int(len(case_rows)), "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are settlement bars (close at "
                           "00:00/08:00/16:00 UTC) with a forecast opposite to the 2-bar pre-move."),
            "reading": reading,
        }

    n_cases = len(case_rows)
    counts = {"cases": int(n_cases)}

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "No cases: the minimum of 1000 cases in total is not reached.",
            "reading": reading,
        }

    coins = [c for c, _, _ in case_rows]
    f = np.array([x for _, x, _ in case_rows], dtype=float)
    r = np.array([x for _, _, x in case_rows], dtype=float)
    d = np.array([drift_by_coin[c] for c in coins], dtype=float)
    excess = r - d
    vals = f / 10.0 * excess

    mean_v = float(np.mean(vals))
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t_main = float(mean_v / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    else:
        t_main = 0.0

    # Supporting check
    dir_ret = np.sign(f) * excess
    order = np.argsort(np.abs(f), kind="mergesort")
    k = n_cases // 3
    sup_t = None
    sup_pass = None
    if k >= 2:
        bottom = dir_ret[order[:k]]
        top = dir_ret[order[-k:]]
        tt = stats.ttest_ind(top, bottom, equal_var=False)
        sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
        sup_pass = bool(sup_t is not None and sup_t >= 2.0)
    counts["top third cases"] = int(k)
    counts["bottom third cases"] = int(k)

    if n_cases < 1000:
        status = "not observable"
        decided = f"Only {n_cases} cases in total, below the plan's minimum of 1000 cases."
    elif t_main >= 2.0 and sup_pass:
        status = "confirmed"
        decided = "Confirm: the main measure has t >= 2 and the supporting check passes (Welch t >= 2)."
    elif t_main <= -2.0:
        status = "rejected"
        decided = "Reject: the main measure has t <= -2."
    elif t_main >= 2.0:
        status = "inconclusive"
        decided = "Inconclusive: the main t >= 2 but the supporting check does not pass."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the main measure's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_v,
                         "statistic": {"name": "ordinary t of the mean", "value": t_main},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": sup_t, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
