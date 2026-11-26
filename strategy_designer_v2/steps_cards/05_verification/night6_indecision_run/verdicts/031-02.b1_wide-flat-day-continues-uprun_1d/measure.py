import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    EPS = 1e-9

    def _ts(s):
        if np.issubdtype(s.dtype, np.number):
            v = s.astype(float)
            unit = "ms" if v.abs().max() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    def _component(df, cid, field):
        col = "debug_info.components.%s.%s" % (cid, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            for i, d in enumerate(df["debug_info.components"].to_numpy()):
                try:
                    if isinstance(d, dict) and cid in d and isinstance(d[cid], dict):
                        v = d[cid].get(field)
                        if v is not None:
                            out[i] = float(v)
                except Exception:
                    pass
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            o = df["open"].to_numpy(float)
            h = df["high"].to_numpy(float)
            l = df["low"].to_numpy(float)
            c = df["close"].to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(float)
            rng = h - l
            # rise: 6-bar return; recorded raw value where present, else from prices
            rise_px = pd.Series(c).pct_change(6).to_numpy()
            rise_rec = _component(df, "prior_rise", "last_history_value")
            rise = np.where(np.isfinite(rise_rec), rise_rec, rise_px)
            # width: range / mean range of last 20 bars including the bar
            mean20 = pd.Series(rng).rolling(20, min_periods=20).mean().to_numpy()
            with np.errstate(divide="ignore", invalid="ignore"):
                width = np.where(mean20 > 0, rng / mean20, np.nan)
                flat = np.where(rng > 0, 1.0 - np.abs(c - o) / rng, np.nan)
            computable = np.isfinite(rise) & np.isfinite(width) & np.isfinite(flat)
            situ = computable & (rise > 0) & (width >= 1.5 - EPS) & (flat >= 0.9 - EPS)
            active = fc != 0
            n_active_uncomputable += int(np.sum(active & ~computable))
            act = active & computable
            n_active += int(np.sum(act))
            n_agree += int(np.sum(act & situ & (fc > 0)))
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess 10-bar return of long bets (minus coin's normal 10-bar drift)"
    thr = "confirm: mean > 0 with day-pooled t >= 2 and slope on forecast > 0; reject: mean < 0 with t <= -2"
    reading_base = ("Situation recomputed from prices (rise from the recorded prior_rise raw value where present), "
                    "active bars whose 20-bar range mean cannot be formed inside the window are left out of the agreement; ")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree,
                       "active bars not computable": n_active_uncomputable},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 6-bar return > 0, "
                           "range >= 1.5x the 20-bar mean range and flatness >= 0.9, as the Fidelity requires."
                           if n_active > 0 else "The forecast is never non-zero, so no bar matches the plan's situation."),
            "reading": reading_base + "the expected side is long (forecast > 0).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 10-bar returns over all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].to_numpy(float)
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(float)
            ts = _ts(df["timestamp"])
            low = 0.0
            seen_cells = set()
            for t in range(len(df)):
                f = fc[t]
                is_bet = False
                if f <= 0:
                    low = 0.0
                else:
                    if f - low >= BAND - EPS:
                        is_bet = True
                        low = f
                    else:
                        low = min(low, f)
                if not is_bet:
                    continue
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= len(df):
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                rows.append({"coin": coin, "day": ts.iloc[t].strftime("%Y-%m-%d"),
                             "excess": r - drift, "forecast": f})

    cases = pd.DataFrame(rows, columns=["coin", "day", "excess", "forecast"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean = float(cases["excess"].mean()) if n_cases else None
    tstat = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["excess"] - mean
        per_day = dev.groupby(cases["day"]).sum().to_numpy()
        var_mean = (n_days / (n_days - 1.0)) * np.sum(per_day ** 2) / (n_cases ** 2)
        if var_mean > 0:
            tstat = float(mean / np.sqrt(var_mean))
    slope = None
    if n_cases >= 2 and cases["forecast"].var() > 0:
        x = cases["forecast"].to_numpy(float)
        y = cases["excess"].to_numpy(float)
        xm = x - x.mean()
        slope = float(np.sum(xm * (y - y.mean())) / np.sum(xm ** 2))
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = "The plan's minimum of 30 cases and 30 distinct days is not reached (%d cases, %d days)." % (n_cases, n_days)
    elif tstat is None:
        status = "inconclusive"
        decided = "The day-pooled t cannot be computed (zero variance), so neither the confirm nor the reject rule is met."
    elif mean > 0 and tstat >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean excess 10-bar return above 0 with t >= 2 and slope on forecast size above 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the slope on forecast size is at or below 0 (inconclusive rule)."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean excess 10-bar return below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The day-pooled t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": None if tstat is None else {"name": "t of the mean, cases of one day pooled", "value": tstat},
                         "threshold": thr},
        "supporting_check": {"name": "OLS slope of excess 10-bar return on signal forecast", "value": slope, "passed": slope_pass},
        "counts": {"cases": n_cases, "distinct days": n_days},
        "decided_by": decided,
        "reading": reading_base + ("a case is the first long bet (forecast rise >= 2 from its lowest long level since the last bet, "
                                   "from 0 after flat) in each 10-bar grid cell of a window counted from its first row, cases without "
                                   "10 bars left in the window are dropped, the day-pooled t uses a D/(D-1) correction, and the plan's "
                                   "'fewer than 30 cases or days' minimum is reported as not observable."),
    }
