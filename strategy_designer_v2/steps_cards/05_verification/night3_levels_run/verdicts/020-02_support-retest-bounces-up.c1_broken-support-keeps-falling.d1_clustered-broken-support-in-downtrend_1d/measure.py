import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    FC = "forecast"
    RAW = "debug_info.components.low_cluster.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce") if FC in df else pd.Series(np.nan, index=df.index)
            sma = close.rolling(50, min_periods=50).mean()
            below = close < sma
            if "regime" in df:
                reg_below = df["regime"].astype(str) == "mean_reversion"
                below = below.where(sma.notna(), reg_below)
            else:
                below = below.where(sma.notna(), False)
            if RAW in df:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            cluster = raw > 0  # at least one swing low at/above the close
            active = fc.notna() & (fc != 0)
            ok = active & below.astype(bool) & cluster & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("Situation = close below its 50-day SMA (recomputed from the window's closes, the recorded regime "
               "used on the first 49 bars of a window where the SMA cannot be rebuilt) and a positive raw "
               "low_cluster value, expected side short; cases are bets (short forecast magnitude rising >= 2 from its "
               "lowest level since the last bet, reset to 0 on flat/long), the first per 5-bar grid cell with a "
               "5-bar return inside the window; the larger half is |forecast| strictly above the cases' median, "
               "the smaller half at or below it.")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with the close below "
                           "its 50-day SMA and swing lows above it, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    unusual = []
    absf = []
    for coin, wins in bars.items():
        # coin's normal 5-bar drift over all windows, non-overlapping grid
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        if len(rets) == 0:
            continue
        drift = float(np.mean(rets))

        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            ref = 0.0
            seen_cells = set()
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi >= 0:
                    ref = 0.0
                    continue
                m = -fi
                if m - ref >= BAND:
                    ref = m
                    cell = i // H
                    if cell in seen_cells:
                        continue
                    if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                        seen_cells.add(cell)
                        r = c[i + H] / c[i] - 1.0
                        unusual.append(-(r - drift))
                        absf.append(abs(fi))
                else:
                    ref = min(ref, m)

    u = np.asarray(unusual, dtype=float)
    a = np.asarray(absf, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    supp_val = None
    n_hi = n_lo = 0
    if n_cases > 1:
        med = float(np.median(a))
        hi = u[a > med]
        lo = u[a <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            supp_val = float(np.mean(hi) - np.mean(lo))
    supp_pass = None if supp_val is None else bool(supp_val > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} independent short-bet cases ({n_cases}), the plan's minimum count."
    elif t_u is not None and mean_u > 0 and t_u >= 2 and supp_pass is True:
        status = "confirmed"
        decided = ("Confirm: mean unusual short-side move positive with t >= 2 over at least 30 cases, and the "
                   "larger-|forecast| half minus the smaller half is above 0.")
    elif t_u is not None and mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "Reject: mean unusual short-side move negative with t <= -2 over at least 30 cases."
    elif t_u is not None and mean_u > 0 and t_u >= 2:
        status = "inconclusive"
        decided = "Inconclusive: a confirming t whose supporting check is not above 0."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the t of the mean unusual short-side move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 5-bar short-side move over short bets",
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
            "threshold": "positive with t >= 2 over at least 30 cases to confirm; negative with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "larger-|forecast| half minus smaller half, mean unusual short move",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": {"cases": n_cases, "larger half": n_hi, "smaller half": n_lo},
        "decided_by": decided,
        "reading": reading,
    }
