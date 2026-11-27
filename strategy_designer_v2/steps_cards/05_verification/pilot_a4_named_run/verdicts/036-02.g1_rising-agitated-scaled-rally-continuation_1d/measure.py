import json
import numpy as np
import pandas as pd


def measure(bars):
    HORIZON = 3
    BAND = 2.0
    GATE = 1.0
    MIN_DAYS = 30
    COMP = "scaled_rise"
    FLAT_COL = "debug_info.components.%s.last_history_value" % COMP

    def _raw_component(df):
        # recorded raw value of the strategy component, if present
        if FLAT_COL in df.columns:
            return pd.to_numeric(df[FLAT_COL], errors="coerce")
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
                    c = d.get(COMP)
                    if isinstance(c, dict):
                        x = c.get("last_history_value")
                        try:
                            val = float(x) if x is not None else np.nan
                        except Exception:
                            val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    def _recompute_sr(df):
        close = df["close"].astype(float)
        rr = (df["high"].astype(float) - df["low"].astype(float)) / close
        base = rr.rolling(30, min_periods=30).mean()
        ret3 = close / close.shift(3) - 1.0
        return ret3 / base.replace(0, np.nan)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            sr = _raw_component(df)
            sr = sr.where(sr.notna(), _recompute_sr(df))
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            situ = (sr >= GATE) & (regime == "trending")
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean unusual 3-day move after bet bars", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"distinct case days": 0, "cases": 0},
            "decided_by": "No active bar in the record, so no case and fewer than 30 distinct case days.",
            "reading": "Situation = recorded (or recomputed) scaled rise >= 1.0 on a bar the detector labelled trending (the regime carries the profile vetoes), side long.",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    reading_situ = ("Situation = scaled rise >= 1.0 from the recorded scaled_rise raw value (recomputed from prices where missing) "
                    "on bars the detector labelled trending, since the profile components are not recorded and the regime carries their vetoes; side long")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 3-day move after bet bars", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"distinct case days": None},
            "decided_by": "Only %.1f%% of active bars are long bars with scaled rise >= 1.0 inside the trending regime, below 90%%." % (100 * agreement),
            "reading": reading_situ + ".",
        }

    # ---------- main measure ----------
    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        # normal drift: mean grid 3-bar return over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for i in range(0, len(c) - HORIZON, HORIZON):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + HORIZON]):
                    grid_rets.append(c[i + HORIZON] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = df["close"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            side_prev = 0
            anchor = 0.0
            for i in range(n):
                fi = f[i]
                side = 1 if fi > 0 else (-1 if fi < 0 else 0)
                if side == 0:
                    side_prev = 0
                    anchor = 0.0
                    continue
                if side != side_prev:
                    anchor = 0.0
                mag = abs(fi)
                if mag - anchor >= BAND:
                    bet[i] = True
                    anchor = mag
                else:
                    anchor = min(anchor, mag)
                side_prev = side
            seen_cells = set()
            for i in range(n):
                if not bet[i]:
                    continue
                cell = i // HORIZON
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + HORIZON >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + HORIZON]) and c[i] > 0):
                    continue
                r = c[i + HORIZON] / c[i] - 1.0
                sgn = 1.0 if f[i] > 0 else -1.0
                u = (r - drift) * sgn
                day = ts.iloc[i].strftime("%Y-%m-%d") if pd.notna(ts.iloc[i]) else str(i)
                cases.append((day, u, float(f[i])))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)
    threshold = "confirm: mean > 0 with t >= 2 and positive slope; reject: mean < 0 with t <= -2"
    reading = (reading_situ + "; a case is the first bet bar (long-side forecast rise >= 2 from its lowest level since the last bet) "
               "in each 3-bar grid cell of a window, t pools same-day deviations with a G/(G-1) cluster correction, "
               "and fewer than 30 distinct case days gives not observable.")

    mean_u = None
    t = None
    slope = None
    if n_cases > 0:
        u = np.array([x[1] for x in cases])
        fc = np.array([x[2] for x in cases])
        mean_u = float(u.mean())
        dev = u - mean_u
        per_day = pd.Series(dev).groupby([x[0] for x in cases]).sum().values
        G = len(per_day)
        if G > 1:
            var = (per_day ** 2).sum() / (n_cases ** 2) * G / (G - 1)
            se = np.sqrt(var)
            t = float(mean_u / se) if se > 0 else None
        if n_cases > 1 and np.var(fc) > 0:
            slope = float(np.polyfit(fc, u, 1)[0])

    slope_pass = None if slope is None else bool(slope > 0)
    main = {"name": "mean unusual 3-day move after bet bars",
            "value": mean_u,
            "statistic": {"name": "t of the mean, same-day cases pooled", "value": t} if t is not None else None,
            "threshold": threshold}
    supp = {"name": "OLS slope of unusual move on forecast", "value": slope, "passed": slope_pass}
    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = "Fewer than 30 distinct case days across all coins and windows (%d)." % n_days
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed, so neither confirm nor reject is met."
    elif mean_u > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and a positive supporting slope."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting slope is not positive."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
