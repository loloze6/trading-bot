import numpy as np
import pandas as pd
from scipy import stats

H = 26
SLOPE_COL = "debug_info.components.cloud_slope.last_history_value"


def _cloud(df):
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    tenkan = (high.rolling(9, min_periods=9).max() + low.rolling(9, min_periods=9).min()) / 2.0
    kijun = (high.rolling(26, min_periods=26).max() + low.rolling(26, min_periods=26).min()) / 2.0
    span_a = ((tenkan + kijun) / 2.0).shift(26)
    span_b = ((high.rolling(52, min_periods=52).max() + low.rolling(52, min_periods=52).min()) / 2.0).shift(26)
    bottom = np.minimum(span_a, span_b)
    mid = (span_a + span_b) / 2.0
    slope = mid / mid.shift(26) - 1.0
    return bottom, slope


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = df["forecast"].astype(float)
            close = df["close"].astype(float)
            bottom, slope_re = _cloud(df)
            if SLOPE_COL in df.columns:
                slope = df[SLOPE_COL].astype(float).where(df[SLOPE_COL].notna(), slope_re)
            else:
                slope = slope_re
            active = fc.notna() & (fc != 0)
            computable = bottom.notna() & slope.notna() & close.notna()
            n_active_uncomputable += int((active & ~computable).sum())
            act = active & computable
            n_active += int(act.sum())
            situ = (close < bottom) & (slope < 0) & (fc < 0)
            n_agree += int((act & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading_sc = ("The cloud position is recomputed from each window's own prices (standard Ichimoku 9/26/52 "
                  "with 26-bar displacement, close below the lower span), the slope is the recorded cloud_slope "
                  "raw value (recomputed where missing), and active bars whose cloud cannot be computed inside "
                  "their window are left out of the agreement share")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active,
                       "active bars not computable": n_active_uncomputable},
            "decided_by": ("Fewer than 90 % of the checkable active bars are bars where the close is below the "
                           "cloud with a falling cloud and a short forecast, as the Fidelity requires"
                           if agreement is not None else
                           "No active bar could be checked against the plan's situation"),
            "reading": reading_sc + ".",
        }

    # ---------- criterion ----------
    case_ret = []
    case_abs_fc = []
    case_coin = []
    coin_mean = {}
    for coin in sorted(bars):
        all_r = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for t in range(0, n - H, H):
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                r = close[t + H] / close[t] - 1.0
                all_r.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    case_ret.append(r)
                    case_abs_fc.append(abs(fc[t]))
                    case_coin.append(coin)
        coin_mean[coin] = float(np.mean(all_r)) if all_r else np.nan

    excess = np.array([-(r - coin_mean[c]) for r, c in zip(case_ret, case_coin)], dtype=float)
    absfc = np.array(case_abs_fc, dtype=float)
    ok = np.isfinite(excess) & np.isfinite(absfc)
    excess = excess[ok]
    absfc = absfc[ok]
    n_cases = int(len(excess))

    mean_val = float(np.mean(excess)) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_cases)))
    slope_val = None
    if n_cases >= 3 and np.ptp(absfc) > 0:
        slope_val = float(stats.linregress(absfc, excess).slope)
    slope_pass = None if slope_val is None else bool(slope_val > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases is not reached ({n_cases} cases)."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_val > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean short-signed excess return is above 0 with t >= 2 over at least 30 cases, and the slope on |forecast| is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 over at least 30 cases but the supporting slope is at or below 0, which the plan calls inconclusive."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean short-signed excess return is below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "mean short-signed 26-bar excess return over the coin's mean, on grid bars with forecast < 0",
            "value": mean_val,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases",
        },
        "supporting_check": {
            "name": "OLS slope of short-signed excess return on |forecast|",
            "value": slope_val,
            "passed": slope_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": (reading_sc + "; cases are grid bars at positions 0, 26, 52, ... of each window with a full "
                    "26-bar return inside the window, and the coin's mean 26-bar return is taken over the same grid "
                    "across all its windows."),
    }
