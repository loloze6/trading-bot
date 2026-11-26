import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    ER_P = 30
    R7_P = 7
    R30_P = 30
    ER_TH = 0.3
    FC = "forecast"
    RAW = "debug_info.components.scaled_week.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            absdiff = close.diff().abs()
            vol_sum = absdiff.rolling(ER_P, min_periods=ER_P).sum()
            net = (close - close.shift(ER_P)).abs()
            er = net / vol_sum
            r7 = close / close.shift(R7_P) - 1.0
            r30 = close / close.shift(R30_P) - 1.0
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            for i in range(len(d)):
                f = fc.iloc[i]
                if f == 0 or not np.isfinite(f):
                    continue
                n_active += 1
                e, a, b = er.iloc[i], r7.iloc[i], r30.iloc[i]
                if np.isfinite(e) and np.isfinite(a) and np.isfinite(b):
                    in_sit = (e <= ER_TH) and (np.sign(a) == np.sign(b)) and a != 0
                    side = np.sign(a)
                else:
                    # not enough in-window history: fall back on the detector's decision and the raw scaled move
                    in_sit = regime.iloc[i] == "chop"
                    rv = raw.iloc[i]
                    side = np.sign(rv) if np.isfinite(rv) else (np.sign(a) if np.isfinite(a) else 0)
                if in_sit and side != 0 and np.sign(f) == side:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("ER(30), the 7-day and 30-day returns are recomputed from each window's closes (ER = |close change over 30 bars| / sum of the 30 absolute daily changes); on bars without enough in-window history the detector's 'chop' regime and the sign of the raw scaled_week value stand in; "
               "the drift is the coin's mean 7-bar return on all grid bars of all its windows, the slope is a pooled OLS of drift-adjusted return on the forecast with its ordinary t, and the supporting t is a day-clustered t (deviations summed per day, G/(G-1) correction).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are aligned-chop bars (ER30 <= 0.3, 7-day and 30-day returns of the same sign) with the forecast on the side of the 7-day move."
                           if n_active > 0 else "No bar has a non-zero forecast, so the config never takes the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    drift = {}
    cases = []
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(0, len(d) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if fc[i] != 0 and np.isfinite(fc[i]):
                    cases.append((coin, float(fc[i]), r, ts.iloc[i].floor("D")))
        drift[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    rows = [(c, f, r - drift[c], day) for (c, f, r, day) in cases if np.isfinite(drift.get(c, np.nan))]
    n = len(rows)
    n_days = len(set(r[3] for r in rows))

    slope = slope_t = None
    sup_mean = sup_t = None
    if n >= 3:
        x = np.array([r[1] for r in rows])
        y = np.array([r[2] for r in rows])
        xm = x.mean()
        sxx = np.sum((x - xm) ** 2)
        if sxx > 0:
            b = np.sum((x - xm) * (y - y.mean())) / sxx
            a = y.mean() - b * xm
            resid = y - a - b * x
            s2 = np.sum(resid ** 2) / (n - 2)
            se = np.sqrt(s2 / sxx)
            slope = float(b)
            slope_t = float(b / se) if se > 0 else None
    if n >= 2:
        s = np.array([np.sign(r[1]) * r[2] for r in rows])
        days = [r[3] for r in rows]
        sup_mean = float(s.mean())
        dev = pd.Series(s - s.mean()).groupby(pd.Series(days)).sum().values
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * np.sum(dev ** 2) / (n ** 2)
            se = np.sqrt(var)
            sup_t = float(sup_mean / se) if se > 0 else None

    sup_pass = None
    if sup_mean is not None and sup_t is not None:
        sup_pass = bool(sup_mean > 0 and sup_t >= 2)

    if n < 30:
        status = "not observable"
        decided = f"Only {n} cases on the 7-bar grid with a non-zero forecast, below the plan's minimum of 30."
    elif slope is not None and slope_t is not None and slope < 0 and slope_t <= -2:
        status = "rejected"
        decided = "Reject: the slope is negative with t <= -2 (larger scaled moves are followed by larger reversals)."
    elif slope is not None and slope_t is not None and slope > 0 and slope_t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Confirm: the slope is positive with t >= 2 and the signed drift-adjusted mean is positive with day-clustered t >= 2, over at least 30 cases."
        else:
            status = "inconclusive"
            decided = "Inconclusive: the slope confirms but the supporting check's day-clustered t is below 2 (or its mean is not positive)."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of drift-adjusted 7-bar forward return on the forecast",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": slope_t} if slope_t is not None else None,
            "threshold": "slope positive with t >= 2 to confirm (with the supporting check); negative with t <= -2 to reject; at least 30 cases",
        },
        "supporting_check": {
            "name": "mean drift-adjusted 7-bar return signed by forecast, day-clustered t >= 2",
            "value": sup_mean,
            "passed": sup_pass,
        },
        "counts": {"cases": int(n), "days": int(n_days), "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
