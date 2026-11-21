import numpy as np
import pandas as pd


def measure(bars):
    H = 8
    BAND = 2.0
    RAW = "debug_info.components.move2h.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            r1 = close.pct_change()
            vol24 = r1.rolling(24, min_periods=24).std()
            vol_avg = vol24.rolling(720, min_periods=720).mean()
            ratio = vol24 / vol_avg
            high_vol = ratio >= 1.0
            # where the ratio cannot be rebuilt inside the window (warm-up cut), use the recorded regime
            fallback = df["regime"].astype(str) == "mean_reversion" if "regime" in df else pd.Series(False, index=df.index)
            high_vol = high_vol.where(ratio.notna(), fallback)
            if RAW in df.columns:
                move = df[RAW].astype(float)
            else:
                move = pd.Series(np.nan, index=df.index)
            move = move.where(move.notna(), close.pct_change(2))
            expected_side = -np.sign(move)
            active = fc != 0
            agree = active & high_vol.astype(bool) & (np.sign(fc) == expected_side) & (expected_side != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "mean unusual 8-bar move of cases, signed in the forecast's direction"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"independent cases": None, "active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars are high-volatility bars (24-bar vol >= its 720-bar average) "
                          "with a forecast opposite to the 2-bar move, as the plan's Fidelity states.",
            "reading": "Situation taken as 24-bar vol of 1-bar returns at or above its 720-bar mean (recorded regime where "
                       "warm-up prevents a rebuild) with the forecast's sign opposite to the raw 2-bar scaled move.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, signed_dir, ret, |forecast|)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            close = df["close"].astype(float).to_numpy()
            n = len(close)
            for p in range(0, n - H, H):
                if close[p] > 0 and np.isfinite(close[p]) and np.isfinite(close[p + H]):
                    grid_rets.append(close[p + H] / close[p] - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, df in wins.items():
            close = df["close"].astype(float).to_numpy()
            fc = df["forecast"].astype(float).fillna(0.0).to_numpy()
            n = len(close)
            side = 0
            low = 0.0
            used_cells = set()
            for t in range(n):
                f = fc[t]
                s = int(np.sign(f))
                if s == 0:
                    side, low = 0, 0.0
                    continue
                if s != side:
                    side, low = s, 0.0
                a = abs(f)
                if a - low >= BAND - 1e-12:
                    low = a
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H < n and close[t] > 0 and np.isfinite(close[t]) and np.isfinite(close[t + H]) \
                            and np.isfinite(drift[coin]):
                        r = close[t + H] / close[t] - 1.0
                        cases.append((s * (r - drift[coin]), a))
                else:
                    low = min(low, a)

    n_cases = len(cases)
    reading = ("A case is the first bet (forecast rise of >= 2 points on its side from its lowest level since the last bet) "
               "in each 8-bar grid cell counted from each window's first row, with its 8-bar return inside the window; "
               "normal drift is the coin's mean grid 8-bar return over all its windows; the supporting check splits cases "
               "strictly above versus strictly below the median |forecast|; the plan's 'fewer than 100 independent cases' "
               "is applied as the minimum count (not observable).")

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"independent cases": 0},
            "decided_by": "Fewer than 100 independent cases in total (none).",
            "reading": reading,
        }

    u = np.array([c[0] for c in cases], dtype=float)
    a = np.array([c[1] for c in cases], dtype=float)
    mean_u = float(np.mean(u))
    sd = float(np.std(u, ddof=1)) if n_cases > 1 else np.nan
    t_stat = float(mean_u / (sd / np.sqrt(n_cases))) if (n_cases > 1 and sd > 0) else np.nan

    med = float(np.median(a))
    hi = u[a > med]
    lo = u[a < med]
    if len(hi) > 0 and len(lo) > 0:
        diff = float(np.mean(hi) - np.mean(lo))
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = False

    counts = {"independent cases": int(n_cases),
              "cases above median |forecast|": int(len(hi)),
              "cases below median |forecast|": int(len(lo))}

    if n_cases < 100:
        status = "not observable"
        decided = f"Fewer than 100 independent cases in total ({n_cases})."
    elif np.isfinite(t_stat) and mean_u > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move > 0 with t >= 2, and the supporting check passes."
    elif np.isfinite(t_stat) and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move < 0 with t <= -2."
    elif np.isfinite(t_stat) and t_stat >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": {"name": "t of the mean",
                                       "value": (t_stat if np.isfinite(t_stat) else None)},
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move above minus below median |forecast|",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
