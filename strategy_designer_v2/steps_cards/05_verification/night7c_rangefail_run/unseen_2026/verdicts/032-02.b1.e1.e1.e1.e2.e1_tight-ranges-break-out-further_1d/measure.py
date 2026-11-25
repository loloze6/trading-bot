import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    LOOK = 60
    NARROW_COL = "debug_info.components.narrow.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    n_agree_regime_fallback = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            prior_max = close.shift(1).rolling(LOOK, min_periods=LOOK).max()
            computable = prior_max.notna() & close.notna()
            situation = computable & (close > prior_max)
            active = fc != 0
            act_comp = active & computable
            n_active += int(act_comp.sum())
            n_agree += int((act_comp & situation & (fc > 0)).sum())
            act_unc = active & ~computable
            n_active_uncomputable += int(act_unc.sum())
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            n_agree_regime_fallback += int((act_unc & (reg == "trending") & (fc > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
    elif n_active_uncomputable > 0:
        agreement = n_agree_regime_fallback / n_active_uncomputable
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    reading = (
        "The situation (close above the highest of the prior 60 closes, long side) is checked on active bars with 60 prior "
        "closes in their window, those without are left out of the agreement (regime used only if none is computable); "
        "a case is the first trending bar in each 20-bar grid cell (positions 0,20,40,... from the window's first row) "
        "with its 20-bar return from that bar inside the window; the coin's mean 20-bar return is over the non-overlapping "
        "grid returns of all its windows; the narrower half is narrow.last_history_value above the coin's median of its "
        "cases (a larger proximity to the low means a tighter range), the wider half below it, cases equal to the median "
        "are left out; a minimum count not reached gives 'not observable'."
    )

    main_name = "Welch t of 20-bar excess return, narrower half minus wider half"
    threshold = "confirm: t >= 2 with positive narrow-half mean excess; reject: t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars on a new 60-day closing high, "
                          "as the plan's situation and side require.",
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    narrow_ex = []
    wide_ex = []
    n_cases = 0
    for coin, wins in bars.items():
        # coin's mean 20-bar return over all windows (non-overlapping grid)
        grid_rets = []
        coin_cases = []  # (narrow value, forward return)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                    grid_rets.append(c1 / c0 - 1.0)
            reg = df["regime"].astype(str).values
            nv = (pd.to_numeric(df[NARROW_COL], errors="coerce").values
                  if NARROW_COL in df.columns else np.full(n, np.nan))
            for start in range(0, n, H):
                end = min(start + H, n)
                idx = [i for i in range(start, end) if reg[i] == "trending"]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 != 0):
                    continue
                if not np.isfinite(nv[t]):
                    continue
                coin_cases.append((float(nv[t]), c1 / c0 - 1.0))
        if not coin_cases or not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        vals = np.array([c[0] for c in coin_cases])
        exc = np.array([c[1] for c in coin_cases]) - mu
        n_cases += len(coin_cases)
        med = np.median(vals)
        narrow_ex.extend(exc[vals > med].tolist())
        wide_ex.extend(exc[vals < med].tolist())

    n_n = len(narrow_ex)
    n_w = len(wide_ex)
    counts = {"cases": int(n_cases), "narrower-half cases": int(n_n), "wider-half cases": int(n_w)}

    t_val = None
    diff = None
    if n_n >= 2 and n_w >= 2:
        r = stats.ttest_ind(np.array(narrow_ex), np.array(wide_ex), equal_var=False)
        t_val = float(r.statistic) if np.isfinite(r.statistic) else None
        diff = float(np.mean(narrow_ex) - np.mean(wide_ex))
    narrow_mean = float(np.mean(narrow_ex)) if n_n > 0 else None
    sup_pass = None if narrow_mean is None else bool(narrow_mean > 0)

    main = {"name": main_name, "value": diff,
            "statistic": None if t_val is None else {"name": "Welch t", "value": t_val},
            "threshold": threshold}
    sup = {"name": "narrower-half mean excess 20-bar return > 0", "value": narrow_mean, "passed": sup_pass}

    if n_cases < 60 or n_n < 20 or n_w < 20:
        status = "not observable"
        decided_by = ("The plan's minimum of 60 cases with at least 20 in each half is not reached "
                      f"({n_cases} cases, {n_n} narrower, {n_w} wider).")
    elif t_val is None:
        status = "inconclusive"
        decided_by = "Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "Welch t of narrow minus wide is 2 or more and the narrower-half mean excess return is positive."
    elif t_val >= 2:
        status = "inconclusive"
        decided_by = "Welch t is 2 or more but the narrower-half mean excess return is not positive."
    elif t_val <= -2:
        status = "rejected"
        decided_by = "Welch t of narrow minus wide is -2 or less."
    else:
        status = "inconclusive"
        decided_by = "Welch t of narrow minus wide lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
