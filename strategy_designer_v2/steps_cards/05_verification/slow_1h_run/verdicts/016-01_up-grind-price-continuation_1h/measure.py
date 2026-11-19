import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW = "debug_info.components.grind_share.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): the window rose and the residual grind share is positive -> raw value > 0.
    # Expected side: the outcome is a rise, so the idea is long (forecast > 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = (pd.to_numeric(df[RAW], errors="coerce")
                   if RAW in df.columns else pd.Series(np.nan, index=df.index))
            active = fc.notna() & (fc != 0)
            situ = raw.notna() & (raw > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "next-72-bar return, top third minus bottom third of forecast (>0) on the 72-bar grid"
    threshold = "Welch t >= 2 confirms (with supporting check), Welch t <= -2 rejects"
    sup_name = "top third mean next-72-bar return minus holding-the-coin mean 72-bar return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the raw grind "
                           "share is positive (a risen window), so the config does not trade the plan's situation."
                           if n_active > 0 else "The record has no active bars, so the config never trades the plan's situation."),
            "reading": "The situation is read as the raw residual share being above 0 (the window rose and small hours carried part of it), on the long side.",
        }

    # ---------- 2. Criterion ----------
    rows = []          # (coin, forecast, fwd return) for grid bars with forecast > 0
    hold = {}          # coin -> list of grid fwd returns over all windows
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                hold.setdefault(coin, []).append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    rows.append((coin, fc[i], r))

    hold_mean = {c: float(np.mean(v)) for c, v in hold.items() if len(v) > 0}

    if len(rows) >= 3:
        d = pd.DataFrame(rows, columns=["coin", "fc", "ret"])
        d = d.sort_values("fc", kind="mergesort").reset_index(drop=True)
        terc = pd.qcut(np.arange(len(d)), 3, labels=False)
        bottom = d[terc == 0]
        top = d[terc == 2]
    else:
        bottom = top = pd.DataFrame(columns=["coin", "fc", "ret"])

    n_top, n_bot = int(len(top)), int(len(bottom))
    counts = {"grid cases in top third": n_top, "grid cases in bottom third": n_bot,
              "grid cases with forecast above 0": int(len(rows))}

    diff = t = None
    if n_top >= 2 and n_bot >= 2:
        diff = float(top["ret"].mean() - bottom["ret"].mean())
        tt = stats.ttest_ind(top["ret"].to_numpy(float), bottom["ret"].to_numpy(float), equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    sup_val = sup_pass = None
    if n_top > 0:
        bench = float(np.mean([hold_mean.get(c, np.nan) for c in top["coin"]]))
        if np.isfinite(bench):
            sup_val = float(top["ret"].mean() - bench)
            sup_pass = bool(sup_val > 0)

    reading = ("Thirds are equal-size splits of the pooled grid cases sorted by forecast (ties kept in coin/window/time order), "
               "and the holding benchmark for the pooled top third is the mean, over its cases, of each case's coin mean "
               "72-bar grid return over all windows; the situation is a positive raw residual share on the long side.")

    if n_top < 100 or n_bot < 100:
        status = "not observable"
        decided = "Fewer than 100 grid cases in at least one third, the plan's minimum count."
    elif t is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The top-minus-bottom Welch t is 2 or more and the top third beats holding the coin."
    elif t <= -2:
        status = "rejected"
        decided = "The top-minus-bottom Welch t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The Welch t is 2 or more but the supporting check fails (top third does not beat holding the coin)."
    else:
        status = "inconclusive"
        decided = "The top-minus-bottom Welch t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": ({"name": "Welch t", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
