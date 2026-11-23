import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        med = float(np.nanmedian(s.values.astype(float))) if len(s) else 0.0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 24
    VOLW = 720
    RAW = "debug_info.components.sunday_move.last_history_value"

    active_total = 0
    active_agree = 0
    cases = []  # dicts: coin, signed_excess, vol

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # coin's mean non-overlapping 24-bar return over all windows (grid 0, 24, 48, ... per window)
        grid_rets = []
        prepared = {}
        for w in sorted(wins.keys(), key=lambda x: (len(str(x)), str(x))):
            df = wins[w].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").astype(float).values
            n = len(close)
            for k in range(0, n - H, H):
                c0, c1 = close[k], close[k + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                    grid_rets.append(c1 / c0 - 1.0)
            prepared[w] = df
        coin_mean = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, df in prepared.items():
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            cv = close.values
            n = len(cv)
            ts = _to_utc(df["timestamp"]).reset_index(drop=True)
            close_time = ts + pd.Timedelta(hours=1)
            is_sit = ((close_time.dt.weekday == 0) & (close_time.dt.hour == 0)).values

            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float).values
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").astype(float).values

            # raw Sunday move: recorded component value, else 24-bar return from closes
            ret_back = (close / close.shift(H) - 1.0).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").astype(float).values
                raw = np.where(np.isfinite(raw), raw, ret_back)
            else:
                raw = ret_back

            # situation check
            act = np.isfinite(fc) & (fc != 0)
            active_total += int(act.sum())
            agree = act & is_sit & np.isfinite(raw) & (np.sign(fc) == -np.sign(raw)) & (raw != 0)
            active_agree += int(agree.sum())

            # 720-bar std of hourly returns from closes (within window)
            hr = close.pct_change()
            vol = hr.rolling(VOLW, min_periods=VOLW).std().values

            for i in range(n):
                if not is_sit[i]:
                    continue
                if not (np.isfinite(pos[i]) and pos[i] != 0 and np.isfinite(fc[i]) and fc[i] != 0):
                    continue
                if i + H >= n:
                    continue  # runs past window end
                c0, c1 = cv[i], cv[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 != 0 and np.isfinite(coin_mean)):
                    continue
                r = c1 / c0 - 1.0
                cases.append({
                    "coin": coin,
                    "x": float(np.sign(fc[i]) * (r - coin_mean)),
                    "vol": float(vol[i]) if np.isfinite(vol[i]) else np.nan,
                })

    main_name = "mean signed 24-bar return of Monday 00:00 cases minus coin's mean non-overlapping 24-bar return, before costs"
    threshold = "confirm: positive with t >= 2 and positive check; reject: negative with t <= -2; else inconclusive; at least 100 cases"
    reading = ("The Monday 00:00 bar is the bar whose start timestamp + 1h is Monday 00:00 UTC; the Sunday move's sign is the recorded raw component (24-bar return from closes when missing); "
               "a case needs a non-zero position and forecast on that bar, the 24 bars are counted in rows of the same window, cases are pooled over coins, "
               "the volatility needs a full 720 hourly returns inside the window, and cases exactly at a coin's median are in neither group.")

    if active_total == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases with a position": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than 100 cases with a position exist.",
            "reading": reading,
        }

    agreement = active_agree / active_total
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are Monday 00:00 bars whose forecast is "
                           "opposite to Sunday's 24-bar move, as the plan's situation and side require."),
            "reading": reading,
        }

    x = np.array([c["x"] for c in cases], dtype=float)
    ncases = int(len(x))
    mean = float(np.mean(x)) if ncases > 0 else None
    t = None
    if ncases > 1:
        sd = float(np.std(x, ddof=1))
        t = float(mean / (sd / np.sqrt(ncases))) if sd > 0 else None

    # supporting check
    above, below = [], []
    for coin in sorted(set(c["coin"] for c in cases)):
        cc = [c for c in cases if c["coin"] == coin and np.isfinite(c["vol"])]
        if not cc:
            continue
        med = float(np.median([c["vol"] for c in cc]))
        for c in cc:
            if c["vol"] > med:
                above.append(c["x"])
            elif c["vol"] < med:
                below.append(c["x"])
    if above and below:
        check_val = float(np.mean(above) - np.mean(below))
        check_pass = bool(check_val > 0)
    else:
        check_val = None
        check_pass = None

    counts = {
        "cases with a position": ncases,
        "cases above volatility median": int(len(above)),
        "cases below volatility median": int(len(below)),
    }

    if ncases < 100:
        status = "not observable"
        decided = f"Only {ncases} cases with a position, fewer than the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the main measure cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t >= 2:
        if check_pass is True:
            status = "confirmed"
            decided = "The main measure is positive with t >= 2 and the supporting check is positive."
        else:
            status = "inconclusive"
            decided = "The main measure is positive with t >= 2 but the supporting check is not positive, which the plan calls inconclusive."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The main measure is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean signed excess return above minus below each coin's median 720-bar volatility",
            "value": check_val,
            "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
