import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.day_move.last_history_value"
    H = 5
    EVENT_LEVEL = 10.0
    MIN_EVENTS = 30

    def tstat(x):
        x = np.asarray(x, dtype=float)
        x = x[np.isfinite(x)]
        n = len(x)
        if n < 2:
            return None
        sd = x.std(ddof=1)
        if not np.isfinite(sd) or sd == 0:
            return None
        return float(x.mean() / (sd / np.sqrt(n)))

    # ---------- 1. situation check ----------
    active_total = 0
    active_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or FC not in df.columns:
                continue
            fc = pd.to_numeric(df[FC], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            px_move = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), px_move)
            else:
                raw = px_move
            act = fc.notna() & (fc != 0)
            active_total += int(act.sum())
            ok = act & (fc > 0) & raw.notna() & (raw > 0)
            active_ok += int(ok.sum())

    agreement = float(active_ok / active_total) if active_total > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of active bars are up days (positive raw one-day rise) "
                           "with a long forecast, so the config does not trade the plan's situation on its long side."
                           if active_total > 0 else "No active bars in the record to check the situation against."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    ex5_all = []
    ex1_all = []
    for coin, wins in bars.items():
        # pooled mean daily return of the coin over all its windows (within-window returns only)
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        if not rets:
            continue
        allr = np.concatenate(rets)
        if len(allr) == 0:
            continue
        mu = float(allr.mean())

        for w, df in wins.items():
            if df is None or len(df) == 0 or FC not in df.columns:
                continue
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            last = None
            for t in range(n):
                if not (np.isfinite(fc[t]) and fc[t] >= EVENT_LEVEL):
                    continue
                if last is not None and t - last <= H:
                    continue  # merged into earlier counted event
                last = t
                if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0:
                    ex5 = c[t + H] / c[t] - 1.0 - H * mu
                    ex5_all.append(ex5)
                    if np.isfinite(c[t + 1]):
                        ex1_all.append(c[t + 1] / c[t] - 1.0 - mu)

    n_ev = len(ex5_all)
    mean5 = float(np.mean(ex5_all)) if n_ev > 0 else None
    t5 = tstat(ex5_all)
    mean1 = float(np.mean(ex1_all)) if len(ex1_all) > 0 else None
    t1 = tstat(ex1_all)
    sup_pass = (abs(t1) < 2) if t1 is not None else None

    if n_ev < MIN_EVENTS:
        status = "not observable"
        decided = f"Only {n_ev} independent events with a measurable 5-bar return, below the plan's minimum of 30."
    elif t5 is not None and mean5 > 0 and t5 >= 2:
        status = "confirmed"
        decided = "Mean 5-bar excess return after events is above 0 with t >= 2 over at least 30 independent events."
    elif t5 is not None and mean5 < 0 and t5 <= -2:
        status = "rejected"
        decided = "Mean 5-bar excess return after events is below 0 with t <= -2 over at least 30 independent events (big up days reverse)."
    else:
        status = "inconclusive"
        decided = "With at least 30 independent events, the t of the mean 5-bar excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 5-bar excess return after forecast>=10 events",
            "value": mean5,
            "statistic": {"name": "t of the mean", "value": t5} if t5 is not None else None,
            "threshold": "confirm if mean > 0 and t >= 2, reject if mean < 0 and t <= -2, over at least 30 independent events",
        },
        "supporting_check": {
            "name": "mean next-bar excess return after events, expected |t| < 2",
            "value": mean1,
            "passed": sup_pass,
        },
        "counts": {"independent events": int(n_ev)},
        "decided_by": decided,
        "reading": ("Events merge when within 5 bars (difference <= 5) of the previous counted event in the same window, "
                    "counted events without a bar t+5 in their window are left out of the measure, the coin's mean daily "
                    "return is the mean of all within-window one-bar returns, and the supporting check is reported but does "
                    "not gate the verdict since the confirm rule does not mention it."),
    }
