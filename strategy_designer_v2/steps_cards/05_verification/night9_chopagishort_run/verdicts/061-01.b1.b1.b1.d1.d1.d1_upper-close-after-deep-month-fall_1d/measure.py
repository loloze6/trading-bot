import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0

    # ---------- helpers ----------
    def _comp_value(df, cid, field="last_history_value"):
        col = "debug_info.components.%s.%s" % (cid, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].tolist():
                val = np.nan
                try:
                    if isinstance(v, dict) and cid in v and isinstance(v[cid], dict):
                        x = v[cid].get(field, None)
                        if x is not None:
                            val = float(x)
                except Exception:
                    val = np.nan
                out.append(val)
            return np.asarray(out, dtype=float)
        return np.full(len(df), np.nan)

    def _pct_change(close, p):
        n = len(close)
        out = np.full(n, np.nan)
        if n > p:
            out[p:] = (close[p:] / close[:-p] - 1.0) * 100.0
        return out

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    # ---------- prepare windows ----------
    prepared = []  # (coin, window, df)
    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            df["_ts"] = _ts(df)
            df = df.sort_values("_ts").reset_index(drop=True)
            prepared.append((coin, win, df))

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, win, df in prepared:
        f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
        close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
        high = pd.to_numeric(df["high"], errors="coerce").to_numpy(dtype=float)
        low = pd.to_numeric(df["low"], errors="coerce").to_numpy(dtype=float)
        regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))

        rng = high - low
        with np.errstate(divide="ignore", invalid="ignore"):
            loc = np.where(rng > 0, (close - low) / rng, np.nan)
        r5 = _pct_change(close, 5)
        t60 = _pct_change(close, 60)
        r20_rec = _comp_value(df, "fall20", "last_history_value")
        r20_px = _pct_change(close, 20)
        r20 = np.where(np.isfinite(r20_rec), r20_rec, r20_px)

        for i in range(len(df)):
            if not np.isfinite(f[i]) or f[i] == 0:
                continue
            n_active += 1
            ok = True
            # conditions computable from the record; others fall back on the detector's own decision
            if np.isfinite(t60[i]):
                ok &= (-10.0 <= t60[i] <= 10.0)
            if np.isfinite(loc[i]):
                ok &= loc[i] > 0.5
            else:
                ok &= False
            if np.isfinite(r5[i]):
                ok &= r5[i] < 0.0
            if np.isfinite(r20[i]):
                ok &= r20[i] <= -10.0
            ok &= (regime[i] == "mean_reversion")  # agitation (365-day vol percentile) not computable inside a window
            ok &= f[i] < 0
            if ok:
                n_agree += 1

    reading = ("Situation check: close location, 5-, 20- and 60-day returns are recomputed from prices inside each "
               "window (20-day from the recorded fall20 raw value when present; a condition whose lookback exceeds the "
               "window's start is left to the detector), and the 365-day volatility percentile, not computable within a "
               "window, is taken from the detector's regime 'mean_reversion'; a case is the first short bet (forecast "
               "magnitude rising >= 2 points from its lowest short level since the last bet) in each 5-bar grid cell "
               "counted from each window's first row; drift is the coin's mean non-overlapping 5-bar return over all "
               "its windows; the clustered t sums deviations per UTC day with a G/(G-1) correction; the deeper half is "
               "|forecast| strictly above the cases' median, the shallower half at or below it.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean short-side unusual 5-day move per case", "value": None,
                             "statistic": None, "threshold": "mean > 0 with day-clustered t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "No bar has a non-zero forecast, so no case exists; the minimum of 30 cases on 20 days is not reached.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean short-side unusual 5-day move per case", "value": None,
                             "statistic": None, "threshold": "mean > 0 with day-clustered t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": None,
            "decided_by": ("Only %.1f%% of the active bars are short bars of the plan's regime (60-day return within ±10%%, "
                           "agitated volatility, close in the upper half, 5-day return < 0, 20-day return <= -10%%), below 90%%."
                           % (100 * agreement)),
            "reading": reading,
        }

    # ---------- normal drift per coin ----------
    drift_lists = {}
    for coin, win, df in prepared:
        close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
        n = len(close)
        for p in range(0, n - H, H):
            a, b = close[p], close[p + H]
            if np.isfinite(a) and np.isfinite(b) and a > 0:
                drift_lists.setdefault(coin, []).append(b / a - 1.0)
    drift = {c: float(np.mean(v)) for c, v in drift_lists.items() if len(v) > 0}

    # ---------- cases ----------
    cases = []  # (value, day, |forecast|)
    for coin, win, df in prepared:
        f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
        close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
        days = df["_ts"].dt.strftime("%Y-%m-%d").to_numpy()
        n = len(df)
        ref = 0.0
        bet_bars = []
        for i in range(n):
            fi = f[i]
            if not np.isfinite(fi) or fi >= 0:
                ref = 0.0
                continue
            m = -fi
            if m - ref >= BAND - 1e-12:
                bet_bars.append(i)
                ref = m
            else:
                ref = min(ref, m)
        seen_cells = set()
        for i in bet_bars:
            cell = i // H
            if cell in seen_cells:
                continue
            seen_cells.add(cell)
            if i + H >= n or coin not in drift:
                continue
            a, b = close[i], close[i + H]
            if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                continue
            ret = b / a - 1.0
            val = -(ret - drift[coin])
            cases.append((float(val), days[i], float(abs(f[i]))))

    n_cases = len(cases)
    n_days = len(set(c[1] for c in cases))
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}
    threshold = "mean > 0 with day-clustered t >= 2 (and supporting difference > 0) to confirm; mean < 0 with t <= -2 to reject"

    def _clustered(vals, ds):
        vals = np.asarray(vals, dtype=float)
        nn = len(vals)
        if nn < 2:
            return (float(vals.mean()) if nn else None), None
        mu = vals.mean()
        dev = pd.Series(vals - mu).groupby(pd.Series(ds)).sum().to_numpy()
        G = len(dev)
        if G < 2:
            return float(mu), None
        var = (G / (G - 1.0)) * np.sum(dev ** 2) / (nn ** 2)
        se = np.sqrt(var)
        if se <= 0:
            return float(mu), None
        return float(mu), float(mu / se)

    mean_val, t_val = (None, None)
    if n_cases > 0:
        mean_val, t_val = _clustered([c[0] for c in cases], [c[1] for c in cases])

    diff = None
    if n_cases > 0:
        absf = np.array([c[2] for c in cases])
        vals = np.array([c[0] for c in cases])
        med = float(np.median(absf))
        deep = vals[absf > med]
        shallow = vals[absf <= med]
        if len(deep) > 0 and len(shallow) > 0:
            diff = float(deep.mean() - shallow.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    main = {"name": "mean short-side unusual 5-day move per case",
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "day-clustered t of the mean", "value": t_val},
            "threshold": threshold}
    sup = {"name": "deeper-fall half minus shallower half mean unusual move (split at median |forecast|)",
           "value": diff, "passed": sup_pass}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = ("The plan's minimum of 30 cases on 20 distinct days is not reached (%d cases on %d days)."
                   % (n_cases, n_days))
    elif t_val is None or mean_val is None:
        status = "inconclusive"
        decided = "The t of the main measure cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_val > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual short-side move is above 0 with t >= 2 and the deeper-minus-shallower difference is above 0."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the supporting difference is not above 0, which the plan calls inconclusive."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual short-side move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 (or its sign does not match the threshold), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
