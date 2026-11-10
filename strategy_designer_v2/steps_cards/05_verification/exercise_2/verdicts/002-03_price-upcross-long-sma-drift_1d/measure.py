import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    MIN_BLOCKS = 15
    MIN_CROSSES = 8

    all_block_rets = []
    in_block_rets = []
    cross_rets = []
    all_bar_rets = []

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True) if "timestamp" in df.columns else df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # forward 20-bar return inside this window only
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0

            # every bar's 20-bar forward return (unconditional share for the supporting check)
            for t in range(n):
                if np.isfinite(fwd[t]):
                    all_bar_rets.append(fwd[t])

            # non-overlapping 20-bar blocks starting at the window's first bar
            for t in range(0, n, H):
                if t + H >= n:
                    break
                r = fwd[t]
                if not np.isfinite(r) or not np.isfinite(fc[t]):
                    continue
                all_block_rets.append(r)
                if fc[t] > 0:
                    in_block_rets.append(r)

            # up-crosses: forecast goes from 0 (or below) on the previous bar to > 0
            for t in range(1, n):
                if np.isfinite(fc[t - 1]) and np.isfinite(fc[t]) and fc[t - 1] <= 0 and fc[t] > 0:
                    if np.isfinite(fwd[t]):
                        cross_rets.append(fwd[t])

    all_block_rets = np.array(all_block_rets, dtype=float)
    in_block_rets = np.array(in_block_rets, dtype=float)
    cross_rets = np.array(cross_rets, dtype=float)
    all_bar_rets = np.array(all_bar_rets, dtype=float)

    n_in = int(len(in_block_rets))
    n_cross = int(len(cross_rets))

    diff = None
    tstat = None
    if n_in > 0 and len(all_block_rets) > 0:
        mean_all = float(np.mean(all_block_rets))
        excess = in_block_rets - mean_all
        diff = float(np.mean(excess))
        if n_in >= 2:
            sd = float(np.std(excess, ddof=1))
            if sd > 0:
                tstat = float(diff / (sd / np.sqrt(n_in)))
            else:
                tstat = float("inf") if diff > 0 else (float("-inf") if diff < 0 else 0.0)

    cross_share = float(np.mean(cross_rets > 0)) if n_cross > 0 else None
    cross_mean = float(np.mean(cross_rets)) if n_cross > 0 else None
    uncond_share = float(np.mean(all_bar_rets > 0)) if len(all_bar_rets) > 0 else None
    sup_value = None
    sup_passed = None
    if cross_share is not None and uncond_share is not None:
        sup_value = float(cross_share - uncond_share)
        sup_passed = bool(cross_share > uncond_share)

    if n_in < MIN_BLOCKS or n_cross < MIN_CROSSES or diff is None:
        status = "inconclusive"
        decided_by = (f"Fewer than {MIN_BLOCKS} non-overlapping in-position blocks ({n_in}) or fewer than "
                      f"{MIN_CROSSES} up-crosses ({n_cross}), so the test neither confirms nor rejects.")
    elif diff <= 0 or (cross_mean is not None and cross_mean < 0):
        status = "rejected"
        if diff <= 0:
            decided_by = "The in-position minus all-bars mean 20-bar return difference is <= 0."
        else:
            decided_by = "The 20-bar forward returns after up-crosses are on average negative (reversal)."
    elif tstat is not None and tstat >= 2 and sup_passed:
        status = "confirmed"
        decided_by = ("The in-position minus all-bars difference is above 0 with t >= 2 and the share of up-crosses "
                      "followed by a positive 20-bar return exceeds the unconditional share.")
    else:
        status = "inconclusive"
        if tstat is None or tstat < 2:
            decided_by = "The difference is positive but with t < 2."
        else:
            decided_by = "The main measure is positive with t >= 2 but the supporting check disagrees."

    t_txt = "n/a" if tstat is None else f"{tstat:.3f}"
    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar fwd return in position minus all bars (non-overlapping blocks), t=" + t_txt,
            "value": diff,
            "threshold": "above 0 with t >= 2 to confirm; <= 0 rejects",
        },
        "supporting_check": {
            "name": "share of positive 20-bar returns after up-crosses minus unconditional share",
            "value": sup_value,
            "passed": sup_passed,
        },
        "cases": n_in,
        "decided_by": decided_by,
        "reading": ("Blocks start at each window's first bar every 20 bars (block in position if forecast > 0 at its "
                    "start), t is the one-sample t of in-position block returns minus the all-blocks mean, up-crosses "
                    "are bars with forecast > 0 after a bar with forecast <= 0 in the same window, and the unconditional "
                    "positive share uses every bar's 20-bar forward return pooled over all windows."),
    }
