import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.dip_in_rise.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            regime = df["regime"].astype(str).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            n = len(df)
            prev_close = np.r_[np.nan, close[:-1]]
            close_168 = np.r_[np.full(min(168, n), np.nan), close[:-168]] if n > 168 else np.full(n, np.nan)
            for i in range(n):
                if fc[i] == 0:
                    continue
                n_active += 1
                # Regime: volume within 0.67..1.5 of its 720-bar mean (the detector's decision)
                in_band = regime[i] == "mean_reversion"
                # Raw component: fall size x positive 168-bar return, > 0 only on a dip in a rise
                raw_ok = np.isfinite(raw[i]) and raw[i] > 0
                # Price cross-checks where computable inside the window
                fall_ok = True
                if np.isfinite(prev_close[i]) and np.isfinite(close[i]):
                    fall_ok = close[i] < prev_close[i]
                rise_ok = True
                if np.isfinite(close_168[i]) and np.isfinite(close[i]):
                    rise_ok = close[i] / close_168[i] - 1 > 0
                side_ok = fc[i] > 0
                if in_band and raw_ok and fall_ok and rise_ok and side_ok:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 6-bar move of long bets (return minus coin's mean 6-bar return)"
    threshold = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; fewer than 30 cases inconclusive"
    reading = ("Situation = regime 'mean_reversion' (volume band) with raw dip_in_rise > 0, a falling close and a positive "
               "168-bar return where computable in the window, on a positive forecast; a case is the first bet "
               "(forecast rise >= 2 from its lowest long level since the last bet) in each 6-bar grid cell from each "
               "window's first row; drift is the coin's mean 6-bar grid return over all its windows; the plan's "
               "'fewer than 30 cases' is treated as the minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of active-forecast bars are long bars of the plan's situation (quiet-volume "
                           "falling hour within a positive 168-bar return): the config's forecast does not follow the Fidelity."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    case_fc = []
    case_unusual = []
    case_coin = []
    for coin, wins in bars.items():
        # drift: mean 6-bar return over all windows' grids
        grid_rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(close) - H, H):
                r = close[i + H] / close[i] - 1
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            ref = 0.0
            prev = 0.0
            used_cells = set()
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                    prev = f
                    continue
                if prev <= 0:
                    ref = 0.0
                bet = (f - ref) >= BAND
                if bet:
                    ref = f
                else:
                    ref = min(ref, f)
                prev = f
                if not bet:
                    continue
                cell = i // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1
                if not np.isfinite(r):
                    continue
                case_fc.append(float(f))
                case_unusual.append(float(r - drift))
                case_coin.append(coin)

    x = np.array(case_unusual, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n_cases = int(len(x))
    counts = {"cases": n_cases}
    for c in bars.keys():
        counts["cases " + str(c)] = int(sum(1 for k in case_coin if k == c))

    mean = float(np.mean(x)) if n_cases > 0 else None
    tval = None
    if n_cases >= 2:
        sd = float(np.std(x, ddof=1))
        if sd > 0:
            tval = float(mean / (sd / np.sqrt(n_cases)))
    corr = None
    if n_cases >= 3 and np.std(fcs) > 0 and np.std(x) > 0:
        corr = float(stats.pearsonr(fcs, x)[0])
    check_passed = (corr is not None and corr > 0)

    main = {"name": main_name, "value": mean,
            "statistic": ({"name": "t of the mean", "value": tval} if tval is not None else None),
            "threshold": threshold}
    support = {"name": "correlation of signal forecast with unusual move > 0", "value": corr,
               "passed": bool(check_passed) if corr is not None else False}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero spread), meeting neither rule."
    elif mean > 0 and tval >= 2 and check_passed:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and a positive forecast/move correlation (confirm rule)."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 (reject rule)."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting correlation check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
