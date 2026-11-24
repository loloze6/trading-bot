import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    BAND = 2.0
    T_THR = 2.0
    MIN_CASES = 30
    MIN_DAYS = 20

    def to_ts(s):
        if pd.api.types.is_numeric_dtype(s):
            unit = "ms" if s.dropna().abs().max() > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    def col(df, name):
        if name in df.columns:
            return pd.to_numeric(df[name], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------------- situation check ----------------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret14 = close / close.shift(H) - 1.0
            v_rec = col(df, "debug_info.components.vol_up.last_history_value")
            v_rec = v_rec.fillna(col(df, "debug_info.components.vol_down.last_history_value"))
            v_calc = vol.rolling(14, min_periods=14).mean() / vol.rolling(30, min_periods=30).mean() - 1.0
            vr = v_rec.fillna(v_calc)
            active = (fc != 0) & ret14.notna() & vr.notna()
            up = (ret14 > 0) & (vr > 0) & (fc > 0)
            dn = (ret14 < 0) & (vr < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & (up | dn)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        sit_passed = bool(agreement >= 0.90)
    else:
        agreement = None
        sit_passed = None

    main_name = "mean unusual 14-bar move over the cases, in the signal's direction"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    reading = ("ret14 is recomputed as close[t]/close[t-14]-1 inside the window and the volume ratio is the recorded "
               "last_history_value (recomputed from volume where missing), active bars where ret14 cannot be computed "
               "are left out of the agreement; a bet starts from 0 at each window's start, the first bet of each "
               "14-bar grid cell is the case and is dropped if its 14-bar forward return leaves the window; the "
               "day-clustered t uses the per-day summed deviations without small-sample correction; the supporting "
               "check splits the cases at the median of |forecast| on the signal bar.")

    if sit_passed is False:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the 14-day return and "
                           "the centred 14/30 volume ratio share a sign with the forecast on that side (long when both "
                           "up, short when both down)."),
            "reading": reading,
        }

    # ---------------- cases ----------------
    cases = []  # (unusual, |forecast|, day)
    for coin in sorted(bars):
        wins = bars[coin]
        # normal drift: non-overlapping 14-bar returns over all windows of the coin
        grid_rets = []
        prepared = {}
        for w in sorted(wins):
            df = wins[w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(close)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared[w] = df
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w in sorted(prepared):
            df = prepared[w]
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = to_ts(df["timestamp"])
            n = len(df)
            side = 0
            trough = 0.0
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                s = int(np.sign(f))
                bet = False
                if s == 0:
                    side = 0
                    trough = 0.0
                else:
                    a = abs(f)
                    if s != side:
                        side = s
                        trough = 0.0
                    else:
                        trough = min(trough, a)
                    if a - trough >= BAND:
                        bet = True
                        trough = a
                if not bet:
                    continue
                cell = t // H
                if cell in taken_cells:
                    continue
                taken_cells.add(cell)
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                unusual = s * (r - drift)
                day = ts.iloc[t].strftime("%Y-%m-%d")
                cases.append((float(unusual), float(abs(f)), day))

    n_cases = len(cases)
    days = sorted(set(c[2] for c in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct days": n_days}
    sit_block = {"agreement": (float(agreement) if agreement is not None else None), "passed": sit_passed}

    mean_u = None
    t_stat = None
    sup = {"name": "mean unusual move, |forecast| >= median minus below median", "value": None, "passed": None}
    if n_cases > 0:
        x = np.array([c[0] for c in cases])
        absf = np.array([c[1] for c in cases])
        dl = np.array([c[2] for c in cases])
        mean_u = float(x.mean())
        dev = pd.Series(x - mean_u).groupby(dl).sum().values
        se = np.sqrt(np.sum(dev ** 2)) / n_cases
        if se > 0:
            t_stat = float(mean_u / se)
        med = np.median(absf)
        hi = x[absf >= med]
        lo = x[absf < med]
        if len(hi) > 0 and len(lo) > 0:
            diff = float(hi.mean() - lo.mean())
            sup["value"] = diff
            sup["passed"] = bool(diff > 0)
        else:
            sup["passed"] = False

    main_block = {"name": main_name, "value": mean_u,
                  "statistic": ({"name": "day-clustered t", "value": t_stat} if t_stat is not None else None),
                  "threshold": threshold}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        return {
            "status": "not observable",
            "situation_check": sit_block,
            "main_measure": main_block,
            "supporting_check": sup,
            "counts": counts,
            "decided_by": (f"The plan's minimum of {MIN_CASES} cases on at least {MIN_DAYS} distinct days is not "
                           f"reached ({n_cases} cases on {n_days} days)."),
            "reading": reading,
        }

    tv = t_stat if t_stat is not None else 0.0
    if mean_u > 0 and tv >= T_THR and sup["passed"]:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the supporting check passes (confirm rule)."
    elif mean_u < 0 and tv <= -T_THR:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2 (reject rule)."
    elif mean_u > 0 and tv >= T_THR:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan rules inconclusive."
    else:
        status = "inconclusive"
        decided = "The day-clustered t lies strictly between -2 and 2 (or its sign disagrees with the mean), which the plan rules inconclusive."

    return {
        "status": status,
        "situation_check": sit_block,
        "main_measure": main_block,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
