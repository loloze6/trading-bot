import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    AGE_COL = "debug_info.components.cross_age.last_history_value"

    def get_age(df):
        if AGE_COL in df.columns:
            return pd.to_numeric(df[AGE_COL], errors="coerce").to_numpy(dtype=float)
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].tolist():
                val = np.nan
                try:
                    if isinstance(v, dict):
                        c = v.get("cross_age")
                        if isinstance(c, dict) and c.get("last_history_value") is not None:
                            val = float(c.get("last_history_value"))
                except Exception:
                    val = np.nan
                out.append(val)
            return np.asarray(out, dtype=float)
        # Column missing: the regime never ran in this window; it is not a value of zero.
        return np.full(len(df), np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            age = get_age(df)
            active = np.isfinite(fc) & (fc != 0)
            with np.errstate(invalid="ignore"):
                sit = np.isfinite(age) & (age >= 1) & (age <= 30)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement if agreement is not None else 0.0, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("No bar has a non-zero forecast, so the config never takes the plan's short in the 1-30 day post-golden-cross regime."
                           if n_active == 0 else
                           "Fewer than 90% of active bars are short bars with 50/200 SMA cross age between 1 and 30, so the config does not trade the plan's situation on its side."),
            "reading": "The situation is read from the raw cross_age component (bars since the 50-day SMA crossed above the 200-day SMA, between 1 and 30), and the expected side is short.",
        }

    # ---------- 2. criterion ----------
    # Per coin: grid rows (positions 0, 10, 20, ... of each window) with forward 10-bar return inside the window.
    coin_rows = {}
    for coin in sorted(bars.keys()):
        rows = []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            age = get_age(df)
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    continue
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((c1 / c0 - 1.0, age[p]))
        coin_rows[coin] = rows

    excess_all, excess_fresh, excess_stale = [], [], []
    for coin, rows in coin_rows.items():
        if not rows:
            continue
        rets = np.array([r[0] for r in rows], dtype=float)
        ages = np.array([r[1] for r in rows], dtype=float)
        base = float(np.mean(rets))
        with np.errstate(invalid="ignore"):
            reg = np.isfinite(ages) & (ages >= 1) & (ages <= 30)
            fresh = reg & (ages <= 15)
            stale = reg & (ages >= 16)
        excess_all.extend((rets[reg] - base).tolist())
        excess_fresh.extend((rets[fresh] - base).tolist())
        excess_stale.extend((rets[stale] - base).tolist())

    x = np.asarray(excess_all, dtype=float)
    n_cases = int(len(x))
    mean_ex = float(np.mean(x)) if n_cases > 0 else None
    t_main = None
    if n_cases >= 2:
        sd = float(np.std(x, ddof=1))
        if sd > 0:
            t_main = float(mean_ex / (sd / np.sqrt(n_cases)))

    f = np.asarray(excess_fresh, dtype=float)
    s = np.asarray(excess_stale, dtype=float)
    diff = float(np.mean(f) - np.mean(s)) if (len(f) > 0 and len(s) > 0) else None
    t_sup = None
    if len(f) >= 2 and len(s) >= 2:
        tt = stats.ttest_ind(f, s, equal_var=False)
        if np.isfinite(tt.statistic):
            t_sup = float(tt.statistic)
    sup_passed = None if t_sup is None else bool(t_sup < 0 and diff is not None and diff < 0)

    counts = {
        "non-overlapping regime cases": n_cases,
        "fresh cases (age 1-15)": int(len(f)),
        "stale cases (age 16-30)": int(len(s)),
    }

    if n_cases < 20:
        status = "not observable"
        decided_by = f"Only {n_cases} non-overlapping regime cases across all coins and windows, below the plan's minimum of 20."
    elif t_main is None:
        status = "inconclusive"
        decided_by = "The main-measure t could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif t_main <= -2:
        if sup_passed:
            status = "confirmed"
            decided_by = "The main-measure t is -2 or less and the fresh-minus-stale excess return is below zero (Welch t below 0)."
        else:
            status = "inconclusive"
            decided_by = "The main-measure t is -2 or less but the fresh-minus-stale difference is not below zero (or could not be measured), which the plan calls inconclusive."
    elif t_main >= 2:
        status = "rejected"
        decided_by = "The main-measure t is +2 or more: after fresh golden crosses the coin rises more than usual."
    else:
        status = "inconclusive"
        decided_by = "The main-measure t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean 10-bar forward excess return on regime bars vs coin's all-window grid mean",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_main} if t_main is not None else None,
            "threshold": "confirm if t <= -2 (with fresh-minus-stale below zero); reject if t >= +2; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "fresh (age 1-15) minus stale (age 16-30) excess return, Welch t below 0",
            "value": t_sup,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": "Regime bars and freshness are read from the raw cross_age value on grid bars (positions 0,10,20,... of each window, with the forward return inside the window), the baseline is each coin's mean 10-bar grid return over all its windows, the supporting check counts as passed only when the Welch t (fresh minus stale) is below 0, and fewer than 20 cases gives 'not observable' as the workflow's minimum-count rule requires.",
    }
