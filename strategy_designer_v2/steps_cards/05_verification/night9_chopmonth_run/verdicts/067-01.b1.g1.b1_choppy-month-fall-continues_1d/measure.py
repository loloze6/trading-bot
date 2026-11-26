import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    RAW = "debug_info.components.month_fall.last_history_value"
    CHOPPY = "unknown"  # the regime that carries the strategy; the detector's vetoes turn trending markets into "chop"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce").values
            reg = d["regime"].astype(str).values
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
            else:
                raw = np.full(len(d), np.nan)
            for i in range(len(d)):
                if fc[i] == 0:
                    continue
                n_active += 1
                r = raw[i]
                if not np.isfinite(r) and i >= 30 and np.isfinite(close[i]) and np.isfinite(close[i - 30]) and close[i - 30] != 0:
                    r = (close[i] / close[i - 30] - 1.0) * 100.0
                fall = np.isfinite(r) and r < 0
                if fall and reg[i] == CHOPPY and fc[i] < 0:
                    n_agree += 1

    reading = ("Choppy is read as the bars whose regime is 'unknown' (the config's only traded regime, the trend vetoes "
               "giving 'chop'); a case is the first short bet (forecast more negative by >= 2 points from its smallest "
               "short size since the last bet, from 0 after a flat) in each 10-bar grid cell of a window, dropped if its "
               "10-bar return leaves the window; drift is the coin's mean 10-bar return on the grid of all its windows; "
               "the day-clustered t uses the sum of deviations per UTC day with a G/(G-1) correction; the 30-distinct-day "
               "minimum gives 'not observable'.")

    main_name = "mean unusual 10-bar move in the short direction of the short bets"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2 and size correlation > 0; reject: mean < 0 with t <= -2"
    supp_name = "correlation of |forecast| with the unusual short move"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": None},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": supp_name, "value": None, "passed": None},
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "The strategy never took a position, so there are no cases on the 30 distinct days the plan needs.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the active bars are short bars after a 30-day fall in the choppy regime: "
                           "the config's positions do not follow the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    xs, sizes, days = [], [], []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(d["close"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            ref = 0.0
            on_short = False
            used_cells = set()
            for i in range(len(d)):
                f = fc[i]
                if f >= 0:
                    on_short = False
                    ref = 0.0
                    continue
                a = -f
                if not on_short:
                    ref = 0.0
                    on_short = True
                bet = (a - ref) >= BAND
                if bet:
                    ref = a
                else:
                    ref = min(ref, a)
                    continue
                cell = i // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if i + H >= len(d):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                xs.append(-(r - drift[coin]))
                sizes.append(a)
                days.append(ts.iloc[i].floor("D"))

    xs = np.asarray(xs, dtype=float)
    sizes = np.asarray(sizes, dtype=float)
    n = len(xs)
    n_days = int(len(set(days)))

    mean = float(np.mean(xs)) if n else None
    t = None
    if n >= 2:
        dev = pd.Series(xs - mean).groupby(pd.Series(days)).sum().values
        G = len(dev)
        if G >= 2:
            var = (G / (G - 1)) * np.sum(dev ** 2) / (n ** 2)
            if var > 0:
                t = float(mean / np.sqrt(var))
    corr = None
    if n >= 3 and np.std(sizes) > 0 and np.std(xs) > 0:
        corr = float(np.corrcoef(sizes, xs)[0, 1])
    supp_passed = None if corr is None else bool(corr > 0)

    counts = {"cases": int(n), "distinct days": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"The cases fall on {n_days} distinct days, fewer than the 30 the plan requires."
    elif t is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t >= 2 and corr is not None and corr > 0:
        status = "confirmed"
        decided = "The mean unusual short move is positive with t >= 2 and the size correlation is above 0."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual short move is negative with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the size correlation is 0 or below (or not computable), so the plan calls it inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, so the idea is neither confirmed nor rejected."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if t is None else {"name": "t clustered by day", "value": t},
            "threshold": main_thr,
        },
        "supporting_check": {"name": supp_name, "value": corr, "passed": supp_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
