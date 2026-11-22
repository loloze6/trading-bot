import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 48
    MIN_CASES = 100
    COMP = "debug_info.components.weekend_move.last_history_value"
    bar_len = pd.Timedelta(hours=1)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ts = _to_utc(df["timestamp"])
            close_time = ts + bar_len
            # the bar closing at Monday 00:00 UTC
            cal = ((close_time.dt.dayofweek == 0) & (close_time.dt.hour == 0)
                   & (close_time.dt.minute == 0)).values
            # calm regime: 720-bar vol vs its 4320-bar mean cannot be rebuilt
            # inside a window (needs 5040 bars), so the detector's decision is used
            calm = (df["regime"].astype(str).values == "trending")
            # weekend move: raw component value, else 48-bar return from prices
            if COMP in df.columns:
                move = pd.to_numeric(df[COMP], errors="coerce").values.astype(float)
            else:
                move = np.full(len(df), np.nan)
            px_move = np.full(len(df), np.nan)
            if len(df) > H:
                px_move[H:] = close[H:] / close[:-H] - 1.0
            move = np.where(np.isnan(move), px_move, move)

            active = fc != 0
            n_active += int(active.sum())
            side_ok = np.sign(fc) == np.sign(move)
            ok = active & cal & calm & side_ok & ~np.isnan(move)
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The bar 'closing at Monday 00:00 UTC' is the bar whose start timestamp plus one hour is Monday 00:00; "
               "the calm-volatility part of the situation is taken from the recorded regime ('trending') because the "
               "720/4320-bar volatility ratio cannot be rebuilt inside one window; the side is the sign of the recorded "
               "48-bar raw return (prices where missing); the coin's mean 48-bar return is taken on the non-overlapping "
               "grid of all its windows; cases are all trending bars with |forecast| >= 2 having 48 bars left in their "
               "window, each counted once.")

    main_name = "mean of (forecast/10) x (48-bar return minus coin's mean 48-bar return) over the bets"
    threshold = "confirm: mean > 0 with t >= 2 over >= 100 cases; reject: mean < 0 with t <= -2 over >= 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on its side": int(n_agree)},
            "decided_by": (f"Only {agreement:.1%} of the active bars are bars closing at Monday 00:00 UTC in the calm "
                           "regime with the forecast on the weekend move's side; the plan requires at least 90%."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    values = []
    n_bets_all = 0
    for coin, wins in bars.items():
        # coin's mean 48-bar return over all its windows, non-overlapping grid
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            grid_rets.extend(r[np.isfinite(r)].tolist())
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            reg = df["regime"].astype(str).values
            sel = np.where((reg == "trending") & np.isfinite(fc) & (np.abs(fc) >= 2))[0]
            n_bets_all += len(sel)
            for i in sel:
                if i + H >= len(c):
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                values.append((fc[i] / 10.0) * (r - mu))

    n = len(values)
    mean = float(np.mean(values)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(values, ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    counts = {
        "bets (trending, |forecast| >= 2)": int(n_bets_all),
        "cases with a full 48 bars left inside their window": int(n),
    }

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases with a full 48 bars left inside their window, below the plan's minimum of 100."
    elif t is not None and mean > 0 and t >= 2:
        status = "confirmed"
        decided = f"The mean is positive with t = {t:.2f} >= 2 over {n} >= 100 cases (confirm rule)."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = f"The mean is negative with t = {t:.2f} <= -2 over {n} >= 100 cases (reject rule)."
    else:
        status = "inconclusive"
        tt = "undefined" if t is None else f"{t:.2f}"
        decided = f"The t of the mean ({tt}) lies between -2 and 2 over {n} cases (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
