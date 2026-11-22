import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.vol_surge.last_history_value"

    # ---------- 1. situation check: volume above its 180-bar mean (raw ratio - 1 > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            # recomputed from prices where the component is not recorded
            recomputed = vol / vol.rolling(180, min_periods=180).mean() - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess 18-bar return of bet cases (return minus coin's normal 18-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Situation is the raw component (volume ratio minus 1) above 0 with a positive forecast; a case is the first bar "
               "of each non-overlapping 18-bar grid cell (from each window's first row) where the forecast rises on its side by "
               ">= 2 points from its lowest level since its last bet (from 0 after flat or a side change), and the excess is the "
               "raw 18-bar return minus the coin's mean non-overlapping 18-bar return over all its windows, not sign-adjusted; "
               "the plan's 'fewer than 30 cases' is treated as the minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("Only %.1f%% of active bars are bars with volume above its 180-bar mean on the long side, below the 90%% "
                           "the plan's Fidelity (long only on above-average volume) requires." % (100 * agreement)),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_ret = []
    case_fc = []
    case_coin = []
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(df)
            # drift grid
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
            # bets
            side = 0
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                s = int(np.sign(f))
                if s == 0:
                    side = 0
                    low = 0.0
                    continue
                if s != side:
                    side = s
                    low = 0.0
                mag = abs(f)
                if mag - low >= BAND:
                    bet[i] = True
                    low = mag
                else:
                    low = min(low, mag)
            # one case per grid cell
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                coin_cases.append((c1 / c0 - 1.0, fc[i]))
        drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) else np.nan
        for r, f in coin_cases:
            if np.isfinite(drift[coin]):
                case_ret.append(r - drift[coin])
                case_fc.append(f)
                case_coin.append(coin)

    x = np.asarray(case_ret, dtype=float)
    fcs = np.asarray(case_fc, dtype=float)
    n_cases = int(len(x))

    mean = float(np.mean(x)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(x, ddof=1))
        t = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None
    rho = None
    if n_cases > 2 and np.std(fcs) > 0 and np.std(x) > 0:
        r = stats.spearmanr(fcs, x).correlation
        rho = float(r) if np.isfinite(r) else None
    rho_pass = None if rho is None else bool(rho > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = "Only %d independent cases, fewer than the plan's minimum of 30." % n_cases
    elif t is not None and mean > 0 and t >= 2 and rho_pass:
        status = "confirmed"
        decided = "Mean excess return above 0 with t >= 2 over at least 30 cases, and the Spearman correlation is above 0."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2 over at least 30 cases."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the Spearman correlation is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 (or undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "ordinary t of the mean", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "Spearman(forecast at signal bar, excess 18-bar return) > 0",
                             "value": rho, "passed": rho_pass},
        "counts": {"cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
