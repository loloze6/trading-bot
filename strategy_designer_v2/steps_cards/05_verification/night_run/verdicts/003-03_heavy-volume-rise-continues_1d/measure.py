import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_CASES = 30
    RAW = "debug_info.components.vol_rise.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): the day's return in usual moves x relative volume, long side only.
    # The bar is in the situation when that graded measure is positive (an up day). The expected side is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            ret = close / close.shift(1) - 1.0
            # Recomputed from prices, used only where the raw column is missing.
            sd = ret.rolling(20, min_periods=20).std()
            vmean = vol.rolling(30, min_periods=30).mean()
            recomputed = ret / sd * (vol / vmean)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            raw = raw.where(raw.notna(), ret)  # last fallback: the sign of the day's return
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the mean 5-bar excess return (vs the coin's mean 5-bar return) on grid bars with forecast >= 5"
    threshold = ("confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; "
                 "reject: mean < 0 with t <= -2 over >= 30 cases")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in the situation on the long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on an up day "
                           "(positive volume-weighted scaled return), which the plan's situation requires."),
            "reading": "The situation is read as a positive raw component value (an up day), on the long side.",
        }

    # ---------- 2. Criterion ----------
    # Build non-overlapping grid samples per coin and window.
    per_coin = {}
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((c1 / c0 - 1.0, fc[i]))
        per_coin[coin] = rows

    excess_large = []
    sup_fc = []
    sup_ex = []
    for coin, rows in per_coin.items():
        if not rows:
            continue
        fwd = np.array([r[0] for r in rows], dtype=float)
        fcs = np.array([r[1] for r in rows], dtype=float)
        coin_mean = float(np.mean(fwd))
        ex = fwd - coin_mean
        ok = np.isfinite(fcs)
        large = ok & (fcs >= 5)
        excess_large.extend(ex[large].tolist())
        pos = ok & (fcs > 0)
        sup_fc.extend(fcs[pos].tolist())
        sup_ex.extend(ex[pos].tolist())

    excess_large = np.array(excess_large, dtype=float)
    n_large = int(len(excess_large))
    mean_ex = float(np.mean(excess_large)) if n_large > 0 else None
    if n_large >= 2:
        sd = float(np.std(excess_large, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n_large))) if sd > 0 else None
    else:
        t = None

    n_pos = int(len(sup_fc))
    rho = None
    if n_pos >= 3:
        r, _ = stats.spearmanr(sup_fc, sup_ex)
        rho = float(r) if np.isfinite(r) else None
    sup_passed = None if rho is None else bool(rho > 0)

    counts = {
        "grid cases with forecast >= 5": n_large,
        "grid bars with forecast > 0": n_pos,
    }

    if n_large < MIN_CASES:
        status = "not observable"
        decided_by = f"Fewer than 30 grid cases with forecast >= 5 ({n_large}), the plan's minimum count."
    elif t is not None and mean_ex > 0 and t >= 2:
        if sup_passed:
            status = "confirmed"
            decided_by = "The mean excess is positive with t >= 2 over at least 30 cases and the Spearman correlation is above 0."
        else:
            status = "inconclusive"
            decided_by = "A confirming t, but the supporting Spearman correlation is not above 0."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided_by = "The mean excess is negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided_by = "The t lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t is None else {"name": "t of the mean", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "Spearman(forecast, 5-bar excess) on grid bars with forecast > 0",
            "value": rho,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Grid bars are positions 0, 5, 10, ... of each window with t+5 inside the window. "
                    "The coin's mean 5-bar return is the mean over all of that coin's grid samples in all windows. "
                    "The plan's 'fewer than 30 cases' rule is reported as not observable."),
    }
