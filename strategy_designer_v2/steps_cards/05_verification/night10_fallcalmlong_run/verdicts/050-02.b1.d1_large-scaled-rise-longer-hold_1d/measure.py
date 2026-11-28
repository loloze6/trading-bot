import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    LHV = "debug_info.components.scaled_week_rise.last_history_value"

    def ts_day(s):
        t = pd.to_datetime(s, utc=True, errors="coerce")
        return t.dt.strftime("%Y-%m-%d")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            regime = df["regime"].astype(str).values
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # fallback: 7-day return sign recomputed from prices inside the window
            r7 = np.full(len(df), np.nan)
            if len(df) > 7:
                r7[7:] = close[7:] / close[:-7] - 1.0
            rise = np.where(np.isnan(raw), r7 > 0, raw > 0)
            # falling calm profile = neither veto fired -> regime "unknown"
            profile = regime == "unknown"
            situ = profile & rise
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = None

    if passed is False:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the falling calm "
                           "profile (regime 'unknown') with a positive scaled 7-day rise, as the Fidelity requires."),
            "reading": ("The falling calm profile is read from the recorded regime ('unknown' = neither veto fired); "
                        "the scaled rise from last_history_value, or the 7-day return from close where missing."),
        }

    # ---------- 2. criterion ----------
    cases = []
    for coin in sorted(bars):
        drifts = []
        per_win = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            days = ts_day(df["timestamp"]).values
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                drifts.append(r)
                per_win.append((r, f[i], days[i]))
        if not drifts:
            continue
        drift = float(np.mean(drifts))
        for r, fv, d in per_win:
            if np.isfinite(fv) and fv > 0:
                cases.append((coin, d, float(fv), r - drift))

    n_cases = len(cases)
    n_days = len(set(c[1] for c in cases))
    counts = {"independent cases (grid bars with forecast > 0)": int(n_cases),
              "days the cases fall on": int(n_days)}

    reading = ("The falling calm profile is read from the recorded regime ('unknown' = neither veto fired); grid "
               "bars without a 10-bar forward close in the window are dropped and drift is each coin's mean 10-bar "
               "grid return over all its windows; the weighted mean's t is a day-clustered standard error "
               "(per-day sums of f*(excess-mean), scaled by G/(G-1)); the thirds are floor(n/3) cases by forecast "
               "with unweighted mean excess.")

    mm_name = "forecast-weighted mean excess 10-bar return"
    mm_thr = "above 0 with t >= 2 confirms; below 0 with t <= -2 rejects"

    if n_cases < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None if agreement is None else float(agreement),
                                "passed": passed},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": {"name": "top-third minus bottom-third mean excess", "value": None,
                                 "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 30 independent cases (grid bars with forecast > 0): the plan's minimum is not reached.",
            "reading": reading,
        }

    fv = np.array([c[2] for c in cases])
    ex = np.array([c[3] for c in cases])
    dy = np.array([c[1] for c in cases])
    m = float(np.sum(fv * ex) / np.sum(fv))

    contrib = pd.Series(fv * (ex - m)).groupby(dy).sum().values
    G = len(contrib)
    if G > 1:
        var = (G / (G - 1)) * np.sum(contrib ** 2) / (np.sum(fv) ** 2)
        se = float(np.sqrt(var))
        t = float(m / se) if se > 0 else 0.0
    else:
        t = 0.0

    order = np.argsort(fv, kind="mergesort")
    k = n_cases // 3
    bottom = ex[order[:k]]
    top = ex[order[n_cases - k:]]
    diff = float(np.mean(top) - np.mean(bottom)) if k > 0 else None
    sup_pass = (diff is not None) and diff > 0

    if m > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The forecast-weighted mean excess is above 0 with t >= 2 and the top-minus-bottom-third difference is above 0."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the top-minus-bottom-third check fails, which the plan calls inconclusive."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the forecast-weighted mean excess lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement),
                            "passed": passed},
        "main_measure": {"name": mm_name, "value": m,
                         "statistic": {"name": "t of the weighted mean, cases of one day pooled", "value": t},
                         "threshold": mm_thr},
        "supporting_check": {"name": "top-third minus bottom-third mean excess (by forecast)",
                             "value": diff, "passed": bool(sup_pass)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
