import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.fall30.last_history_value"

    # ---------- 1. Situation check: 30-day return negative -> short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # Rebuild the 30-bar return from prices, inside this window only.
            recomputed = close / close.shift(30) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw < 0) & (fc < 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    threshold_txt = ("confirm if t >= 2 and the supporting check is negative; "
                     "reject if t <= -2; minimum 100 independent forecast < 0 cases")
    main_name = "t of mean (forecast/10) x (3-bar return minus coin mean 3-bar return), forecast < 0 cases, pooled over coins"
    supp_name = "mean excess 3-bar return of deeper half (forecast below median) minus shallower half"

    if not passed:
        if agreement is None:
            decided = "No bar has a non-zero forecast, so the plan's falling-month short situation is never traded."
        else:
            decided = (f"Only {agreement:.1%} of active bars have a negative 30-bar return with a short forecast; "
                       f"the plan's situation needs 90 %.")
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": decided,
            "reading": "The situation is the raw fall30 value (30-bar return) below 0, recomputed from closes where the column is missing; the side is short.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append((fc[t], c1 / c0 - 1.0))
        if not coin_rows:
            continue
        arr = np.array(coin_rows, dtype=float)
        coin_mean = float(np.mean(arr[:, 1]))
        for f, r in arr:
            if np.isfinite(f) and f < 0:
                rows.append((f, r - coin_mean))

    n_cases = len(rows)
    counts = {"independent forecast < 0 cases": int(n_cases)}

    if n_cases < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": {"name": supp_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} independent forecast < 0 cases, below the plan's minimum of 100.",
            "reading": "The coin's mean 3-bar return is taken over all grid cases of all its windows; the median split is pooled over coins, with cases at the median in the shallower half.",
        }

    arr = np.array(rows, dtype=float)
    f = arr[:, 0]
    ex = arr[:, 1]
    gain = (f / 10.0) * ex
    mean_gain = float(np.mean(gain))
    sd = float(np.std(gain, ddof=1))
    t_stat = mean_gain / (sd / np.sqrt(n_cases)) if sd > 0 else float("nan")

    med = float(np.median(f))
    deep = ex[f < med]
    shallow = ex[f >= med]
    if len(deep) > 0 and len(shallow) > 0:
        supp_val = float(np.mean(deep) - np.mean(shallow))
        supp_pass = bool(supp_val < 0)
    else:
        supp_val = None
        supp_pass = None

    if np.isfinite(t_stat) and t_stat >= 2 and supp_pass is True:
        status = "confirmed"
        decided = f"t = {t_stat:.2f} >= 2 and the supporting check is negative ({supp_val:.5f})."
    elif np.isfinite(t_stat) and t_stat <= -2:
        status = "rejected"
        decided = f"t = {t_stat:.2f} <= -2: deeper falls are followed by higher-than-usual returns."
    else:
        status = "inconclusive"
        if np.isfinite(t_stat) and t_stat >= 2:
            decided = f"t = {t_stat:.2f} >= 2 but the supporting check is not negative ({supp_val})."
        else:
            decided = f"t = {t_stat:.2f} lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_gain,
            "statistic": {"name": "t of the mean", "value": float(t_stat) if np.isfinite(t_stat) else None},
            "threshold": threshold_txt,
        },
        "supporting_check": {"name": supp_name, "value": supp_val, "passed": supp_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "The coin's mean 3-bar return is taken over all grid cases of all its windows; the median split is pooled over coins, with cases at the median in the shallower half.",
    }
