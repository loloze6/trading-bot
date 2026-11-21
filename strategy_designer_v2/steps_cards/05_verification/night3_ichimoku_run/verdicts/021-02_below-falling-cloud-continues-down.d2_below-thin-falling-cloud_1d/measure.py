import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 26
    TEN, KIJ, SEN, DISP, LB = 9, 26, 52, 26, 26
    FC = "forecast"

    # ---------- 1. situation check: recompute the regime rule from prices, per window ----------
    n_active = 0
    n_active_computable = 0
    n_agree = 0
    n_fallback_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            hi = d["high"].astype(float)
            lo = d["low"].astype(float)
            cl = d["close"].astype(float)
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            tenkan = (hi.rolling(TEN).max() + lo.rolling(TEN).min()) / 2.0
            kijun = (hi.rolling(KIJ).max() + lo.rolling(KIJ).min()) / 2.0
            span_a = ((tenkan + kijun) / 2.0).shift(DISP)
            span_b = ((hi.rolling(SEN).max() + lo.rolling(SEN).min()) / 2.0).shift(DISP)
            bottom = np.minimum(span_a, span_b)
            mid = (span_a + span_b) / 2.0
            slope = mid / mid.shift(LB) - 1.0
            computable = bottom.notna() & slope.notna()
            situ = (cl < bottom) & (slope < 0)
            active = fc != 0
            n_active += int(active.sum())
            ac = active & computable
            n_active_computable += int(ac.sum())
            n_agree += int((ac & situ & (fc < 0)).sum())
            if "regime" in d.columns:
                n_fallback_agree += int((active & (d["regime"] == "trending") & (fc < 0)).sum())

    used_fallback = False
    if n_active_computable > 0:
        agreement = n_agree / n_active_computable
    elif n_active > 0:
        used_fallback = True
        agreement = n_fallback_agree / n_active
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    reading_base = ("Situation recomputed from each window's own prices (Ichimoku 9/26/52, cloud at t = spans "
                    "computed at t-26, close below the lower span and cloud mid lower than 26 bars before), "
                    "agreement taken over active bars where it is computable"
                    + (" (none were, so the recorded regime 'trending' was used)" if used_fallback else "")
                    + "; the plan's 'fewer than 30 cases' is treated as its minimum count, giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars computable": int(n_active_computable)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with the close below "
                           "a falling cloud, as the plan's situation requires."
                           if agreement is not None else "The forecast is never non-zero, so no bar shows the plan's situation."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean 26-bar return on the non-overlapping grid of all its windows
    drift = {}
    cases = []  # (coin, abs forecast, raw return)
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            cl = d["close"].astype(float).values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            for i in range(0, len(d) - H, H):
                if not (np.isfinite(cl[i]) and np.isfinite(cl[i + H]) and cl[i] > 0):
                    continue
                r = cl[i + H] / cl[i] - 1.0
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    cases.append((coin, abs(float(fc[i])), r))
        drift[coin] = float(np.mean(allr)) if allr else np.nan

    vals, absf = [], []
    for coin, af, r in cases:
        if np.isfinite(drift.get(coin, np.nan)):
            vals.append(-(r - drift[coin]))
            absf.append(af)
    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    n = int(len(vals))

    mean = float(np.mean(vals)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    rho = None
    if n > 2 and np.std(absf) > 0 and np.std(vals) > 0:
        rr = stats.spearmanr(absf, vals).correlation
        rho = float(rr) if np.isfinite(rr) else None
    sup_pass = None if rho is None else bool(rho > 0)

    if n < 30:
        status = "not observable"
        decided = f"Only {n} non-overlapping cases, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no dispersion), meeting neither confirm nor reject."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Main t >= 2 with at least 30 cases and a Spearman correlation above 0 (confirm rule)."
    elif t <= -2:
        status = "rejected"
        decided = "Main t <= -2 with at least 30 cases: coins below a falling cloud rose more than their drift (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "Main t >= 2 but the Spearman correlation is 0 or below (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "Main t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean short-direction 26-bar return in excess of the coin's drift",
            "value": mean,
            "statistic": None if t is None else {"name": "ordinary t of the mean", "value": t},
            "threshold": "confirm if t >= 2 with >= 30 cases and Spearman > 0; reject if t <= -2 with >= 30 cases",
        },
        "supporting_check": {
            "name": "Spearman of |forecast| vs short-direction excess return",
            "value": rho,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping cases": n},
        "decided_by": decided,
        "reading": reading_base,
    }
