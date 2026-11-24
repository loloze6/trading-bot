import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    LH = "debug_info.components.range_mult.last_history_value"

    # ---------- situation check ----------
    n_active_eval = 0
    n_agree = 0
    n_active_unevaluable = 0

    drift_by_coin = {}
    cases = []  # (coin, day, move_raw, forecast)

    for coin, wins in bars.items():
        coin_grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            high = pd.to_numeric(df["high"], errors="coerce").to_numpy(dtype=float)
            low = pd.to_numeric(df["low"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)

            # ret20 recomputed from prices, inside the window only
            ret20 = np.full(n, np.nan)
            if n > 20:
                ret20[20:] = close[20:] / close[:-20] - 1.0
            # wide-range multiple: recorded raw value, else recomputed (range / mean of last 20 ranges, bar included)
            if LH in df.columns:
                wr = pd.to_numeric(df[LH], errors="coerce").to_numpy(dtype=float)
            else:
                wr = np.full(n, np.nan)
            rng = pd.Series(high - low)
            wr_re = (rng / rng.rolling(20, min_periods=20).mean()).to_numpy(dtype=float)
            wr = np.where(np.isnan(wr), wr_re, wr)

            for i in range(n):
                if fc[i] != 0:
                    if np.isnan(ret20[i]) or np.isnan(wr[i]):
                        n_active_unevaluable += 1
                        continue
                    n_active_eval += 1
                    if ret20[i] > 0 and wr[i] >= 1.5 - 1e-9 and fc[i] > 0:
                        n_agree += 1

            # ---------- coin's 3-bar returns on the non-overlapping grid ----------
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    coin_grid_rets.append(r)

            # ---------- bets (rise of the long forecast of at least the band) ----------
            bet = np.zeros(n, dtype=bool)
            base = 0.0
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    base = 0.0
                    continue
                if f - base >= BAND - 1e-12:
                    bet[i] = True
                    base = f
                else:
                    base = min(base, f)

            # one case per 3-bar grid cell: its first bet into the trending regime
            for start in range(0, n, H):
                for i in range(start, min(start + H, n)):
                    if bet[i] and regime[i] == "trending":
                        if i + H < n:
                            r = close[i + H] / close[i] - 1.0
                            if np.isfinite(r) and not pd.isna(ts.iloc[i]):
                                coin_cases.append((coin, ts.iloc[i].strftime("%Y-%m-%d"), r, fc[i]))
                        break
        drift_by_coin[coin] = float(np.mean(coin_grid_rets)) if coin_grid_rets else np.nan
        cases.extend(coin_cases)

    agreement = (n_agree / n_active_eval) if n_active_eval > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.90)

    reading = ("Bets are rises of the long forecast of at least 2 points from its lowest level since the last bet "
               "(reset at flat), each 3-bar grid cell counted once at its first bet on a 'trending' bar, the move "
               "taken from that bar's close over the next 3 bars inside the window; the coin's mean 3-bar return is "
               "over its non-overlapping grid of all windows; the main t clusters deviations by UTC day; the slope t "
               "is the ordinary OLS t; active bars whose 20-day return cannot be computed inside the window "
               f"({n_active_unevaluable}) are left out of the situation check; the plan's 'fewer than 30 cases or "
               "30 days' rule is reported as 'not observable' as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active_eval)},
            "decided_by": ("Fewer than 90% of the active bars are long bars with a positive 20-day return and a "
                           "range at least 1.5 times its 20-day mean, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- main measure ----------
    moves, fcs, days = [], [], []
    for coin, day, r, f in cases:
        d = drift_by_coin.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        moves.append(r - d)
        fcs.append(f)
        days.append(day)
    moves = np.array(moves, dtype=float)
    fcs = np.array(fcs, dtype=float)
    n_cases = int(len(moves))
    n_days = int(len(set(days)))

    mean_move = float(np.mean(moves)) if n_cases > 0 else None
    t_main = None
    if n_cases > 1 and n_days > 1:
        dev = pd.Series(moves - mean_move, index=days).groupby(level=0).sum().to_numpy()
        D = len(dev)
        var_m = (dev ** 2).sum() / (n_cases ** 2) * D / (D - 1)
        if var_m > 0:
            t_main = float(mean_move / np.sqrt(var_m))

    slope, t_slope = None, None
    if n_cases > 2 and np.std(fcs) > 0:
        lr = stats.linregress(fcs, moves)
        slope = float(lr.slope)
        if lr.stderr and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)
    slope_pass = None if t_slope is None else bool(slope > 0 and t_slope >= 2)

    main = {
        "name": "mean unusual 3-bar move per bet (return minus coin's mean 3-bar return)",
        "value": mean_move,
        "statistic": {"name": "t of the mean, cases clustered by day", "value": t_main} if t_main is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 (and slope check passes); reject: mean < 0 with t <= -2",
    }
    support = {"name": "OLS slope of unusual move on signal-bar forecast (t)", "value": t_slope, "passed": slope_pass}
    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases on 30 distinct days is not reached ({n_cases} cases, {n_days} days)."
    elif t_main is not None and mean_move > 0 and t_main >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the supporting slope is positive with t >= 2."
    elif t_main is not None and mean_move < 0 and t_main <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        if t_main is not None and mean_move > 0 and t_main >= 2:
            decided = "The mean unusual move is positive with t >= 2 but the supporting slope check fails."
        else:
            decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
