import json
import numpy as np
import pandas as pd


def _component_value(df, comp_id, field="last_history_value"):
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").to_numpy(dtype=float)
    out = np.full(len(df), np.nan)
    if "debug_info.components" not in df.columns:
        return out
    for i, d in enumerate(df["debug_info.components"].tolist()):
        if isinstance(d, str):
            try:
                d = json.loads(d)
            except Exception:
                d = None
        if isinstance(d, dict):
            c = d.get(comp_id)
            if isinstance(c, str):
                try:
                    c = json.loads(c)
                except Exception:
                    c = None
            if isinstance(c, dict):
                v = c.get(field)
                try:
                    out[i] = float(v) if v is not None else np.nan
                except Exception:
                    out[i] = np.nan
    return out


def _price_run(close, max_bars=30):
    """Count of consecutive down closes before an up close at t; nan when undeterminable."""
    n = len(close)
    run = np.zeros(n)
    det = np.ones(n, dtype=bool)
    for t in range(n):
        if t == 0:
            det[t] = False
            run[t] = np.nan
            continue
        if not (close[t] > close[t - 1]):
            run[t] = 0
            continue
        k = 0
        j = t - 1
        reached_start = False
        while k < max_bars:
            if j - 1 < 0:
                reached_start = True
                break
            if close[j] < close[j - 1]:
                k += 1
                j -= 1
            else:
                break
        run[t] = k
        if reached_start:
            det[t] = False
    return run, det


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    MIN_DAYS = 30

    # ---------- situation check ----------
    active_total = 0
    active_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            rec = _component_value(df, "run_len")
            run_p, det = _price_run(close, 30)
            for t in range(len(df)):
                if fc[t] == 0:
                    continue
                active_total += 1
                if det[t]:
                    sit = run_p[t] >= 2
                else:
                    sit = (not np.isnan(rec[t])) and rec[t] >= 2
                if sit and fc[t] > 0:
                    active_ok += 1
    agreement = (active_ok / active_total) if active_total > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 5-bar move of cases (forecast rise >= 2, one per 5-bar grid cell)"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and run-length slope > 0; reject: mean < 0 with t <= -2"
    reading = ("Situation recomputed from closes as an up close after >= 2 consecutive down closes (recorded run_len used "
               "only where the run reaches the window start), long side, the profile filter left to the regime detector; "
               "the plan's 'fewer than 30 cases on 30 days' is reported as not observable; the clustered t uses a D/(D-1) "
               "correction so it equals the ordinary t with one case per day; the case's run length is run_len's "
               "last_history_value on the case bar.")

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "active bars in situation on long side": int(active_ok)},
            "decided_by": (f"Only {agreement:.1%} of the bars with a non-zero forecast are long bets on an up close after "
                           "2 or more down closes, below the 90 % the plan's situation requires."),
            "reading": reading,
        }

    # ---------- normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    xs, days, runs = [], [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            rec = _component_value(df, "run_len")
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[t] = True
                    low = f
                else:
                    low = min(low, f)
            for start in range(0, n, H):
                cell = np.where(bet[start:start + H])[0]
                if len(cell) == 0:
                    continue
                t = start + int(cell[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                d = drift.get(coin, np.nan)
                if not np.isfinite(d):
                    continue
                xs.append(close[t + H] / close[t] - 1.0 - d)
                days.append(ts.iloc[t].strftime("%Y-%m-%d"))
                runs.append(rec[t])

    xs = np.array(xs, dtype=float)
    runs = np.array(runs, dtype=float)
    n_cases = int(len(xs))
    n_days = int(len(set(days)))

    mean = float(np.mean(xs)) if n_cases > 0 else None
    tstat = None
    if n_cases > 1 and n_days > 1:
        dev = pd.Series(xs - mean).groupby(pd.Series(days)).sum().to_numpy()
        D = len(dev)
        var = (D / (D - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        tstat = float(mean / se) if se > 0 else None

    slope = None
    m = np.isfinite(runs) & np.isfinite(xs)
    if m.sum() >= 2 and len(np.unique(runs[m])) >= 2:
        slope = float(np.polyfit(runs[m], xs[m], 1)[0])
    sup_passed = (slope > 0) if slope is not None else None

    counts = {"cases": n_cases, "distinct days": n_days}
    main = {"name": main_name, "value": mean,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": tstat}
                          if tstat is not None else None),
            "threshold": threshold}
    support = {"name": "least-squares slope of unusual moves on run_len", "value": slope,
               "passed": (bool(sup_passed) if sup_passed is not None else None)}
    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": passed}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": support, "counts": counts,
                "decided_by": f"The plan needs at least 30 cases on at least 30 distinct days; the record has {n_cases} cases on {n_days} days.",
                "reading": reading}

    if tstat is None:
        status = "inconclusive"
        decided = "The t could not be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif mean > 0 and tstat >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The main measure is above 0 with t >= 2 and the run-length slope is above 0: the confirm rule."
        else:
            status = "inconclusive"
            decided = "The main measure is above 0 with t >= 2 but the run-length slope is 0, negative or undefined: inconclusive by the plan."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The main measure is below 0 with t <= -2: the reject rule."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2: inconclusive by the plan."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": support, "counts": counts,
            "decided_by": decided, "reading": reading}
