import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    BAND = 2.0
    THR = -2.0
    COMP = "scaled_fall"
    LHV = "debug_info.components.%s.last_history_value" % COMP

    def to_time(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            med = np.nanmedian(np.abs(v.values)) if len(v) else 0
            unit = "ms" if med > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    def recorded_raw(df):
        if LHV in df.columns:
            return pd.to_numeric(df[LHV], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for x in df["debug_info.components"].values:
                val = np.nan
                try:
                    if isinstance(x, dict) and COMP in x and isinstance(x[COMP], dict):
                        v = x[COMP].get("last_history_value")
                        if v is not None:
                            val = float(v)
                except Exception:
                    val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    def z14_from_prices(close):
        r = close.pct_change()
        sd = r.rolling(30, min_periods=30).std()
        ret14 = close / close.shift(14) - 1.0
        denom = sd * np.sqrt(14.0)
        z = ret14 / denom
        z[(denom == 0) | ~np.isfinite(z)] = np.nan
        return z

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            raw = recorded_raw(df)
            zp = z14_from_prices(close)
            z = raw.where(raw.notna(), zp)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & (z <= THR + 1e-9) & (fc < 0)).sum())
            prepared[(coin, w)] = (df, close, fc)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-signed 7-day unusual move after short signals"
    threshold = "confirm: mean > 0 with t >= 2 over >= 20 distinct case days and slope on |forecast| > 0; reject: mean < 0 with t <= -2 over >= 20 distinct case days"
    reading = ("Situation checked as raw 14-day swing-scaled return (recorded scaled_fall last_history_value, else recomputed from closes) <= -2 with a short forecast, the profile vetoes not being recomputed; "
               "cases are short bets (rise of |forecast| on the short side of >= 2 points from its lowest level since the last bet, reset at flat), first per 7-bar grid cell from each window's first row; "
               "normal drift is the coin's mean non-overlapping 7-bar return over all its windows; t uses day-clustered errors with D/(D-1) correction; fewer than 20 distinct case days is 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct case days": None},
            "decided_by": "Fewer than 90% of the active bars are short bars where the 14-day swing-scaled return is -2 or lower, as the Fidelity's situation requires (or no active bar at all).",
            "reading": reading,
        }

    # ---------- normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if (coin, w) not in prepared:
                continue
            close = prepared[(coin, w)][1].values
            for i in range(0, len(close) - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    cases = []
    for (coin, w), (df, close, fc) in prepared.items():
        f = fc.values
        c = close.values
        ts = to_time(df["timestamp"]) if "timestamp" in df.columns else pd.Series(pd.NaT, index=df.index)
        ref = 0.0
        prev_short = False
        taken_cells = set()
        for i in range(len(f)):
            if f[i] < 0:
                m = -f[i]
                if not prev_short:
                    ref = 0.0
                if m - ref >= BAND - 1e-12:
                    ref = m
                    cell = i // H
                    if cell not in taken_cells:
                        taken_cells.add(cell)
                        if i + H < len(c) and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0 \
                                and np.isfinite(drift.get(coin, np.nan)):
                            ret = c[i + H] / c[i] - 1.0
                            u = -(ret - drift[coin])
                            t_i = ts.iloc[i]
                            day = str(t_i.date()) if pd.notna(t_i) else "%s_%s_%d" % (coin, w, i)
                            cases.append((day, u, m))
                else:
                    ref = min(ref, m)
                prev_short = True
            else:
                ref = 0.0
                prev_short = False

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)

    mean_u = None
    t_val = None
    slope = None
    if n_cases > 0:
        u = np.array([x[1] for x in cases], dtype=float)
        mag = np.array([x[2] for x in cases], dtype=float)
        mean_u = float(u.mean())
        dev = u - mean_u
        day_sums = pd.Series(dev).groupby([x[0] for x in cases]).sum().values
        D = len(day_sums)
        if D > 1:
            var_mean = (D / (D - 1.0)) * np.sum(day_sums ** 2) / (n_cases ** 2)
            se = np.sqrt(var_mean)
            t_val = float(mean_u / se) if se > 0 else None
        if n_cases >= 2 and np.unique(mag).size >= 2:
            slope = float(stats.linregress(mag, u).slope)

    sup_passed = None if slope is None else bool(slope > 0)

    if n_days < 20:
        status = "not observable"
        decided = "Fewer than 20 distinct case days (%d), the plan's minimum count, so the data cannot show the idea." % n_days
    elif mean_u is None or t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Mean short-signed unusual move above 0 with t >= 2 over at least 20 distinct case days, and the slope on |forecast| is positive."
        else:
            status = "inconclusive"
            decided = "A confirming mean (above 0, t >= 2) but the slope on |forecast| is not positive: inconclusive by the plan."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean short-signed unusual move below 0 with t <= -2 over at least 20 distinct case days: the coin rebounds."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-signed unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day taken together", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of short-signed unusual move on |forecast|", "value": slope, "passed": sup_passed},
        "counts": {"distinct case days": int(n_days), "cases": int(n_cases), "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
