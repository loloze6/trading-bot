import numpy as np
import pandas as pd


def measure(bars):
    POS = "postRebalance_current_allocation"
    H = 2
    MIN_CASES = 200

    def _ts(df):
        t = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        return t.reset_index(drop=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = _ts(d)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            # the coming bar (opening at this bar's close) is stamped 21:00 or 22:00 UTC
            coming_hour = (ts + pd.Timedelta(hours=1)).dt.hour.values
            situ = np.isin(coming_hour, [21, 22])
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading_sit = ("The situation is read as the bars whose coming bar is stamped 21:00 or 22:00 UTC "
                   "(bars stamped 20:00 and 21:00, so the long is held over the 21:00-23:00 stretch), long side.")
    threshold_txt = "weighted mean excess > 0 with t >= 2 (confirm, with supporting check); < 0 with t <= -2 (reject)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "position-weighted mean 2-bar excess return from 20:00 close",
                             "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars whose coming bar is "
                           "stamped 21:00 or 22:00 UTC, so the config does not hold the plan's situation and side."),
            "reading": reading_sit,
        }

    # ---------- 2. criterion ----------
    xs, ws = [], []
    for coin, wins in bars.items():
        # coin's mean 2-bar return over all windows, non-overlapping grid
        grid = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            grid.append(r[np.isfinite(r)])
        if not grid:
            continue
        grid = np.concatenate(grid)
        if grid.size == 0:
            continue
        drift = float(np.mean(grid))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = _ts(d)
            c = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            pos = pd.to_numeric(d[POS], errors="coerce").values if POS in d.columns else np.full(len(d), np.nan)
            ts_map = {t: i for i, t in enumerate(ts) if pd.notna(t)}
            entries = np.where((ts.dt.hour.values == 20) & (ts.dt.minute.values == 0))[0]
            for i in entries:
                j = ts_map.get(ts[i] + pd.Timedelta(hours=H))
                if j is None:
                    continue
                if fc[i] == 0 or not np.isfinite(pos[i]) or pos[i] <= 0:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[j]) and c[i] > 0):
                    continue
                xs.append(c[j] / c[i] - 1.0 - drift)
                ws.append(float(pos[i]))

    x = np.asarray(xs, float)
    wt = np.asarray(ws, float)
    n = int(x.size)

    reading = (reading_sit + " A case is a coin-day whose 20:00 bar has a non-zero forecast and a positive position "
               "after its trade, its return runs to the bar stamped 22:00 by timestamp, the weight is that position, "
               "the t uses the weighted mean's sandwich standard error, the supporting check compares unweighted mean "
               "excess returns of cases strictly above versus strictly below the median position, and the plan's "
               "200-case minimum gives 'not observable' when not reached.")

    mean_w = None
    t_w = None
    if n >= 2 and wt.sum() > 0:
        sw = wt.sum()
        mean_w = float(np.sum(wt * x) / sw)
        var = float(np.sum(wt ** 2 * (x - mean_w) ** 2) / sw ** 2 * n / (n - 1))
        t_w = float(mean_w / np.sqrt(var)) if var > 0 else None

    sup_val = None
    sup_pass = None
    n_hi = n_lo = 0
    if n >= 2:
        med = float(np.median(wt))
        hi = x[wt > med]
        lo = x[wt < med]
        n_hi, n_lo = int(hi.size), int(lo.size)
        if n_hi > 0 and n_lo > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    counts = {"cases": n, "cases above median position": n_hi, "cases below median position": n_lo}
    main = {"name": "position-weighted mean 2-bar excess return from 20:00 close",
            "value": mean_w,
            "statistic": {"name": "t of weighted mean", "value": t_w} if t_w is not None else None,
            "threshold": threshold_txt}
    support = {"name": "mean excess above-median minus below-median position", "value": sup_val, "passed": sup_pass}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 200 cases."
    elif mean_w is None or t_w is None:
        status = "inconclusive"
        decided = "The weighted mean or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_w > 0 and t_w >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The position-weighted mean excess return is above 0 with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The weighted mean excess return is above 0 with t >= 2, but the supporting check fails."
    elif mean_w < 0 and t_w <= -2:
        status = "rejected"
        decided = "The position-weighted mean excess return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the weighted mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
