import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    short_rets = []
    all_rets = []
    crosses = 0

    for coin, windows in bars.items():
        for wname, df in windows.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # Distinct downward crosses: entries into a short (forecast < 0) episode inside the window
            prev_short = False
            for i in range(n):
                if np.isnan(fc[i]):
                    prev_short = False
                    continue
                is_short = fc[i] < 0
                if is_short and not prev_short:
                    crosses += 1
                prev_short = is_short

            # Non-overlapping 10-bar blocks starting at bar 0, 10, 20, ... within the window
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if np.isnan(c0) or np.isnan(c1) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if not np.isnan(fc[t]) and fc[t] < 0:
                    short_rets.append(r)

    short_rets = np.asarray(short_rets, dtype=float)
    all_rets = np.asarray(all_rets, dtype=float)
    n_short = int(len(short_rets))
    n_all = int(len(all_rets))

    diff = None
    tstat = None
    share_diff = None
    if n_short > 0 and n_all > 0:
        diff = float(short_rets.mean() - all_rets.mean())
        share_short = float((short_rets < 0).mean())
        share_all = float((all_rets < 0).mean())
        share_diff = share_short - share_all
        if n_short > 1:
            sd = float(short_rets.std(ddof=1))
            if sd > 0:
                tstat = diff / (sd / np.sqrt(n_short))

    supp_passed = None if share_diff is None else bool(share_diff >= 0.10)

    if n_short < 12 or crosses < 2 or diff is None:
        status = "inconclusive"
        decided_by = (f"Inconclusive: {n_short} non-overlapping 10-bar short blocks (minimum 12) and "
                      f"{crosses} distinct downward crosses (minimum 2).")
    elif diff <= -0.01 and tstat is not None and tstat <= -2 and share_diff >= 0.10:
        status = "confirmed"
        decided_by = ("Confirmed: difference at most -1.0% per 10 bars, t-stat of -2 or lower, and falling "
                      "share on short bars at least 10 points above the unconditional share.")
    elif diff >= 0 or share_diff <= 0:
        status = "rejected"
        decided_by = ("Rejected: the conditional-minus-unconditional difference is 0 or above, or the falling "
                      "share on short bars is not above the unconditional share.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: difference between -1.0% and 0, or |t| below 2, or falling-share excess "
                      "below 10 points, without meeting a reject rule.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean 10-bar fwd return on short bars minus mean over all bars (non-overlapping blocks)",
            "value": None if diff is None else float(diff),
            "threshold": "at most -1.0% per 10 bars with t-stat <= -2 to confirm; 0 or above rejects",
        },
        "supporting_check": {
            "name": "falling share on short blocks minus falling share on all blocks",
            "value": None if share_diff is None else float(share_diff),
            "passed": supp_passed,
        },
        "cases": n_short,
        "decided_by": decided_by,
        "reading": ("Blocks are non-overlapping 10-bar returns starting at bars 0,10,20,... of each window, a block "
                    "is short when the forecast at its start bar is below 0, the t-stat is the difference divided "
                    "by the standard error of the short-block returns, a downward cross is each entry of the "
                    "forecast into negative values within a window (including a window opening short), minimum "
                    "counts are checked before confirm, and reject takes precedence over the |t|<2 inconclusive rule "
                    f"(t-stat = {None if tstat is None else round(float(tstat), 3)}, all blocks = {n_all}, "
                    f"crosses = {crosses})."),
    }
