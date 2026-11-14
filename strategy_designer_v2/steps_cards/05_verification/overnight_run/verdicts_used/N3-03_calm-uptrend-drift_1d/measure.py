import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RET_COL = "debug_info.components.ret20.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            n_active += int(active.sum())
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            if RET_COL in df.columns:
                r20 = pd.to_numeric(df[RET_COL], errors="coerce")
            else:
                r20 = pd.Series(np.nan, index=df.index)
            situ = (reg == "trending") & (r20 > 0)
            agree = active & situ & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess 5-bar forward return on long bars (fwd 5-bar return minus coin's mean 5-bar return), pooled, before costs"
    threshold = "confirm if mean > 0 and t >= 2; reject if mean < 0 and t <= -2 (t on non-overlapping 5-bar blocks); otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars (forecast != 0) are long bars in the 'trending' (low-volatility) "
                           "regime with a positive 20-day return, so the config does not do what the plan's situation says."),
            "reading": "Situation checked as regime == 'trending' and ret20 raw value > 0, with a long (positive) forecast.",
        }

    # ---------- 2. Criterion ----------
    all_exc, all_fc = [], []
    grid_exc = []
    for coin, wins in bars.items():
        # coin mean 5-bar forward return over all its windows together
        fwd_all = []
        frames = {}
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fwd = close.shift(-H) / close - 1.0
            frames[w] = (df.reset_index(drop=True), fwd)
            fwd_all.append(fwd.dropna().values)
        fwd_all = np.concatenate(fwd_all) if fwd_all else np.array([])
        if fwd_all.size == 0:
            continue
        coin_mean = float(np.mean(fwd_all))
        for w, (df, fwd) in frames.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            long_ = (fc > 0) & fwd.notna()
            exc = fwd - coin_mean
            pos = np.arange(len(df))
            on_grid = (pos % H) == 0
            all_exc.extend(exc[long_].tolist())
            all_fc.extend(fc[long_].tolist())
            grid_exc.extend(exc[long_ & on_grid].tolist())

    all_exc = np.asarray(all_exc, dtype=float)
    all_fc = np.asarray(all_fc, dtype=float)
    grid_exc = np.asarray(grid_exc, dtype=float)
    n_long = int(all_exc.size)
    n_grid = int(grid_exc.size)

    mean_exc = float(np.mean(all_exc)) if n_long > 0 else None
    t_val = None
    if n_grid >= 2:
        sd = float(np.std(grid_exc, ddof=1))
        if sd > 0:
            t_val = float(np.mean(grid_exc) / (sd / np.sqrt(n_grid)))

    slope = None
    sup_passed = None
    if n_long >= 3 and np.std(all_fc) > 0:
        slope = float(stats.linregress(all_fc, all_exc).slope)
        sup_passed = bool(slope > 0)

    counts = {"non-overlapping 5-bar long cases pooled across coins": n_grid, "long bars": n_long}

    if n_grid < 30:
        status = "not observable"
        decided = f"Only {n_grid} non-overlapping 5-bar long cases pooled across coins, below the plan's minimum of 30."
    elif t_val is None or mean_exc is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_exc > 0 and t_val >= 2:
        status = "confirmed"
        decided = "Mean excess 5-bar return on long bars is above 0 with t >= 2 on non-overlapping blocks (confirm rule)."
    elif mean_exc < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean excess 5-bar return on long bars is below 0 with t <= -2 on non-overlapping blocks (reject rule)."
    else:
        status = "inconclusive"
        decided = "The result meets neither the confirm nor the reject rule (t between -2 and 2 or sign disagreeing), so it is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_exc,
            "statistic": {"name": "t of the mean on non-overlapping 5-bar blocks", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of excess 5-bar return on forecast across long bars (should be > 0)",
                             "value": slope, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's mean 5-bar return is taken over all its bars' forward returns in all windows; the mean excess "
                    "is over all long bars while the t uses only long bars on each window's 0,5,10,... grid; the supporting "
                    "slope is reported but not part of the decision since the confirm/reject rules do not mention it."),
    }
