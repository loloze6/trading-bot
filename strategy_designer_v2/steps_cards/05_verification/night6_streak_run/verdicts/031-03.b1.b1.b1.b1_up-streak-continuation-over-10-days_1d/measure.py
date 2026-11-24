import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    STREAK_COL = "debug_info.components.streak.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret30 = close / close.shift(30) - 1.0
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            # 30-day return > 0: from prices where 30 bars of the window exist, else the detector's own decision
            pos30 = np.where(ret30.notna(), ret30 > 0, regime == "trending")
            # up-close streak in progress: the raw streak value > 0, or the close above the previous close if not recorded
            if STREAK_COL in df.columns:
                sv = pd.to_numeric(df[STREAK_COL], errors="coerce")
            else:
                sv = pd.Series([np.nan] * len(df))
            up_close = (close > close.shift(1)).values
            streak_on = np.where(sv.notna(), sv > 0, up_close)
            active = (fc != 0).values
            situ = streak_on & pos30 & (fc > 0).values
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are long bars of an up-close streak "
                          "with a positive 30-day return, as the plan's Fidelity states.",
            "reading": "The 30-day return is recomputed from the window's closes, falling back to the recorded regime "
                       "on the window's first 30 bars; the streak is on when its raw value is above 0.",
        }

    # ---------- 2. Criterion ----------
    cases = []  # (coin, day, unusual move, forecast)
    for coin, wins in bars.items():
        # normal drift: mean 10-bar return on the non-overlapping grid of all the coin's windows
        grid_rets = []
        per_window = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            per_window.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df in per_window:
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            low = 0.0
            used_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    low = 0.0
                    continue
                is_bet = (f - low) >= BAND
                if is_bet:
                    low = f
                else:
                    low = min(low, f)
                    continue
                cell = t // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                cases.append((coin, ts.iloc[t].normalize(), r - drift, f))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct days": n_days}

    reading = ("A case is the first bet (a forecast rise of at least 2 points from its lowest positive level since the "
               "last bet, from 0 after a flat) in each 10-bar grid cell of a window, with its 10-bar return inside the "
               "window; the day-clustered t uses the summed deviations per UTC day with a D/(D-1) correction; the top "
               "and bottom thirds are the cases with forecast at or above the 2/3 quantile and at or below the 1/3 "
               "quantile; the plan's minimum counts lead to 'not observable' as the workflow requires.")

    main = {"name": "mean unusual 10-day move of the cases", "value": None, "statistic": None,
            "threshold": "mean above 0 with t >= 2 confirms (with the supporting check); below 0 with t <= -2 rejects"}
    sup = {"name": "top-third minus bottom-third mean unusual move", "value": None, "passed": None}

    if n_cases > 0:
        u = np.array([c[2] for c in cases])
        f = np.array([c[3] for c in cases])
        dayk = np.array([c[1].value for c in cases])
        mean_u = float(u.mean())
        main["value"] = mean_u
        dev = u - mean_u
        s = pd.Series(dev).groupby(dayk).sum().values
        D = len(s)
        t_val = None
        if D > 1:
            var = (D / (D - 1)) * np.sum(s ** 2) / (n_cases ** 2)
            if var > 0:
                t_val = float(mean_u / np.sqrt(var))
        main["statistic"] = {"name": "t of the mean, cases clustered by day",
                             "value": t_val if t_val is not None else None}
        q1, q2 = np.quantile(f, [1 / 3, 2 / 3])
        top = u[f >= q2]
        bot = u[f <= q1]
        if len(top) > 0 and len(bot) > 0:
            diff = float(top.mean() - bot.mean())
            sup["value"] = diff
            sup["passed"] = bool(diff > 0)
    else:
        t_val = None

    sc = {"agreement": float(agreement) if agreement is not None else None, "passed": True}

    if n_cases < 100 or n_days < 50:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": "The plan's minimum of 100 cases on at least 50 distinct days is not reached.",
                "reading": reading}

    mean_u = main["value"]
    if t_val is not None and mean_u > 0 and t_val >= 2 and sup["passed"] is True:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the top third beats the bottom third."
    elif t_val is not None and mean_u > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-third case mean does not exceed the bottom-third mean."
    elif t_val is not None and mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": decided, "reading": reading}
