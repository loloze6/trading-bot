import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    RISE = "debug_info.components.rise.last_history_value"
    PRIOR = "debug_info.components.prior_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            fc = d["forecast"].astype(float).fillna(0.0)
            d["forecast"] = fc
            # rise today: raw value when recorded, else recomputed from prices
            rise_px = close / close.shift(1) - 1.0
            prior_px = close.shift(1) / close.shift(6) - 1.0
            rise_raw = d[RISE].astype(float) if RISE in d.columns else pd.Series(np.nan, index=d.index)
            prior_raw = d[PRIOR].astype(float) if PRIOR in d.columns else pd.Series(np.nan, index=d.index)
            rise_v = rise_raw.where(rise_raw.notna(), rise_px)
            prior_v = prior_raw.where(prior_raw.notna(), prior_px)
            situ = (rise_v > 0) & (prior_v < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())
            prepared[coin][w] = d

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean unusual 3-bar move after short bets, in the short direction"
    main_thr = "mean > 0 with day-pooled t >= 2 to confirm; mean < 0 with t <= -2 to reject"
    sup_name = "large-minus-small (median |forecast|) mean unusual move, Welch t"

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "Fewer than 90% of the active bars are short bars on a rise day after a 5-day fall "
                          "(close[t] > close[t-1] and close[t-1] < close[t-6]), as the plan's Fidelity requires.",
            "reading": "The situation is the adapted regime (today up, prior 5-day fall) on the short side; "
                       "the profile is not part of the check since it is added by code.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in prepared.items():
        # normal drift: mean 3-bar return on non-overlapping grid of all windows
        grid_rets = []
        for w, d in wins.items():
            c = d["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, d in wins.items():
            c = d["close"].astype(float).values
            fc = d["forecast"].values
            ts = d["timestamp"]
            n = len(d)
            # short bets: rise of |short forecast| of >= BAND from its lowest level since the last bet
            ref = 0.0
            prev_side = 0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                side = -1 if f < 0 else (1 if f > 0 else 0)
                if side != -1:
                    ref = 0.0
                    prev_side = side
                    continue
                m = -f
                if prev_side != -1:
                    ref = 0.0
                if m - ref >= BAND:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
                prev_side = -1
            seen_cells = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                rows.append({
                    "day": ts.iloc[i].strftime("%Y-%m-%d"),
                    "unusual": -(r - drift),
                    "absf": abs(float(fc[i])),
                })

    cases = pd.DataFrame(rows, columns=["day", "unusual", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_val = None
    t_main = None
    if n_cases >= 2:
        x = cases["unusual"].values
        mean_val = float(np.mean(x))
        dev = pd.Series(x - mean_val).groupby(cases["day"].values).sum().values
        G = len(dev)
        if G > 1:
            se = np.sqrt(np.sum(dev ** 2) * G / (G - 1)) / n_cases
            t_main = float(mean_val / se) if se > 0 else None

    diff = None
    t_w = None
    if n_cases >= 4:
        med = float(np.median(cases["absf"].values))
        large = cases.loc[cases["absf"] > med, "unusual"].values
        small = cases.loc[cases["absf"] <= med, "unusual"].values
        if len(large) >= 2 and len(small) >= 2:
            diff = float(np.mean(large) - np.mean(small))
            tw = stats.ttest_ind(large, small, equal_var=False).statistic
            t_w = float(tw) if np.isfinite(tw) else None
    sup_pass = None if diff is None else bool(diff > 0)

    reading = ("A case is the first short bet (|forecast| rise of >= 2 points from its lowest level since the last bet) "
               "in each 3-bar grid cell of a window, its 3-bar return taken from that bar's close; the median split puts "
               "|forecast| above the median in the larger group and the rest in the smaller; the plan's 'else inconclusive' "
               "for too few cases is reported as 'not observable' per the workflow; the day-pooled t sums deviations per "
               "UTC day with a G/(G-1) correction.")

    if n_cases < 50 or n_days < 30:
        status = "not observable"
        decided = f"The minimum of 50 cases on 30 distinct days is not reached ({n_cases} cases, {n_days} days)."
    elif t_main is None:
        status = "inconclusive"
        decided = "The main t could not be computed, so neither the confirm nor the reject rule is met."
    elif (mean_val < 0 and t_main <= -2) or (t_w is not None and t_w <= -2):
        status = "rejected"
        if mean_val < 0 and t_main <= -2:
            decided = "Reject: the main mean is below 0 with t <= -2 (bounces are followed by rises)."
        else:
            decided = "Reject: the large-minus-small difference has a Welch t <= -2."
    elif mean_val > 0 and t_main >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = "Confirm: the main mean is above 0 with t >= 2 and the large-minus-small difference is above 0."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "Inconclusive: main t >= 2 but the large-minus-small difference is <= 0 (or missing) with a t above -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t with same-day cases pooled", "value": t_main} if t_main is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name,
            "value": diff,
            "passed": sup_pass,
            "welch_t": t_w,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
