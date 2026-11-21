import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.excess_power_against.last_history_value"
    MIN_CASES = 300

    # ---------- 1. situation check ----------
    # Situation (graded): raw = (w - w_bar) * z(nearness); expected side = lean against: sign(forecast) == -sign(raw)
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for wname, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw != 0) & (np.sign(f) == -np.sign(raw))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 1.0
    passed = agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "mean of (forecast/10) x (5-bar return minus coin mean 5-bar return)",
                "value": None, "statistic": None,
                "threshold": "confirm t >= 2, reject t <= -2, with at least 300 non-zero cases",
            },
            "supporting_check": None,
            "counts": {"non-overlapping cases where the forecast is not zero": None},
            "decided_by": "Fewer than 90% of active bars have a forecast sign opposite to the sign of (w - w_bar) x z(nearness), "
                          "so the config does not lean against excess past power as the Fidelity states.",
            "reading": "The situation is graded: a bar is in it when the raw component value is non-zero, and on its side when the forecast sign is opposite to that raw value.",
        }

    # ---------- 2. criterion ----------
    cells = []  # (coin, forecast, ret)
    for coin, wins in bars.items():
        for wname, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                cells.append((coin, f[t], c1 / c0 - 1.0))

    cdf = pd.DataFrame(cells, columns=["coin", "forecast", "ret"])
    if len(cdf):
        coin_mean = cdf.groupby("coin")["ret"].mean()
        cdf["excess"] = cdf["ret"] - cdf["coin"].map(coin_mean)
        cdf = cdf[cdf["forecast"].notna()]
        cdf["val"] = cdf["forecast"] / 10.0 * cdf["excess"]
    n_cells = int(len(cdf))
    n_nonzero = int((cdf["forecast"] != 0).sum()) if n_cells else 0

    mean_val, t_val = None, None
    if n_cells >= 2:
        v = cdf["val"].to_numpy(dtype=float)
        mean_val = float(np.mean(v))
        sd = float(np.std(v, ddof=1))
        t_val = float(mean_val / (sd / np.sqrt(n_cells))) if sd > 0 else 0.0

    if n_nonzero < MIN_CASES or t_val is None:
        status = "not observable"
        decided = f"Only {n_nonzero} non-overlapping cases with a non-zero forecast, below the plan's minimum of 300."
    elif t_val >= 2:
        status = "confirmed"
        decided = "Confirm rule met: t >= 2 with at least 300 non-zero non-overlapping cases."
    elif t_val <= -2:
        status = "rejected"
        decided = "Reject rule met: t <= -2 with at least 300 non-zero non-overlapping cases (power tends to persist)."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: -2 < t < 2 with at least 300 non-zero cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean of (forecast/10) x (5-bar return minus coin mean 5-bar return)",
            "value": mean_val,
            "statistic": {"name": "ordinary t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": "confirm t >= 2, reject t <= -2, with at least 300 non-zero cases",
        },
        "supporting_check": None,
        "counts": {
            "non-overlapping cases where the forecast is not zero": n_nonzero,
            "non-overlapping cells": n_cells,
        },
        "decided_by": decided,
        "reading": "The mean and its t are taken over all non-overlapping 5-bar cells (zero-forecast cells contribute zero), with the coin's mean 5-bar return taken on the same grid over all its windows, while the 300 minimum counts only cells with a non-zero forecast.",
    }
