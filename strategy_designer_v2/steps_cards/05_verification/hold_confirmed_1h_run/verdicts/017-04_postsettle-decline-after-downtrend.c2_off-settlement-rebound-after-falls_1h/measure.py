import numpy as np
import pandas as pd


def measure(bars):
    HTS_REGIME = "mean_reversion"
    RAW = "debug_info.components.fall72.last_history_value"
    H = 2
    MIN_CASES = 200

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): an off-settlement close (the detector's regime mean_reversion, hts 3..6)
    # after a 72-bar fall (raw 72-bar price change < 0). Expected side: long (outcome is a rise).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            active = fc != 0
            if not active.any():
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # where the raw value is missing, recompute the 72-bar change from the prices
            recomputed = np.full(len(df), np.nan)
            if len(df) > 72:
                recomputed[72:] = close[72:] / close[:-72] - 1.0
            raw = np.where(np.isnan(raw), recomputed, raw)
            regime = df["regime"].astype(str).values
            situation = (regime == HTS_REGIME) & (raw < 0)
            agree = situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((agree & active).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "t of mean of (forecast/10) x excess 2-bar return",
                "value": None,
                "statistic": None,
                "threshold": "t >= 2 confirms, t <= -2 rejects, with at least 200 cases",
            },
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": (
                "Fewer than 90% of the active bars are off-settlement (mean_reversion) bars after a 72-bar fall "
                "with a long forecast" if n_active > 0 else "The forecast is never active, so the config never "
                "takes the plan's long-after-fall position"
            ),
            "reading": "The off-settlement condition is read from the recorded regime (the detector's decision) "
                       "and the fall from the raw 72-bar change being below 0.",
        }

    # ---------- 2. Criterion ----------
    # coin mean 2-bar return over all windows (non-overlapping grid, all grid bars)
    records = []
    coin_means = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            regime = df["regime"].astype(str).values
            idx = np.arange(0, len(df) - H, H)
            ret = close[idx + H] / close[idx] - 1.0
            ok = np.isfinite(ret)
            all_rets.append(ret[ok])
            for i, r in zip(idx, ret):
                if not np.isfinite(r):
                    continue
                if regime[i] == HTS_REGIME and np.isfinite(fc[i]) and fc[i] > 0:
                    records.append((coin, float(fc[i]), float(r)))
        coin_means[coin] = float(np.mean(np.concatenate(all_rets))) if all_rets and \
            sum(len(a) for a in all_rets) > 0 else np.nan

    cases = pd.DataFrame(records, columns=["coin", "forecast", "ret"])
    if len(cases):
        cases["excess"] = cases["ret"] - cases["coin"].map(coin_means)
        cases = cases.dropna(subset=["excess"])
    n = int(len(cases))

    t_val = None
    mean_val = None
    if n >= 2:
        vals = (cases["forecast"] / 10.0 * cases["excess"]).values
        mean_val = float(np.mean(vals))
        sd = float(np.std(vals, ddof=1))
        t_val = float(mean_val / (sd / np.sqrt(n))) if sd > 0 else None

    diff = None
    if n >= 5:
        r = cases["forecast"].rank(method="first")
        q = pd.qcut(r, 5, labels=False)
        top = cases.loc[q == 4, "excess"].mean()
        bot = cases.loc[q == 0, "excess"].mean()
        diff = float(top - bot)
    sup_passed = None if diff is None else bool(diff > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 200."
    elif t_val is not None and t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "The main t is 2 or more with at least 200 cases and the top-minus-bottom quintile difference is above 0."
    elif t_val is not None and t_val <= -2:
        status = "rejected"
        decided = "The main t is -2 or less with at least 200 cases."
    elif t_val is not None and t_val >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more but the top-minus-bottom quintile difference is 0 or less."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean of (forecast/10) x (2-bar return minus coin mean 2-bar return)",
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "ordinary t of the mean", "value": t_val},
            "threshold": "t >= 2 confirms (with quintile check), t <= -2 rejects, with at least 200 cases",
        },
        "supporting_check": {
            "name": "top minus bottom forecast quintile mean excess 2-bar return",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": "The coin's mean 2-bar return is taken over all non-overlapping grid bars of all its windows, "
                   "quintiles are cut on the forecast rank (ties by order), and the off-settlement situation is "
                   "read from the recorded regime.",
    }
