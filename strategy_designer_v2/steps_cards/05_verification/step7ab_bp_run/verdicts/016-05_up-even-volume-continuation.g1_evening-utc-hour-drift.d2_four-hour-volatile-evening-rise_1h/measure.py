import numpy as np
import pandas as pd
from scipy import stats


def _to_utc(ts):
    if np.issubdtype(np.asarray(ts).dtype, np.number):
        arr = np.asarray(ts, dtype="float64")
        med = np.nanmedian(np.abs(arr)) if arr.size else 0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(arr, unit=unit, utc=True)
    return pd.to_datetime(ts, utc=True)


def _t_of_mean(x):
    x = np.asarray(x, dtype="float64")
    n = x.size
    if n < 2:
        return None
    sd = x.std(ddof=1)
    if not np.isfinite(sd) or sd == 0:
        return None
    return float(x.mean() / (sd / np.sqrt(n)))


def measure(bars):
    H = 4
    BAND = 2.0

    n_active = 0
    n_agree = 0
    coin_frames = {}

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        frames = []
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _to_utc(df["timestamp"])
            ts = pd.Series(ts)
            diffs = ts.diff().dropna()
            step = diffs.median() if len(diffs) else pd.Timedelta(hours=1)
            if pd.isna(step) or step <= pd.Timedelta(0):
                step = pd.Timedelta(hours=1)
            close_time = ts + step
            close_hour = close_time.dt.hour.values
            close_min = close_time.dt.minute.values
            situation = (close_hour == 21) & (close_min == 0)

            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype("float64")
            fc0 = np.where(np.isfinite(fc), fc, 0.0)
            active = fc0 != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc0 > 0)).sum())

            close = pd.to_numeric(df["close"], errors="coerce").values.astype("float64")
            n = len(close)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:-H] = close[H:] / close[:-H] - 1.0
            frames.append({"fc": fc0, "situation": situation, "fwd": fwd})
        coin_frames[coin] = frames

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "t of the mean 4-bar unusual move after the 21:00 UTC close, pooled"
    main_thr = "confirm if t >= 2 with a positive mean; reject if t <= -2"
    sup_name = "top minus bottom volatility-third mean unusual move (thirds per coin)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation, long": int(n_agree)},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are long bets on the bar "
                           "closing at 21:00 UTC, which the plan's Fidelity requires"),
            "reading": "the situation bar is the bar whose close (start timestamp plus one bar) is 21:00 UTC, on the long side",
        }

    all_unusual = []
    top_vals = []
    bot_vals = []
    for coin, frames in coin_frames.items():
        grid = []
        for f in frames:
            g = f["fwd"][0::H]
            grid.append(g[np.isfinite(g)])
        grid = np.concatenate(grid) if grid else np.array([])
        if grid.size == 0:
            continue
        drift = float(grid.mean())

        c_fc = []
        c_un = []
        for f in frames:
            mask = f["situation"] & (f["fc"] >= BAND) & np.isfinite(f["fwd"])
            if mask.any():
                c_fc.append(f["fc"][mask])
                c_un.append(f["fwd"][mask] - drift)
        if not c_fc:
            continue
        c_fc = np.concatenate(c_fc)
        c_un = np.concatenate(c_un)
        all_unusual.append(c_un)
        order = np.argsort(c_fc, kind="stable")
        parts = np.array_split(order, 3)
        bot_vals.append(c_un[parts[0]])
        top_vals.append(c_un[parts[2]])

    un = np.concatenate(all_unusual) if all_unusual else np.array([])
    top = np.concatenate(top_vals) if top_vals else np.array([])
    bot = np.concatenate(bot_vals) if bot_vals else np.array([])
    n_cases = int(un.size)

    mean_un = float(un.mean()) if n_cases else None
    t_main = _t_of_mean(un)
    diff = float(top.mean() - bot.mean()) if (top.size and bot.size) else None
    welch = None
    if top.size >= 2 and bot.size >= 2:
        r = stats.ttest_ind(top, bot, equal_var=False)
        if np.isfinite(r.statistic):
            welch = float(r.statistic)

    counts = {
        "cases in total": n_cases,
        "cases in the top volatility third": int(top.size),
        "cases in the bottom volatility third": int(bot.size),
    }
    reading = ("a case is a bar closing at 21:00 UTC (start timestamp plus one bar) whose forecast rises from 0 "
               "by at least the 2-point band, its return is close[t+4]/close[t]-1 within the window; thirds are "
               "split per coin by forecast rank (stable sort, near-equal parts) and the top and bottom thirds are "
               "pooled over coins for the difference, its Welch t and the 30-per-third minimum.")

    sup = {"name": sup_name, "value": diff, "passed": (None if diff is None else bool(diff > 0))}
    main = {"name": main_name, "value": mean_un,
            "statistic": (None if t_main is None else {"name": "ordinary t of the mean", "value": t_main}),
            "threshold": main_thr}

    if n_cases < 200 or top.size < 30 or bot.size < 30:
        which = "at least 200 cases in total" if n_cases < 200 else "at least 30 cases per volatility third"
        return {"status": "not observable",
                "situation_check": {"agreement": agreement, "passed": True},
                "main_measure": main, "supporting_check": sup, "counts": counts,
                "decided_by": f"the plan's minimum count of {which} is not reached",
                "reading": reading}

    if (t_main is not None and t_main <= -2) or (welch is not None and welch <= -2):
        status = "rejected"
        if t_main is not None and t_main <= -2:
            decided = "the main t is -2 or less, which meets the reject rule"
        else:
            decided = "the top-minus-bottom volatility-third difference has a Welch t of -2 or less, which meets the reject rule"
    elif t_main is not None and t_main >= 2 and mean_un > 0 and diff is not None and diff > 0:
        status = "confirmed"
        decided = "the main t is 2 or more with a positive mean and the top-minus-bottom volatility-third difference is above 0"
    else:
        status = "inconclusive"
        if t_main is not None and t_main >= 2:
            decided = ("the main t is 2 or more but the volatility-third difference is at or below 0 with a Welch t above -2 "
                       "(or the mean is not positive), which the plan calls inconclusive")
        else:
            decided = "the main t is between -2 and 2, which the plan calls inconclusive"

    sup["welch_t"] = welch
    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main, "supporting_check": sup, "counts": counts,
            "decided_by": decided, "reading": reading}
