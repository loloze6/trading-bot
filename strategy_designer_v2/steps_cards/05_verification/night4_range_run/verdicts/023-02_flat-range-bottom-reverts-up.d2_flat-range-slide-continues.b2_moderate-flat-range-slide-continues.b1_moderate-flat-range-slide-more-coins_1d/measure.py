import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    MIN_CASES = 30
    P = 30
    FL = "debug_info.components.fall_lin.last_history_value"
    EPS = 1e-12

    def sit_flags(df):
        close = pd.to_numeric(df["close"], errors="coerce")
        high = pd.to_numeric(df["high"], errors="coerce")
        low = pd.to_numeric(df["low"], errors="coerce")
        hh = high.rolling(P, min_periods=P).max()
        ll = low.rolling(P, min_periods=P).min()
        rng = hh - ll
        net = (close - close.shift(P)).abs()
        ratio = net / rng.where(rng > 0)
        mid = (hh + ll) / 2.0
        flat_c = ratio <= 0.3 + 1e-9
        below_c = (close - mid) < 0
        computable = ratio.notna() & mid.notna()
        regime_c = flat_c & below_c
        # Where the window lacks 30 bars of its own history, fall back on the
        # detector's recorded decision (its components are not recorded).
        regime_rec = df["regime"].astype(str) == "mean_reversion" if "regime" in df.columns \
            else pd.Series(False, index=df.index)
        regime_ok = regime_c.where(computable, regime_rec).astype(bool)
        # 10-day fall: sign of the raw scaled 10-day return, else from prices
        if FL in df.columns:
            raw = pd.to_numeric(df[FL], errors="coerce")
        else:
            raw = pd.Series(np.nan, index=df.index)
        r10 = close / close.shift(10) - 1.0
        fall = raw.where(raw.notna(), r10) < 0
        return (regime_ok & fall.fillna(False)).astype(bool)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            act = f.notna() & (f != 0)
            if act.sum() == 0:
                continue
            s = sit_flags(df)
            n_active += int(act.sum())
            n_agree += int((act & s & (f < 0)).sum())

    mm_name = "mean short-side unusual 5-bar move / coin's usual 5-bar move, forecast < 0 grid bars"
    mm_thr = "confirm: mean > 0 with t >= 2 over >= 30 cases (and supporting check passes); reject: mean < 0 with t <= -2 over >= 30 cases"
    sc_name = "|forecast|-weighted mean of the same unusual move > 0"
    reading = ("Situation recomputed per window from prices (net move = |close[t]-close[t-30]| over the 30-bar "
               "high-low range, close below the 30-bar high-low midpoint), falling back on the recorded regime where "
               "a window lacks 30 bars of history, with the fall read from the sign of fall_lin's raw value; the "
               "coin's normal drift and usual move are the mean and standard deviation of its 5-bar returns on the "
               "non-overlapping grid of all its windows, and cases are grid bars with forecast < 0 and a close 5 bars "
               "later in the same window.")

    if n_active == 0:
        agreement = None
        passed = False
    else:
        agreement = n_agree / n_active
        passed = agreement >= 0.9

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are bars of the plan's situation (flat 30-day range, close "
                           "below its midpoint, negative 10-day return) with a short forecast."),
            "reading": reading,
        }

    # ---------- main measure ----------
    cases = []  # (unusual_strength, |forecast|)
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values if "forecast" in df.columns \
                else np.full(len(df), np.nan)
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(f[i]) and f[i] < 0:
                    coin_cases.append((r, abs(f[i])))
        if len(grid_rets) < 2 or not coin_cases:
            continue
        gr = np.asarray(grid_rets, dtype=float)
        drift = gr.mean()
        usual = gr.std(ddof=1)
        if not np.isfinite(usual) or usual <= EPS:
            continue
        for r, a in coin_cases:
            cases.append((-(r - drift) / usual, a))

    n_cases = len(cases)
    if n_cases > 0:
        u = np.array([c[0] for c in cases], dtype=float)
        a = np.array([c[1] for c in cases], dtype=float)
        mean = float(u.mean())
        if n_cases > 1:
            sd = u.std(ddof=1)
            t = float(mean / (sd / np.sqrt(n_cases))) if sd > EPS else None
        else:
            t = None
        wmean = float((u * a).sum() / a.sum()) if a.sum() > 0 else None
    else:
        mean, t, wmean = None, None, None

    sc_pass = (wmean > 0) if wmean is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}) on the 5-bar grid with forecast below 0: the minimum count is not reached."
    elif t is not None and mean > 0 and t >= 2 and sc_pass:
        status = "confirmed"
        decided = "Mean above 0 with t >= 2 over at least 30 cases, and the |forecast|-weighted mean is above 0."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean below 0 with t <= -2 over at least 30 cases."
    elif t is not None and mean > 0 and t >= 2 and not sc_pass:
        status = "inconclusive"
        decided = "A positive t >= 2 whose supporting check (|forecast|-weighted mean above 0) fails."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": bool(passed)},
        "main_measure": {"name": mm_name,
                         "value": mean,
                         "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
                         "threshold": mm_thr},
        "supporting_check": {"name": sc_name, "value": wmean,
                             "passed": (bool(sc_pass) if sc_pass is not None else None)},
        "counts": {"cases": int(n_cases), "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
