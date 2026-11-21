import numpy as np
import pandas as pd
from scipy import stats

H = 26
BAND = 2.0
COL_RAW = "debug_info.components.thin_cloud.last_history_value"


def _cloud_state(df):
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)
    tenkan = (high.rolling(9).max() + low.rolling(9).min()) / 2.0
    kijun = (high.rolling(26).max() + low.rolling(26).min()) / 2.0
    span_a = ((tenkan + kijun) / 2.0).shift(26)
    span_b = ((high.rolling(52).max() + low.rolling(52).min()) / 2.0).shift(26)
    top = np.maximum(span_a, span_b)
    bot = np.minimum(span_a, span_b)
    state = np.full(len(df), np.nan)
    ok = (~top.isna()) & (~bot.isna())
    c = close.values
    state[ok.values & (c > top.values)] = 1
    state[ok.values & (c < bot.values)] = -1
    state[ok.values & (c <= top.values) & (c >= bot.values)] = 0
    return state


def _situation(state):
    # 1.0 situation holds, 0.0 does not, nan unknown (cloud or cross origin not computable)
    n = len(state)
    sit = np.full(n, np.nan)
    for t in range(n):
        s = state[t]
        if np.isnan(s):
            continue
        if s != 1:
            sit[t] = 0.0
            continue
        # start of current above-cloud run
        r = t
        while r - 1 >= 0 and state[r - 1] == 1:
            r -= 1
        if r - 1 < 0 or np.isnan(state[r - 1]):
            continue  # unknown
        # where did the run come from: last bar outside the cloud before r
        j = r - 1
        while j >= 0 and state[j] == 0:
            j -= 1
        if j < 0 or np.isnan(state[j]):
            continue  # unknown
        if state[j] == -1:
            sit[t] = 1.0 if (t - r) <= H else 0.0
        else:
            sit[t] = 0.0
    return sit


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    n_active_fallback = 0
    n_agree_fallback = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = df["forecast"].astype(float).fillna(0.0).values
            sit = _situation(_cloud_state(df))
            act = fc != 0
            known = act & ~np.isnan(sit)
            n_active += int(known.sum())
            n_agree += int((known & (sit == 1.0) & (fc > 0)).sum())
            reg = df["regime"].astype(str).values
            n_active_fallback += int(act.sum())
            n_agree_fallback += int((act & (reg == "trending") & (fc > 0)).sum())
    if n_active > 0:
        agreement = n_agree / n_active
        check_note = "agreement measured on active bars where the cloud (9/26/52, displacement 26) and the cross origin are computable from the window's prices"
    elif n_active_fallback > 0:
        agreement = n_agree_fallback / n_active_fallback
        check_note = "no active bar had a computable cloud, so agreement uses the recorded regime ('trending') with a positive forecast"
    else:
        agreement = None
        check_note = "no active bars"
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": "thin minus thick cloud unusual 26-bar return", "value": None,
                             "statistic": None, "threshold": "Welch t >= 2 (confirm), <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"cases": 0, "thin_cases": 0, "thick_cases": 0},
            "decided_by": "Fewer than 90% of active bars are long bars while above the cloud within 26 bars of an up-cross from below, as the Fidelity states.",
            "reading": check_note + "; the up-cross counts when the close leaves the cloud upward after last being outside it below, active from the cross bar for up to 26 further bars while above.",
        }

    # ---------- coin normal drift ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df.sort_values("timestamp")["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    cases = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = df["forecast"].astype(float).fillna(0.0).values
            c = df["close"].astype(float).values
            raw = df[COL_RAW].astype(float).values if COL_RAW in df.columns else np.full(len(df), np.nan)
            taken = set()
            for t in range(1, len(df)):
                if fc[t - 1] == 0 and fc[t] - fc[t - 1] >= BAND:
                    cell = t // H
                    if cell in taken:
                        continue
                    taken.add(cell)
                    if t + H >= len(df):
                        continue
                    if not (np.isfinite(raw[t]) and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                        continue
                    if not np.isfinite(drift.get(coin, np.nan)):
                        continue
                    r = c[t + H] / c[t] - 1.0
                    cases.append((raw[t], r - drift[coin]))

    n = len(cases)
    raws = np.array([x[0] for x in cases]) if n else np.array([])
    unus = np.array([x[1] for x in cases]) if n else np.array([])
    if n:
        med = float(np.median(raws))
        thin = unus[raws > med]
        thick = unus[raws <= med]
    else:
        thin = thick = np.array([])
    n_thin, n_thick = len(thin), len(thick)
    counts = {"cases": int(n), "thin_cases": int(n_thin), "thick_cases": int(n_thick)}

    diff = welch = None
    if n_thin >= 2 and n_thick >= 2:
        diff = float(thin.mean() - thick.mean())
        welch = float(stats.ttest_ind(thin, thick, equal_var=False).statistic)
    mean_all = t_all = None
    if n >= 2:
        mean_all = float(unus.mean())
        sd = float(unus.std(ddof=1))
        t_all = float(mean_all / (sd / np.sqrt(n))) if sd > 0 else None
    sup_pass = None if t_all is None else bool(mean_all > 0 and t_all >= 2)

    reading = (check_note + "; a case is a bar where the forecast rises by at least 2 from 0 on the previous bar, the first such in each 26-bar grid cell from the window's first row, "
               "thin cases have raw proximity strictly above the median of all cases and the rest are thick, and the plan's 'inconclusive with few cases' is reported as not observable.")

    if n < 40 or n_thin < 20 or n_thick < 20:
        status = "not observable"
        decided = f"Minimum counts not reached: {n} cases (need 40), {n_thin} thin and {n_thick} thick (need 20 each)."
    elif (welch is not None and welch <= -2) or (t_all is not None and t_all <= -2):
        status = "rejected"
        decided = "Reject rule met: thin-minus-thick Welch t is -2 or less, or the all-case mean unusual return has t of -2 or less."
    elif diff is not None and diff > 0 and welch is not None and welch >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule met: thin-minus-thick difference above 0 with Welch t >= 2, and the all-case mean unusual return above 0 with t >= 2."
    else:
        status = "inconclusive"
        decided = "Neither the confirm rule (difference > 0, Welch t >= 2, with supporting check passed) nor the reject rule (t <= -2) is met."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "thin minus thick cloud unusual 26-bar return", "value": diff,
                         "statistic": None if welch is None else {"name": "Welch t", "value": welch},
                         "threshold": "difference > 0 with Welch t >= 2 to confirm; Welch t <= -2 to reject"},
        "supporting_check": {"name": "all-case mean unusual 26-bar return > 0 with t >= 2",
                             "value": mean_all, "passed": sup_pass,
                             "t": t_all},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
