import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rise_px = close / close.shift(3) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                rising = np.where(raw.notna(), raw > 0, rise_px > 0)
            else:
                rising = (rise_px > 0).values
            profile = (df["regime"].astype(str) == "unknown").values
            active = (fc != 0).values
            ok = profile & np.asarray(rising, dtype=bool) & (fc < 0).values
            n_active += int(active.sum())
            n_agree += int((active & ok).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars on a 3-day rise inside the "
                           "falling-agitated profile (regime 'unknown'), so the forecast does not do what "
                           "the Fidelity says." if n_active > 0 else "The record has no active bar."),
            "reading": "The profile is read from the recorded regime ('unknown' = no veto, the falling agitated profile) and the rise from the sign of the raw scaled 3-day return (prices where it is not recorded).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        # normal drift: mean 5-bar return on the grid of all the coin's windows
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # short bets: rise of the short forecast's size by >= band from its lowest size since last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f < 0:
                    m = -f
                    if m - ref >= BAND:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                else:
                    ref = 0.0
            # one case per 5-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                ret = c[i + H] / c[i] - 1.0
                if not np.isfinite(ret):
                    continue
                unusual_short = -(ret - drift)
                rise = c[i] / c[i - 3] - 1.0 if i >= 3 else np.nan
                share = unusual_short / rise if (np.isfinite(rise) and rise > 0) else np.nan
                rows.append({
                    "coin": coin, "window": w, "ts": ts.iloc[i],
                    "day": ts.iloc[i].floor("D"),
                    "u": unusual_short, "share": share, "absf": abs(fc[i]),
                })

    cases = pd.DataFrame(rows)
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_u = None
    if n_cases >= 2:
        dev = cases["u"] - mean_u
        per_day = dev.groupby(cases["day"]).sum()
        G = len(per_day)
        if G >= 2:
            se = np.sqrt(G / (G - 1) * float((per_day ** 2).sum())) / n_cases
            t_u = float(mean_u / se) if se > 0 else None

    welch = None
    diff = None
    n_top = n_bot = 0
    sc = cases.dropna(subset=["share"]) if n_cases else cases
    if len(sc) >= 4:
        sc = sc.sort_values(["absf", "ts", "coin"], kind="mergesort").reset_index(drop=True)
        k = len(sc) // 2
        bot = sc["share"].iloc[:k].values
        top = sc["share"].iloc[k:].values
        n_top, n_bot = len(top), len(bot)
        if n_top >= 2 and n_bot >= 2:
            diff = float(np.mean(top) - np.mean(bot))
            tt = stats.ttest_ind(top, bot, equal_var=False)
            if np.isfinite(tt.statistic):
                welch = float(tt.statistic)
    sup_passed = None if welch is None else bool(welch >= 2)

    counts = {"cases": n_cases, "distinct days": n_days,
              "top half cases": int(n_top), "bottom half cases": int(n_bot)}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"Minimum count not reached: {n_cases} cases and {n_days} distinct days, the plan needs at least 30 of each."
    elif t_u is not None and mean_u > 0 and t_u >= 2 and welch is not None and welch >= 2:
        status = "confirmed"
        decided = "Confirm: the mean unusual short move is above 0 with t >= 2 and the share-given-back Welch t (top minus bottom half of |forecast|) is >= 2."
    elif (t_u is not None and t_u <= -2) or (welch is not None and welch <= -2):
        status = "rejected"
        decided = "Reject: the mean unusual short move has t <= -2 (rises continue) or the share-given-back Welch t is <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: enough cases, but the numbers meet neither the confirm rule (both t >= 2) nor the reject rule (either t <= -2)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 5-day move in the short direction per short-bet case",
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "t of the mean, cases of one day pooled", "value": t_u},
            "threshold": "confirm: mean > 0 with t >= 2; reject: t <= -2",
        },
        "supporting_check": {
            "name": "share given back, top minus bottom half of |forecast|, Welch t",
            "value": welch,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first short bet (|forecast| rising >= 2 from its lowest size since the last bet, reset at flat or side change) in each 5-bar grid cell of a window, the share given back is the short-direction unusual move over the 3-day price rise to that bar, "
                    "and the halves are split by sorting cases on |forecast| (ties by time) with the lower floor(n/2) as the bottom half."),
    }
