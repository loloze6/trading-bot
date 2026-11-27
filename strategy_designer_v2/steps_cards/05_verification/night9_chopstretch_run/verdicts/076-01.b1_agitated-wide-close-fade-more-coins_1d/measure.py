import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.wide_high_close.last_history_value"
    WIDTH_MIN = 1.5
    EPS = 1e-9

    # ---------- coin drift: mean 1-bar return over all windows of the coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            c = df["close"].astype(float).values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        drift[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- situation check + collect cases ----------
    n_active = 0
    n_agree = 0
    cases = []  # (day, short-side unusual move, |forecast|)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            o = df["open"].astype(float)
            h = df["high"].astype(float)
            l = df["low"].astype(float)
            c = df["close"].astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            reg = df["regime"].astype(str)
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            rng = h - l
            # price-based width: range / mean range over last 20 bars including this bar
            width_px = rng / rng.rolling(20, min_periods=20).mean()
            # component-based width: raw = (close-low)/base  ->  width = range*raw/(close-low)
            cl = c - l
            width_comp = pd.Series(np.where((cl > EPS) & raw.notna() & (raw > 0),
                                            rng * raw / cl.where(cl > EPS), np.nan), index=df.index)
            nxt = c.shift(-1) / c - 1.0
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(len(df)):
                if f.iloc[i] == 0:
                    continue
                n_active += 1
                agitated = reg.iloc[i] == "mean_reversion"  # veto (profile) passed and width rule met
                if np.isfinite(width_comp.iloc[i]):
                    wide = width_comp.iloc[i] >= WIDTH_MIN - 1e-6
                elif np.isfinite(width_px.iloc[i]):
                    wide = width_px.iloc[i] >= WIDTH_MIN - 1e-6
                else:
                    wide = agitated
                near_high_ok = (not np.isfinite(raw.iloc[i])) or raw.iloc[i] >= -EPS
                side_ok = f.iloc[i] < 0
                if agitated and wide and near_high_ok and side_ok:
                    n_agree += 1
            for i in range(len(df) - 1):
                if f.iloc[i] < 0 and np.isfinite(nxt.iloc[i]) and np.isfinite(drift[coin]):
                    x = -(nxt.iloc[i] - drift[coin])
                    cases.append((ts.iloc[i].normalize(), float(x), float(abs(f.iloc[i]))))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    main_name = "mean short-side unusual next-bar move on forecast<0 bars"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of active bars are short bars of an agitated day with range >= 1.5x its 20-day mean range, as the Fidelity's situation requires.",
            "reading": "Agitated profile read from the recorded regime (the detector's volatility component is not recorded and needs 365 bars); width rebuilt from the component's own base, else from 20-bar high-low mean in the window.",
        }

    n_cases = len(cases)
    days = pd.Series([d for d, _, _ in cases])
    n_days = int(days.nunique()) if n_cases else 0
    x = np.array([v for _, v, _ in cases]) if n_cases else np.array([])
    a = np.array([v for _, _, v in cases]) if n_cases else np.array([])

    mean = float(np.mean(x)) if n_cases else None
    t = None
    if n_cases > 1:
        dev = pd.Series(x - mean).groupby(days.values).sum()
        se = np.sqrt(np.sum(dev.values ** 2)) / n_cases
        if n_days > 1:
            se *= np.sqrt(n_days / (n_days - 1))
        t = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 1:
        med = np.median(a)
        big = x[a > med]
        small = x[a <= med]
        if len(big) and len(small):
            sup_val = float(np.mean(big) - np.mean(small))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"distinct days with a case": n_days, "cases": int(n_cases)}
    reading = ("Agitated profile read from the recorded regime; cases are every forecast<0 bar with a next close in its window "
               "(1-bar grid, no overlap); the day-clustered t sums deviations per UTC day with a small-sample factor d/(d-1); "
               "the larger half is |forecast| strictly above the median, the smaller half at or below it.")

    if n_days < 100 or t is None:
        status = "not observable"
        decided = f"Only {n_days} distinct days with a case, below the plan's minimum of 100."
    elif t >= 2 and mean > 0 and sup_pass:
        status = "confirmed"
        decided = "Mean short-side unusual move above 0 with t >= 2 and the larger-|forecast| half beats the smaller half."
    elif t <= -2:
        status = "rejected"
        decided = "Mean short-side unusual move has t <= -2: these days rise more than the coin's drift."
    elif t >= 2 and mean > 0:
        status = "inconclusive"
        decided = "Confirming t with a failed supporting check."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean, cases of one day together", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean move of larger |forecast| half minus smaller half", "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
