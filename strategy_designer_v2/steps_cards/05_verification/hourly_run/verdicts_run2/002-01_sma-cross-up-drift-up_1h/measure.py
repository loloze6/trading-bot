import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. Situation check: SMA50 above SMA200 (raw spread > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            ok = fc.notna()
            active = ok & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("The plan's situation is long only while SMA50 is above SMA200 (raw spread > 0), "
                           "but fewer than 90% of bars with a non-zero forecast are long bars with a positive spread "
                           "(or there are no active bars)."),
            "reading": "Situation taken as last_history_value > 0 with forecast > 0 on every bar where forecast != 0.",
        }

    # ---------- 2. Criterion ----------
    excess_all = []          # per-bar excess (forecast>0 bars), pooled
    block_excess = []        # excess on non-overlapping block starts
    pos_cond = []            # positive fwd return indicator, forecast>0 bars
    pos_all = []             # positive fwd return indicator, all bars
    n_cond_bars = 0

    for coin, wins in bars.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            fwd = np.full(n, np.nan)
            if n > H:
                with np.errstate(divide="ignore", invalid="ignore"):
                    fwd[:n - H] = np.log(close[H:] / close[:n - H])
            fwd[~np.isfinite(fwd)] = np.nan
            valid = ~np.isnan(fwd)
            if valid.sum() == 0:
                continue
            win_mean = float(np.nanmean(fwd))
            pos_all.extend((fwd[valid] > 0).astype(float).tolist())

            cond = valid & ~np.isnan(fc) & (fc > 0)
            n_cond_bars += int(cond.sum())
            excess_all.extend((fwd[cond] - win_mean).tolist())
            pos_cond.extend((fwd[cond] > 0).astype(float).tolist())

            # non-overlapping blocks, each starting at a bar with forecast > 0
            t = 0
            while t < n:
                if cond[t]:
                    block_excess.append(fwd[t] - win_mean)
                    t += H
                else:
                    t += 1

    n_blocks = len(block_excess)
    value = float(np.mean(excess_all)) if len(excess_all) > 0 else None

    t_stat = None
    if n_blocks >= 2:
        arr = np.asarray(block_excess, dtype=float)
        sd = arr.std(ddof=1)
        if sd > 0:
            t_stat = float(arr.mean() / (sd / np.sqrt(n_blocks)))

    supp = None
    if len(pos_cond) > 0 and len(pos_all) > 0:
        supp = float(np.mean(pos_cond) - np.mean(pos_all))

    supp_passed = None
    if supp is not None and value is not None:
        supp_passed = bool(np.sign(supp) == np.sign(value) and supp != 0)

    # ---------- decision ----------
    if n_blocks < 100 or value is None or t_stat is None or supp is None:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 100 non-overlapping 24-bar blocks with forecast above 0 pooled across "
                      "windows (or the measure could not be computed), so no verdict is allowed.")
    elif value > 0 and t_stat >= 2 and supp > 0:
        status = "confirmed"
        decided_by = ("Confirm: the excess 24-bar log return is above 0 with t >= 2 and the hit rate when the forecast "
                      "is above 0 is higher than over all bars.")
    elif value < 0 and t_stat <= -2 and supp <= 0:
        status = "rejected"
        decided_by = ("Reject: the excess 24-bar log return is below 0 with t <= -2, and the supporting check does not "
                      "disagree in sign.")
    else:
        status = "inconclusive"
        if -2 < t_stat < 2:
            decided_by = "Inconclusive: the t-statistic lies between -2 and 2."
        else:
            decided_by = "Inconclusive: the main measure and the supporting check disagree in sign."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "forward 24-bar log return when forecast > 0 minus window mean over all bars",
            "value": value,
            "statistic": None if t_stat is None else {"name": "one-sample t of mean excess on non-overlapping 24-bar blocks", "value": t_stat},
            "threshold": "confirm if excess > 0 with t >= 2; reject if excess < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "hit rate when forecast > 0 minus hit rate over all bars",
            "value": supp,
            "passed": supp_passed,
        },
        "counts": {
            "non-overlapping 24-bar blocks with forecast above 0": int(n_blocks),
            "bars with forecast above 0": int(n_cond_bars),
        },
        "decided_by": decided_by,
        "reading": ("The main measure's value is the mean, over all pooled bars with forecast > 0, of each bar's forward "
                    "24-bar log return minus its window's mean over all bars. Its t is the ordinary one-sample t of the "
                    "same excess on greedy non-overlapping blocks, each started at the next bar with forecast > 0 and "
                    "then skipping 24 bars. The hit-rate shares are pooled across windows. A reject also needs a "
                    "supporting check that is not positive."),
    }
