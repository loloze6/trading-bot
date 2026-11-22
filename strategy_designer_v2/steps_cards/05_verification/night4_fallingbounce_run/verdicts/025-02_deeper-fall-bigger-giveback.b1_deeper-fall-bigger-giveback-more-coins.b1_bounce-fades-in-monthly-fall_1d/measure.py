import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    POS = "postRebalance_current_allocation"
    R30 = "debug_info.components.fall30.last_history_value"

    # ---------- per coin: mean daily return over all its windows (pooled) ----------
    coin_drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp") if "timestamp" in df.columns else df
            c = pd.to_numeric(d["close"], errors="coerce").values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_drift[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check + case collection ----------
    n_active = 0
    n_evaluable = 0
    n_agree = 0
    n_active_regime_fallback = 0
    n_agree_regime_fallback = 0

    case_val = []
    case_fc = []
    case_adj = []

    for coin, wins in bars.items():
        drift = coin_drift.get(coin, np.nan)
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True) if "timestamp" in df.columns else df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))

            # raw components recomputed from prices inside the window
            r90 = close / close.shift(90) - 1.0
            r30_px = close / close.shift(30) - 1.0
            if R30 in d.columns:
                r30_rec = pd.to_numeric(d[R30], errors="coerce")
                r30 = r30_rec.where(r30_rec.notna(), r30_px)
            else:
                r30 = r30_px
            ret1 = close / close.shift(1) - 1.0
            vol_incl = ret1.rolling(20, min_periods=20).std()
            vol_excl = vol_incl.shift(1)
            jump_incl = ret1 / vol_incl
            jump_excl = ret1 / vol_excl

            active = fc != 0
            n_active += int(active.sum())

            jump_ok = (jump_incl >= 2.0) | (jump_excl >= 2.0)
            jump_known = jump_incl.notna() | jump_excl.notna()
            evaluable = r90.notna() & r30.notna() & jump_known
            situation = (r90 < 0) & (r30 < 0) & jump_ok
            side_ok = fc < 0

            ev = active & evaluable
            n_evaluable += int(ev.sum())
            n_agree += int((ev & situation & side_ok).sum())

            # fallback (only used if nothing is evaluable from prices)
            n_active_regime_fallback += int(active.sum())
            n_agree_regime_fallback += int((active & (regime == "mean_reversion") & side_ok).sum())

            # cases: mean_reversion bars with nonzero forecast
            pos = pd.to_numeric(d[POS], errors="coerce") if POS in d.columns else pd.Series(np.nan, index=d.index)
            nxt = close.shift(-1) / close - 1.0
            is_case = (regime == "mean_reversion") & active
            for i in np.where(is_case.values)[0]:
                p = pos.iloc[i]
                r = nxt.iloc[i]
                if not (np.isfinite(p) and np.isfinite(r) and np.isfinite(drift)):
                    continue
                adj = r - drift
                case_val.append(p * adj)
                case_fc.append(float(fc.iloc[i]))
                case_adj.append(adj)

    if n_evaluable > 0:
        agreement = n_agree / n_evaluable
    elif n_active_regime_fallback > 0:
        agreement = n_agree_regime_fallback / n_active_regime_fallback
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation check uses active bars where r90 (close/close 90 bars earlier within the window), r30 "
               "(recorded fall30 raw value, else from prices) and the jump (1-day return over the 20-day std of daily "
               "returns, accepted if >= 2 with the std either including or excluding today) can be computed, side short; "
               "cases are regime == mean_reversion bars with nonzero forecast and a next close in the same window, "
               "the drift is the coin's pooled mean daily return over all its windows, the correlation is Pearson between "
               "forecast and drift-adjusted next-day return, and the plan's 'fewer than 30 cases' minimum gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars evaluable": int(n_evaluable),
                       "cases": int(len(case_val))},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are bars with a negative 90-day return, "
                           "a negative 30-day return and a one-day rise of at least 2 usual moves with a short forecast."),
            "reading": reading,
        }

    vals = np.asarray(case_val, dtype=float)
    n = int(vals.size)
    mean = float(np.mean(vals)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    corr = None
    if n > 2:
        f = np.asarray(case_fc, dtype=float)
        a = np.asarray(case_adj, dtype=float)
        if np.std(f) > 0 and np.std(a) > 0:
            corr = float(np.corrcoef(f, a)[0, 1])
    corr_passed = None if corr is None else bool(corr > 0)

    if n < 30:
        status = "not observable"
        decided_by = f"Only {n} cases over all coins and windows, fewer than the plan's minimum of 30."
    elif t is not None and mean > 0 and t >= 2:
        if corr_passed:
            status = "confirmed"
            decided_by = "The main measure's mean is above 0 with t >= 2 and the forecast/return correlation is above 0."
        else:
            status = "inconclusive"
            decided_by = "A confirming t (mean > 0, t >= 2) but a correlation of 0 or less (or not computable)."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided_by = "The main measure's mean is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "The t of the main measure lies between -2 and 2 (or could not be computed)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean of position x (next-day return minus coin's mean daily return) over mean_reversion cases",
            "value": mean,
            "statistic": None if t is None else {"name": "t of the mean", "value": t},
            "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "correlation of forecast with next-day drift-adjusted return > 0",
            "value": corr,
            "passed": corr_passed,
        },
        "counts": {"cases": n},
        "decided_by": decided_by,
        "reading": reading,
    }
