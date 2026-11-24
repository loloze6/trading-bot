import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 0.05  # config strategies.min_allocation_change, read as forecast points
    COMP = "depth"

    def _ts(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            unit = "ms" if v.dropna().abs().median() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    def _parse_comp(x):
        if x is None:
            return np.nan
        if isinstance(x, float) and np.isnan(x):
            return np.nan
        d = x
        if isinstance(x, str):
            try:
                d = json.loads(x)
            except Exception:
                try:
                    import ast
                    d = ast.literal_eval(x)
                except Exception:
                    return np.nan
        if not isinstance(d, dict):
            return np.nan
        c = d.get(COMP)
        if not isinstance(c, dict):
            return np.nan
        v = c.get("last_history_value")
        try:
            return float(v)
        except Exception:
            return np.nan

    def _raw(df):
        col = "debug_info.components.%s.last_history_value" % COMP
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        if "debug_info.components" in df.columns:
            return df["debug_info.components"].map(_parse_comp).to_numpy(dtype=float)
        return np.full(len(df), np.nan)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            raw = _raw(df)
            active = np.isfinite(f) & (f != 0)
            situ = np.isfinite(raw) & (raw < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else agreement >= 0.9

    main_name = "mean short-side unusual 10-bar move of short bets (vs coin's normal 10-bar drift)"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2; reject: mean < 0 with t <= -2"
    supp_name = "deeper half (|forecast| above median) mean unusual move >= shallower half mean"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars where the close is below "
                          "the prior 365-day closing low (raw depth < 0), so the config does not do what the Fidelity says.",
            "reading": "Situation bars are those whose recorded raw depth component is below 0; bars where it is not "
                       "recorded are not situation bars.",
        }

    # ---------- coin drift (normal 10-bar drift over all windows) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    cases = []  # (day, unusual, |forecast|)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            ts = _ts(df["timestamp"]).reset_index(drop=True)
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            on_short = False
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi >= 0:
                    on_short = False
                    ref = 0.0
                    continue
                size = -fi
                if not on_short:
                    ref = 0.0
                    on_short = True
                if size - ref >= BAND:
                    bet[i] = True
                    ref = size
                else:
                    ref = min(ref, size)
            for start in range(0, n, H):
                idx = np.where(bet[start:min(start + H, n)])[0]
                if len(idx) == 0:
                    continue
                i = start + int(idx[0])
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                unusual = -(r - drift[coin])
                day = ts.iloc[i]
                day = str(day.date()) if pd.notna(day) else "%s_%s_%d" % (coin, w, i)
                cases.append((day, unusual, abs(f[i])))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean = None
    tval = None
    if n_cases > 0:
        x = np.array([u for _, u, _ in cases], dtype=float)
        mean = float(x.mean())
        if n_days >= 2:
            dev = pd.Series(x - mean).groupby([d for d, _, _ in cases]).sum().to_numpy()
            var = (n_days / (n_days - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = float(np.sqrt(var))
            if se > 0:
                tval = float(mean / se)

    supp = {"name": supp_name, "value": None, "passed": None}
    if n_cases > 0:
        a = np.array([af for _, _, af in cases], dtype=float)
        x = np.array([u for _, u, _ in cases], dtype=float)
        med = float(np.median(a))
        deep = x[a > med]
        shallow = x[a <= med]
        if len(deep) > 0 and len(shallow) > 0:
            diff = float(deep.mean() - shallow.mean())
            supp = {"name": supp_name + " (deeper minus shallower)", "value": diff, "passed": bool(diff >= 0)}
        else:
            supp = {"name": supp_name + " (deeper minus shallower)", "value": None, "passed": False}

    main = {"name": main_name, "value": mean,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": tval}
                          if tval is not None else None),
            "threshold": main_thr}

    reading = ("A case is the first short bet (forecast rising in size on the short side by at least 0.05 forecast "
               "points, the config's min_allocation_change, from its lowest size since the last bet) in each 10-bar "
               "grid cell counted from each window's first row, dropped if its 10-bar return leaves the window; the "
               "deeper half is |forecast| strictly above the median and the shallower half the rest; the plan's "
               "minimum of 30 cases on 20 days, when unmet, gives 'not observable'.")

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = "The plan's minimum of at least 30 cases on at least 20 distinct days is not reached."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and tval >= 2:
        if supp["passed"]:
            status = "confirmed"
            decided = ("Confirm rule: the mean short-side unusual move is above 0 with t >= 2 and the deeper half's "
                       "mean is at least the shallower half's.")
        else:
            status = "inconclusive"
            decided = ("Inconclusive rule: the main measure confirms (mean > 0, t >= 2) but the supporting check "
                       "fails (deeper half's mean below the shallower half's).")
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule: the mean short-side unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the t of the mean short-side unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
