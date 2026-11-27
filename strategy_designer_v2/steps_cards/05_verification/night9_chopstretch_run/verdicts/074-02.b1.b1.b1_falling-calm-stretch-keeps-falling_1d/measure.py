import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    COMP = "stretch"
    KEY = "debug_info.components.%s.last_history_value" % COMP

    def get_raw(df):
        """Raw stretch value per bar (NaN where not recorded)."""
        if KEY in df.columns:
            return pd.to_numeric(df[KEY], errors="coerce")
        if "debug_info.components" in df.columns:
            vals = []
            for v in df["debug_info.components"]:
                x = np.nan
                if isinstance(v, dict):
                    c = v.get(COMP)
                    if isinstance(c, dict):
                        try:
                            x = float(c.get("last_history_value"))
                        except (TypeError, ValueError):
                            x = np.nan
                vals.append(x)
            return pd.Series(vals, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    def recompute_stretch(close):
        sma = close.rolling(20, min_periods=20).mean()
        ret = close.pct_change()
        sd = ret.rolling(20, min_periods=20).std()
        return ((close - sma) / sma) / sd

    def to_days(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            unit = "ms" if s.abs().max() > 1e11 else "s"
            d = pd.to_datetime(s, unit=unit, utc=True)
        else:
            d = pd.to_datetime(s, utc=True)
        return d.dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            raw = get_raw(df)
            rec = recompute_stretch(close)
            raw = raw.where(raw.notna(), rec)
            active = fc != 0
            n_active += int(active.sum())
            ok = active & (raw < 0) & (fc < 0)
            n_agree += int(ok.sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean unusual 5-bar short move", "value": None,
                             "statistic": None,
                             "threshold": "mean > 0 with day-clustered t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "No bar of the record holds a non-zero forecast, so there are no cases (fewer than 30 cases and 20 days).",
            "reading": "none",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": None,
            "decided_by": "Fewer than 90 % of the active bars are short bets with the close below its 20-day average "
                          "(raw stretch < 0), as the plan's Fidelity requires.",
            "reading": "The situation is a negative raw stretch (close below its 20-day SMA) and the side is short; "
                       "the falling calm profile is left to the regime and not rechecked.",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean of non-overlapping 5-bar returns over all its windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (unusual short move, |forecast|, day)
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            days = to_days(df["timestamp"])
            n = len(df)
            # short bets: a rise of the short forecast of at least the band
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                m = -fc[i] if fc[i] < 0 else 0.0
                if m <= 0:
                    ref = 0.0
                    continue
                if m - ref >= BAND:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            # one case per 5-bar grid cell (first bet in the cell)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                cases.append((-(r - drift[coin]), abs(fc[t]), days[t]))

    n_cases = len(cases)
    n_days = len(set(x[2] for x in cases))
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}
    thr = "mean > 0 with day-clustered t >= 2 (and supporting check) to confirm; mean < 0 with t <= -2 to reject"
    reading = ("Situation: raw stretch < 0 on short-forecast bars (profile left to the regime); a case is the first "
               "short bet (forecast rise of >= 2 points on the short side) in each 5-bar grid cell, with its 5-bar "
               "return inside the window; t is the mean over a day-clustered standard error with D/(D-1) correction; "
               "halves are the floor(n/2) largest and smallest |forecast| cases, the middle one dropped when n is odd.")

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": "mean unusual 5-bar short move", "value": None, "statistic": None,
                             "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "No case: fewer than 30 cases and fewer than 20 distinct days.",
            "reading": reading,
        }

    x = np.array([a[0] for a in cases], dtype=float)
    f = np.array([a[1] for a in cases], dtype=float)
    d = np.array([a[2] for a in cases])
    mean = float(x.mean())
    dev = x - mean
    sums = pd.Series(dev).groupby(d).sum().values
    D = len(sums)
    tstat = None
    if D > 1:
        var = np.sum(sums ** 2) * D / (D - 1) / (n_cases ** 2)
        se = np.sqrt(var)
        tstat = float(mean / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    h = n_cases // 2
    if h >= 1:
        order = np.argsort(f, kind="mergesort")
        shallow = x[order[:h]]
        deep = x[order[-h:]]
        sup_val = float(deep.mean() - shallow.mean())
        sup_pass = bool(sup_val > 0)

    main = {"name": "mean unusual 5-bar short move (fraction)", "value": mean,
            "statistic": {"name": "t of the mean, cases of one day together",
                          "value": tstat if tstat is not None else None},
            "threshold": thr}
    sup = {"name": "deeper half minus shallower half mean unusual short move", "value": sup_val, "passed": sup_pass}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = "Minimum not reached: %d cases (need 30) and %d distinct days (need 20)." % (n_cases, n_days)
    elif tstat is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual short move above 0 with t >= 2 and the deeper half beats the shallower half."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean unusual short move below 0 with t <= -2: stretched coins rise more than their drift."
    elif mean > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "Positive main measure with t >= 2 but the supporting check failed, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
