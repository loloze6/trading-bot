import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.drop.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the bar is a down day (one-day change < 0) and its volume is at or above
    # its 20-bar mean. The expected side is short (forecast < 0).
    n_active_checked = 0
    n_agree = 0

    # ---------- 2. Data for the criterion ----------
    act_rets, act_fc, all_rets = [], [], []
    per_window = []  # (window key, excess) per window

    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].sort_values("timestamp").reset_index(drop=True)
            if df.empty:
                continue
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df[FC].astype(float)

            if RAW in df.columns:
                move = df[RAW].astype(float)
                move = move.where(move.notna(), close.pct_change())
            else:
                move = close.pct_change()
            vol_mean = vol.rolling(20, min_periods=20).mean()

            active = fc.notna() & (fc != 0)
            decidable = active & move.notna() & vol_mean.notna() & vol.notna()
            situ = (move < 0) & (vol >= vol_mean)
            agree = decidable & situ & (fc < 0)
            n_active_checked += int(decidable.sum())
            n_agree += int(agree.sum())

            # Next-bar return inside this window only (horizon 1: every bar on the grid)
            nxt = close.shift(-1) / close - 1.0
            valid = nxt.notna()
            all_w = nxt[valid]
            act_mask = active & valid
            act_w = nxt[act_mask]
            all_rets.extend(all_w.tolist())
            act_rets.extend(act_w.tolist())
            act_fc.extend(fc[act_mask].tolist())
            if len(act_w) > 0 and len(all_w) > 0:
                per_window.append((f"{coin}/{w}", float(act_w.mean() - all_w.mean())))
            else:
                per_window.append((f"{coin}/{w}", None))

    agreement = (n_agree / n_active_checked) if n_active_checked > 0 else 0.0
    passed = bool(agreement >= 0.90)

    threshold_txt = ("Confirm: excess < 0 with t <= -2 over >= 60 active bars and negative in >= 4 of 6 "
                     "windows; reject: excess >= 0 with >= 60 active bars; otherwise inconclusive")
    main_name = "Mean next-bar return after active bars minus mean next-bar return over all bars"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active_checked)},
            "decided_by": ("Fewer than 90% of active bars are heavy-volume down days held short "
                           f"(agreement {agreement:.3f}), so the config does not do what the Fidelity says."),
            "reading": ("Situation computed as one-day change (drop raw value) < 0 and volume >= its "
                        "20-bar rolling mean including the current bar; active bars without 20 bars of "
                        "volume history in the window were left out of the check."),
        }

    act = np.array(act_rets, dtype=float)
    allr = np.array(all_rets, dtype=float)
    afc = np.array(act_fc, dtype=float)
    n_act = int(len(act))

    excess = None
    t_val = None
    if n_act >= 1 and len(allr) >= 1:
        excess = float(act.mean() - allr.mean())
    if n_act >= 2 and len(allr) >= 2:
        t_res = stats.ttest_ind(act, allr, equal_var=False)
        t_val = float(t_res.statistic) if np.isfinite(t_res.statistic) else None

    neg_windows = int(sum(1 for _, e in per_window if e is not None and e < 0))

    # Supporting check: slope of next-bar return on (signed) forecast across active bars
    slope = None
    sup_pass = None
    if n_act >= 3 and np.std(afc) > 0:
        slope = float(stats.linregress(afc, act).slope)
        sup_pass = bool(slope > 0)

    # Decision
    if n_act < 60 or excess is None:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 60 active bars across the windows."
    elif excess >= 0:
        status = "rejected"
        decided = "Reject: the excess return is zero or positive with at least 60 active bars."
    elif t_val is not None and t_val <= -2 and neg_windows >= 4:
        status = "confirmed"
        decided = ("Confirm: the excess return is negative with t <= -2 over at least 60 active bars "
                   "and negative in at least 4 of the 6 windows.")
    else:
        status = "inconclusive"
        if neg_windows < 4:
            decided = "Inconclusive: a negative excess return, but negative in fewer than 4 windows."
        else:
            decided = "Inconclusive: a negative excess return with t between -2 and 0."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": excess,
            "statistic": ({"name": "Welch t", "value": t_val} if t_val is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "OLS slope of next-bar return on signed forecast across active bars (should be > 0)",
            "value": slope,
            "passed": sup_pass,
        },
        "counts": {
            "active bars": n_act,
            "windows with negative excess": neg_windows,
            "windows": int(len(per_window)),
        },
        "decided_by": decided,
        "reading": ("Active bars are those with forecast != 0; the baseline is every bar of the same "
                    "windows (horizon 1, so all bars are on the grid); the t is Welch's between the active "
                    "and all-bar returns; a window with no active bars does not count as negative; "
                    "the supporting slope regresses next-bar return on the signed forecast, so a "
                    "positive slope means a larger short is followed by a larger fall."),
    }
