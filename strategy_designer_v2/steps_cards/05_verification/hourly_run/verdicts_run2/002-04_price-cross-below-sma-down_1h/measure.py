import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.below_long_ma.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if RAW not in df.columns or "forecast" not in df.columns:
                continue
            sub = df[[RAW, "forecast"]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            # situation: close below SMA(200) (raw percent distance < 0), expected side short
            agree = active & (sub[RAW] < 0) & (sub["forecast"] < 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Used non-overlapping 24-bar blocks (bars 0, 24, 48, ... of each window) pooled across all coins "
               "and windows with a plain OLS slope t-stat of excess return on forecast (all grid bars, zero forecasts "
               "included), the excess taken against the mean 24-bar forward return of all bars of the same window, "
               "and the 200-block minimum applied before the confirm/reject rules.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "OLS slope of 24-bar excess forward return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "slope t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation (close below SMA(200), short) and the forecast disagree: only "
                           f"{agreement:.1%} of active bars are short bars with the close below the average, under 90%."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            mean_all = fwd.dropna().mean()
            if not np.isfinite(mean_all):
                continue
            excess = fwd - mean_all
            grid = np.arange(0, len(d), H)
            f = d["forecast"].astype(float).iloc[grid].values
            e = excess.iloc[grid].values
            ok = np.isfinite(f) & np.isfinite(e)
            xs.append(f[ok])
            ys.append(e[ok])

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])

    short_mask = x < 0
    n_short_blocks = int(short_mask.sum())

    slope = None
    t_slope = None
    if len(x) >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else None

    fall_share = float(np.mean(y[short_mask] < 0)) if n_short_blocks > 0 else None
    share_passed = (fall_share > 0.5) if fall_share is not None else None

    if n_short_blocks < 200:
        status = "inconclusive"
        decided_by = f"Inconclusive: fewer than 200 non-overlapping 24-bar blocks have forecast < 0 ({n_short_blocks})."
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope t-stat could not be computed."
    elif t_slope >= 2 and share_passed:
        status = "confirmed"
        decided_by = "Confirm: slope t >= 2 across the pooled windows and the short-bar fall share is above 50%."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "Reject: slope t <= -2, price rises after the close sits below the average."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "Inconclusive: confirm-level slope but the short-bar fall share is not above 50%."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: slope t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "OLS slope of 24-bar excess forward return on forecast",
                         "value": slope,
                         "statistic": ({"name": "OLS slope t (non-overlapping 24-bar blocks)", "value": t_slope}
                                       if t_slope is not None else None),
                         "threshold": "slope t >= 2 confirms (with fall share > 50%), t <= -2 rejects"},
        "supporting_check": {"name": "share of forecast<0 blocks followed by negative 24-bar excess return (> 50%)",
                             "value": fall_share,
                             "passed": share_passed},
        "counts": {"non-overlapping 24-bar blocks with forecast < 0": n_short_blocks,
                   "non-overlapping 24-bar blocks": int(len(x))},
        "decided_by": decided_by,
        "reading": reading,
    }
