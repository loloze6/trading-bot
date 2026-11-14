import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_BLOCKS = 30
    LHV = "debug_info.components.below_ma.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. Situation check: close below SMA200 (raw distance < 0), side short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce")
            else:
                lhv = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0) & lhv.notna()
            n_active += int(active.sum())
            agree = active & (lhv < 0) & (fc < 0)
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {
                "name": "mean allocation x excess 10-bar return, pooled non-overlapping blocks",
                "value": None,
                "statistic": None,
                "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2",
            },
            "supporting_check": None,
            "counts": {},
            "decided_by": (
                f"Only {agreement:.1%} of active bars are short bars with the close below its 200-day SMA "
                "(component distance < 0), below the 90% needed: the forecast is not limited to the plan's situation and side."
            ),
            "reading": "Situation taken as below_ma last_history_value < 0 with forecast < 0; active bars with a missing component value are left out.",
        }

    # ---------- 2. Coin mean daily return over all windows together ----------
    mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) >= 2:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- 3. Non-overlapping 10-bar blocks ----------
    products = []
    nz_alloc = []
    nz_excess = []
    for coin, wins in bars.items():
        m = mu.get(coin, np.nan)
        if not np.isfinite(m):
            continue
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if ALLOC not in df.columns:
                continue
            a = pd.to_numeric(df[ALLOC], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and np.isfinite(a[i])) or c[i] == 0:
                    continue
                r10 = c[i + H] / c[i] - 1.0
                ex = r10 - H * m
                products.append(a[i] * ex)
                if a[i] != 0:
                    nz_alloc.append(a[i])
                    nz_excess.append(ex)

    products = np.asarray(products, dtype=float)
    n_blocks = int(len(products))
    n_nz = int(len(nz_alloc))

    mean_val = float(np.mean(products)) if n_blocks > 0 else None
    t_val = None
    if n_blocks > 1:
        sd = float(np.std(products, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_blocks)))

    # ---------- 4. Supporting check: slope of excess on allocation in nonzero blocks ----------
    slope = None
    sup_passed = None
    if n_nz >= 3 and len(np.unique(nz_alloc)) >= 2:
        lr = stats.linregress(np.asarray(nz_alloc), np.asarray(nz_excess))
        slope = float(lr.slope)
        sup_passed = bool(slope > 0)

    # ---------- 5. Decision ----------
    if n_nz < MIN_BLOCKS:
        status = "not observable"
        decided_by = f"Only {n_nz} non-overlapping 10-bar blocks with a nonzero position, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The t-statistic of the mean excess gain cannot be computed (no dispersion), so neither confirm nor reject is met."
    elif mean_val > 0 and t_val >= 2:
        if sup_passed:
            status = "confirmed"
            decided_by = "Mean excess gain is positive with t >= 2 and the slope of excess return on allocation is positive (confirm rule)."
        else:
            status = "inconclusive"
            decided_by = "Mean excess gain is positive with t >= 2, but the supporting check (positive slope) fails, so the result is inconclusive."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "Mean excess gain is negative with t <= -2: coins rose beyond holding after closes below the SMA200 (reject rule)."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean excess gain lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "mean allocation x excess 10-bar return, pooled non-overlapping blocks",
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "slope of excess 10-bar return on allocation, nonzero-position blocks",
            "value": slope,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping 10-bar blocks with a nonzero position": n_nz,
            "non-overlapping 10-bar blocks (all)": n_blocks,
        },
        "decided_by": decided_by,
        "reading": (
            "The main measure pools the products of all blocks (zero-position blocks included) as the plan's main measure says, "
            "blocks start at rows 0, 10, 20, ... of each window with the allocation after that bar's trade, the coin mean daily "
            "return pools all its windows, the situation is below_ma last_history_value < 0 with forecast < 0 (rows with missing "
            "values left out), and a block count under 30 is reported as not observable."
        ),
    }
