import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    MIN_BLOCKS = 100
    LHV = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. situation check ----------
    # Situation (adapted): SMA50 above SMA200, i.e. raw percent spread > 0; expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            lhv = pd.to_numeric(df[LHV], errors="coerce") if LHV in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (lhv > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The forecast is not mostly positive on bars where SMA50 is above SMA200 (raw spread > 0): "
                           "fewer than 90% of active bars are long bars of the plan's situation."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    excess_all = []        # excess fwd log return on every forecast>0 bar (pooled)
    excess_blocks = []     # excess on non-overlapping blocks starting at forecast>0 bars
    pos_cond = []          # positive fwd return indicator, forecast>0 bars
    pos_all = []           # positive fwd return indicator, all bars

    for coin, wins in bars.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            fwd = np.full(n, np.nan)
            if n > H:
                with np.errstate(divide="ignore", invalid="ignore"):
                    fwd[: n - H] = np.log(close[H:] / close[: n - H])
            fwd[~np.isfinite(fwd)] = np.nan
            valid = ~np.isnan(fwd)
            if valid.sum() == 0:
                continue
            win_mean = float(np.mean(fwd[valid]))
            cond = valid & ~np.isnan(fc) & (fc > 0)

            excess_all.extend((fwd[cond] - win_mean).tolist())
            pos_cond.extend((fwd[cond] > 0).astype(float).tolist())
            pos_all.extend((fwd[valid] > 0).astype(float).tolist())

            # non-overlapping blocks: each block starts at a bar with forecast > 0, then skip H bars
            i = 0
            while i < n:
                if cond[i]:
                    excess_blocks.append(fwd[i] - win_mean)
                    i += H
                else:
                    i += 1

    n_blocks = len(excess_blocks)
    value = float(np.mean(excess_all)) if len(excess_all) > 0 else None

    t_val = None
    if n_blocks >= 2:
        eb = np.asarray(excess_blocks, dtype=float)
        sd = float(np.std(eb, ddof=1))
        if sd > 0:
            t_val = float(np.mean(eb) / (sd / np.sqrt(n_blocks)))
        else:
            t_val = 0.0

    supp = None
    if len(pos_cond) > 0 and len(pos_all) > 0:
        supp = float(np.mean(pos_cond) - np.mean(pos_all))

    supp_passed = None
    if supp is not None and value is not None:
        supp_passed = bool(np.sign(supp) == np.sign(value) and supp != 0)

    # ---------- decision ----------
    if n_blocks < MIN_BLOCKS or value is None or t_val is None or supp is None:
        status = "inconclusive"
        decided_by = (f"Only {n_blocks} non-overlapping 24-bar blocks with forecast above 0, fewer than the "
                      f"{MIN_BLOCKS} a verdict needs.")
    elif np.sign(value) != np.sign(supp) or supp == 0 or value == 0:
        status = "inconclusive"
        decided_by = "The main measure and the supporting check disagree in sign, so the result is inconclusive."
    elif value > 0 and t_val >= 2 and supp > 0:
        status = "confirmed"
        decided_by = "The excess return is above 0 with t >= 2 and the hit rate when the forecast is above 0 is higher."
    elif value < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "The excess return is below 0 with t <= -2: moves after upward crosses lag the coin."
    else:
        status = "inconclusive"
        decided_by = "The t-statistic lies between -2 and 2 (or does not match the sign of the excess), so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean forward 24-bar log return when forecast > 0 minus window mean over all bars, pooled",
            "value": value,
            "statistic": None if t_val is None else {"name": "t of the mean of excess over non-overlapping blocks", "value": t_val},
            "threshold": "excess > 0 with t >= 2 to confirm; excess < 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "share of positive fwd 24-bar returns when forecast > 0 minus share over all bars",
            "value": supp,
            "passed": supp_passed,
        },
        "counts": {"non-overlapping 24-bar blocks with forecast above 0": int(n_blocks)},
        "decided_by": decided_by,
        "reading": ("The measure's value is the pooled mean excess over all forecast>0 bars (each demeaned by its own "
                    "window's mean over all bars), its t is the ordinary one-sample t of that excess on greedy "
                    "non-overlapping blocks that each start at the next forecast>0 bar after the previous block ends "
                    "within a window, and the hit-rate shares are pooled across windows."),
    }
