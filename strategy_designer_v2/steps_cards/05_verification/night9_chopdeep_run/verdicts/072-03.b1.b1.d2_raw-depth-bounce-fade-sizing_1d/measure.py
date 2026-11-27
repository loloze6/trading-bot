import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    RAW = "debug_info.components.depth_swings.last_history_value"

    # ---------- 1. situation check ----------
    n_active_det = 0
    n_agree = 0
    n_active_total = 0
    n_active_fallback = 0
    n_agree_fallback = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            n = len(df)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active_total += 1
                below_high = np.isfinite(raw[t]) and raw[t] < 0
                short_side = f < 0
                if t >= 60:
                    up = close[t] / close[t - 1] - 1.0 > 0
                    r60 = (close[t] / close[t - 60] - 1.0) * 100.0
                    choppy = (r60 >= -10.0) and (r60 <= 10.0)
                    n_active_det += 1
                    if up and choppy and below_high and short_side:
                        n_agree += 1
                else:
                    # 60-day move not computable inside the window: fall back on the recorded regime
                    n_active_fallback += 1
                    up = (close[t] / close[t - 1] - 1.0 > 0) if t >= 1 else (regime[t] == "trending")
                    if up and regime[t] == "trending" and below_high and short_side:
                        n_agree_fallback += 1

    if n_active_det > 0:
        agreement = n_agree / n_active_det
    elif n_active_fallback > 0:
        agreement = n_agree_fallback / n_active_fallback
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    reading_check = ("Choppy is read as the 60-day close-to-close move within ±10 % (the veto's thresholds read as percent), "
                     "an up day as a positive one-day close return, below the high as a raw depth < 0, on bars with 60 bars "
                     "of in-window history (the recorded regime only if none have it)")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active_total, "active bars checked": n_active_det},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are up days in the choppy profile "
                           "(|60-day move| ≤ 10 %), closing below the 20-day high, with a short forecast."
                           if agreement is not None else "No active bars to check against the plan's situation."),
            "reading": reading_check + ".",
        }

    # ---------- 2. criterion ----------
    # coin drift: mean 10-day return over non-overlapping grid samples of all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, |forecast|)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            ref = 0.0
            used_cells = set()
            for t in range(n):
                f = fc[t]
                if f < 0:
                    mag = -f
                    if mag - ref >= BAND:
                        cell = t // H
                        if cell not in used_cells and t + H < n:
                            used_cells.add(cell)
                            r = c[t + H] / c[t] - 1.0
                            if np.isfinite(r):
                                cases.append((ts.iloc[t].floor("D"), -(r - drift[coin]), mag))
                        ref = mag
                    else:
                        ref = min(ref, mag)
                else:
                    ref = 0.0

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)

    mean_u = None
    t_stat = None
    diff = None
    if n_cases > 0:
        x = np.array([u for _, u, _ in cases])
        mean_u = float(x.mean())
        dser = pd.Series(x - mean_u, index=[d for d, _, _ in cases])
        s = dser.groupby(level=0).sum().values
        se = np.sqrt(np.sum(s ** 2)) / n_cases
        t_stat = float(mean_u / se) if se > 0 else None
        a = np.array([m for _, _, m in cases])
        med = np.median(a)
        deep = x[a > med]
        shallow = x[a <= med]
        if len(deep) > 0 and len(shallow) > 0:
            diff = float(deep.mean() - shallow.mean())

    sup_pass = (diff > 0) if diff is not None else None
    counts = {"cases": n_cases, "distinct days of cases": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct days of cases ({n_days})."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed (zero standard error)."
    elif t_stat >= 2 and mean_u > 0 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t ≥ 2 and the deeper half beats the shallower half."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move has t ≤ −2: prices rose more than the coin's drift after these up days."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t ≥ 2 but the deeper half does not beat the shallower half."
    else:
        status = "inconclusive"
        decided = "The t lies between −2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 10-day move in the short direction",
            "value": mean_u,
            "statistic": {"name": "t clustered by day", "value": t_stat} if t_stat is not None else None,
            "threshold": "confirm: mean > 0 with t ≥ 2; reject: t ≤ −2",
        },
        "supporting_check": {
            "name": "deeper half minus shallower half (median |forecast| at entry)",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": (reading_check + "; a case is a short bet (|forecast| rising ≥ 2 from its lowest short level since the last bet, "
                    "from 0 after flat), the first per 10-bar cell counted from each window's first row, needing 10 bars after it "
                    "in the window; the deeper half is |forecast| above the median and the shallower half at or below it; the "
                    "clustered t sums the deviations from the mean per UTC day."),
    }
