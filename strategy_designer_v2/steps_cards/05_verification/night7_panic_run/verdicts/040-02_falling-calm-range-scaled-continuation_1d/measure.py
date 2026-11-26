import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    MIN_DAYS = 30
    LHV = "debug_info.components.scaled_fall.last_history_value"

    def to_time(s):
        if pd.api.types.is_numeric_dtype(s):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            active = f != 0
            # situation: inside the falling calm profile (detector not vetoing -> regime "unknown")
            # and the coin fell over the last 3 days (raw scaled 3-day return < 0); side: short.
            in_profile = reg == "unknown"
            fell = np.where(np.isnan(raw), False, raw < 0)
            situ = in_profile & fell
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean unusual 3-bar move after short signals, short direction (day-clustered t)"
    main_thr = "confirm if t >= 2 (with supporting difference > 0); reject if t <= -2"
    sup_name = "top minus bottom half by |forecast| of mean unusual move (Welch t)"

    reading = ("Profile taken as bars with regime 'unknown' (the detector's non-vetoed falling calm state) and the fall as "
               "a negative raw scaled_fall value; signals are forecast.md-7 bets (short size rising >= 2 points above its "
               "lowest level since the last bet, starting from 0 at each window start), the first bet of each 3-bar grid "
               "cell from the window's first row; drift is the mean of each coin's non-overlapping 3-bar grid returns "
               "pooled over all its windows; the t clusters case deviations summed per UTC day with a D/(D-1) correction; "
               "the median split puts |forecast| above the median in the top half and the rest in the bottom half; the "
               "plan's 30-day minimum is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling calm "
                           "profile after a 3-day fall, so the config does not do what the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, unusual, absf)
    for coin, wins in bars.items():
        # coin's normal 3-bar drift over all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = to_time(df["timestamp"])
            n = len(df)
            low = 0.0
            side = 0
            taken_cells = set()
            for t in range(n):
                ft = f[t]
                s_side = 1 if ft > 0 else (-1 if ft < 0 else 0)
                size = abs(ft)
                if s_side == 0:
                    side = 0
                    low = 0.0
                    continue
                if s_side != side:
                    side = s_side
                    low = 0.0
                if size - low >= BAND:
                    low = size
                    if side == -1:
                        cell = t // H
                        if cell in taken_cells:
                            continue
                        taken_cells.add(cell)
                        if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0:
                            r = c[t + H] / c[t] - 1.0
                            unusual = -(r - drift)
                            day = ts.iloc[t].floor("D")
                            cases.append((day, unusual, size))
                else:
                    low = min(low, size)

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)

    mean_u = None
    t_main = None
    if n_cases > 0:
        x = np.array([u for _, u, _ in cases], dtype=float)
        mean_u = float(x.mean())
        if n_days >= 2:
            dev = pd.Series(x - mean_u, index=[d for d, _, _ in cases])
            sums = dev.groupby(level=0).sum().values
            D = len(sums)
            var = (D / (D - 1.0)) * np.sum(sums ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_main = float(mean_u / se) if se > 0 else None

    diff = None
    t_w = None
    sup_pass = None
    n_top = n_bot = 0
    if n_cases > 0:
        absf = np.array([a for _, _, a in cases], dtype=float)
        x = np.array([u for _, u, _ in cases], dtype=float)
        med = np.median(absf)
        top = x[absf > med]
        bot = x[absf <= med]
        n_top, n_bot = len(top), len(bot)
        if n_top > 0 and n_bot > 0:
            diff = float(top.mean() - bot.mean())
            sup_pass = bool(diff > 0)
            if n_top >= 2 and n_bot >= 2:
                tt = stats.ttest_ind(top, bot, equal_var=False).statistic
                t_w = float(tt) if np.isfinite(tt) else None

    counts = {"distinct case days": n_days, "cases": n_cases,
              "top half cases": n_top, "bottom half cases": n_bot}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 30 for a verdict."
    elif t_main is not None and t_main >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the top-minus-bottom difference is above 0."
    elif (t_main is not None and t_main <= -2) or (t_w is not None and t_w <= -2):
        status = "rejected"
        if t_main is not None and t_main <= -2:
            decided = "The main measure's t is -2 or less: no decline beyond drift after the falls."
        else:
            decided = "The supporting difference has a Welch t of -2 or less: larger falls followed by less decline."
    else:
        status = "inconclusive"
        decided = "With at least 30 case days, the numbers meet neither the confirm rule nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases summed per day", "value": t_main}
                                       if t_main is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass,
                             "welch_t": t_w},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
