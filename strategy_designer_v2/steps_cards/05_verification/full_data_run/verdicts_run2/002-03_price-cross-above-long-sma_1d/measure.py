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
            if "forecast" not in df.columns or COMP not in df.columns:
                continue
            sub = df[["forecast", COMP]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            agree = active & (sub[COMP] > 0) & (sub["forecast"] > 0)
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else float("nan")
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if np.isnan(agreement) else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is 'close above its 200-day SMA, long only', but fewer than 90% "
                           "of the bars with a non-zero forecast are bars with a positive distance above the SMA "
                           "and a positive forecast."),
            "reading": "Situation taken as the component's raw distance from the SMA being above zero, expected side long.",
        }

    # ---------- 2. Criterion ----------
    block_sums = []
    blocks_nonzero = 0
    sup_total = 0
    sup_beat = 0

    for coin, wins in bars.items():
        # coin's mean daily return pooled over all its windows (within-window returns only)
        daily = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r = (c / c.shift(1) - 1).dropna()
            daily.append(r.values)
        daily = np.concatenate(daily) if daily else np.array([])
        daily = daily[np.isfinite(daily)]
        if daily.size == 0:
            continue
        mu = float(np.mean(daily))
        bench = H * mu

        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            fwd = c.shift(-H) / c - 1
            excess = fwd - bench
            alloc = d[ALLOC].astype(float) if ALLOC in d.columns else pd.Series(np.nan, index=d.index)
            fc = d["forecast"].astype(float)
            pos = np.arange(len(d))
            frame = pd.DataFrame({"alloc": alloc, "excess": excess, "fwd": fwd, "fc": fc, "blk": pos // H})

            # main measure: allocation x excess, summed in non-overlapping 20-bar blocks per window
            valid = frame.dropna(subset=["alloc", "excess"])
            for b, g in valid.groupby("blk"):
                block_sums.append(float((g["alloc"] * g["excess"]).sum()))
                if (g["alloc"] != 0).any():
                    blocks_nonzero += 1

            # supporting check: bars with forecast > 0
            s = frame.dropna(subset=["fc", "fwd"])
            s = s[s["fc"] > 0]
            sup_total += int(len(s))
            sup_beat += int((s["fwd"] > bench).sum())

    x = np.asarray(block_sums, dtype=float)
    n_blocks = int(x.size)
    if n_blocks >= 2:
        mean = float(np.mean(x))
        sd = float(np.std(x, ddof=1))
        t = mean / (sd / np.sqrt(n_blocks)) if sd > 0 else float("nan")
    else:
        mean = float(np.mean(x)) if n_blocks == 1 else float("nan")
        t = float("nan")

    share = (sup_beat / sup_total) if sup_total > 0 else None
    sup_passed = None if share is None else bool(share > 0.5)

    if blocks_nonzero < 50:
        status = "inconclusive"
        decided = "Fewer than 50 non-overlapping 20-bar blocks with a non-zero position pooled over the coins, so the run is inconclusive."
    elif np.isfinite(t) and mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The block-mean excess return is positive with t >= 2."
    elif np.isfinite(t) and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The block-mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "forecast-weighted 20-bar excess return per non-overlapping block, before costs",
            "value": None if not np.isfinite(mean) else float(mean),
            "statistic": {"name": "t of the block mean", "value": None if not np.isfinite(t) else float(t)},
            "threshold": "confirm if mean > 0 and t >= 2; reject if mean < 0 and t <= -2; else inconclusive; inconclusive if fewer than 50 blocks with a non-zero position",
        },
        "supporting_check": {
            "name": "share of forecast>0 bars whose next 20-bar return beats 20 x pooled mean daily return, vs 50%",
            "value": None if share is None else float(share),
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping 20-bar blocks with a non-zero position": int(blocks_nonzero),
            "non-overlapping 20-bar blocks": n_blocks,
            "bars with forecast > 0": int(sup_total),
        },
        "decided_by": decided,
        "reading": ("Allocation is postRebalance_current_allocation, blocks are bars at positions 0-19, 20-39, ... of each "
                    "window with bars lacking a 20-bar forward return left out, the t uses all such blocks (zero-position "
                    "ones included) while the minimum counts blocks holding any non-zero position, and the supporting "
                    "check passes when the share exceeds 50% over all (overlapping) forecast>0 bars."),
    }
