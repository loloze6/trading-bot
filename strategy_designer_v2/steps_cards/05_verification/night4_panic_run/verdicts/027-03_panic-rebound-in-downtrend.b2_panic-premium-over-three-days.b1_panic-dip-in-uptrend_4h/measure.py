import json
import numpy as np
import pandas as pd
from scipy import stats


def _component_series(df, cid, field):
    col = f"debug_info.components.{cid}.{field}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"].values:
            val = np.nan
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(cid)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        val = float(x) if x is not None else np.nan
                    except Exception:
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def _bets(fc, band=2.0):
    """Long-side bets: a rise of the forecast of at least `band` from its lowest
    level on the long side since its last bet (from 0 after a flat or side change)."""
    n = len(fc)
    bet = np.zeros(n, dtype=bool)
    base = 0.0
    prev = 0.0
    for i in range(n):
        f = fc[i]
        if not np.isfinite(f):
            f = 0.0
        if f > 0:
            if prev <= 0:
                base = 0.0
            if f - base >= band:
                bet[i] = True
                base = f
            else:
                base = min(base, f)
        else:
            base = 0.0
        prev = f
    return bet


def measure(bars):
    H = 18
    RR_MAX = 0.3333

    n_active = 0
    n_agree = 0
    case_rows = []  # (excess, rise_ppv)

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # coin's normal 18-bar drift: non-overlapping grid of all windows together
        grid_rets = []
        for w in wins:
            df = wins[w]
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w in wins:
            df = wins[w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values

            # --- situation from prices and raw component values ---
            rng = (high - low) / close
            short_m = rng.rolling(6, min_periods=6).mean()
            long_m = rng.rolling(180, min_periods=180).mean()
            rr = long_m / short_m
            rr_ok = rr <= RR_MAX

            fall_raw = _component_series(df, "fall", "last_history_value")
            ret6 = close / close.shift(6) - 1.0
            fall_val = fall_raw.where(fall_raw.notna(), ret6)
            fall_ok = fall_val < 0

            rise_raw = _component_series(df, "rise", "last_history_value")
            prior_ret = close.shift(6) / close.shift(186) - 1.0
            prior_val = rise_raw.where(rise_raw.notna(), prior_ret)
            prior_ok = prior_val > 0

            computable = rr.notna() & fall_val.notna() & prior_val.notna()
            situation = rr_ok & fall_ok & prior_ok

            active = fc != 0
            m = active & computable.values
            n_active += int(m.sum())
            n_agree += int((m & situation.values & (fc > 0)).sum())

            # --- cases ---
            bet = _bets(fc)
            rise_ppv = _component_series(df, "rise", "post_pipeline_value").values
            c = close.values
            n = len(df)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                if not np.isfinite(drift):
                    continue
                ex = c[t + H] / c[t] - 1.0 - drift
                case_rows.append((ex, rise_ppv[t]))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation computed from prices with bar range = (high-low)/close and the ratio = 180-bar mean / 6-bar mean "
               "(<= 0.3333), using the recorded raw fall/rise values for the return signs where present, bars where it "
               "cannot be computed (window start) left out of the agreement; cases are long bets (rise >= 2 from the lowest "
               "long level since the last bet), the first per 18-bar cell of each window, and fewer than 30 cases is "
               "'not observable'.")

    main_name = "mean 18-bar excess return per case (over coin's normal drift)"
    thr = "confirm t >= 2 with slope > 0; reject t <= -2 or slope t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": len(case_rows), "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's panic "
                           "situation (24h range >= 3x its 30-day mean, 24h fall, prior 30-day rise)."),
            "reading": reading,
        }

    ex = np.array([r[0] for r in case_rows], dtype=float)
    xs = np.array([r[1] for r in case_rows], dtype=float)
    n_cases = int(len(ex))

    mean_ex = float(np.mean(ex)) if n_cases > 0 else None
    t_mean = None
    if n_cases > 1:
        sd = float(np.std(ex, ddof=1))
        t_mean = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    ok = np.isfinite(xs) & np.isfinite(ex)
    slope = None
    slope_t = None
    n_reg = int(ok.sum())
    if n_reg >= 3 and np.std(xs[ok]) > 0:
        lr = stats.linregress(xs[ok], ex[ok])
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            slope_t = float(lr.slope / lr.stderr)
    slope_pass = (slope > 0) if slope is not None else None

    counts = {"cases": n_cases, "cases with rise value": n_reg}
    stat = {"name": "t of the mean", "value": t_mean} if t_mean is not None else None
    supp = {"name": "slope of excess return on rise post_pipeline_value", "value": slope,
            "passed": slope_pass}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases across all coins and windows, below the plan's minimum of 30."
    elif t_mean is not None and t_mean >= 2 and slope_pass is True:
        status = "confirmed"
        decided = "The mean excess return has t >= 2 and the slope on rise is above 0."
    elif (t_mean is not None and t_mean <= -2) or (slope_t is not None and slope_t <= -2):
        status = "rejected"
        decided = "The mean excess return has t <= -2, or the slope on rise has t <= -2."
    else:
        status = "inconclusive"
        decided = "Neither the confirm rule (t >= 2 and slope > 0) nor the reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": main_name, "value": mean_ex, "statistic": stat, "threshold": thr},
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
