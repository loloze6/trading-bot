import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.high_prox.last_history_value"

    def prox_from_prices(df):
        hi20 = df["high"].astype(float).rolling(20, min_periods=20).max()
        close = df["close"].astype(float)
        dist_pct = (hi20 - close) / hi20 * 100.0
        return 1.0 / (1.0 + dist_pct)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            prox = raw.where(raw.notna(), prox_from_prices(df))
            regime = df["regime"].astype(str)
            calm = (regime != "chop") & df["regime"].notna()
            situation = calm & prox.notna() & (prox > 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess 3-day return on forecast, in-profile grid cases"
    threshold = "confirm: slope t >= 2 with top-minus-bottom > 0; reject: slope t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are calm-profile bars with a positive "
                           "proximity to the 20-day high and a long forecast, as the Fidelity's situation and rise require."),
            "reading": "Calm profile read as regime other than 'chop'; proximity from the recorded raw value, else recomputed from prices.",
        }

    # ---------- 2. criterion ----------
    # coin mean 3-day return over all windows (non-overlapping grid)
    coin_mean = {}
    grid_rows = []
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    grid_rows.append((coin, float(fc[i]), r))
        coin_mean[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    f = np.array([g[1] for g in grid_rows], dtype=float)
    ex = np.array([g[2] - coin_mean[g[0]] for g in grid_rows], dtype=float)
    ok = np.isfinite(f) & np.isfinite(ex)
    f, ex = f[ok], ex[ok]
    n_cases = int(len(f))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(f) > 0:
        lr = stats.linregress(f, ex)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    diff = None
    welch_t = None
    k = n_cases // 3
    if k >= 2:
        order = np.argsort(f, kind="mergesort")
        bottom = ex[order[:k]]
        top = ex[order[-k:]]
        diff = float(np.mean(top) - np.mean(bottom))
        wt = stats.ttest_ind(top, bottom, equal_var=False)
        welch_t = float(wt.statistic) if np.isfinite(wt.statistic) else None
    sup_pass = (diff > 0) if diff is not None else None

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} grid cases, below the plan's minimum of 300."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-minus-bottom difference is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-minus-bottom difference is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top-third minus bottom-third mean excess 3-day return (Welch t %s)"
                    % ("n/a" if welch_t is None else f"{welch_t:.3f}"),
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {"grid cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": ("Calm profile read as regime other than 'chop'; the coin's mean 3-day return is taken on the same "
                    "non-overlapping grid over all its windows; thirds are the n//3 lowest and highest forecasts after a "
                    "stable sort, pooled across coins; the plan's 'inconclusive' under 300 cases is reported as 'not observable' per the workflow."),
    }
