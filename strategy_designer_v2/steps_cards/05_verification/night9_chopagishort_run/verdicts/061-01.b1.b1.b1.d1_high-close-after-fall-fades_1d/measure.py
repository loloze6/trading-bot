import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0

    def _comp_series(df, cid, field="last_history_value"):
        col = "debug_info.components.%s.%s" % (cid, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                val = np.nan
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(cid)
                    if isinstance(c, dict):
                        x = c.get(field)
                        try:
                            val = float(x) if x is not None else np.nan
                        except Exception:
                            val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    n_active = 0
    n_agree = 0
    cases = []  # (coin, day, abs_forecast, ret5)
    drift_samples = {}

    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)

            # --- situation check ---
            ret5_rec = _comp_series(df, "fall5")
            cloc_rec = _comp_series(df, "highclose")
            ret5_px = close / close.shift(5) - 1.0
            rng = (high - low).replace(0, np.nan)
            cloc_px = (close - low) / rng
            ret5 = ret5_rec.where(ret5_rec.notna(), ret5_px)
            cloc = cloc_rec.where(cloc_rec.notna(), cloc_px)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            profile_ok = (regime != "chop").values
            situ = ((ret5 < 0) & (cloc >= 0.75)).values & profile_ok
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

            # --- normal drift samples (grid 0, H, 2H, ...) ---
            cv = close.values
            for p in range(0, n - H, H):
                if np.isfinite(cv[p]) and np.isfinite(cv[p + H]) and cv[p] > 0:
                    drift_samples.setdefault(coin, []).append(cv[p + H] / cv[p] - 1.0)

            # --- short bets ---
            ref = 0.0
            side = 0
            used_cells = set()
            for t in range(n):
                f = fc[t]
                s = 1 if f > 0 else (-1 if f < 0 else 0)
                if s != side or s == 0:
                    ref = 0.0
                    side = s
                if s != -1:
                    continue
                m = -f
                ref = min(ref, m)
                if m - ref >= BAND:
                    ref = m
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H < n and np.isfinite(cv[t]) and np.isfinite(cv[t + H]) and cv[t] > 0 and pd.notna(ts[t]):
                        cases.append((coin, ts[t].floor("D"), abs(f), cv[t + H] / cv[t] - 1.0))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    reading_base = ("Profile taken from the regime column (bars not vetoed to 'chop') since its components are not recorded; "
                    "the 5-day return and close location from the recorded fall5/highclose raw values, else from prices; "
                    "cases are short bets only, first bet per 5-bar cell; day-clustered t with G/(G-1) correction; "
                    "the |forecast| halves are the lower and upper n//2 cases by rank (middle case dropped when odd).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars with a negative 5-day return, a close in the "
                           "top quarter of the range and the choppy-agitated profile (agreement %.3f)." % agreement),
            "reading": reading_base,
        }

    drift = {c: float(np.mean(v)) for c, v in drift_samples.items() if len(v) > 0}
    rows = []
    for coin, day, af, r in cases:
        if coin in drift:
            rows.append((coin, day, af, -(r - drift[coin])))
    cdf = pd.DataFrame(rows, columns=["coin", "day", "absf", "u"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_u = float(cdf["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cdf["u"] - mean_u
        S = dev.groupby(cdf["day"]).sum().values
        G = len(S)
        var = (G / (G - 1.0)) * float(np.sum(S ** 2)) / (n_cases ** 2)
        if var > 0:
            t_val = float(mean_u / np.sqrt(var))

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        srt = cdf.sort_values("absf", kind="mergesort").reset_index(drop=True)
        k = n_cases // 2
        small = srt["u"].iloc[:k]
        large = srt["u"].iloc[n_cases - k:]
        sup_val = float(large.mean() - small.mean())
        sup_pass = bool(sup_val >= 0)

    main = {
        "name": "mean unusual 5-bar move per short bet, in the short direction",
        "value": mean_u,
        "statistic": {"name": "t of the mean, cases grouped by day", "value": t_val} if t_val is not None else None,
        "threshold": "confirm: a fall with t >= 2; reject: a rise with t <= -2; over at least 30 cases on at least 20 days",
    }
    support = {"name": "mean unusual move of larger-|forecast| half minus smaller half (>= 0)",
               "value": sup_val, "passed": sup_pass}
    counts = {"cases": n_cases, "days": n_days}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = "Minimum counts not reached: %d cases (need 30) on %d days (need 20)." % (n_cases, n_days)
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and mean_u > 0:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is a fall with t >= 2 over at least 30 cases on 20 days, and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "A confirming t >= 2 whose supporting check fails is inconclusive."
    elif t_val <= -2 and mean_u < 0:
        status = "rejected"
        decided = "The mean unusual move is a rise with t <= -2 (short direction) over at least 30 cases on 20 days."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
