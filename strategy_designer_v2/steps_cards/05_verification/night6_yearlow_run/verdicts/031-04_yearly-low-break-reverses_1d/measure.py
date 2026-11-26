import json
import numpy as np
import pandas as pd

H = 10
BAND = 2.0
MIN_CASES = 20
MIN_DAYS = 15
COMP = "depth"


def _lhv(df, comp=COMP):
    """Raw value of a strategy component (last_history_value); NaN where it is not recorded."""
    flat = "debug_info.components.%s.last_history_value" % comp
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").to_numpy(dtype=float)
    out = np.full(len(df), np.nan)
    if "debug_info.components" not in df.columns:
        return out
    for i, v in enumerate(df["debug_info.components"].tolist()):
        d = v
        if isinstance(d, str):
            try:
                d = json.loads(d)
            except Exception:
                d = None
        if isinstance(d, dict):
            c = d.get(comp)
            if isinstance(c, str):
                try:
                    c = json.loads(c)
                except Exception:
                    c = None
            if isinstance(c, dict):
                x = c.get("last_history_value")
                try:
                    out[i] = float(x)
                except (TypeError, ValueError):
                    pass
    return out


def _bets(fc):
    """Bars where the forecast rises on the long side by at least the band from its lowest level since the last bet."""
    n = len(fc)
    is_bet = np.zeros(n, dtype=bool)
    ref = 0.0
    for i in range(n):
        f = fc[i]
        if not np.isfinite(f) or f <= 0:
            ref = 0.0
            continue
        if f - ref >= BAND - 1e-12:
            is_bet[i] = True
            ref = f
        else:
            ref = min(ref, f)
    return is_bet


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            raw = _lhv(df)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            situ = np.isfinite(raw) & (raw < 0)
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 10-bar move after long bets in the mean_reversion regime"
    main_thr = "confirm: mean > 0 with t >= 2 and deeper half beats shallower; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars whose close lies below "
                           "the prior 365-day lowest close (depth raw value < 0), so the config does not do what the "
                           "Fidelity's situation and long side say."),
            "reading": "The situation is read from the recorded raw value of the 'depth' component (same as the detector's), a bar without it counting as outside the situation.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, ret, forecast)
    drift = {}
    for coin in sorted(bars):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            # holding-the-coin grid
            for p in range(0, n, H):
                if p + H < n and np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            is_bet = _bets(fc) & (reg == "mean_reversion")
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if is_bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not (np.isfinite(close[t]) and np.isfinite(close[t + H])) or close[t] <= 0:
                    continue
                if pd.isna(ts.iloc[t]):
                    continue
                r = close[t + H] / close[t] - 1.0
                coin_cases.append((coin, ts.iloc[t].normalize(), r, fc[t]))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        cases.extend(coin_cases)

    rows = [(c, d, r - drift[c], f) for (c, d, r, f) in cases if np.isfinite(drift.get(c, np.nan))]
    n_cases = len(rows)
    days = pd.Series([r[1] for r in rows])
    n_days = int(days.nunique()) if n_cases else 0
    u = np.array([r[2] for r in rows], dtype=float)
    f = np.array([r[3] for r in rows], dtype=float)

    mean_u = float(np.mean(u)) if n_cases else None
    t_stat = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(u - mean_u).groupby(days.values).sum().to_numpy()
        D = len(dev)
        var = (D / (D - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
        if var > 0:
            t_stat = float(mean_u / np.sqrt(var))

    diff = None
    chk = None
    if n_cases >= 2:
        med = float(np.median(f))
        deep = u[f > med]
        shallow = u[f <= med]
        if len(deep) > 0 and len(shallow) > 0:
            diff = float(np.mean(deep) - np.mean(shallow))
            chk = bool(diff > 0)

    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = ("Minimum not reached: %d cases (need 20) on %d distinct days (need 15)." % (n_cases, n_days))
    elif t_stat is not None and mean_u > 0 and t_stat >= 2 and chk is True:
        status = "confirmed"
        decided = "Confirm rule met: mean unusual move above 0 with t >= 2, and the deeper-break half's mean exceeds the shallower half's."
    elif t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Reject rule met: mean unusual move below 0 with t <= -2."
    else:
        status = "inconclusive"
        if t_stat is not None and t_stat >= 2 and mean_u > 0:
            decided = "Inconclusive rule: t >= 2 but the depth check (deeper half minus shallower half > 0) fails."
        else:
            decided = "Inconclusive rule: t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, same-day cases summed", "value": t_stat}
                                       if t_stat is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": "deeper-break half minus shallower half mean unusual move (split at median forecast)",
                             "value": diff, "passed": chk},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are the first long bet (forecast rise >= 2 from its lowest level since the last bet, reset at 0) "
                    "in the mean_reversion regime in each 10-bar grid cell from each window's first row, dropped when the "
                    "10-bar return leaves the window; the drift is the coin's mean grid 10-bar return over all windows; the t "
                    "sums deviations per UTC day with a D/(D-1) correction; the deeper half is forecast above the median and "
                    "the shallower half forecast at or below it; the plan's 'fewer than 20 cases or 15 days' minimum is "
                    "reported as not observable."),
    }
