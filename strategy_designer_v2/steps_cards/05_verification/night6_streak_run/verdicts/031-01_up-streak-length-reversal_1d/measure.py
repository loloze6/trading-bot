import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.up_streak_rank.last_history_value"

    # ---------- 1. Situation check: up-close days, short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            raw = pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns else np.full(len(df), np.nan)
            for i in range(len(df)):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if i > 0 and np.isfinite(close[i - 1]) and np.isfinite(close[i]):
                    up = close[i] > close[i - 1]
                else:
                    # first bar of a window: no previous close inside the window, use the raw streak rank
                    up = bool(np.isfinite(raw[i]) and raw[i] > 0)
                if up and f < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean unusual 5-bar move per short case, short direction, before costs"
    threshold = "day-clustered t >= 2 to confirm, <= -2 to reject, on at least 100 cases over at least 30 days"
    sup_name = "mean unusual short move of top third of |forecast| minus bottom third"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "days": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are up-close days with a short "
                          "forecast, so the config does not take the plan's short position on up-close streak days.",
            "reading": "The situation is a close above the previous close in the same window (the raw streak rank "
                       "above 0 on a window's first bar), and the expected side is short.",
        }

    # ---------- 2. Normal drift per coin: non-overlapping 5-bar returns on the grid of every window ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = df["close"].astype(float).values
            for p in range(0, len(close) - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases: short bets (forecast falls >= 2 points on the short side), once per 5-bar cell ----------
    cases = []  # (day, unusual move short, |forecast|)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            side_prev = 0
            ref = 0.0
            bet = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                f = fc[i]
                side = int(np.sign(f))
                if side == 0:
                    side_prev, ref = 0, 0.0
                    continue
                if side != side_prev:
                    ref = 0.0
                m = abs(f)
                if m - ref >= BAND - 1e-12:
                    if side < 0:
                        bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
                side_prev = side
            used_cells = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if i + H >= len(df):
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                r = b / a - 1.0
                unusual_short = -(r - drift[coin])
                cases.append((ts.iloc[i].strftime("%Y-%m-%d"), unusual_short, abs(fc[i])))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)

    mean_val = None
    t_val = None
    if n_cases > 0:
        x = np.array([c[1] for c in cases])
        mean_val = float(x.mean())
        dev = pd.Series(x - mean_val).groupby([c[0] for c in cases]).sum().values
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * np.sum(dev ** 2) / n_cases ** 2
            se = np.sqrt(var)
            t_val = float(mean_val / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        order = sorted(cases, key=lambda c: c[2])
        k = n_cases // 3
        bottom = np.mean([c[1] for c in order[:k]])
        top = np.mean([c[1] for c in order[-k:]])
        sup_val = float(top - bottom)
        sup_pass = bool(top > bottom)

    reading = ("Situation = close above the previous close inside the window (raw rank > 0 on a window's first bar), "
               "side short; a case is the first short bet in each 5-bar grid cell of its window (bet = |forecast| "
               "rising >= 2 from its lowest level on the short side since the last bet, reset after flat or side "
               "change), its return taken from that bar's close 5 bars ahead inside the window; the day-clustered t "
               "uses per-day summed deviations with a G/(G-1) correction; the thirds are the n//3 cases with the "
               "largest and smallest |forecast|.")

    if n_cases < 100 or n_days < 30:
        status = "not observable"
        decided = f"The plan's minimum of 100 cases over 30 days is not reached ({n_cases} cases, {n_days} days)."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main measure's t is 2 or more on at least 100 cases over 30 days and the top third of |forecast| beats the bottom third."
        else:
            status = "inconclusive"
            decided = "A confirm-level t whose supporting check fails (top third of |forecast| does not exceed the bottom third)."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less on at least 100 cases over 30 days: up streaks are followed by rises beyond the drift."
    else:
        status = "inconclusive"
        decided = "The main measure's t is strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": {"name": "t of the mean, cases clustered by day", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"cases": int(n_cases), "days": int(n_days)},
        "decided_by": decided,
        "reading": reading,
    }
