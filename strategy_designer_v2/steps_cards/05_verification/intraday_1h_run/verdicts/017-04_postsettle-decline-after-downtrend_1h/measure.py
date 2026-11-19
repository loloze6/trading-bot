import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype("float64")
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0
        unit = "s"
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    raw_col = "debug_info.components.fall3d.last_history_value"
    H = 2

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            ts = _to_utc(d["timestamp"]).reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").reset_index(drop=True)
            # bar closes (next bar starts) at timestamp + 1h
            next_start_hour = (ts + pd.Timedelta(hours=1)).dt.hour
            # held window: coming bar starts at a settlement hour or one hour after it
            timing_ok = next_start_hour.isin([0, 8, 16, 1, 9, 17])
            # settlement events: the bar's close falls at 00:00, 08:00, 16:00 UTC
            is_event = next_start_hour.isin([0, 8, 16])
            # raw 72-bar change: recorded value, else recomputed from prices in this window
            if raw_col in d.columns:
                raw = pd.to_numeric(d[raw_col], errors="coerce").reset_index(drop=True)
            else:
                raw = pd.Series(np.nan, index=d.index)
            recomputed = close / close.shift(72) - 1.0
            raw = raw.where(raw.notna(), recomputed)

            active = fc.notna() & (fc != 0)
            situation = timing_ok & (raw < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situation).sum())
            prepared[coin][w] = (close, fc, is_event)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "events with forecast below 0": None},
            "decided_by": ("Fewer than 90% of the active bars are bars two hours after a settlement with a negative "
                           "72-bar return and a short forecast, so the config does not do what the Fidelity says"
                           if n_active > 0 else "No active bars: the config never takes the plan's short position"),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    gains = []
    excesses = []
    absf = []
    for coin, wins in prepared.items():
        # coin's mean 2-bar return over all windows, from the non-overlapping grid
        grid_rets = []
        for w, (close, fc, is_event) in wins.items():
            c = close.values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for w, (close, fc, is_event) in wins.items():
            c = close.values
            f = fc.values
            ev = is_event.values
            n = len(c)
            for i in range(n - H):
                if not ev[i]:
                    continue
                if not (np.isfinite(f[i]) and f[i] < 0):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                ex = c[i + H] / c[i] - 1.0 - mu
                gains.append(-(f[i] / 10.0) * ex)
                excesses.append(ex)
                absf.append(abs(f[i]))

    gains = np.asarray(gains, dtype=float)
    excesses = np.asarray(excesses, dtype=float)
    absf = np.asarray(absf, dtype=float)
    n_ev = int(len(gains))

    mean_gain = float(np.mean(gains)) if n_ev > 0 else None
    t = None
    if n_ev > 1:
        sd = float(np.std(gains, ddof=1))
        t = float(mean_gain / (sd / np.sqrt(n_ev))) if sd > 0 else None

    diff = None
    check_passed = None
    if n_ev >= 3:
        order = np.argsort(absf, kind="mergesort")
        parts = np.array_split(order, 3)
        diff = float(np.mean(excesses[parts[2]]) - np.mean(excesses[parts[0]]))
        check_passed = bool(diff < 0)

    main = {
        "name": "mean per-event gain -(forecast/10) x excess 2-bar return after settlements, forecast < 0",
        "value": mean_gain,
        "statistic": {"name": "ordinary t of the mean", "value": t} if t is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2",
    }
    support = {
        "name": "mean excess 2-bar return, largest third of |forecast| minus smallest third",
        "value": diff,
        "passed": check_passed,
    }
    counts = {"events with forecast below 0": n_ev}
    reading = ("Events are the bars whose close (timestamp + 1h) is at 00:00, 08:00 or 16:00 UTC with a 2-bar forward "
               "return inside the window, pooled over all coins and windows, each coin's excess taken against its own "
               "all-window mean on the non-overlapping 2-bar grid, and thirds formed by rank of |forecast| over the "
               "pooled events; the situation is a negative 72-bar change on the held bars two hours after a settlement.")

    if n_ev < 300:
        status = "not observable"
        decided = f"Only {n_ev} events with forecast below 0, fewer than the 300 the plan requires."
    elif t is not None and mean_gain > 0 and t >= 2 and check_passed:
        status = "confirmed"
        decided = "The mean gain is positive with t >= 2 and the largest-minus-smallest third difference is below 0."
    elif t is not None and mean_gain < 0 and t <= -2:
        status = "rejected"
        decided = "The mean gain is negative with t <= -2."
    else:
        status = "inconclusive"
        if t is not None and t >= 2:
            decided = "t >= 2 but the supporting check fails (largest-minus-smallest third difference not below 0)."
        else:
            decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
