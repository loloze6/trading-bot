import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    LHV = "debug_info.components.scaled_rise.last_history_value"

    def is_rising(df):
        # The profile's own decision: the detector's regime; "chop" is the flat (non-rising) state.
        return df["regime"].astype(str) != "chop"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret3_price = close / close.shift(H) - 1.0  # inside this window only
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Scaled rise > 0 <=> 3-day return > 0; use raw value where recorded, else recompute from prices
            rise = np.where(raw.notna(), raw > 0, ret3_price > 0)
            rising = is_rising(df).values
            active = (fc.notna() & (fc != 0)).values
            agree = active & rising & rise & (fc > 0).values
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90 % of the forecast's active bars are long bars inside the rising profile "
                          "after a positive 3-day return, as the Fidelity's situation and side require.",
            "reading": "Rising profile read as regime not 'chop'; the scaled rise read from last_history_value, "
                       "recomputed as the 3-day price return where not recorded.",
        }

    # ---------- 2. Coin drift and usual move (non-overlapping 3-bar grid, all windows) ----------
    coin_stats = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(close)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        rets = np.array(rets)
        drift = float(np.mean(rets)) if len(rets) else np.nan
        usual = float(np.std(rets, ddof=1)) if len(rets) > 1 else np.nan
        coin_stats[coin] = (drift, usual)

    # ---------- 3. Main measure: OLS of excess 3-bar return on forecast, grid bars in rising profile ----------
    xs, ys = [], []
    n_pos_grid = 0
    strengths = []
    for coin, wins in bars.items():
        drift, usual = coin_stats[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            rising = is_rising(df).values
            n = len(df)
            for i in range(0, n - H, H):
                if not rising[i]:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not (np.isfinite(r) and np.isfinite(fc[i]) and np.isfinite(drift)):
                    continue
                xs.append(fc[i])
                ys.append(r - drift)
                if fc[i] > 0:
                    n_pos_grid += 1

            # ---------- Supporting check cases: long bets (rise of >= band), once per grid cell ----------
            ref = 0.0
            prev_pos = False
            bet_bars = []
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    ref = 0.0
                    prev_pos = False
                    continue
                if not prev_pos:
                    ref = 0.0
                prev_pos = True
                ref = min(ref, f)
                if f - ref >= BAND:
                    bet_bars.append(t)
                    ref = f
            seen_cells = set()
            for t in bet_bars:
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r) and np.isfinite(usual) and usual > 0:
                    strengths.append((r - drift) / usual)

    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    slope, tval = None, None
    if len(xs) >= 3 and np.var(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    strength = float(np.mean(strengths)) if len(strengths) else None
    check_passed = (strength > 0) if strength is not None else None

    counts = {
        "grid cases with forecast > 0": int(n_pos_grid),
        "grid cases in rising profile": int(len(xs)),
        "supporting check cases": int(len(strengths)),
    }

    main = {
        "name": "OLS slope of excess 3-bar forward return on forecast (rising-profile grid bars)",
        "value": slope,
        "statistic": {"name": "OLS t of slope", "value": tval} if tval is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2 and mean unusual move > 0; reject: slope < 0 with t <= -2",
    }
    supp = {
        "name": "mean unusual move (strength) of long cases",
        "value": strength,
        "passed": check_passed,
    }
    reading = ("Rising profile read as regime not 'chop'; excess return uses the coin's mean 3-bar return on the "
               "non-overlapping grid of all its windows; supporting-check cases are the workflow's long bets "
               "(forecast rise >= 2 points from its lowest level since the last bet), one per 3-bar grid cell, "
               "strength = (return - drift) / the coin's 3-bar std; the plan's 'fewer than 100 is inconclusive' "
               "minimum is reported as 'not observable' per the workflow.")

    sc = {"agreement": float(agreement) if agreement is not None else None, "passed": True}

    if n_pos_grid < 100:
        return {
            "status": "not observable",
            "situation_check": sc,
            "main_measure": main,
            "supporting_check": supp,
            "counts": counts,
            "decided_by": "Fewer than 100 grid cases with forecast > 0, pooled over coins and windows, the plan's minimum.",
            "reading": reading,
        }

    if slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if check_passed:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean unusual move of the forecast > 0 cases is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the mean unusual move is not above 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
