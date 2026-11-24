import numpy as np
import pandas as pd


def measure(bars):
    H = 30
    RAW = "debug_info.components.depth.last_history_value"

    def to_days(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            mx = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
            unit = "ns" if mx > 1e17 else ("us" if mx > 1e14 else ("ms" if mx > 1e11 else "s"))
            dt = pd.to_datetime(s, unit=unit, utc=True)
        else:
            dt = pd.to_datetime(s, utc=True)
        return dt.dt.floor("D").dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check: raw fall_z <= -1, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw <= -1.0 + 1e-12) & (f > 0)
            n_agree += int(ok.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else (agreement >= 0.90)

    main_name = "mean excess 30-day return after positive-forecast mean_reversion cases (minus the coin's mean 30-day return)"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; else inconclusive; at least 30 independent case-days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast have the raw 90-day mean-abs-scaled return at or below -1 with a positive (long) forecast, as the Fidelity's situation and side require.",
            "reading": "Active bars are those with forecast != 0; the situation is read from the recorded raw component value (depth.last_history_value <= -1), a bar where it is missing counting as not in the situation.",
        }

    # ---------- 2. coin mean 30-day return over all its windows (non-overlapping grid) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    xs, fs, days = [], [], []
    for coin, wins in bars.items():
        if not np.isfinite(coin_mean.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            d = to_days(df["timestamp"])
            for i in range(0, len(c) - H, H):
                if reg[i] != "mean_reversion" or not np.isfinite(f[i]) or f[i] <= 0:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                xs.append(c[i + H] / c[i] - 1.0 - coin_mean[coin])
                fs.append(float(f[i]))
                days.append(d[i])

    xs = np.array(xs, dtype=float)
    fs = np.array(fs, dtype=float)
    n_cases = int(len(xs))
    n_days = int(len(set(days)))

    mean_x = float(np.mean(xs)) if n_cases > 0 else None
    t_val = None
    if n_cases > 0 and n_days >= 2:
        dev = pd.Series(xs - mean_x).groupby(pd.Series(days)).sum().values
        G = len(dev)
        var_mean = (G / (G - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
        se = np.sqrt(var_mean)
        if se > 0:
            t_val = float(mean_x / se)

    # supporting check: top half by forecast minus bottom half
    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        order = np.argsort(fs, kind="mergesort")
        k = n_cases // 2
        low = xs[order[:k]]
        high = xs[order[n_cases - k:]]
        sup_val = float(np.mean(high) - np.mean(low))
        sup_pass = bool(sup_val > 0)

    counts = {"independent case-days": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} independent case-days across coins and windows, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_x > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean excess 30-day return is above 0 with t >= 2 and the larger-forecast half beats the smaller-forecast half."
        else:
            status = "inconclusive"
            decided = "The mean excess 30-day return is above 0 with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean_x < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean excess 30-day return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The day-clustered t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_x,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day taken together (day-clustered)", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess return of larger-forecast half minus smaller-forecast half > 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases are grid bars (positions 0, 30, 60, ... of each window with a full 30 bars ahead) whose regime is mean_reversion and forecast > 0; the coin's mean 30-day return is taken on the same grid over all its windows; the t sums the cases' deviations per UTC day with a G/(G-1) correction; with an odd number of cases the middle-forecast case is left out of both halves.",
    }
