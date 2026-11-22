import numpy as np
import pandas as pd


def measure(bars):
    H = 48
    FC = "forecast"
    RAW = "debug_info.components.thin_weekend_rise.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float).values
            vol = d["volume"].astype(float).values
            fc = d[FC].astype(float).values
            raw = d[RAW].astype(float).values if RAW in d.columns else np.full(len(d), np.nan)
            regime = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * len(d))
            active = np.where(np.isfinite(fc) & (fc != 0))[0]
            for i in active:
                n_active += 1
                t = ts.iloc[i]
                # bar whose next bar starts Monday 00:00 UTC: Sunday 23:00 start
                is_time = (t.dayofweek == 6) and (t.hour == 23)
                # weekend rise: component raw value (weekend 48-bar return, scaled) if recorded, else price return
                if np.isfinite(raw[i]):
                    rose = raw[i] > 0
                elif i >= H and close[i - H] > 0:
                    rose = close[i] / close[i - H] - 1 > 0
                else:
                    rose = False
                # thin weekend: mean volume of last 48 bars < mean of the 120 bars before them
                if i >= H + 120 - 1 + 0 and i - H - 120 + 1 >= 0:
                    wk_end = vol[i - H + 1:i + 1]
                    wk_day = vol[i - H - 120 + 1:i - H + 1]
                    md = np.nanmean(wk_day)
                    thin = (md > 0) and (np.nanmean(wk_end) / md < 1.0)
                else:
                    thin = regime[i] == "mean_reversion"
                short = fc[i] < 0
                if is_time and rose and thin and short:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "|forecast|-weighted mean short-side 48-bar unusual move per weekend case"
    thr = "confirm: weighted mean > 0 with t >= 2 and supporting check passing; reject: weighted mean < 0 with t <= -2"
    reading = ("Situation bars are Sunday 23:00 UTC bars with a positive weekend 48-bar rise (component raw value, else price return) "
               "and last-48-bar mean volume below the prior 120 bars' mean (regime used when history is short); drift is the coin's mean "
               "48-bar return on the non-overlapping grid of all its windows; the t is that of the |forecast|-weighted mean "
               "(weighted-residual standard error with n/(n-1) correction); the halves split all cases pooled by sorted |forecast| "
               "(smaller half gets the extra case when odd) with unweighted half means; fewer than 100 cases is treated as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of nonzero-forecast bars are short forecasts on Sunday 23:00 bars after a weekend rise "
                           "on thin weekend volume, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    rets.append(c[p + H] / c[p] - 1)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    xs, ws = [], []
    for coin, wins in bars.items():
        dr = drift.get(coin, np.nan)
        if not np.isfinite(dr):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).values
            fc = d[FC].astype(float).values
            active = np.where(np.isfinite(fc) & (fc != 0))[0]
            for i in active:
                if i + H >= len(c) or not (c[i] > 0) or not np.isfinite(c[i + H]):
                    continue
                r = c[i + H] / c[i] - 1
                direction = -1.0 if fc[i] < 0 else 1.0
                xs.append(direction * (r - dr))
                ws.append(abs(fc[i]))
    xs = np.array(xs, dtype=float)
    ws = np.array(ws, dtype=float)
    n = len(xs)
    counts = {"cases": int(n)}

    value, tval = None, None
    if n >= 2 and ws.sum() > 0:
        m = float(np.sum(ws * xs) / np.sum(ws))
        se = np.sqrt(np.sum(ws ** 2 * (xs - m) ** 2) * n / (n - 1)) / np.sum(ws)
        value = m
        tval = float(m / se) if se > 0 else (float("inf") if m > 0 else (float("-inf") if m < 0 else 0.0))
    elif n == 1:
        value = float(xs[0])

    sup_val, sup_pass = None, None
    if n >= 2:
        order = np.argsort(ws, kind="mergesort")
        k = n // 2
        small = xs[order[:n - k]]
        large = xs[order[n - k:]]
        sup_val = float(np.mean(large) - np.mean(small))
        sup_pass = bool(sup_val > 0)

    stat = {"name": "t of the weighted mean", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": value, "statistic": stat, "threshold": thr}
    sup = {"name": "mean unusual move, larger half of |forecast| minus smaller half",
           "value": sup_val, "passed": sup_pass}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases over all coins and windows, below the plan's minimum of 100."
    elif tval is not None and value > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Weighted mean short-side unusual move above 0 with t >= 2, and the larger-|forecast| half beats the smaller half."
    elif tval is not None and value < 0 and tval <= -2:
        status = "rejected"
        decided = "Weighted mean short-side unusual move below 0 with t <= -2: weekend rises are followed by further rises."
    elif tval is not None and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (larger half above smaller half) fails."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
