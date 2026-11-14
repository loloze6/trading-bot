import numpy as np
import pandas as pd


def measure(bars):
    raw_col = "debug_info.components.sma_cross_down.last_history_value"
    threshold_words = ("in-state mean at least 0.10% per day below the all-bars mean "
                       "with stretch-clustered t <= -2 (confirm); difference >= 0 (reject)")
    main_name = "mean next-bar return on forecast<0 bars minus mean next-bar return on all bars (BTC, pooled windows)"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[raw_col], errors="coerce") if raw_col in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: SMA50 below SMA200 (raw spread < 0); expected side: short (forecast < 0)
            agree = active & raw.notna() & (raw < 0) & (fc < 0)
            n_agree += int(agree.sum())

    if n_active == 0:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_words},
            "supporting_check": None,
            "counts": {"active bars": 0},
            "decided_by": "The forecast is never non-zero, so no bar is short during the SMA50-below-SMA200 stretches the plan describes.",
            "reading": "With no active bars, agreement is undefined and the test is treated as not matching its plan.",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_words},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars with the raw SMA50/SMA200 spread below 0: "
                           "the standardised-and-clipped forecast does not hold the short exactly over the down-cross stretches."),
            "reading": "The situation is the raw component value (last_history_value) below 0 and the expected side is short (forecast < 0).",
        }

    # ---------- 2. Criterion ----------
    in_rets = []
    in_cluster = []
    all_rets = []
    stretch_id = 0
    for coin, wins in bars.items():
        for w in sorted(wins.keys()):
            df = wins[w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ret = close.shift(-1) / close - 1.0
            in_state = (fc < 0).fillna(False).values
            prev = False
            cur_id = None
            for i in range(len(df)):
                if in_state[i]:
                    if not prev:
                        stretch_id += 1
                        cur_id = stretch_id
                    prev = True
                else:
                    prev = False
                r = ret.iloc[i]
                if pd.isna(r) or not np.isfinite(r):
                    continue
                all_rets.append(float(r))
                if in_state[i]:
                    in_rets.append(float(r))
                    in_cluster.append(cur_id)

    in_rets = np.asarray(in_rets, dtype=float)
    in_cluster = np.asarray(in_cluster)
    all_rets = np.asarray(all_rets, dtype=float)

    n_in = int(in_rets.size)
    n_stretch = int(len(np.unique(in_cluster))) if n_in > 0 else 0
    counts = {"distinct down-cross stretches": n_stretch, "in-state bars pooled": n_in}

    diff = None
    t_val = None
    down_in = down_all = None
    sup_passed = None
    if n_in > 0 and all_rets.size > 0:
        mean_in = in_rets.mean()
        mean_all = all_rets.mean()
        diff = float(mean_in - mean_all)
        G = n_stretch
        if G >= 2:
            resid = in_rets - mean_in
            sums = pd.Series(resid).groupby(in_cluster).sum().values
            var = (G / (G - 1)) * np.sum(sums ** 2) / (n_in ** 2)
            se = np.sqrt(var)
            if se > 0:
                t_val = float(diff / se)
        down_in = float(np.mean(in_rets < 0))
        down_all = float(np.mean(all_rets < 0))
        sup_passed = bool(down_in > down_all)

    reading = ("In-state bars are bars with forecast < 0 and a next-bar return inside the window; a stretch is a maximal run of "
               "consecutive forecast<0 bars within one window; the t is the in-state-minus-all-bars difference over the "
               "stretch-clustered (CR1, G/(G-1)) standard error of the in-state mean, treating the all-bars mean as the reference; "
               "the supporting check's pass is the down-bar share comparison the confirm rule names.")

    main = {
        "name": main_name,
        "value": None if diff is None else diff * 100.0,
        "statistic": None if t_val is None else {"name": "stretch-clustered t", "value": t_val},
        "threshold": threshold_words,
    }
    supporting = {
        "name": "share of down bars in stretches minus share over all bars",
        "value": None if down_in is None else down_in - down_all,
        "passed": sup_passed,
    }

    if n_stretch < 3 or n_in < 60:
        status = "inconclusive"
        decided = "Fewer than 3 distinct down-cross stretches or fewer than 60 in-state bars pooled, so the test cannot conclude."
    elif diff is None:
        status = "inconclusive"
        decided = "No in-state returns could be measured."
    elif diff >= 0:
        status = "rejected"
        decided = "The in-state mean return is at or above the all-bars mean, so price did not fall faster during down-cross stretches."
    elif diff <= -0.001 and t_val is not None and t_val <= -2 and sup_passed:
        status = "confirmed"
        decided = ("The in-state mean is at least 0.10% per day below the all-bars mean with stretch-clustered t <= -2, "
                   "and the down-bar share inside the stretches is higher than over all bars.")
    else:
        status = "inconclusive"
        decided = ("The difference is negative but t > -2, or it is smaller than 0.10% per day, "
                   "or the down-bar share inside the stretches is not higher, so the confirm rule is not met.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
