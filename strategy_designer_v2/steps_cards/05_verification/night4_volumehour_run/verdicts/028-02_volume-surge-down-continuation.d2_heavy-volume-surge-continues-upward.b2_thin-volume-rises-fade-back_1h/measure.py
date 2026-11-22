import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 4
    BAND = 2.0
    RAW = "debug_info.components.rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            # volume ratio: volume / mean of last 720 volumes (current included), inside the window
            vr = vol / vol.rolling(720, min_periods=720).mean()
            reg_thin = (df["regime"].astype(str) == "mean_reversion").values
            thin = np.where(vr.notna().values, (vr <= 1.0).values, reg_thin)
            # the hour's rise: raw component value, else the hour's return from the prices
            ret1 = (close / close.shift(1) - 1.0).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
                rise = np.where(np.isnan(raw), ret1 > 0, raw > 0)
            else:
                rise = ret1 > 0
            rise = np.where(np.isnan(ret1) & ~(RAW in df.columns), False, rise)
            active = fc != 0
            ok = active & thin.astype(bool) & rise.astype(bool) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean short-side unusual 4-bar return of short bets, pooled over coins"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; fewer than 100 cases: inconclusive/not observable"
    reading = ("Situation = raw rise component > 0 (or the hour's close-to-close return > 0 where unrecorded) and volume over its "
               "720-bar mean (current included, inside the window) <= 1, using the recorded regime on the first 719 bars of a window "
               "where that mean cannot be computed; a case is the first bar of each 4-bar grid cell (positions from the window's first row) "
               "where the short forecast's size rises by >= 2 from its smallest size since the last bet (from 0 after flat or a side change); "
               "drift is the coin's mean non-overlapping 4-bar return over all its windows; the minimum of 100 pooled cases maps to 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases pooled over coins and windows": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are thin-volume rising hours with a short forecast "
                           f"(agreement {agreement:.3f}), so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    vals = []
    absf = []
    for coin, wins in bars.items():
        # coin's drift: mean non-overlapping 4-bar return over all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            grid_rets.extend(list(r[np.isfinite(r)]))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(fc)
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f >= 0:
                    ref = 0.0
                    continue
                mag = -f
                if mag - ref >= BAND:
                    bet[i] = True
                    ref = mag
                else:
                    ref = min(ref, mag)
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                vals.append(-(r - drift))
                absf.append(abs(fc[i]))

    vals = np.asarray(vals, dtype=float)
    absf = np.asarray(absf, dtype=float)
    n_cases = int(len(vals))
    counts = {"cases pooled over coins and windows": n_cases}

    mean = float(np.mean(vals)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None
    slope = None
    if n_cases > 2 and np.ptp(absf) > 0:
        slope = float(stats.linregress(absf, vals).slope)

    main = {"name": main_name, "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": thr}
    slope_pass = None if slope is None else bool(slope > 0)
    supp = {"name": "OLS slope of short-side unusual return on |forecast|", "value": slope, "passed": slope_pass}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases pooled over coins and windows, fewer than the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean short-side unusual 4-bar return is above 0 with t >= 2 and the slope on |forecast| is above 0."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (mean > 0, t >= 2) but the supporting slope is <= 0, which the plan calls inconclusive."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean short-side unusual 4-bar return is below 0 with t <= -2: price rises more than drift after thin-volume rises."
    else:
        status = "inconclusive"
        decided = "The t of the mean lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
