import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FALL_THRESHOLD = -10.0   # profile veto: 60-bar price evolution >= -10 (percent) -> chop
    RANGE_LONG = 20
    TREND_PERIOD = 60
    CASE_LEVEL = -2.0
    MIN_DAYS = 30

    def col(df, name):
        return df[name] if name in df.columns else pd.Series(np.nan, index=df.index)

    # ---------- per-coin drift (normal 1-bar drift over all windows together) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            r = (c.shift(-1) / c - 1.0).dropna()
            rets.append(r.values)
        allr = np.concatenate(rets) if rets else np.array([])
        drift[coin] = float(np.mean(allr)) if allr.size else np.nan

    n_active = 0
    n_agree = 0
    case_rows = []  # (day, coin, forecast, r_minus_drift)

    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            o = d["close"].astype(float)
            c = d["close"].astype(float)
            hi = d["high"].astype(float)
            lo = d["low"].astype(float)
            fc = pd.to_numeric(col(d, "forecast"), errors="coerce").fillna(0.0)
            regime = col(d, "regime").astype(str)

            # up day: close above prior close (within window)
            prev = c.shift(1)
            up = pd.Series(np.where(prev.notna(), (c > prev).astype(float), np.nan), index=d.index)

            # range multiple: recorded raw value where present, else from prices (mean incl. current bar)
            rng_rec = pd.to_numeric(col(d, "debug_info.components.width.last_history_value"), errors="coerce")
            bar_rng = hi - lo
            mean_rng = bar_rng.rolling(RANGE_LONG, min_periods=RANGE_LONG).mean()
            rng_px = bar_rng / mean_rng.replace(0, np.nan)
            rng = rng_rec.where(rng_rec.notna(), rng_px)
            wide = pd.Series(np.where(rng.notna(), (rng > 1.0).astype(float), np.nan), index=d.index)

            # falling market: 60-bar price evolution (percent) below -10
            evo = (c / c.shift(TREND_PERIOD) - 1.0) * 100.0
            falling = pd.Series(np.where(evo.notna(), (evo < FALL_THRESHOLD).astype(float), np.nan),
                                index=d.index)

            # fallback where prices of the window cannot give the value: the detector's own regime
            not_chop = (regime != "chop").astype(float)
            is_mr = (regime == "mean_reversion").astype(float)
            falling = falling.where(falling.notna(), not_chop)
            up = up.where(up.notna(), is_mr)
            wide = wide.where(wide.notna(), is_mr)

            situation = (falling > 0.5) & (up > 0.5) & (wide > 0.5)

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # cases: forecast <= -2, next-day return inside the window
            r_next = c.shift(-1) / c - 1.0
            dr = drift[coin]
            mask = (fc <= CASE_LEVEL) & r_next.notna()
            for i in np.where(mask.values)[0]:
                case_rows.append((ts.iloc[i].floor("D"), coin, float(fc.iloc[i]),
                                  float(r_next.iloc[i] - dr)))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement is not None and agreement >= 0.9) if n_active > 0 else None

    main_name = "mean next-day return minus drift, short direction, over forecast <= -2"
    threshold = "confirm: mean is a fall with day-clustered t >= 2 over >= 30 case-days; reject: t <= -2 over >= 30 case-days"
    reading = ("Falling market read as the config's profile (60-bar close change in percent below -10), with the bar's "
               "regime used only where a window lacks the bars to compute a condition; positive forecasts count as off "
               "side; cases are forecast <= -2 per the plan, drift is the coin's mean 1-bar return over all windows, "
               "the day-clustered t sums deviations per UTC day with a D/(D-1) factor, and the slope t is ordinary OLS "
               "across cases; fewer than 30 case-days gives 'not observable'.")

    if passed is False:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are falling-market up days with range above the "
                           "20-day mean range held short, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["day", "coin", "fc", "rd"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = None
    t_u = None
    slope = None
    t_slope = None
    if n_cases > 0:
        u = -cases["rd"].values
        mean_u = float(np.mean(u))
        dev = pd.Series(u - mean_u).groupby(cases["day"].values).sum().values
        D = len(dev)
        if D > 1:
            var = (D / (D - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
            t_u = float(mean_u / np.sqrt(var)) if var > 0 else None
        if n_cases >= 3 and np.std(cases["fc"].values) > 0:
            lr = stats.linregress(cases["fc"].values, cases["rd"].values)
            slope = float(lr.slope)
            t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    slope_pass = None
    if slope is not None and t_slope is not None:
        slope_pass = bool(slope > 0 and t_slope >= 1.0)
    elif n_cases > 0:
        slope_pass = False

    counts = {"cases": n_cases, "case-days": n_days, "active bars": int(n_active)}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} case-days, below the plan's minimum of 30 case-days."
    elif t_u is not None and mean_u > 0 and t_u >= 2.0 and slope_pass:
        status = "confirmed"
        decided = "The mean unusual move is a fall with t >= 2 over at least 30 case-days and the slope is positive with t >= 1."
    elif t_u is not None and mean_u < 0 and t_u <= -2.0:
        status = "rejected"
        decided = "The mean unusual move is a rise with t <= -2 over at least 30 case-days."
    else:
        status = "inconclusive"
        if t_u is not None and mean_u > 0 and t_u >= 2.0:
            decided = "The mean unusual move is a fall with t >= 2, but the supporting slope check fails."
        else:
            decided = "The t of the mean unusual move lies between -2 and 2 (any other result)."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": (True if passed is None else bool(passed))},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_u}
                                       if t_u is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "OLS slope of next-day return minus drift on forecast (positive, t >= 1)",
                             "value": t_slope if t_slope is not None else None,
                             "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
