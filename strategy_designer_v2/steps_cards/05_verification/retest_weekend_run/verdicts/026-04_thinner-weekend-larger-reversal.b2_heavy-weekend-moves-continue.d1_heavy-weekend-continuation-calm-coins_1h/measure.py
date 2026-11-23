import numpy as np
import pandas as pd


def _ts(series):
    s = series
    if np.issubdtype(s.dtype, np.number):
        v = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if v > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 48
    SHORT = 48
    BASE = 120

    agree_n = 0
    active_checked = 0
    active_unverifiable = 0

    case_vals = []

    for coin in sorted(bars.keys()):
        wins = bars[coin]

        # normal 48h drift of the coin: non-overlapping grid of every window, all windows together
        grid_rets = []
        for w in sorted(wins.keys()):
            df = wins[w]
            c = df["close"].astype(float).values
            n = len(c)
            for i in range(0, n - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        drift = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for w in sorted(wins.keys()):
            df = wins[w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            ts = _ts(df["timestamp"])
            nxt = ts + pd.Timedelta(hours=1)
            is_close_of_weekend = ((nxt.dt.weekday == 0) & (nxt.dt.hour == 0)).values

            vol = df["volume"].astype(float)
            recent = vol.rolling(SHORT, min_periods=SHORT).mean()
            prior = vol.shift(SHORT).rolling(BASE, min_periods=BASE).mean()
            ratio = (recent / prior).values

            c = df["close"].astype(float).values
            move = np.full(n, np.nan)
            move[H:] = c[H:] / c[:-H] - 1.0

            fc = df["forecast"].astype(float).fillna(0.0).values
            active = fc != 0

            seen_weekends = set()
            for i in np.where(active)[0]:
                # situation check
                if not np.isfinite(ratio[i]) or not np.isfinite(move[i]):
                    active_unverifiable += 1
                else:
                    active_checked += 1
                    in_sit = bool(is_close_of_weekend[i]) and ratio[i] > 1.0
                    side_ok = np.sign(fc[i]) == np.sign(move[i]) and move[i] != 0
                    if in_sit and side_ok:
                        agree_n += 1

                # case for the main measure: one per coin and weekend
                key = ts.iloc[i].normalize()
                if key in seen_weekends:
                    continue
                if i + H >= n or not np.isfinite(drift):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                seen_weekends.add(key)
                r = c[i + H] / c[i] - 1.0
                case_vals.append(fc[i] / 10.0 * (r - drift))

    agreement = float(agree_n / active_checked) if active_checked > 0 else 0.0
    passed = active_checked > 0 and agreement >= 0.9

    reading = ("The situation bar is read literally as the bar whose start + 1h is Monday 00:00 UTC (Sunday 23:00 start) "
               "with mean volume of its last 48 rows over the mean of the 120 rows before them > 1 and the forecast signed "
               "like the 48h close-to-close move; active bars without 168 prior rows in their window cannot be checked and "
               "are left out of the agreement; cases are active bars (one per coin and weekend) whose 48-bar return lies "
               "inside the window, with drift the mean of non-overlapping 48h returns over all windows of the coin.")

    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 100 cases"
    mm_name = "mean of forecast/10 x (48h return minus normal 48h drift) over weekend bets, before costs"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(active_checked),
                       "active bars unverifiable": int(active_unverifiable),
                       "cases": int(len(case_vals))},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Sunday-close bars of a heavy-volume "
                           "weekend with the forecast signed like the weekend move (agreement %.3f)." % agreement),
            "reading": reading,
        }

    x = np.asarray(case_vals, dtype=float)
    x = x[np.isfinite(x)]
    ncases = int(len(x))
    mean = float(np.mean(x)) if ncases > 0 else None
    if ncases > 1:
        sd = float(np.std(x, ddof=1))
        t = float(mean / (sd / np.sqrt(ncases))) if sd > 0 else 0.0
    else:
        t = None

    if ncases < 100:
        status = "not observable"
        decided = "Fewer than 100 cases (%d): the plan's minimum count is not reached." % ncases
    elif mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean position-weighted unusual 48h move is positive with t >= 2 over at least 100 cases."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean is negative with t <= -2 over at least 100 cases: weekend moves are reversed, not continued."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or the sign and t disagree), which neither confirms nor rejects."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name,
                         "value": mean,
                         "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
                         "threshold": threshold},
        "supporting_check": None,
        "counts": {"cases": ncases},
        "decided_by": decided,
        "reading": reading,
    }
