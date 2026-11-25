import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    PERIOD_LOW = 30
    TREND_PERIOD = 60
    TREND_LIMIT = -10.0
    MIN_CASES = 30
    MIN_DAYS = 30

    def _parse(x):
        if isinstance(x, dict):
            return x
        if isinstance(x, str):
            try:
                v = json.loads(x)
                return v if isinstance(v, dict) else None
            except Exception:
                return None
        return None

    def get_comp(df, cid, field):
        col = "debug_info.components.%s.%s" % (cid, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            for i, x in enumerate(df["debug_info.components"].to_numpy()):
                d = _parse(x)
                if d and cid in d:
                    c = d[cid]
                    if isinstance(c, dict) and field in c:
                        try:
                            out[i] = float(c[field])
                        except Exception:
                            pass
        return out

    # ---------- situation check + cases ----------
    n_active = 0
    n_agree = 0
    drift = {}
    case_rows = []

    for coin, wins in bars.items():
        # coin's normal 5-bar drift: non-overlapping grid of every window, all windows together
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            low = pd.to_numeric(df["low"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            raw_depth = get_comp(df, "pierce_depth", "last_history_value")

            # pierce depth: recorded raw value where present, else recomputed from prices
            depth = np.full(n, np.nan)
            for t in range(n):
                if np.isfinite(raw_depth[t]):
                    depth[t] = raw_depth[t]
                elif t >= PERIOD_LOW:
                    pl = np.nanmin(low[t - PERIOD_LOW:t])
                    if np.isfinite(pl) and pl > 0:
                        if low[t] < pl and close[t] >= pl:
                            depth[t] = (pl - low[t]) / pl * 100.0
                        else:
                            depth[t] = 0.0

            for t in range(n):
                if fc[t] == 0:
                    continue
                n_active += 1
                pierce_ok = np.isfinite(depth[t]) and depth[t] > 0
                # falling: 60-bar price evolution below -10 %, from prices when history allows
                if t >= TREND_PERIOD and close[t - TREND_PERIOD] > 0:
                    trend = (close[t] / close[t - TREND_PERIOD] - 1.0) * 100.0
                    falling_ok = trend < TREND_LIMIT
                else:
                    falling_ok = regime[t] == "mean_reversion"
                # agitated: 365-bar volatility percentile cannot be rebuilt inside a window;
                # the detector's vetoes (chop) are read from its recorded regime
                agitated_ok = regime[t] == "mean_reversion"
                if pierce_ok and falling_ok and agitated_ok and fc[t] > 0:
                    n_agree += 1

            # bets: a rise of the forecast on the long side of at least the band
            ref = 0.0
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    ref = f
                    cell = t // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if t + H < n and np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                        r = close[t + H] / close[t] - 1.0
                        day = ts.iloc[t].strftime("%Y-%m-%d") if pd.notna(ts.iloc[t]) else None
                        case_rows.append({"coin": coin, "day": day, "ret": r, "forecast": f})
                else:
                    ref = min(ref, f)

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    main_name = "mean unusual 5-bar move of the cases (return minus coin's normal 5-bar drift)"
    threshold = "mean > 0 with t >= 2 (confirm, with positive depth slope); mean < 0 with t <= -2 (reject)"
    stat_name = "t of the mean, cases of one day taken together"
    sup_name = "OLS slope of the unusual 5-bar move on the forecast at the signal bar"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation, long": int(n_agree)},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are long bars of a reclaimed "
                          "30-day-low pierce in the falling agitated profile, as the plan's Fidelity requires.",
            "reading": "Pierce depth taken from the recorded pierce_depth raw value (recomputed from prices where "
                       "missing); falling = 60-bar price change below -10 % from prices where 60 bars exist, else the "
                       "recorded regime; agitated (365-bar volatility percentile, not rebuildable inside a window) "
                       "read from the recorded regime.",
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "ret", "forecast"])
    if len(cases):
        cases["drift"] = cases["coin"].map(drift)
        cases["u"] = cases["ret"] - cases["drift"]
        cases = cases.dropna(subset=["u", "forecast", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_stat = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        per_day = dev.groupby(cases["day"]).sum().to_numpy()
        D = len(per_day)
        se = np.sqrt(np.sum(per_day ** 2) * D / (D - 1)) / n_cases
        if se > 0:
            t_stat = float(mean_u / se)

    slope = None
    if n_cases >= 2:
        x = cases["forecast"].to_numpy(dtype=float)
        y = cases["u"].to_numpy(dtype=float)
        vx = np.sum((x - x.mean()) ** 2)
        if vx > 0:
            slope = float(np.sum((x - x.mean()) * (y - y.mean())) / vx)
    slope_ok = (slope is not None and slope > 0)

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = "The plan's minimum of 30 cases on at least 30 distinct days is not reached " \
                  "(%d cases on %d days)." % (n_cases, n_days)
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2 and slope_ok:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the depth slope is positive."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the depth slope is 0 or below, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": stat_name, "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": bool(slope_ok) if slope is not None else None},
        "counts": {"cases": n_cases, "distinct days": n_days},
        "decided_by": decided,
        "reading": "Cases are long bets (forecast rise >= 2 points from its lowest level since the last bet, reset at "
                   "flat), the first per 5-bar grid cell counted from each window's first row, with the 5-bar return "
                   "inside the window minus the coin's mean non-overlapping 5-bar return over all its windows; the t "
                   "sums deviations per signal day (cluster standard error with D/(D-1)); the situation check reads "
                   "the agitated part of the profile from the recorded regime since a 365-bar percentile cannot be "
                   "rebuilt inside a window.",
    }
