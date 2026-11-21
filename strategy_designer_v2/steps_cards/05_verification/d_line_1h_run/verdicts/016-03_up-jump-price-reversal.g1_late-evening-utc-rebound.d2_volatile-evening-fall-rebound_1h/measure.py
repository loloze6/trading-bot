import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        mx = float(np.nanmax(np.abs(s.values.astype(float)))) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        if mx > 1e14:
            unit = "us"
        if mx > 1e17:
            unit = "ns"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 24
    RAW = "debug_info.components.fall24.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            active = fc != 0
            if not active.any():
                continue
            ts = _to_utc(df["timestamp"])
            # bar closing at 20:00 UTC starts at 19:00 UTC
            close_hour = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            close = pd.to_numeric(df["close"], errors="coerce")
            chg_prices = (close / close.shift(H) - 1.0).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
                chg = np.where(np.isfinite(raw), raw, chg_prices)
            else:
                chg = chg_prices
            fell = np.isfinite(chg) & (chg < 0)
            high_vol = (df["regime"].astype(str) == "mean_reversion").values
            situ = (close_hour == 20) & fell & high_vol
            ok = situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((ok & active).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The bar 'closing at 20:00 UTC' is the bar whose start timestamp is 19:00 UTC; the fall is the recorded "
               "raw 24-bar change (recomputed from closes where missing) below 0; the high-volatility condition is read "
               "from the recorded regime 'mean_reversion' since the detector's volatility rank is not recorded; the "
               "coin's mean 24-bar return uses the non-overlapping grid 0,24,48,... of every window pooled per coin; "
               "the t of the forecast-weighted mean uses the weighted standard error "
               "sqrt(n/(n-1)*sum(w^2(x-m)^2))/sum(w); thirds are equal-size splits of the cases sorted by forecast and "
               "compared on unweighted mean excess return.")

    main_name = "forecast-weighted mean excess 24-bar forward return of forecast>0 cases"
    main_thr = "confirm: positive with t >= 2 (and top-minus-bottom third > 0); reject: negative with t <= -2; at least 100 pooled cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"pooled cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bets on bars closing at 20:00 UTC "
                           "after a 24-bar fall in the high-volatility regime, so the config does not do what the "
                           "plan's Fidelity says." if n_active > 0 else
                           "The record has no bar with a non-zero forecast, so the config never takes the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ws = [], []
    for coin in bars:
        grid_rets = []
        cases = []
        for w in bars[coin]:
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fwd = (close.shift(-H) / close - 1.0).values
            idx = np.arange(0, len(df), H)
            g = fwd[idx]
            grid_rets.extend(list(g[np.isfinite(g)]))
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            m = np.isfinite(fc) & (fc > 0) & np.isfinite(fwd)
            for f, r in zip(fc[m], fwd[m]):
                cases.append((float(f), float(r)))
        if not cases or not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for f, r in cases:
            xs.append(r - mu)
            ws.append(f)

    x = np.asarray(xs, dtype=float)
    wt = np.asarray(ws, dtype=float)
    n = int(len(x))

    value = None
    tval = None
    diff = None
    if n >= 2 and wt.sum() > 0:
        sw = wt.sum()
        value = float(np.sum(wt * x) / sw)
        se = np.sqrt(n / (n - 1.0) * np.sum(wt ** 2 * (x - value) ** 2)) / sw
        tval = float(value / se) if se > 0 else (float(np.sign(value)) * np.inf if value != 0 else 0.0)
    if n >= 3:
        order = np.argsort(wt, kind="mergesort")
        parts = np.array_split(order, 3)
        diff = float(np.mean(x[parts[2]]) - np.mean(x[parts[0]]))
    sup_pass = None if diff is None else bool(diff > 0)

    if n < 100:
        status = "not observable"
        decided = f"Only {n} pooled cases with forecast > 0, fewer than the plan's minimum of 100, so neither a confirm nor a reject is possible."
    elif value is not None and tval is not None and value > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is positive with t >= 2 and the top-minus-bottom-third difference is above 0."
    elif value is not None and tval is not None and value < 0 and tval <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is negative with t <= -2."
    elif tval is not None and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-minus-bottom-third difference is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    def _num(v):
        if v is None:
            return None
        v = float(v)
        return v if np.isfinite(v) else (1e308 if v > 0 else -1e308)

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": _num(value),
            "statistic": None if tval is None else {"name": "t of the forecast-weighted mean", "value": _num(tval)},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "top-third minus bottom-third mean excess 24-bar return",
            "value": _num(diff),
            "passed": sup_pass,
        },
        "counts": {"pooled cases": n},
        "decided_by": decided,
        "reading": reading,
    }
