import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    def find_col(df, suffix):
        cands = [c for c in df.columns
                 if c.startswith("debug_info.components.sma_cross") and c.endswith(suffix)]
        return cands[0] if cands else None

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    in_rets, all_rets = [], []
    n_stretches = 0

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            raw_col = find_col(df, ".last_history_value")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[raw_col], errors="coerce") if raw_col else pd.Series(np.nan, index=df.index)

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: SMA50 above SMA200 (positive spread), expected side long
            agree = active & raw.notna() & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

            # ---------- 2. Returns (horizon 1 bar, within window) ----------
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            # non-overlapping grid with h=1: every bar of the window
            valid = nxt.notna() & np.isfinite(nxt) & fc.notna()
            all_rets.extend(nxt[valid].tolist())
            ins = valid & (fc > 0)
            in_rets.extend(nxt[ins].tolist())

            # distinct stretches: runs of consecutive in-stretch bars (forecast > 0) in this window
            pos = (fc > 0).fillna(False).astype(int).values
            if len(pos):
                starts = np.sum((pos[1:] == 1) & (pos[:-1] == 0)) + (1 if pos[0] == 1 else 0)
                n_stretches += int(starts)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    threshold_txt = ("confirm: in-stretch mean > all-bar mean with one-sided t >= 2.0 and higher up-day share; "
                     "reject: in-stretch mean <= all-bar mean or t <= -2.0; inconclusive: -2.0 < t < 2.0, "
                     "fewer than 100 in-stretch bars or fewer than 3 up-cross stretches")
    mm_name = "in-stretch minus all-bar mean next-bar return (before costs)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is a positive SMA50-SMA200 spread traded long, but fewer than 90% "
                           "of the bars with a non-zero forecast have a positive raw spread and a long forecast."),
            "reading": "Situation taken as the component's raw spread (last_history_value) above 0 with a positive forecast.",
        }

    a = np.asarray(in_rets, dtype=float)
    b = np.asarray(all_rets, dtype=float)
    n_in, n_all = len(a), len(b)

    diff = float(a.mean() - b.mean()) if n_in > 0 and n_all > 0 else None
    t_val = None
    if n_in >= 2 and n_all >= 2:
        t_res = stats.ttest_ind(a, b, equal_var=False)
        t_val = float(t_res.statistic) if np.isfinite(t_res.statistic) else None

    up_in = float(np.mean(a > 0)) if n_in > 0 else None
    up_all = float(np.mean(b > 0)) if n_all > 0 else None
    sup_val = (up_in - up_all) if (up_in is not None and up_all is not None) else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    if n_in < 100 or n_stretches < 3 or diff is None:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 100 in-stretch bars or fewer than 3 distinct up-cross stretches across the windows."
    elif diff <= 0 or (t_val is not None and t_val <= -2.0):
        status = "rejected"
        decided = ("Rejected: the in-stretch mean daily return is at or below the all-bar mean"
                   + (" (t <= -2.0, moves reverse)." if (t_val is not None and t_val <= -2.0) else "."))
    elif t_val is not None and t_val >= 2.0 and sup_pass:
        status = "confirmed"
        decided = ("Confirmed: the in-stretch mean exceeds the all-bar mean with t >= 2.0 and the in-stretch "
                   "up-day share exceeds the all-bar share.")
    else:
        status = "inconclusive"
        if t_val is not None and t_val >= 2.0:
            decided = ("Inconclusive: t >= 2.0 but the in-stretch up-day share does not exceed the all-bar share, "
                       "so the confirm rule is not fully met.")
        else:
            decided = "Inconclusive: the in-stretch mean exceeds the all-bar mean but the t-statistic lies between -2.0 and 2.0."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": mm_name,
            "value": diff,
            "statistic": {"name": "Welch t (in-stretch vs all bars)", "value": t_val} if t_val is not None else None,
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "in-stretch up-day share minus all-bar up-day share",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "in-stretch bars": int(n_in),
            "all bars": int(n_all),
            "distinct up-cross stretches": int(n_stretches),
        },
        "decided_by": decided,
        "reading": ("Situation taken as the component's raw spread (last_history_value) above 0 with a positive forecast; "
                    "in-stretch means forecast > 0, the all-bar group includes the in-stretch bars, an up day is a next-bar "
                    "return above 0, and distinct up-cross stretches are counted as runs of consecutive forecast > 0 bars "
                    "within each window (a run open at a window's first row counts as one)."),
    }
