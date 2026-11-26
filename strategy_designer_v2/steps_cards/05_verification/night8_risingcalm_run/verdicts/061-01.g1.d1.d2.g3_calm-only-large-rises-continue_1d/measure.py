import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RISE_COL = "debug_info.components.rise.last_history_value"

    def _prep(df):
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.sort_values("timestamp").reset_index(drop=True)
        df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        return df

    def _bets(f):
        # bet = rise of the forecast on its side of at least the band, from the lowest level
        # on that side since the last bet (from 0 after a flat or a change of side)
        out = np.zeros(len(f), dtype=bool)
        side = 0
        ref = 0.0
        for i, v in enumerate(f):
            s = 1 if v > 0 else (-1 if v < 0 else 0)
            if s == 0:
                side = 0
                ref = 0.0
                continue
            a = abs(v)
            if s != side:
                side = s
                ref = 0.0
            if a - ref >= BAND:
                out[i] = True
                ref = a
            else:
                ref = min(ref, a)
        return out

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepped = {}
    for coin, wins in bars.items():
        prepped[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = _prep(df)
            prepped[coin][w] = d
            r = d["close"].pct_change()
            rise_calc = r / r.rolling(30, min_periods=30).std()
            if RISE_COL in d.columns:
                rise = pd.to_numeric(d[RISE_COL], errors="coerce")
                rise = rise.where(rise.notna(), rise_calc)
            else:
                rise = rise_calc
            regime = d["regime"].astype(str).str.lower() if "regime" in d.columns else pd.Series("", index=d.index)
            calm = regime != "chop"
            situation = calm & (rise >= 1.0)
            active = d["forecast"] != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (d["forecast"] > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    main_name = "mean unusual 5-day move per long case (minus coin's normal 5-day drift)"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2; fewer than 30 distinct days: not observable"
    reading = ("Calm is read as the regime not being the 'chop' veto and the rise from the recorded rise component (recomputed from closes where missing); "
               "a case is the first bet bar in each 5-bar grid cell of its window; t uses day-clustered standard errors with a G/(G-1) correction; "
               "upper half = cases with entry forecast above the median, lower half = at or below it; the plan's 'fewer than 30 distinct days' minimum is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are calm-market bars with a one-day rise of at least one "
                           "30-day standard deviation taken long, as the Fidelity's situation requires." if n_active > 0 else
                           "No bar has a non-zero forecast, so the config never takes the plan's situation."),
            "reading": reading,
        }

    # ---------- criterion ----------
    cases = []  # (coin, day, forecast, raw return)
    drift = {}
    for coin, wins in prepped.items():
        grid_rets = []
        for w, d in wins.items():
            c = d["close"].values
            n = len(d)
            for p in range(0, n - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
            bets = _bets(d["forecast"].values)
            f = d["forecast"].values
            seen = set()
            for i in np.where(bets)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                cases.append((coin, d["timestamp"].iloc[i].strftime("%Y-%m-%d"),
                              float(f[i]), float(np.sign(f[i])), c[i + H] / c[i] - 1.0))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    rows = []
    for coin, day, fc, sgn, ret in cases:
        if np.isfinite(drift.get(coin, np.nan)):
            rows.append({"coin": coin, "day": day, "fc": fc, "u": sgn * (ret - drift[coin])})
    cdf = pd.DataFrame(rows, columns=["coin", "day", "fc", "u"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_u = float(cdf["u"].mean()) if n_cases else None
    t_val = None
    if n_cases and n_days >= 2:
        dev = cdf["u"] - mean_u
        g = dev.groupby(cdf["day"]).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(g ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None

    sup_val, sup_pass = None, None
    if n_cases >= 2:
        med = cdf["fc"].median()
        up = cdf.loc[cdf["fc"] > med, "u"]
        lo = cdf.loc[cdf["fc"] <= med, "u"]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    counts = {"cases": n_cases, "distinct days with cases": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct days with cases, fewer than the plan's minimum of 30."
    elif t_val is not None and mean_u > 0 and t_val >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t of 2 or more, and the upper half of entry forecasts beats the lower half."
    elif t_val is not None and mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t of -2 or less."
    elif t_val is not None and mean_u > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "A confirming t with a failed supporting check is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move, upper half minus lower half of entry forecasts",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
