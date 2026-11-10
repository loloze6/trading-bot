import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10

    def find_raw_col(df):
        cols = [c for c in df.columns
                if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        if not cols:
            return None
        pref = [c for c in cols if "below" in c]
        return (pref or cols)[0]

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            raw_col = find_raw_col(df)
            if raw_col is None:
                continue
            d = df[["forecast", raw_col]].dropna()
            fc = d["forecast"].astype(float).values
            raw = d[raw_col].astype(float).values
            active = fc != 0
            n_active += int(active.sum())
            # situation: close below SMA200 (raw distance < 0); expected side: short
            n_agree += int((active & (raw < 0) & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    threshold_txt = ("confirm if slope t >= +2 with mean excess on short blocks < 0 and decline share higher than "
                     "on all blocks; reject if slope t <= -2; otherwise inconclusive; inconclusive if fewer than 15 "
                     "non-overlapping short blocks")
    main_name = "OLS slope of forward 10-bar excess log return on forecast, short-bar blocks"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are short bars with the close below its 200-day SMA, "
                           "so the forecast does not hold the plan's 'short while below the SMA200' situation."),
            "reading": "none",
        }

    # ---------- non-overlapping blocks ----------
    all_rets = []
    short_rets = []
    short_fc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                c0, c1 = close[i], close[j]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0 or c1 <= 0:
                    continue
                r = float(np.log(c1 / c0))
                all_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    short_rets.append(r)
                    short_fc.append(float(fc[i]))

    all_rets = np.array(all_rets)
    short_rets = np.array(short_rets)
    short_fc = np.array(short_fc)
    n_short = int(len(short_rets))
    n_all = int(len(all_rets))

    baseline = float(all_rets.mean()) if n_all > 0 else np.nan
    excess = short_rets - baseline if n_short > 0 else np.array([])
    mean_excess = float(excess.mean()) if n_short > 0 else None

    slope = None
    t_stat = None
    if n_short >= 3 and np.std(short_fc) > 0:
        res = stats.linregress(short_fc, excess)
        slope = float(res.slope)
        if res.stderr is not None and res.stderr > 0:
            t_stat = float(res.slope / res.stderr)

    share_short = float((short_rets < 0).mean()) if n_short > 0 else None
    share_all = float((all_rets < 0).mean()) if n_all > 0 else None
    sup_val = (share_short - share_all) if (share_short is not None and share_all is not None) else None
    sup_pass = (bool(sup_val > 0) if sup_val is not None else None)

    # ---------- decision ----------
    if n_short < 15:
        status = "inconclusive"
        decided = f"Only {n_short} non-overlapping 10-bar blocks with forecast < 0 (fewer than 15): inconclusive whatever the t-statistic."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The slope t-statistic cannot be computed (no variation in the forecast), so no confirm or reject rule is met: inconclusive."
    elif t_stat <= -2:
        status = "rejected"
        decided = f"Slope t-statistic {t_stat:.2f} <= -2: price rebounds more strongly the deeper the close sits below the SMA200."
    elif t_stat >= 2 and mean_excess is not None and mean_excess < 0 and sup_pass:
        status = "confirmed"
        decided = (f"Slope t-statistic {t_stat:.2f} >= +2, mean excess forward return on short blocks {mean_excess:.4f} < 0, "
                   f"and the decline share on short blocks exceeds that on all blocks.")
    elif t_stat >= 2:
        status = "inconclusive"
        decided = (f"Slope t-statistic {t_stat:.2f} >= +2 but the other confirm conditions fail (mean excess "
                   f"{mean_excess}, decline-share difference {sup_val}), and the reject rule is not met: inconclusive.")
    else:
        status = "inconclusive"
        decided = f"Slope t-statistic {t_stat:.2f} lies between -2 and +2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "share of negative 10-bar returns, short blocks minus all blocks",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping 10-bar blocks with forecast < 0": n_short,
            "non-overlapping 10-bar blocks, all bars": n_all,
        },
        "decided_by": decided,
        "reading": ("Blocks start at rows 0, 10, 20, ... of each window with the forecast read at the block's first bar, "
                    "the buy-and-hold baseline is the mean forward 10-bar log return over all blocks on that same grid, "
                    "and the component's raw column is found by its last_history_value name since the record calls it "
                    "below_sma200 rather than below_ma."),
    }
