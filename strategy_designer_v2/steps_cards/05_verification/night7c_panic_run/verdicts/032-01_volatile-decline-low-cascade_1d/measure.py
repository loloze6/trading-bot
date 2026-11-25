import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_DAYS = 30

    def get_component(df, cid, field="last_history_value"):
        col = "debug_info.components.%s.%s" % (cid, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                val = np.nan
                if isinstance(v, dict):
                    c = v.get(cid)
                    if isinstance(c, dict):
                        x = c.get(field)
                        try:
                            val = float(x) if x is not None else np.nan
                        except (TypeError, ValueError):
                            val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = df["close"].astype(float).values
            low = df["low"].astype(float).values
            regime = df["regime"].astype(str).values
            depth = get_component(df, "depth").values
            n = len(df)
            # recompute ret30 and break depth from prices where 30 prior bars exist in the window
            ret30 = np.full(n, np.nan)
            brk = np.full(n, np.nan)
            for t in range(n):
                if t >= 30:
                    ret30[t] = close[t] / close[t - 30] - 1.0
                    prior_low = np.min(low[t - 30:t])
                    brk[t] = close[t] / prior_low - 1.0
            for t in range(n):
                if f[t] == 0:
                    continue
                n_active += 1
                ok = regime[t] == "trending"
                d = depth[t] if not np.isnan(depth[t]) else brk[t]
                if np.isnan(d):
                    ok = False  # break depth cannot be shown
                elif not d < 0:
                    ok = False
                if not np.isnan(ret30[t]) and not ret30[t] < 0:
                    ok = False
                ok = ok and f[t] < 0  # expected side: short
                if ok:
                    n_agree += 1

    reading_check = ("situation bars are those the detector labelled 'trending' (it alone holds the 365-day range "
                     "ratio, which a ~122-bar window cannot recompute) whose recorded raw depth (or price-recomputed "
                     "break) is below 0 and whose 30-bar return, recomputed from prices when 30 prior bars exist in "
                     "the window, is below 0, with a negative forecast")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": None},
            "main_measure": {"name": "mean short-signed 5-day unusual move", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"distinct case days": 0, "cases": 0},
            "decided_by": "No active bars: fewer than 30 distinct case days across all coins and windows.",
            "reading": reading_check,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean short-signed 5-day unusual move", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Only %.1f%% of the active bars are short bars in the plan's situation (30-day return "
                           "below 0, range ratio regime, close below the prior 30-day low)." % (100 * agreement)),
            "reading": reading_check,
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, unusual short-signed, abs forecast)
    for coin, wins in bars.items():
        # normal drift: non-overlapping 5-bar returns over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = df["close"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            # bets on the short side: rise of the short magnitude of >= BAND from its lowest since last bet
            bet = np.zeros(n, dtype=bool)
            anchor = 0.0
            prev_side = 0
            for t in range(n):
                side = -1 if f[t] < 0 else (1 if f[t] > 0 else 0)
                if side != -1:
                    anchor = 0.0
                    prev_side = side
                    continue
                m = -f[t]
                if prev_side != -1:
                    anchor = 0.0
                anchor = min(anchor, m)
                if m - anchor >= BAND:
                    bet[t] = True
                    anchor = m
                prev_side = -1
            # once per grid cell
            for start in range(0, n, H):
                idx = [t for t in range(start, min(start + H, n)) if bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                unusual = -(r - drift)
                cases.append((ts.iloc[t].strftime("%Y-%m-%d"), unusual, abs(f[t])))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)
    thr = "mean > 0 with t >= 2 (and deeper-minus-shallower > 0) confirms; t <= -2 rejects"

    if n_days < MIN_DAYS or n_cases < 2:
        mean_val = float(np.mean([u for _, u, _ in cases])) if n_cases else None
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": "mean short-signed 5-day unusual move", "value": mean_val,
                             "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"distinct case days": int(n_days), "cases": int(n_cases)},
            "decided_by": "Fewer than 30 distinct case days across all coins and windows (%d)." % n_days,
            "reading": reading_check,
        }

    x = np.array([u for _, u, _ in cases])
    dlab = np.array([d for d, _, _ in cases])
    mean = float(x.mean())
    dev = x - mean
    dsum = pd.Series(dev).groupby(dlab).sum().values
    G = len(dsum)
    var_sum = float(np.sum(dsum ** 2))
    se = np.sqrt(var_sum * G / (G - 1)) / n_cases if G > 1 else np.nan
    t_stat = float(mean / se) if se and np.isfinite(se) and se > 0 else float("nan")

    a = np.array([fa for _, _, fa in cases])
    med = float(np.median(a))
    deep = x[a > med]
    shallow = x[a <= med]
    if len(deep) > 0 and len(shallow) > 0:
        diff = float(deep.mean() - shallow.mean())
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = False

    if np.isfinite(t_stat) and mean > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean short-signed unusual move is above 0 with t >= 2 and the deeper half beats the shallower half."
    elif np.isfinite(t_stat) and t_stat <= -2:
        status = "rejected"
        decided = "The mean short-signed unusual move has t <= -2: the coin rises more than its drift after the break."
    elif np.isfinite(t_stat) and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the depth check fails (deeper half minus shallower half not above 0)."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-signed unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean short-signed 5-day unusual move", "value": mean,
                         "statistic": {"name": "t of the mean, same-day cases summed", "value": t_stat},
                         "threshold": thr},
        "supporting_check": {"name": "deeper-half minus shallower-half mean unusual move (median |forecast| split)",
                             "value": diff, "passed": sup_pass},
        "counts": {"distinct case days": int(n_days), "cases": int(n_cases)},
        "decided_by": decided,
        "reading": (reading_check + "; a case is the first short bet (forecast magnitude up >= 2 from its low since "
                    "the last bet) in each 5-bar grid cell from each window's first row, the deeper half is |forecast| "
                    "strictly above the median and the shallower half at or below it, and the 30-day minimum is applied "
                    "as a not-observable minimum count."),
    }
