import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    LOOK = 60

    # ---------- 1. Situation check: close above every one of its prior 60 closes, long side ----------
    n_active = 0
    n_agree = 0
    n_active_unevaluable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).astype(float)
            prior_max = close.shift(1).rolling(LOOK, min_periods=LOOK).max()
            evaluable = prior_max.notna() & close.notna()
            situation = evaluable & (close > prior_max)
            active = fc != 0
            act_eval = active & evaluable
            n_active_unevaluable += int((active & ~evaluable).sum())
            n_active += int(act_eval.sum())
            n_agree += int((act_eval & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation check uses only active bars with 60 prior closes inside the same window "
               f"({n_active_unevaluable} active bars without them left out); cases are pooled over all coins and "
               "windows, a break is counted only if it is at least 20 bars after the last counted one in its "
               "coin-window, the forecast median is taken over all pooled cases, the coin's mean 20-bar return "
               "is from the 0,20,40,... grid of each window pooled over its windows, and minimum counts not "
               "reached give 'not observable'.")

    main_name = "Welch t of 20-bar excess return, forecast above vs at/below cases' median"
    threshold = "confirm: t >= 2 with forecast-weighted mean excess > 0; reject: t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active (non-zero forecast) bars are long bars on a close above "
                           "the prior 60 closes, so the config does not trade the plan's situation on its side."
                           if agreement is not None else
                           "No active bar could be checked against the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    case_rows = []
    for coin, wins in bars.items():
        # coin's mean 20-bar return over all windows (non-overlapping grid)
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        coin_mean = float(np.mean(grid_rets)) if len(grid_rets) > 0 else np.nan

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").astype(float).to_numpy()
            fc = pd.to_numeric(d["forecast"], errors="coerce").astype(float).to_numpy()
            reg = d["regime"].astype(str).to_numpy()
            last = None
            for i in range(len(d)):
                if reg[i] != "trending":
                    continue
                if last is not None and i - last < H:
                    continue
                last = i
                if i + H >= len(c):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                if not np.isfinite(fc[i]) or not np.isfinite(coin_mean):
                    continue
                r = c[i + H] / c[i] - 1.0
                case_rows.append((coin, w, i, float(fc[i]), r - coin_mean))

    n_cases = len(case_rows)
    if n_cases > 0:
        f = np.array([x[3] for x in case_rows])
        ex = np.array([x[4] for x in case_rows])
        med = float(np.median(f))
        hi = ex[f > med]
        lo = ex[f <= med]
    else:
        f = np.array([]); ex = np.array([]); med = None
        hi = np.array([]); lo = np.array([])

    n_hi, n_lo = int(len(hi)), int(len(lo))
    counts = {"non-overlapping break cases": int(n_cases),
              "cases above median forecast": n_hi,
              "cases at or below median forecast": n_lo}

    # supporting check
    sw = float(np.sum(f)) if n_cases > 0 else 0.0
    wmean = float(np.sum(ex * f) / sw) if sw != 0 else None
    supp_pass = None if wmean is None else bool(wmean > 0)

    # main t
    t = None
    diff = None
    if n_hi >= 2 and n_lo >= 2:
        diff = float(np.mean(hi) - np.mean(lo))
        tt = stats.ttest_ind(hi, lo, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    main = {"name": main_name,
            "value": diff,
            "statistic": None if t is None else {"name": "Welch t", "value": t},
            "threshold": threshold}
    supporting = {"name": "forecast-weighted mean 20-bar excess return of cases",
                  "value": wmean, "passed": supp_pass}

    if n_cases < 60 or n_hi < 25 or n_lo < 25:
        status = "not observable"
        decided = (f"The plan's minimum of 60 non-overlapping break cases with at least 25 in each half is not "
                   f"reached ({n_cases} cases, {n_hi} above and {n_lo} at or below the median).")
    elif t is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and supp_pass is True:
        status = "confirmed"
        decided = "The main t is 2 or more and the forecast-weighted mean excess return is above 0 (confirm rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more but the forecast-weighted mean excess return is not above 0 (inconclusive rule)."
    elif t <= -2:
        status = "rejected"
        decided = "The main t is -2 or less: low-run-up breaks rise less than high-run-up breaks (reject rule)."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
