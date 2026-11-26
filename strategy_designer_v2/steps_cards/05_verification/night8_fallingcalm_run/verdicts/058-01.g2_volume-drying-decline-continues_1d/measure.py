import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    VCOL = "debug_info.components.vol_dryup.last_history_value"

    def _ts(df):
        ts = df["timestamp"]
        if np.issubdtype(ts.dtype, np.number):
            unit = "ms" if ts.abs().max() > 1e11 else "s"
            return pd.to_datetime(ts, unit=unit, utc=True)
        return pd.to_datetime(ts, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            vol = df["volume"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).values
            n = len(df)
            # 30-day percent return from prices, inside the window
            fall30 = np.full(n, np.nan)
            if n > 30:
                fall30[30:] = close[30:] / close[:-30] - 1.0
            # raw volume log ratio, recorded; recomputed from volume where missing
            if VCOL in df.columns:
                vlog = pd.to_numeric(df[VCOL], errors="coerce").values.astype(float)
            else:
                vlog = np.full(n, np.nan)
            for t in range(n):
                if np.isnan(vlog[t]) and t >= 59:
                    a = vol[t - 29:t + 1].mean()
                    b = vol[t - 59:t - 29].mean()
                    if a > 0 and b > 0:
                        vlog[t] = np.log(a / b)
            for t in range(n):
                if fc[t] == 0:
                    continue
                n_active += 1
                in_regime = regime[t] == "mean_reversion"  # fall30<0 and profile vetoes passed
                falling = (fall30[t] < 0) if not np.isnan(fall30[t]) else in_regime
                shrink = (not np.isnan(vlog[t])) and vlog[t] < 0
                if in_regime and falling and shrink and fc[t] < 0:
                    n_agree += 1

    reading_sit = ("Situation = regime 'mean_reversion' (the detector's fall30<0 with the falling-calm profile "
                   "vetoes passed) and the 30-day return from prices <0 where computable in the window, and the "
                   "raw vol_dryup log ratio <0 (recomputed from volume where not recorded), on the short side")
    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move, short direction", "value": None,
                             "statistic": None, "threshold": "mean > 0 with day-clustered t >= 2 to confirm; t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"distinct case-days": 0, "cases": 0},
            "decided_by": "No bar has a non-zero forecast, so there are no cases and fewer than 30 distinct case-days.",
            "reading": reading_sit + ".",
        }
    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move, short direction", "value": None,
                             "statistic": None, "threshold": "mean > 0 with day-clustered t >= 2 to confirm; t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Only %.1f%% of the active bars are short bars of a 30-day fall with shrinking 30-day "
                           "volume inside the falling calm profile, below 90%%." % (100 * agreement)),
            "reading": reading_sit + ".",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: non-overlapping 5-bar returns over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (unusual, |forecast|, day)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            days = _ts(df).dt.floor("D").values
            n = len(df)
            # short bets: rise of short magnitude >= band from its lowest level since last bet
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for t in range(n):
                m = -fc[t] if fc[t] < 0 else 0.0
                if m == 0.0:
                    ref = 0.0
                    continue
                if m - ref >= BAND:
                    bet[t] = True
                    ref = m
                else:
                    ref = min(ref, m)
            for start in range(0, n, H):
                idx = [t for t in range(start, min(start + H, n)) if bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or np.isnan(drift[coin]):
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                cases.append((-(r - drift[coin]), abs(fc[t]), days[t]))

    n_cases = len(cases)
    x = np.array([a for a, _, _ in cases], dtype=float)
    af = np.array([b for _, b, _ in cases], dtype=float)
    dd = pd.Series([d for _, _, d in cases])
    n_days = int(dd.nunique()) if n_cases else 0

    mean = float(x.mean()) if n_cases else None
    tval = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(x - x.mean()).groupby(dd.values).sum().values
        G = len(dev)
        var = (G / (G - 1)) * np.sum(dev ** 2) / n_cases ** 2
        se = np.sqrt(var)
        tval = float(mean / se) if se > 0 else None

    check_val = None
    check_pass = None
    if n_cases >= 2:
        med = np.median(af)
        hi = x[af > med]
        lo = x[af <= med]
        if len(hi) > 0 and len(lo) > 0:
            check_val = float(hi.mean() - lo.mean())
            check_pass = bool(check_val > 0)
        else:
            check_pass = False

    if n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 distinct case-days (%d), the plan's minimum." % n_days
    elif tval is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval <= -2:
        status = "rejected"
        decided = "The main measure has t <= -2: the decline reverses more than the drift after volume dry-ups."
    elif tval >= 2 and mean > 0 and check_pass:
        status = "confirmed"
        decided = "The mean unusual short move is above 0 with t >= 2 and the larger-forecast half beats the smaller half."
    elif tval >= 2:
        status = "inconclusive"
        decided = "Main t >= 2 but the supporting check is at or below 0 (or not computable), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean unusual 5-bar move, short direction",
            "value": mean,
            "statistic": ({"name": "t of the mean, cases of one day together", "value": tval}
                          if tval is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 and check > 0; reject: t <= -2",
        },
        "supporting_check": {
            "name": "larger-|forecast| half minus smaller half, mean unusual move",
            "value": check_val,
            "passed": check_pass,
        },
        "counts": {"distinct case-days": n_days, "cases": int(n_cases)},
        "decided_by": decided,
        "reading": (reading_sit + "; a case is the first short bet in each 5-bar grid cell counted from each "
                    "window's first row, with cases lacking 5 bars ahead in the window dropped; the day-clustered t "
                    "uses the per-day summed deviations with a G/(G-1) correction; the larger half is |forecast| "
                    "strictly above the median and the smaller half at or below it; the plan's 'at least 30 distinct "
                    "case-days' is applied as the minimum count giving 'not observable'."),
    }
