import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RISE = "debug_info.components.rise.last_history_value"
    BAND = 2.0
    H = 1

    def to_day(ts):
        s = pd.Series(ts)
        if np.issubdtype(s.dtype, np.number):
            unit = "ms" if s.abs().max() > 1e11 else "s"
            t = pd.to_datetime(s, unit=unit, utc=True)
        else:
            t = pd.to_datetime(s, utc=True)
        return t.dt.strftime("%Y-%m-%d").values

    # ---------- coin drift: mean daily return over all windows ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    n_active = 0
    n_agree = 0
    case_vals = []   # short-direction excess
    case_excess = []  # raw excess (unflipped)
    case_rise = []
    case_days = []

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            # raw scaled rise: recorded value, else recomputed from prices inside the window
            r1 = close.pct_change()
            vol = r1.rolling(30, min_periods=30).std(ddof=1)
            vsr_px = (r1 / vol).replace([np.inf, -np.inf], np.nan)
            if RISE in df.columns:
                rec = pd.to_numeric(df[RISE], errors="coerce")
                vsr = rec.where(rec.notna(), vsr_px).values
            else:
                vsr = vsr_px.values
            days = to_day(df["timestamp"])
            c = close.values

            # situation check
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                v = vsr[i]
                in_sit = (np.isfinite(v) and 0.0 <= v <= 1.0 and regime[i] != "chop")
                if in_sit and fc[i] < 0:
                    n_agree += 1

            # cases: bets (rise of the forecast on its side of at least the band), short side
            side, base = 0, 0.0
            for i in range(len(df)):
                f = fc[i]
                if f == 0:
                    side, base = 0, 0.0
                    continue
                s = 1 if f > 0 else -1
                m = abs(f)
                if s != side:
                    side, base = s, 0.0
                if m - base >= BAND:
                    base = m
                    is_bet = True
                else:
                    base = min(base, m)
                    is_bet = False
                if not is_bet or s != -1:
                    continue
                if i + H >= len(df):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                ex = r - drift[coin]
                if not np.isfinite(ex):
                    continue
                case_excess.append(ex)
                case_vals.append(-ex)
                rv = pd.to_numeric(df[RISE], errors="coerce").values[i] if RISE in df.columns else np.nan
                case_rise.append(rv)
                case_days.append(days[i])

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    threshold = "confirm: mean > 0 with t >= 2 and slope < 0; reject: mean < 0 with t <= -2"
    reading = ("Agitation is read from the recorded regime (not 'chop', the profile veto) since the 365-day volatility "
               "percentile cannot be rebuilt inside a window, the scaled rise from last_history_value or else from window "
               "prices; cases are the short-side bets of the forecast (rise of at least 2 points from its lowest level since "
               "the last bet) on every bar with a next-day close in the same window; the day-clustered t uses per-day "
               "summed deviations with a G/(G-1) correction; the slope is the OLS of the unflipped excess return on the raw rise; "
               "the plan's 'fewer is inconclusive' minimum is reported as 'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean next-day excess return, short direction", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars in an agitated market with a scaled rise "
                           "between 0 and 1, so the forecast does not act on the plan's situation and side."),
            "reading": reading,
        }

    vals = np.array(case_vals, dtype=float)
    n = len(vals)
    dser = pd.Series(case_days)
    n_days = int(dser.nunique()) if n else 0

    mean = float(np.mean(vals)) if n else None
    t = None
    if n >= 2:
        dev = vals - vals.mean()
        sums = pd.Series(dev).groupby(dser.values).sum().values
        G = len(sums)
        if G > 1:
            se = np.sqrt(G / (G - 1) * np.sum(sums ** 2)) / n
            t = float(mean / se) if se > 0 else None

    ex = np.array(case_excess, dtype=float)
    rz = np.array(case_rise, dtype=float)
    ok = np.isfinite(ex) & np.isfinite(rz)
    slope = None
    if ok.sum() >= 3 and np.std(rz[ok]) > 0:
        slope = float(stats.linregress(rz[ok], ex[ok]).slope)
    slope_pass = (slope < 0) if slope is not None else None

    counts = {"cases": int(n), "distinct days": n_days}

    if n < 200 or n_days < 150:
        status = "not observable"
        decided = f"The plan's minimum of 200 cases on 150 distinct days is not reached ({n} cases, {n_days} days)."
    elif t is not None and mean > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "The main mean is positive with t >= 2 and the supporting slope is below 0 (confirm rule)."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The main mean is negative with t <= -2 (reject rule): ordinary rises continue more than the drift."
    else:
        status = "inconclusive"
        if t is not None and mean > 0 and t >= 2:
            decided = "The main t is >= 2 but the supporting slope is at or above 0 (inconclusive rule)."
        else:
            decided = "The main t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean next-day excess return over drift, short direction",
                         "value": mean,
                         "statistic": ({"name": "t, cases of one day taken together", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "OLS slope of next-day excess return on raw scaled rise",
                             "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
