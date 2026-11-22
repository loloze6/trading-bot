import numpy as np
import pandas as pd
from scipy import stats


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype("float64")
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 48
    RAW = "debug_info.components.weekend_move.last_history_value"
    MIN_CASES = 300

    n_active = 0
    n_agree = 0
    unusual_all = []
    absf_all = []

    for coin, wins in bars.items():
        prepared = []
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            ts = _to_utc(d["timestamp"]).reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).reset_index(drop=True)
            end = ts + pd.Timedelta(hours=1)
            monday0 = (end.dt.weekday == 0) & (end.dt.hour == 0) & (end.dt.minute == 0)

            # weekend return: the component's raw value, else recomputed from prices
            price_ret = close / close.shift(H) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").reset_index(drop=True)
                wk = raw.where(raw.notna(), price_ret)
            else:
                wk = price_ret
            rise = wk > 0

            # volatility rule (720 / 4320 bars) cannot be rebuilt inside a window: detector's decision
            if "regime" in d.columns:
                hivol = (d["regime"].astype(str).reset_index(drop=True) == "mean_reversion")
            else:
                hivol = pd.Series(True, index=d.index)

            situation = monday0 & rise & hivol
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            fwd = close.shift(-H) / close - 1.0
            # non-overlapping grid for the coin's normal drift
            idx = np.arange(0, len(close) - H, H)
            if len(idx):
                g = (close.values[idx + H] / close.values[idx]) - 1.0
                grid_rets.extend([x for x in g if np.isfinite(x)])
            prepared.append((fc, monday0, fwd))

        drift = float(np.mean(grid_rets)) if len(grid_rets) else np.nan
        for fc, monday0, fwd in prepared:
            case = (fc <= -2) & monday0 & fwd.notna()
            if not np.isfinite(drift):
                continue
            for i in np.where(case.values)[0]:
                u = -(float(fwd.iloc[i]) - drift)
                if np.isfinite(u):
                    unusual_all.append(u)
                    absf_all.append(abs(float(fc.iloc[i])))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    threshold = "mean unusual short move > 0 with t >= 2 (confirm); < 0 with t <= -2 (reject); at least 300 cases"
    reading = ("A case is a bar whose close (timestamp + 1 h) is Monday 00:00 UTC with forecast <= -2 and a full "
               "48-bar forward return in its window; the normal drift is each coin's mean 48-bar return on the "
               "non-overlapping grid of all its windows; the situation's volatility condition is read from the "
               "recorded regime since the 720/4320-bar ratio cannot be rebuilt inside a window, and the weekend "
               "rise from the component's raw 48-bar return (prices where missing).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bets on bars closing at "
                           "Monday 00:00 UTC after a weekend rise in a high-volatility regime."),
            "reading": reading,
        }

    u = np.array(unusual_all, dtype=float)
    a = np.array(absf_all, dtype=float)
    n = int(len(u))
    mean = float(np.mean(u)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(u, ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    corr = None
    if n > 2 and np.std(a) > 0 and np.std(u) > 0:
        corr = float(stats.pearsonr(a, u)[0])
    corr_pass = (corr > 0) if corr is not None else None

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases over all coins and windows, below the plan's minimum of 300."
    elif t is not None and mean > 0 and t >= 2:
        if corr_pass:
            status = "confirmed"
            decided = "Mean unusual short move positive with t >= 2 and correlation of abs(forecast) with it above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t >= 2 but the correlation of abs(forecast) with the unusual move is at or below 0."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual short move negative with t <= -2: weekend rises carry on in high-volatility weeks."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual short move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean 48-bar unusual move in the short direction after Monday 00:00 short bets",
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "correlation of abs(forecast) with the unusual move above 0",
            "value": corr,
            "passed": corr_pass,
        },
        "counts": {"cases over all coins and windows": n},
        "decided_by": decided,
        "reading": reading,
    }
