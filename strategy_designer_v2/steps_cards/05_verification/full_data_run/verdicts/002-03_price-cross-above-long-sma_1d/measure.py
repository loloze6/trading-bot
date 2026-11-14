import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    COMP = "debug_info.components.above_ma.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. Situation check: close above the 200-day SMA (raw distance > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if COMP in df.columns:
                raw = pd.to_numeric(df[COMP], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0) & raw.notna()
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "forecast-weighted 20-bar excess return, block mean over non-overlapping 20-bar blocks (before costs)"
    threshold = "confirm: block mean > 0 with t >= 2; reject: block mean < 0 with t <= -2; else inconclusive; at least 50 blocks with a non-zero position"
    sup_name = "share of forecast > 0 bars whose next 20-bar return beats 20 x the coin's pooled mean daily return, vs 50%"
    reading = ("The allocation is postRebalance_current_allocation; a block is each run of 20 rows from position 0 of each window "
               "and sums allocation x excess over its rows that have a full 20-bar forward return inside the window, all such blocks "
               "are pooled for the t (ordinary t of the mean), a block 'has a non-zero position' if any of those rows has a non-zero "
               "allocation; the supporting check uses the non-overlapping grid rows (positions 0, 20, 40, ...) with forecast > 0 and "
               "passes if the share is above 50%; active rows with a missing raw component value are left out of the situation check.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with the close above its 200-day SMA "
                           "(raw distance > 0), so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- 2. Coin pooled mean daily return ----------
    mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        mu[coin] = float(allr.mean()) if len(allr) else np.nan

    # ---------- 3. Main measure and supporting check ----------
    block_vals = []
    blocks_nonzero = 0
    sup_total = 0
    sup_beat = 0
    for coin, wins in bars.items():
        m = mu.get(coin, np.nan)
        if not np.isfinite(m):
            continue
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            a = pd.to_numeric(df[ALLOC], errors="coerce").to_numpy(dtype=float) if ALLOC in df.columns else np.full(len(c), np.nan)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = c[H:] / c[: n - H] - 1.0
            exc = fwd - H * m
            for start in range(0, n, H):
                idx = np.arange(start, min(start + H, n))
                valid = np.isfinite(exc[idx]) & np.isfinite(a[idx])
                if valid.any():
                    vi = idx[valid]
                    block_vals.append(float(np.sum(a[vi] * exc[vi])))
                    if np.any(a[vi] != 0):
                        blocks_nonzero += 1
                # supporting check on the grid row
                if np.isfinite(fc[start]) and fc[start] > 0 and np.isfinite(exc[start]):
                    sup_total += 1
                    if exc[start] > 0:
                        sup_beat += 1

    block_vals = np.array(block_vals, dtype=float)
    nb = len(block_vals)
    mean_b = float(block_vals.mean()) if nb > 0 else None
    if nb > 1:
        sd = float(block_vals.std(ddof=1))
        t = float(mean_b / (sd / np.sqrt(nb))) if sd > 0 else None
    else:
        t = None

    sup_share = float(sup_beat / sup_total) if sup_total > 0 else None
    sup_passed = (sup_share > 0.5) if sup_share is not None else None

    counts = {
        "non-overlapping 20-bar blocks with a non-zero position": int(blocks_nonzero),
        "non-overlapping 20-bar blocks": int(nb),
        "forecast > 0 grid bars (supporting check)": int(sup_total),
    }

    if blocks_nonzero < 50:
        status = "not observable"
        decided = f"Only {blocks_nonzero} non-overlapping 20-bar blocks with a non-zero position, fewer than the plan's 50."
    elif t is None or mean_b is None:
        status = "inconclusive"
        decided = "The t-statistic of the block mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_b > 0 and t >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The block-mean excess return is positive with t >= 2 and the supporting share is above 50%."
        else:
            status = "inconclusive"
            decided = "The block-mean excess return is positive with t >= 2, but the supporting check (share above 50%) fails."
    elif mean_b < 0 and t <= -2:
        status = "rejected"
        decided = "The block-mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the block-mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_b,
            "statistic": {"name": "t of the block mean", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_share, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
