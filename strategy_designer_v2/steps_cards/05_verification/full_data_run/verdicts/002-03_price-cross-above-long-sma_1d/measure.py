import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    RAW = "debug_info.components.above_ma.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            sub = df[["forecast", RAW]].dropna()
            fc = sub["forecast"].astype(float).values
            raw = sub[RAW].astype(float).values
            active = fc != 0
            n_active += int(active.sum())
            # situation: close above the 200-day SMA (raw distance > 0), long side
            n_agree += int((active & (raw > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "forecast-weighted 20-bar excess return, block mean over non-overlapping 20-bar blocks"
    threshold_txt = "confirm if block mean > 0 with t >= 2; reject if block mean < 0 with t <= -2; else inconclusive; inconclusive if fewer than 50 blocks with a non-zero position"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are bars where the close is above its 200-day SMA with a long forecast, so the config does not do what the plan's situation says.",
            "reading": "none",
        }

    # ---------- 2. Coin's pooled mean daily return ----------
    mean_daily = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).dropna()
            rets.append(r.values)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        mean_daily[coin] = float(allr.mean()) if allr.size else np.nan

    # ---------- 3. Main measure and supporting check ----------
    block_vals = []
    n_blocks_nonzero = 0
    n_blocks_total = 0
    sup_n = 0
    sup_beat = 0
    for coin, wins in bars.items():
        md = mean_daily[coin]
        if not np.isfinite(md):
            continue
        bench = H * md
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            fwd = c.shift(-H) / c - 1.0
            alloc = d[ALLOC].astype(float) if ALLOC in d.columns else pd.Series(np.nan, index=d.index)
            fc = d["forecast"].astype(float)
            excess = fwd - bench
            contrib = alloc * excess
            pos = np.arange(len(d))
            blk = pos // H
            valid = contrib.notna().values
            for b in np.unique(blk):
                m = (blk == b) & valid
                if not m.any():
                    continue
                n_blocks_total += 1
                a = alloc.values[m]
                if np.any(a != 0):
                    n_blocks_nonzero += 1
                    block_vals.append(float(contrib.values[m].sum()))
            # supporting check
            sm = (fc > 0) & fwd.notna()
            sup_n += int(sm.sum())
            sup_beat += int((fwd[sm] > bench).sum())

    bv = np.array(block_vals, dtype=float)
    if bv.size >= 2:
        mean_b = float(bv.mean())
        sd = float(bv.std(ddof=1))
        t = float(mean_b / (sd / np.sqrt(bv.size))) if sd > 0 else (0.0 if mean_b == 0 else float(np.sign(mean_b) * np.inf))
    elif bv.size == 1:
        mean_b, t = float(bv[0]), None
    else:
        mean_b, t = None, None

    sup_share = float(sup_beat / sup_n) if sup_n > 0 else None
    sup_pass = (sup_share > 0.5) if sup_share is not None else None

    # ---------- 4. Decision ----------
    if n_blocks_nonzero < 50 or t is None or mean_b is None:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 50 non-overlapping 20-bar blocks with a non-zero position pooled over the coins."
    elif mean_b > 0 and t >= 2:
        status = "confirmed"
        decided = "Confirm: the block-mean excess return is positive with t >= 2."
    elif mean_b < 0 and t <= -2:
        status = "rejected"
        decided = "Reject: the block-mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t lies between -2 and 2."

    if t is not None and not np.isfinite(t):
        t_out = float(np.sign(t) * 1e12)
    else:
        t_out = t

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_b,
            "statistic": {"name": "t of the block mean", "value": t_out} if t_out is not None else None,
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "share of forecast>0 bars whose next 20-bar return beats 20 x pooled mean daily return, vs 50%",
            "value": sup_share,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping 20-bar blocks with a non-zero position": int(n_blocks_nonzero),
            "non-overlapping 20-bar blocks": int(n_blocks_total),
            "bars with forecast > 0": int(sup_n),
        },
        "decided_by": decided,
        "reading": "Allocation is postRebalance_current_allocation, blocks are rows 0-19, 20-39, ... of each window summed over bars that have a 20-bar forward return, the t-statistic is taken over the blocks holding a non-zero position (the blocks the plan's minimum counts), and the supporting check passes when the share exceeds 50%.",
    }
