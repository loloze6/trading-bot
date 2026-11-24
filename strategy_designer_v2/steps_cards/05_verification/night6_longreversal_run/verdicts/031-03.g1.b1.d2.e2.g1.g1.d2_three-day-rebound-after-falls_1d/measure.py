import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"
    H = 3

    # ---------- 1. Situation check ----------
    active_total = 0
    active_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Where the raw value is not recorded, use the sign of the 1-day return
            # (same sign as the raw value, since the volatility terms are positive).
            ret1 = df["close"] / df["close"].shift(1) - 1
            raw_sign_src = raw.where(raw.notna(), ret1)
            active = fc.notna() & (fc != 0)
            situation = raw_sign_src < 0  # a one-day fall
            expected_side = fc > 0        # long
            active_total += int(active.sum())
            active_ok += int((active & situation & expected_side).sum())

    agreement = (active_ok / active_total) if active_total > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "Pearson correlation of forecast with excess next-3-day return",
                "value": None, "statistic": None,
                "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"grid bars with forecast > 0": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are one-day falls "
                           "(raw value below 0) with a long forecast, as the Fidelity's situation "
                           "and long side require." if agreement is not None else
                           "No bar has a non-zero forecast, so the config never takes the plan's situation."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    fcs, rets = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fwd = close.shift(-H) / close - 1
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            grid = np.arange(0, len(df), H)
            g = pd.DataFrame({"fc": fc.iloc[grid].values, "r": fwd.iloc[grid].values}).dropna()
            fcs.extend(g["fc"].tolist())
            rets.extend(g["r"].tolist())

    fcs = np.asarray(fcs, dtype=float)
    rets = np.asarray(rets, dtype=float)
    n = len(fcs)
    mean_ret = float(np.mean(rets)) if n > 0 else np.nan
    excess = rets - mean_ret

    pos_mask = fcs > 0
    n_pos = int(pos_mask.sum())

    r = None
    t = None
    if n >= 3 and np.std(fcs) > 0 and np.std(excess) > 0:
        r = float(stats.pearsonr(fcs, excess)[0])
        if abs(r) < 1:
            t = float(r * np.sqrt(n - 2) / np.sqrt(1 - r ** 2))
        else:
            t = float(np.sign(r) * np.inf)

    # Supporting check: top third of positive-forecast grid bars by forecast
    top_mean = None
    sup_pass = None
    if n_pos > 0:
        pf = fcs[pos_mask]
        pe = excess[pos_mask]
        k = int(np.ceil(n_pos / 3.0))
        order = np.argsort(-pf, kind="mergesort")
        top_mean = float(np.mean(pe[order[:k]]))
        sup_pass = bool(top_mean > 0)

    counts = {"grid bars with forecast > 0": n_pos, "grid bars": int(n)}

    if n_pos < 100:
        status = "not observable"
        decided_by = (f"Only {n_pos} grid bars have forecast > 0, below the plan's minimum of 100.")
    elif t is None:
        status = "inconclusive"
        decided_by = "The correlation could not be computed (no variation), so neither confirm nor reject is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The correlation t is >= 2, the top-third check passes, with at least 100 grid bars with forecast > 0."
    elif t <= -2:
        status = "rejected"
        decided_by = "The correlation t is <= -2: larger scaled, volatility-weighted falls are followed by weaker 3-day returns."
    elif t >= 2:
        status = "inconclusive"
        decided_by = "The correlation t is >= 2 but the top-third check fails."
    else:
        status = "inconclusive"
        decided_by = "The correlation t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "Pearson correlation of forecast with excess next-3-day return (grid bars)",
            "value": r,
            "statistic": ({"name": "correlation t", "value": t} if t is not None else None),
            "threshold": "t >= 2 (with top-third check and >= 100 grid bars with forecast > 0) to confirm; t <= -2 to reject",
        },
        "supporting_check": {
            "name": "mean excess 3-day return in top third of forecast > 0 grid bars",
            "value": top_mean,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("The correlation uses all grid bars (positions 0, 3, 6, ... of each window, forecast zero included) "
                    "with the excess over the mean 3-day grid return of all windows; the top third is the ceil(n/3) "
                    "positive-forecast grid bars with the largest forecasts; the plan's fewer-than-100 rule is applied "
                    "as a minimum count, giving 'not observable'."),
    }
