import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    MIN_DAYS = 25
    PIERCE_COL = "debug_info.components.pierce_depth.last_history_value"

    def _pierce_from_prices(df):
        # depth of the low below the lowest low of the prior 30 bars (in %), on days closing at/above it; NaN if not computable
        low = df["low"].astype(float).values
        close = df["close"].astype(float).values
        n = len(df)
        out = np.full(n, np.nan)
        for i in range(30, n):
            pl = np.nanmin(low[i - 30:i])
            if not np.isfinite(pl) or pl <= 0:
                continue
            if low[i] < pl and close[i] >= pl:
                out[i] = (pl - low[i]) / pl * 100.0
            else:
                out[i] = 0.0
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            if PIERCE_COL in df.columns:
                rec = pd.to_numeric(df[PIERCE_COL], errors="coerce").values
            else:
                rec = np.full(len(df), np.nan)
            recomputed = _pierce_from_prices(df)
            pierce = np.where(np.isfinite(rec), rec, recomputed)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                in_sit = (np.isfinite(pierce[i]) and pierce[i] > 0
                          and regime[i] == "mean_reversion")
                if in_sit and fc[i] > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else (agreement >= 0.9)

    reading = ("Situation = a reclaimed pierce of the prior 30-day low (recorded pierce_depth raw value > 0, recomputed from "
               "prices where not recorded) on a bar the detector sent to mean_reversion (the regime column carries the "
               "falling-agitated profile vetoes, whose 60-bar trend and 365-bar volatility percentile cannot be rebuilt "
               "inside a window), expected side long; a case is a forecast rise of at least 2 points from its lowest "
               "positive level since the last bet (from 0 after a flat), the first in each 5-bar grid cell of its window; "
               "the coin's mean 5-day return is taken on the non-overlapping grid of all its windows; the day-clustered "
               "t uses per-day sums of deviations with a G/(G-1) correction; the deeper half is forecast above the "
               "median, the shallower half at or below it; the plan's 'fewer than 30 cases or 25 days' rule is reported "
               "as 'not observable'.")

    main_name = "mean excess 5-day return of long bets over the coin's mean 5-day return"
    main_thr = "confirm: mean > 0 with t >= 2 and deeper-minus-shallower > 0; reject: mean < 0 with t <= -2"
    sup_name = "deeper-half minus shallower-half mean excess 5-day return (split at median forecast)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on the long side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars of a reclaimed 30-day-low "
                           "pierce in the mean_reversion regime, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. coin mean 5-day return (non-overlapping grid, all windows) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    cases = []  # (day, excess, forecast)
    for coin, wins in bars.items():
        cm = coin_mean.get(coin, np.nan)
        if not np.isfinite(cm):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = df["close"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            floor = 0.0
            used_cells = set()
            for i in range(len(df)):
                f = fc[i]
                bet = False
                if f <= 0:
                    floor = 0.0
                else:
                    if f - floor >= BAND:
                        bet = True
                        floor = f
                    else:
                        floor = min(floor, f)
                if not bet:
                    continue
                cell = i // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if i + H >= len(df):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                cases.append((ts.iloc[i].normalize(), r - cm, float(f)))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_ex = None
    t_val = None
    if n_cases > 0:
        ex = np.array([x[1] for x in cases])
        mean_ex = float(ex.mean())
        if n_days >= 2:
            dev = pd.Series(ex - mean_ex, index=[x[0] for x in cases]).groupby(level=0).sum().values
            G = len(dev)
            se = np.sqrt(G / (G - 1) * np.sum(dev ** 2)) / n_cases
            t_val = float(mean_ex / se) if se > 0 else None

    sup_val = None
    sup_t = None
    sup_pass = None
    if n_cases >= 2:
        fcs = np.array([x[2] for x in cases])
        ex = np.array([x[1] for x in cases])
        med = np.median(fcs)
        deep = ex[fcs > med]
        shal = ex[fcs <= med]
        if len(deep) > 0 and len(shal) > 0:
            sup_val = float(deep.mean() - shal.mean())
            sup_pass = bool(sup_val > 0)
            if len(deep) >= 2 and len(shal) >= 2:
                tt = stats.ttest_ind(deep, shal, equal_var=False)
                if np.isfinite(tt.statistic):
                    sup_t = float(tt.statistic)
        else:
            sup_pass = False
    counts["cases in deeper half"] = int(np.sum(np.array([x[2] for x in cases]) > np.median([x[2] for x in cases]))) if n_cases else 0

    # ---------- 4. decision ----------
    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"The plan's minimum is not reached: {n_cases} cases (minimum 30) on {n_days} distinct days "
                   f"(minimum 25).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed (zero spread), so neither rule is met."
    elif mean_ex > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean excess 5-day return is above 0 with t >= 2 and the deeper-minus-shallower difference is above 0."
        else:
            status = "inconclusive"
            decided = "The mean excess 5-day return is above 0 with t >= 2 but the depth check is not above 0, which the plan calls inconclusive."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean excess 5-day return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess 5-day return lies between -2 and 2 (or its sign disagrees with the mean), meeting neither rule."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean, deviations summed per day", "value": t_val} if t_val is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name + (f" (Welch t {sup_t:.3f})" if sup_t is not None else ""),
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
