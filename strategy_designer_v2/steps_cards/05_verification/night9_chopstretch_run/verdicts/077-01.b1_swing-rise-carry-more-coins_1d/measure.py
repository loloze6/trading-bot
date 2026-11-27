import json
import numpy as np
import pandas as pd


def _component_series(df, comp_id, field="last_history_value"):
    col = f"debug_info.components.{comp_id}.{field}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        vals = []
        for v in df["debug_info.components"].tolist():
            out = np.nan
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict) and c.get(field) is not None:
                    try:
                        out = float(c.get(field))
                    except Exception:
                        out = np.nan
            vals.append(out)
        return pd.Series(vals, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def _vsr_from_prices(close, period=14, vol_period=30):
    ret = close.pct_change()
    vol = ret.rolling(vol_period, min_periods=vol_period).std()
    r14 = close / close.shift(period) - 1.0
    den = vol * np.sqrt(period)
    return r14 / den.replace(0, np.nan)


def measure(bars):
    H = 7
    BAND = 2.0
    THR = 2.0
    MIN_DAYS = 30

    n_active = 0
    n_agree = 0
    cases = []  # (day, unusual, forecast)

    for coin in sorted(bars.keys()):
        windows = bars[coin]
        # normal drift of the coin: mean 7-bar return on non-overlapping grid of all windows
        grid_rets = []
        prepared = {}
        for w in sorted(windows.keys()):
            df = windows[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            prepared[w] = (df, close)
            n = len(close)
            for i in range(0, n, H):
                if i + H < n:
                    c0, c1 = close.iloc[i], close.iloc[i + H]
                    if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                        grid_rets.append(c1 / c0 - 1.0)
        drift = float(np.mean(grid_rets)) if len(grid_rets) > 0 else np.nan

        for w, (df, close) in prepared.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(fc)
            # situation check
            vsr_rec = _component_series(df, "vsr").values
            vsr_px = _vsr_from_prices(close).values
            vsr = np.where(np.isfinite(vsr_rec), vsr_rec, vsr_px)
            active = fc != 0
            n_active += int(active.sum())
            agree = active & (fc > 0) & np.isfinite(vsr) & (vsr >= THR - 1e-9)
            n_agree += int(agree.sum())

            # bets: a rise of the long forecast of at least the band from its lowest level since last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND - 1e-12:
                    bet[i] = True
                    ref = f
                else:
                    ref = min(ref, f)

            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.floor("D").values
            cl = close.values
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                c0, c1 = cl[i], cl[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0 or not np.isfinite(drift):
                    continue
                r = c1 / c0 - 1.0
                cases.append((days[i], r - drift, float(fc[i])))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean unusual 7-day move per case (return minus coin's normal 7-day drift)"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 days with cases"
    reading = ("A case is the first bar of each 7-bar grid cell (positions 0, 7, 14, ... of each window) on which the long "
               "forecast rises at least 2 points from its lowest level since the last such rise (from 0 after flat), with "
               "its 7-bar return inside the window; the t clusters deviations by UTC day with a D/(D-1) correction; "
               "the situation is the recorded vsr value (recomputed from prices if missing) at least 2.0 with forecast > 0.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "days with cases": None},
            "decided_by": (f"Only {agreement:.1%} of active bars have a 14-day swing-scaled return of at least 2.0 with a "
                           f"long forecast, below the 90% the plan's situation requires."),
            "reading": reading,
        }

    n_cases = len(cases)
    if n_cases > 0:
        cdf = pd.DataFrame(cases, columns=["day", "u", "f"])
        n_days = int(cdf["day"].nunique())
    else:
        cdf = pd.DataFrame(columns=["day", "u", "f"])
        n_days = 0

    mean_u = float(cdf["u"].mean()) if n_cases > 0 else None
    t = None
    if n_cases > 0 and n_days >= 2:
        dev = cdf["u"] - mean_u
        s = dev.groupby(cdf["day"]).sum().values
        var = (n_days / (n_days - 1)) * float(np.sum(s ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        if se > 0:
            t = float(mean_u / se)

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        med = float(cdf["f"].median())
        hi = cdf.loc[cdf["f"] >= med, "u"]
        lo = cdf.loc[cdf["f"] < med, "u"]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"days with cases": n_days, "cases": n_cases, "active bars": int(n_active)}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} days with cases, fewer than the plan's minimum of 30."
    elif t is not None and mean_u > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 over at least 30 days with cases, and the larger-forecast cases show the larger mean unusual move."
    elif t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 over at least 30 days with cases."
    elif t is not None and mean_u > 0 and t >= 2:
        status = "inconclusive"
        decided = "t is 2 or more but the cases at or above the median forecast do not show a larger mean unusual move than those below."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (neither the confirm nor the reject rule is met)."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": passed},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t}
                                       if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move, forecast at/above median minus below median",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
