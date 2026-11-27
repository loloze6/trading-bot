import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.run_depth.last_history_value"
    BAND = 2.0
    H = 1

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            v = s.astype(float)
            unit = "ms" if v.abs().max() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).reset_index(drop=True)
            lhv = (pd.to_numeric(df[LHV], errors="coerce").reset_index(drop=True)
                   if LHV in df.columns else pd.Series(np.nan, index=close.index))
            regime = df["regime"].astype(str).reset_index(drop=True)
            prev1 = close.shift(1)
            prev2 = close.shift(2)
            ret60 = close / close.shift(60) - 1.0
            for i in range(len(close)):
                f = fc.iloc[i]
                if f == 0:
                    continue
                n_active += 1
                # run break: raw run loss above 0, today an up close ending a down day
                brk = bool(np.isfinite(lhv.iloc[i]) and lhv.iloc[i] > 0)
                if np.isfinite(prev1.iloc[i]):
                    brk = brk and close.iloc[i] > prev1.iloc[i]
                if np.isfinite(prev1.iloc[i]) and np.isfinite(prev2.iloc[i]):
                    brk = brk and prev1.iloc[i] < prev2.iloc[i]
                # falling market: 60-bar price change below 0 where it can be read in the window,
                # else the regime detector's decision (falling profile passed)
                if np.isfinite(ret60.iloc[i]):
                    falling = ret60.iloc[i] < 0
                else:
                    falling = regime.iloc[i] == "mean_reversion"
                if brk and falling and f < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean unusual short gain over 1 day (next-day return minus coin mean daily return, sign flipped)"
    thr = "confirm: mean > 0 with day-pooled t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    sup_name = "mean unusual short gain, top third by |forecast| minus bottom third"
    reading = ("Situation computed as raw run_depth > 0 on an up close after a down close, in a falling market read as "
               "a negative 60-bar price change inside the window (the recorded regime where 60 bars are not available), "
               "on a negative forecast; cases are bets of the short forecast rising in size by at least 2 from its lowest "
               "level since the last bet (reset at flat), every bar being a 1-bar grid cell; the t pools cases per UTC "
               "day (cluster standard error with D/(D-1) correction); thirds are floor(n/3) cases sorted by |forecast| "
               "then time; the plan's 'fewer than 30 distinct case days' is applied as a minimum count, giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bets on a run-break up close "
                           "in a falling market, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift: mean daily return over all windows (non-overlapping 1-bar returns)
    drift = {}
    for coin in sorted(bars):
        rets = []
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) < 2:
                continue
            c = df["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    cases = []  # (time, coin, absf, gain, day)
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = to_time(df["timestamp"]).reset_index(drop=True)
            ref = 0.0
            for i in range(len(c)):
                s = -fc[i] if fc[i] < 0 else 0.0
                if s <= 0:
                    ref = 0.0
                    continue
                if s - ref >= BAND:
                    ref = s
                    if i + H < len(c) and np.isfinite(c[i]) and np.isfinite(c[i + H]) and np.isfinite(drift[coin]):
                        r = c[i + H] / c[i] - 1.0
                        gain = -(r - drift[coin])
                        t = ts.iloc[i]
                        cases.append((t, coin, abs(fc[i]), gain, t.floor("D")))
                else:
                    ref = min(ref, s)

    n_cases = len(cases)
    days = sorted(set(cc[4] for cc in cases))
    n_days = len(days)

    mean = float(np.mean([cc[3] for cc in cases])) if n_cases else None
    tstat = None
    if n_cases >= 2 and n_days >= 2:
        g = np.array([cc[3] for cc in cases])
        dev = pd.Series(g - mean).groupby([cc[4] for cc in cases]).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        tstat = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    k = n_cases // 3
    if k >= 1:
        srt = sorted(cases, key=lambda cc: (cc[2], cc[0], cc[1]))
        bottom = np.mean([cc[3] for cc in srt[:k]])
        top = np.mean([cc[3] for cc in srt[-k:]])
        sup_val = float(top - bottom)
        sup_pass = bool(sup_val > 0)

    counts = {"cases": int(n_cases), "distinct case days": int(n_days)}
    main = {"name": main_name, "value": mean,
            "statistic": ({"name": "t of the mean, cases pooled by day", "value": tstat} if tstat is not None else None),
            "threshold": thr}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}
    sit = {"agreement": float(agreement), "passed": True}

    if n_days < 30:
        status = "not observable"
        decided = f"The minimum of 30 distinct case days is not reached ({n_days})."
    elif tstat is None or mean is None:
        status = "inconclusive"
        decided = "The t cannot be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif mean > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual short gain is above 0 with t >= 2 and the top third beats the bottom third."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean unusual short gain is below 0 with t <= -2."
    elif mean > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (top third minus bottom third above 0) fails."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
