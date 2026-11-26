import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.fall_in_swings.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            calm = df["regime"].astype(str) == "unknown"
            day_ret = df["close"].astype(float).pct_change()
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            fall = (raw < 0) | (raw.isna() & (day_ret < 0))
            active = fc != 0
            situ = calm & fall & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "pooled slope of 10-bar excess forward return on forecast (forecast > 0, grid bars)"
    thr = "slope t >= 2 confirms (with mean excess > 0); slope t <= -2 rejects"
    sup_name = "mean excess 10-bar return on the same cases above 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases (days)": 0},
            "decided_by": ("Fewer than 90% of active bars are long forecasts on down days inside the calm profile "
                           "(regime 'unknown', fall_in_swings raw value < 0), as the plan's Fidelity requires."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                coin_grid.append((r, fc[i], ts.iloc[i].normalize()))
        if not coin_grid:
            continue
        mean_r = float(np.mean([g[0] for g in coin_grid]))
        for r, f, d in coin_grid:
            if np.isfinite(f) and f > 0:
                rows.append({"day": d, "excess": r - mean_r, "forecast": float(f)})

    cases = pd.DataFrame(rows, columns=["day", "excess", "forecast"])
    n_bars = int(len(cases))
    if n_bars > 0:
        daily = cases.groupby("day")[["excess", "forecast"]].sum()
    else:
        daily = pd.DataFrame(columns=["excess", "forecast"])
    n_days = int(len(daily))

    slope = None
    slope_t = None
    if n_days >= 3 and daily["forecast"].nunique() > 1:
        lr = stats.linregress(daily["forecast"].values, daily["excess"].values)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    mean_ex = None
    mean_t = None
    if n_bars > 0:
        mean_ex = float(cases["excess"].mean())
        dev = cases["excess"] - mean_ex
        S = dev.groupby(cases["day"]).sum().values
        D = len(S)
        if D > 1:
            se = np.sqrt(np.sum(S ** 2) * D / (D - 1)) / n_bars
            mean_t = float(mean_ex / se) if se > 0 else None
    sup_pass = None if mean_ex is None else bool(mean_ex > 0)

    counts = {"independent cases (days)": n_days, "grid bars with forecast > 0": n_bars,
              "active bars": int(n_active)}

    if n_days < 30 or slope_t is None:
        status = "not observable"
        decided = f"Fewer than 30 independent cases (days): {n_days}, the plan's minimum count is not reached."
    elif slope_t <= -2 or (mean_ex is not None and mean_ex < 0 and mean_t is not None and mean_t <= -2):
        status = "rejected"
        decided = ("Reject rule met: the slope's t is -2 or less, or the mean excess return is below 0 "
                   "with a t of -2 or less.")
    elif slope_t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule met: the slope's t is 2 or more and the mean excess 10-bar return is above 0."
    else:
        status = "inconclusive"
        decided = ("Neither rule met: the slope's t is between -2 and 2, or it is 2 or more "
                   "while the supporting check fails.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if slope_t is None else {"name": "OLS slope t (day-summed cases)", "value": slope_t},
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": mean_ex, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid bars on the same UTC day are summed (both excess return and forecast) into one case "
                    "before the OLS regression; the coin's mean 10-bar return is the mean over all its windows' "
                    "grid returns; the mean excess is over grid bars, and its t uses day-summed deviations."),
    }
