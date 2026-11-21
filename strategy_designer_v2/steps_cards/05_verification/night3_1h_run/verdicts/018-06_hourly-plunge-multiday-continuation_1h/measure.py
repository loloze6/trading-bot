import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 120
    BAND = 2.0
    RAW = "debug_info.components.drop24.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                c = pd.to_numeric(df["close"], errors="coerce")
                raw = (c / c.shift(24) - 1.0) * 100.0
            situ = raw.notna() & (raw < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "ordinary t of mean strength of short cases over 120 bars (drift-adjusted, per usual 120-bar move)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are short bars with a negative 24-bar return, the plan's downside-drop situation on the short side.",
            "reading": "The adapted situation (graded size, while it holds) is read as a negative 24-bar return on the bar, expected side short.",
        }

    # ---------- 2. criterion ----------
    strengths = []
    absf = []
    for coin, wins in bars.items():
        # coin's normal drift and usual move: non-overlapping 120-bar returns, all windows pooled
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        rets = np.asarray(rets, dtype=float)
        if len(rets) < 2:
            continue
        drift = float(np.mean(rets))
        usual = float(np.std(rets, ddof=1))
        if not np.isfinite(usual) or usual <= 0:
            continue

        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(f)
            ref = 0.0
            seen_cells = set()
            for t in range(n):
                s = -f[t] if f[t] < 0 else 0.0
                is_bet = False
                if s <= 0:
                    ref = 0.0
                else:
                    if s - ref >= BAND:
                        is_bet = True
                        ref = s
                    else:
                        ref = min(ref, s)
                if not is_bet:
                    continue
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                strengths.append(-(r - drift) / usual)
                absf.append(abs(f[t]))

    strengths = np.asarray(strengths, dtype=float)
    absf = np.asarray(absf, dtype=float)
    n_cases = int(len(strengths))

    mean_s = float(np.mean(strengths)) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = float(np.std(strengths, ddof=1))
        t_val = float(mean_s / (sd / np.sqrt(n_cases))) if sd > 0 else None
    rho = None
    if n_cases >= 3 and np.std(absf) > 0 and np.std(strengths) > 0:
        rho = float(stats.spearmanr(absf, strengths).correlation)
        if not np.isfinite(rho):
            rho = None
    rho_passed = (rho > 0) if rho is not None else None

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases in total, fewer than the plan's minimum of 30."
    elif t_val is not None and mean_s > 0 and t_val >= 2 and rho_passed:
        status = "confirmed"
        decided = "Mean strength positive with t >= 2 over at least 30 cases and the rank correlation above 0."
    elif t_val is not None and mean_s < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean strength negative with t <= -2 over at least 30 cases."
    elif t_val is not None and t_val >= 2:
        status = "inconclusive"
        decided = "A confirming t with a rank correlation of 0 or below (or undefined)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_s,
            "statistic": {"name": "ordinary t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "Spearman of |forecast| at signal bar vs strength > 0",
            "value": rho,
            "passed": rho_passed,
        },
        "counts": {"cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": "The situation is a negative 24-bar return with a short forecast; a case is a deepening of the short forecast by at least 2 points from its shallowest level since the last bet (reset at flat), first one per 120-bar grid cell from each window's first row, dropped if its 120-bar return leaves the window; drift and usual move are the mean and sample std of each coin's non-overlapping 120-bar returns pooled over windows; fewer than 30 cases gives not observable per the workflow's minimum-count rule.",
    }
