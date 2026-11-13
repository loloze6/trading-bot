import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    RAW = "debug_info.components.range_top.last_history_value"

    # ---------- 1. Situation check ----------
    # Decide the scale of the raw Donchian value from its range alone:
    # centred at 0 if it ever goes negative, otherwise a 0..1 position.
    raw_min = np.inf
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if RAW in df.columns:
                v = pd.to_numeric(df[RAW], errors="coerce").min()
                if pd.notna(v):
                    raw_min = min(raw_min, v)
    raw_mid = 0.0 if raw_min < 0 else 0.5

    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            # 60-bar price change below 0. Use the prices where 60 earlier bars
            # exist in the window, and the detector's regime label otherwise.
            pe60 = close / close.shift(60) - 1
            reg_mr = (df["regime"].astype(str) == "mean_reversion") if "regime" in df.columns \
                else pd.Series(False, index=df.index)
            decline = pd.Series(np.where(pe60.notna(), pe60 < 0, reg_mr), index=df.index).astype(bool)

            # Close in the upper part of its 20-bar range.
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                upper = (raw > raw_mid).fillna(False)
            else:
                upper = pd.Series(False, index=df.index)

            active = fc.notna() & (fc != 0)
            situ = decline & upper & (fc < 0)  # the expected side is short
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 7-bar excess return of the coin after forecast <= -10 over its mean 7-bar return"
    thr = "confirm: mean < 0 with t <= -2 and share negative > 50%; reject: mean > 0 with t >= +2; at least 30 non-overlapping cases"
    reading = ("Non-overlapping cases are the grid bars at positions 0, 7, 14, ... of each window "
               "where forecast <= -10 and the bar 7 later is in the window. The coin's mean 7-bar return "
               "is taken on the same grid over all its windows. The excess over holding in the supporting "
               "check is that same return minus the coin mean. The 30-case minimum, if not reached, gives "
               "'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with the close "
                           "in the upper half of its 20-bar range while the 60-bar price change is below 0."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    excess = []
    for coin in bars:
        all_r = []
        case_r = []
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1
                all_r.append(r)
                if np.isfinite(fc[i]) and fc[i] <= -10:
                    case_r.append(r)
        if len(all_r) == 0 or len(case_r) == 0:
            continue
        m = float(np.mean(all_r))
        excess.extend([r - m for r in case_r])

    excess = np.array(excess, dtype=float)
    n_cases = int(len(excess))
    counts = {"non-overlapping cases": n_cases}

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    if n_cases >= 2:
        sd = float(np.std(excess, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else (0.0 if mean_ex == 0 else float(np.sign(mean_ex) * np.inf))
    else:
        t = None
    share = float(np.mean(excess < 0)) if n_cases > 0 else None

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases pooled over all coins and windows, fewer than the plan's minimum of 30."
        sup_pass = None
    else:
        sup_pass = bool(share > 0.5)
        if mean_ex < 0 and t <= -2 and sup_pass:
            status = "confirmed"
            decided = ("Confirm rule: the mean excess return is below 0 with t <= -2 on non-overlapping cases, "
                       "and the share of negative excess returns is above 50%.")
        elif mean_ex > 0 and t >= 2:
            status = "rejected"
            decided = "Reject rule: the mean excess return is above 0 with t >= +2 on non-overlapping cases."
        else:
            status = "inconclusive"
            if -2 < t < 2:
                decided = "Inconclusive rule: t lies between -2 and +2."
            else:
                decided = ("Neither rule met: t <= -2 but the share of negative excess returns is not above 50%, "
                           "so the result is inconclusive.")

    if t is not None and not np.isfinite(t):
        t = float(np.sign(t) * 1e12)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "share of cases with negative 7-bar excess return over holding",
            "value": share,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
