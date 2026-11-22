import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    FC = "forecast"
    RAW = "debug_info.components.bounce.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            n = len(df)
            ret90 = np.full(n, np.nan)
            if n > 90:
                ret90[90:] = close[90:] / close[:-90] - 1.0
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            falling = np.where(np.isnan(ret90), regime == "mean_reversion", ret90 < 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(n, np.nan)
            r1 = np.full(n, np.nan)
            if n > 1:
                r1[1:] = close[1:] / close[:-1] - 1.0
            rise = np.where(np.isnan(raw), r1 > 0, raw > 0)
            active = np.nan_to_num(fc, nan=0.0) != 0
            n_active += int(active.sum())
            n_agree += int((active & falling & rise & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move of short cases, in the short direction",
                             "value": None, "statistic": None,
                             "threshold": "positive with t >= 2 confirms; negative with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars on an up day in a coin with a negative "
                           "90-day return, which the plan's situation requires."
                           if n_active > 0 else "The record has no active bars."),
            "reading": "The 90-day fall is computed from the window's prices where 90 bars exist, else read from the regime; a rise is a positive raw bounce value (or a positive one-day return where it is not recorded).",
        }

    # ---------- 2. Criterion ----------
    case_ret = []
    case_fc = []
    case_coin = []
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            for i in range(0, n - H, H):
                grid_rets.append(close[i + H] / close[i] - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            n = len(close)
            ref = 0.0
            bets = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f >= 0:
                    ref = 0.0
                    continue
                m = -f
                if m - ref >= BAND - 1e-9:
                    bets[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            for start in range(0, n, H):
                idx = np.where(bets[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if np.isnan(drift[coin]):
                    continue
                r = close[t + H] / close[t] - 1.0
                case_ret.append(-(r - drift[coin]))
                case_fc.append(fc[t])
                case_coin.append(coin)

    um = np.array(case_ret, dtype=float)
    cf = np.array(case_fc, dtype=float)
    n_cases = int(len(um))
    big = cf <= -10
    small = (cf > -10) & (cf <= -2)
    n_big = int(big.sum())
    n_small = int(small.sum())

    mean_um = float(np.mean(um)) if n_cases > 0 else None
    t_um = None
    if n_cases > 1:
        sd = np.std(um, ddof=1)
        t_um = float(mean_um / (sd / np.sqrt(n_cases))) if sd > 0 else None

    mean_big = float(np.mean(um[big])) if n_big > 0 else None
    mean_small = float(np.mean(um[small])) if n_small > 0 else None
    if mean_big is not None and mean_small is not None:
        diff = mean_big - mean_small
        sup_passed = bool(diff > 0)
    else:
        diff = None
        sup_passed = None

    counts = {"cases": n_cases, "cases at forecast -10 or below": n_big,
              "cases with forecast between -2 and -10": n_small}

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}), the plan's minimum count."
    elif n_big < 10:
        status = "not observable"
        decided = f"Fewer than 10 cases at forecast -10 or below ({n_big}), the plan's minimum count."
    elif t_um is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (zero dispersion)."
    elif mean_um > 0 and t_um >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the largest bounces are given back more."
        else:
            status = "inconclusive"
            decided = "A confirming t with a failed supporting check is inconclusive."
    elif mean_um < 0 and t_um <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: bounces in falling coins are followed by rises beyond the drift."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean unusual 5-bar move of short cases, in the short direction",
                         "value": mean_um,
                         "statistic": {"name": "t of the mean", "value": t_um} if t_um is not None else None,
                         "threshold": "positive with t >= 2 (and supporting check) confirms; negative with t <= -2 rejects; else inconclusive"},
        "supporting_check": {"name": "mean unusual move at forecast <= -10 minus that at forecast between -2 and -10",
                             "value": diff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first short bet (|forecast| rising >= 2 from its lowest short level since the last bet, reset at flat) "
                    "in each 5-bar grid cell of a window, judged on close[t+5]/close[t]-1 minus the coin's mean non-overlapping 5-bar return over all windows; "
                    "'between -2 and -10' is read as -10 < forecast <= -2."),
    }
