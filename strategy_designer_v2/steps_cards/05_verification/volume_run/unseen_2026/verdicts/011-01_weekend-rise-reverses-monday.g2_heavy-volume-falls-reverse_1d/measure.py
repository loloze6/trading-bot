import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    VR_COL = "debug_info.components.vol.last_history_value"
    RET_COL = "debug_info.components.fall.last_history_value"

    # ---------- coin mean daily return over all windows (within-window returns only) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).dropna()
            rets.append(r.values)
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- collect active bars and situation check ----------
    n_active_all = 0
    n_agree = 0
    rows = []  # (forecast, excess, vr)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            volume = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # volume ratio: recorded raw value where present, else recomputed from prices
            vr_rec = pd.to_numeric(df[VR_COL], errors="coerce") if VR_COL in df.columns else pd.Series(np.nan, index=df.index)
            vr_calc = volume / volume.rolling(60, min_periods=60).mean()
            vr = vr_rec.where(vr_rec.notna(), vr_calc)

            # down day: recorded raw vol-scaled 1-bar return where present, else close below previous close
            ret_rec = pd.to_numeric(df[RET_COL], errors="coerce") if RET_COL in df.columns else pd.Series(np.nan, index=df.index)
            down_calc = close < close.shift(1)
            down = pd.Series(np.where(ret_rec.notna(), ret_rec < 0, down_calc), index=df.index).astype(bool)

            situation = (vr >= 1.5 - 1e-9) & down
            active = fc != 0
            n_active_all += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            nxt = close.shift(-1) / close - 1.0  # horizon 1: every bar is on the grid
            excess = nxt - coin_mean[coin]
            for i in np.where(fc.values > 0)[0]:
                ex = excess.iloc[i]
                if pd.notna(ex):
                    rows.append((float(fc.iloc[i]), float(ex), float(vr_rec.iloc[i]) if pd.notna(vr_rec.iloc[i]) else np.nan))

    agreement = (n_agree / n_active_all) if n_active_all > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "forecast-weighted mean excess next-bar return on forecast > 0 bars"
    main_thr = "weighted mean > 0 with ordinary t of (forecast/10 x excess) >= 2 to confirm; t <= -2 to reject"
    sup_name = "mean excess next-bar return, high-volume-ratio half minus low half (Welch t)"
    reading = ("Volume halves split active bars sorted by the recorded vol.last_history_value into the lower n//2 and "
               "upper n//2 (middle bar dropped when n is odd); the supporting check passes when high minus low > 0; "
               "the plan's 'fewer is inconclusive' minimum is reported as 'not observable' per the workflow; the "
               "situation check uses recorded component values where present and recomputes them from prices otherwise.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active_all)},
            "decided_by": ("Fewer than 90% of active bars are heavy-volume (ratio >= 1.5) down days with a long forecast, "
                           "so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    arr = np.array(rows, dtype=float) if rows else np.zeros((0, 3))
    f = arr[:, 0]
    ex = arr[:, 1]
    n = len(f)

    wmean = float(np.sum(f * ex) / np.sum(f)) if n > 0 and np.sum(f) > 0 else None
    x = f / 10.0 * ex
    if n > 1 and np.std(x, ddof=1) > 0:
        t_main = float(np.mean(x) / (np.std(x, ddof=1) / np.sqrt(n)))
    else:
        t_main = None

    # volume halves
    valid = ~np.isnan(arr[:, 2]) if n else np.array([], dtype=bool)
    sub = arr[valid]
    order = np.argsort(sub[:, 2], kind="mergesort") if len(sub) else np.array([], dtype=int)
    half = len(sub) // 2
    low = sub[order[:half], 1] if half > 0 else np.array([])
    high = sub[order[len(sub) - half:], 1] if half > 0 else np.array([])
    n_low, n_high = len(low), len(high)
    diff = float(np.mean(high) - np.mean(low)) if n_low > 0 and n_high > 0 else None
    t_diff = None
    if n_low > 1 and n_high > 1:
        tt = stats.ttest_ind(high, low, equal_var=False)
        t_diff = float(tt.statistic) if np.isfinite(tt.statistic) else None
    sup_passed = (diff > 0) if diff is not None else None

    counts = {"active bars": int(n), "high volume half": int(n_high), "low volume half": int(n_low)}

    result = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": wmean,
                         "statistic": {"name": "ordinary t of forecast/10 x excess return", "value": t_main} if t_main is not None else None,
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed,
                             "welch_t": t_diff},
        "counts": counts,
        "reading": reading,
    }

    if n < 100 or n_high < 40 or n_low < 40:
        result["status"] = "not observable"
        result["decided_by"] = ("The plan needs at least 100 active bars and 40 in each volume half; "
                                f"there are {n} active, {n_high} high and {n_low} low.")
        return result

    if t_main is None or wmean is None:
        result["status"] = "inconclusive"
        result["decided_by"] = "The main measure's t could not be computed, so neither the confirm nor the reject rule is met."
        return result

    if t_main <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "The main measure's t is <= -2 (reject rule)."
    elif wmean > 0 and t_main >= 2:
        if t_diff is not None and t_diff <= -2:
            result["status"] = "rejected"
            result["decided_by"] = "The main measure confirms but the high-minus-low volume difference has Welch t <= -2 (reject rule)."
        elif diff is not None and diff > 0:
            result["status"] = "confirmed"
            result["decided_by"] = "Weighted mean excess return > 0 with t >= 2 and the high-volume half beats the low half (confirm rule)."
        else:
            result["status"] = "inconclusive"
            result["decided_by"] = "The main measure confirms but the volume difference is not > 0 with Welch t between -2 and 0 (inconclusive rule)."
    else:
        result["status"] = "inconclusive"
        result["decided_by"] = "The main measure's t lies between -2 and 2 (inconclusive rule)."
    return result
