import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    RAW = "debug_info.components.streak_loss.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            raw = pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns \
                else np.full(len(df), np.nan)
            regime = df["regime"].astype(str).values if "regime" in df.columns \
                else np.array([""] * len(df))
            n = len(df)
            for t in range(n):
                if f[t] == 0:
                    continue
                n_active += 1
                # 180-bar return regime condition, recomputed from prices when possible
                if t >= 180 and np.isfinite(close[t]) and np.isfinite(close[t - 180]) and close[t - 180] > 0:
                    up_regime = (close[t] / close[t - 180] - 1.0) > 0
                else:
                    up_regime = regime[t] == "mean_reversion"
                in_streak = np.isfinite(raw[t]) and raw[t] > 0
                if up_regime and in_streak and f[t] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    threshold_txt = "confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Bets are long forecast rises of at least 2 points from the lowest positive forecast since the last bet "
               "(reset to 0 when the forecast is not positive), the first bet of each 18-bar grid cell counted from each "
               "window's first row is the case, the normal drift is the mean 18-bar return on each coin's non-overlapping "
               "grid over all its windows, the median split puts cases with entry forecast above the median in the top half "
               "and the rest in the bottom half, and the 180-bar regime is recomputed from closes where 180 bars exist in "
               "the window and taken from the recorded regime otherwise.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside a down streak "
                           "(positive raw streak loss) with a positive 180-bar return, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    unusual = []
    entry_f = []
    for coin, wins in bars.items():
        # normal drift: mean 18-bar return on non-overlapping grid over all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            ref = 0.0
            seen_cells = set()
            for t in range(n):
                ft = f[t]
                if ft <= 0:
                    ref = 0.0
                    continue
                if ft - ref >= BAND:
                    ref = ft
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                        r = c[t + H] / c[t] - 1.0
                        unusual.append(r - drift)
                        entry_f.append(ft)
                else:
                    ref = min(ref, ft)

    u = np.array(unusual, dtype=float)
    ef = np.array(entry_f, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_top = n_bot = 0
    if n_cases > 1:
        med = float(np.median(ef))
        top = u[ef > med]
        bot = u[ef <= med]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            sup_val = float(np.mean(top) - np.mean(bot))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {
        "name": "mean unusual 18-bar move of long bets",
        "value": mean_u,
        "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
        "threshold": threshold_txt,
    }
    supporting = {"name": "top-half minus bottom-half mean unusual move (median entry forecast split)",
                  "value": sup_val, "passed": sup_pass}
    counts = {"cases": n_cases, "top half cases": n_top, "bottom half cases": n_bot}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_u is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither rule is met."
    elif mean_u > 0 and t_u >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 over at least 30 cases and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is positive with t >= 2 but the supporting check fails."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
