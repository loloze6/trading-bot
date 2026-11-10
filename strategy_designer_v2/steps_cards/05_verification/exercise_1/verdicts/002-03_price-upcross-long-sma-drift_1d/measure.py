import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    MIN_BLOCKS = 15
    MIN_CROSSES = 8

    block_all = []      # 20-bar returns of all non-overlapping blocks
    block_in = []       # 20-bar returns of blocks whose start bar has forecast > 0
    uncond = []         # 20-bar forward returns from every bar (unconditional)
    cross_rets = []     # 20-bar forward returns after up-crosses

    for coin in bars:
        for window in bars[coin]:
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0

            # Unconditional forward returns, every bar
            for t in range(n):
                if np.isfinite(fwd[t]):
                    uncond.append(fwd[t])

            # Non-overlapping 20-bar blocks starting at the window's first bar
            for t in range(0, n - H, H):
                r = fwd[t]
                if not np.isfinite(r):
                    continue
                block_all.append(r)
                if np.isfinite(fc[t]) and fc[t] > 0:
                    block_in.append(r)

            # Up-crosses: forecast goes from 0 (<= 0) to > 0 between consecutive bars
            for t in range(1, n):
                if np.isfinite(fc[t - 1]) and np.isfinite(fc[t]) and fc[t - 1] <= 0 and fc[t] > 0:
                    if np.isfinite(fwd[t]):
                        cross_rets.append(fwd[t])

    block_all = np.array(block_all, dtype=float)
    block_in = np.array(block_in, dtype=float)
    uncond = np.array(uncond, dtype=float)
    cross_rets = np.array(cross_rets, dtype=float)

    n_in = len(block_in)
    n_cross = len(cross_rets)

    diff = None
    t_stat = None
    if n_in > 0 and len(block_all) > 0:
        diff = float(block_in.mean() - block_all.mean())
        if n_in > 1:
            sd = block_in.std(ddof=1)
            if sd > 0:
                t_stat = float(diff / (sd / np.sqrt(n_in)))

    share_cross = float((cross_rets > 0).mean()) if n_cross > 0 else None
    share_uncond = float((uncond > 0).mean()) if len(uncond) > 0 else None
    mean_cross = float(cross_rets.mean()) if n_cross > 0 else None

    passed = None
    if share_cross is not None and share_uncond is not None:
        passed = bool(share_cross > share_uncond)

    if n_in < MIN_BLOCKS or n_cross < MIN_CROSSES or diff is None:
        status = "inconclusive"
        decided_by = (f"Fewer than the minimum counts ({n_in} in-position blocks vs 15 needed, "
                      f"{n_cross} up-crosses vs 8 needed), so the test neither confirms nor rejects.")
    elif diff <= 0 or (mean_cross is not None and mean_cross < 0):
        status = "rejected"
        if diff <= 0:
            decided_by = "Reject: the in-position minus all-bars difference is <= 0."
        else:
            decided_by = "Reject: the 20-bar forward returns after up-crosses are on average negative (reversal)."
    elif t_stat is not None and t_stat >= 2 and passed is True:
        status = "confirmed"
        decided_by = ("Confirm: the difference is above 0 with t >= 2 across the non-overlapping blocks and the "
                      "share of up-crosses followed by a positive 20-bar return exceeds the unconditional share.")
    else:
        status = "inconclusive"
        if t_stat is None or t_stat < 2:
            decided_by = "Inconclusive: a positive difference with t < 2."
        else:
            decided_by = "Inconclusive: the main measure and the supporting check disagree."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar fwd return on forecast>0 blocks minus mean over all blocks",
            "value": diff,
            "threshold": "above 0 with t >= 2 (t = %s)" % (None if t_stat is None else round(t_stat, 3)),
        },
        "supporting_check": {
            "name": "share of up-crosses with positive 20-bar return vs unconditional share (%s vs %s; mean after cross %s)"
                    % (share_cross, share_uncond, mean_cross),
            "value": share_cross,
            "passed": passed,
        },
        "cases": int(n_in),
        "decided_by": decided_by,
        "reading": ("Non-overlapping blocks start at each window's first bar every 20 bars, a block is in-position when "
                    "forecast > 0 at its start bar, t is the difference divided by the standard error of the "
                    "in-position block returns, an up-cross is forecast <= 0 on the prior bar and > 0 on the bar, and "
                    "the unconditional share uses the 20-bar forward returns of every bar in the windows."),
    }
