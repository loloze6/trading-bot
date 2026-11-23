import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.range_excess.last_history_value"

    def frame(df):
        d = df.copy()
        if "timestamp" in d.columns:
            d = d.sort_values("timestamp", kind="mergesort")
        return d.reset_index(drop=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            d = frame(bars[coin][w])
            if len(d) == 0:
                continue
            close = d["close"].astype(float)
            rng = (d["high"].astype(float) - d["low"].astype(float))
            fc = d["forecast"].astype(float).fillna(0.0)

            # closes lower: from prices; first bar of a window falls back to the recorded regime
            prev = close.shift(1)
            down = (close < prev)
            first_mask = prev.isna()
            if "regime" in d.columns:
                down = down.where(~first_mask, d["regime"].astype(str) == "mean_reversion")
            else:
                down = down.where(~first_mask, False)

            # range above its 30-day mean range (today included): from prices; when 30 bars are not
            # available in the window, fall back to the recorded raw component (negated compression > 0)
            mean30 = rng.rolling(30, min_periods=30).mean()
            excess = rng / mean30 - 1.0
            wide = excess > 0
            no_hist = mean30.isna()
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                fallback = (-raw > 0)
                wide = wide.where(~no_hist, fallback)
            else:
                wide = wide.where(~no_hist, False)

            active = fc != 0
            ok = active & down.astype(bool) & wide.astype(bool) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean unusual 3-bar move per case (3-bar return from signal close minus coin's normal 3-bar drift, long)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move, top third of entry forecast minus bottom third"
    reading = ("Cases are the first bet (forecast rise of >= 2 points on its side from its lowest level since the last bet) "
               "in each non-overlapping 3-bar cell counted from each window's first row, the normal drift is the coin's mean "
               "3-bar return on that grid over all its windows, thirds are split by rank of entry forecast (n//3 cases each), "
               "the plan's 'fewer than 30 cases' minimum is reported as not observable, and the situation is rebuilt from prices "
               "(falling back to the recorded regime / raw component where a window lacks the prior close or 30 bars).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars on a down close with a range above "
                           "its 30-bar mean, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_ret = []   # (coin, raw return, entry forecast)
    drift = {}
    for coin in sorted(bars):
        grid_rets = []
        for w in sorted(bars[coin]):
            d = frame(bars[coin][w])
            close = d["close"].astype(float).values
            n = len(close)
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0:
                    grid_rets.append(close[i + H] / close[i] - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for w in sorted(bars[coin]):
            d = frame(bars[coin][w])
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).fillna(0.0).values
            n = len(close)
            bets = np.zeros(n, dtype=bool)
            prev_side = 0
            low = 0.0
            for i in range(n):
                f = fc[i]
                side = int(np.sign(f))
                if side == 0:
                    prev_side = 0
                    low = 0.0
                    continue
                if side != prev_side:
                    low = 0.0
                a = abs(f)
                if a - low >= BAND - 1e-12:
                    if side > 0:
                        bets[i] = True
                    low = a
                else:
                    low = min(low, a)
                prev_side = side
            for c0 in range(0, n, H):
                idx = [j for j in range(c0, min(c0 + H, n)) if bets[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H])) or close[t] == 0:
                    continue
                case_ret.append((coin, close[t + H] / close[t] - 1.0, fc[t]))

    unusual = np.array([r - drift[c] for c, r, _ in case_ret if np.isfinite(drift[c])], dtype=float)
    entry = np.array([f for c, r, f in case_ret if np.isfinite(drift[c])], dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    k = n_cases // 3
    if k >= 1:
        order = np.argsort(entry, kind="mergesort")
        bottom = unusual[order[:k]]
        top = unusual[order[-k:]]
        sup_val = float(np.mean(top) - np.mean(bottom))
        sup_pass = bool(sup_val > 0)

    counts = {"cases": n_cases, "active bars": int(n_active)}
    base = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean", "value": t_u} if t_u is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "reading": reading,
    }

    if n_cases < 30:
        base["status"] = "not observable"
        base["decided_by"] = f"Only {n_cases} cases, below the plan's minimum of 30 cases in total."
        return base

    if mean_u is not None and t_u is not None and mean_u > 0 and t_u >= 2:
        if sup_pass:
            base["status"] = "confirmed"
            base["decided_by"] = "The mean unusual move is above 0 with t >= 2 and the top third beats the bottom third."
        else:
            base["status"] = "inconclusive"
            base["decided_by"] = "The mean unusual move is above 0 with t >= 2 but the supporting check fails."
    elif mean_u is not None and t_u is not None and mean_u < 0 and t_u <= -2:
        base["status"] = "rejected"
        base["decided_by"] = "The mean unusual move is below 0 with t <= -2."
    else:
        base["status"] = "inconclusive"
        base["decided_by"] = "The t of the mean unusual move lies between -2 and 2 (or is undefined)."
    return base
