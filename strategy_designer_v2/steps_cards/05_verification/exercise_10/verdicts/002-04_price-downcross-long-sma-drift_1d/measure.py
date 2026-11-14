import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_BLOCKS = 15

    def find_col(df, suffix):
        cols = [c for c in df.columns
                if c.startswith("debug_info.components.") and c.endswith(suffix)]
        return cols[0] if cols else None

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    all_fwd_log = []        # forward 10-bar log returns over all tested bars
    block_rows = []         # (forecast, fwd_log, fwd_simple) on the non-overlapping grid

    for coin in bars:
        for win in bars[coin]:
            df = bars[coin][win].reset_index(drop=True)
            raw_col = find_col(df, ".last_history_value")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = (pd.to_numeric(df[raw_col], errors="coerce")
                   if raw_col is not None else pd.Series(np.nan, index=df.index))
            close = pd.to_numeric(df["close"], errors="coerce")

            # Situation: close below its 200-bar SMA (raw distance < 0); expected side: short
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw < 0) & (fc < 0)
            n_agree += int(agree.sum())

            # Forward 10-bar returns within this window only
            fwd_simple = close.shift(-H) / close - 1.0
            fwd_log = np.log(close.shift(-H) / close)
            valid = fwd_log.notna() & np.isfinite(fwd_log)
            all_fwd_log.extend(fwd_log[valid].tolist())

            for pos in range(0, len(df), H):
                if pd.notna(fwd_log.iloc[pos]) and np.isfinite(fwd_log.iloc[pos]) \
                        and pd.notna(fc.iloc[pos]):
                    block_rows.append((float(fc.iloc[pos]),
                                       float(fwd_log.iloc[pos]),
                                       float(fwd_simple.iloc[pos])))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "slope of excess forward 10-bar log return on forecast (short bars, non-overlapping blocks)"
    threshold = "slope t >= +2 (with mean excess < 0 and higher decline share) confirms; slope t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active),
                       "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars with the close "
                           "below its 200-bar SMA, so the config does not trade the plan's situation."),
            "reading": "The situation is read from the component's raw distance to the SMA200 (negative = close below), the expected side is short.",
        }

    # ---------- 2. criterion ----------
    baseline = float(np.mean(all_fwd_log)) if all_fwd_log else np.nan
    blocks = pd.DataFrame(block_rows, columns=["fc", "fwd_log", "fwd_simple"])
    short = blocks[blocks["fc"] < 0].copy()
    n_short_blocks = int(len(short))
    n_all_blocks = int(len(blocks))
    short["excess"] = short["fwd_log"] - baseline

    slope = None
    t_slope = None
    mean_excess = None
    if n_short_blocks >= 3 and short["fc"].nunique() > 1:
        res = stats.linregress(short["fc"].values, short["excess"].values)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None
    if n_short_blocks > 0:
        mean_excess = float(short["excess"].mean())

    share_short = float((short["fwd_simple"] < 0).mean()) if n_short_blocks > 0 else None
    share_all = float((blocks["fwd_simple"] < 0).mean()) if n_all_blocks > 0 else None
    sup_value = (share_short - share_all) if (share_short is not None and share_all is not None) else None
    sup_passed = (sup_value > 0) if sup_value is not None else None

    counts = {"non-overlapping 10-bar blocks with forecast < 0": n_short_blocks,
              "non-overlapping 10-bar blocks, all": n_all_blocks}

    if n_short_blocks < MIN_BLOCKS:
        status = "not observable"
        decided = (f"Only {n_short_blocks} non-overlapping 10-bar blocks with forecast < 0, "
                   f"below the plan's minimum of {MIN_BLOCKS}.")
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t-statistic could not be computed (no variation in the forecast), so no rule is met."
    elif t_slope >= 2 and mean_excess is not None and mean_excess < 0 and sup_passed:
        status = "confirmed"
        decided = ("Slope t >= +2, mean excess forward return on short bars below 0, and the share of "
                   "declines on short blocks higher than on all blocks.")
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t <= -2: price rebounds more strongly the deeper the close is below the SMA200."
    else:
        status = "inconclusive"
        if t_slope >= 2:
            decided = ("Slope t >= +2 but the mean excess return or the decline-share condition of the "
                       "confirm rule is not met, so neither confirm nor reject applies.")
        else:
            decided = "Slope t-statistic lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t_slope}
                                       if t_slope is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "decline share on short blocks minus decline share on all blocks",
                             "value": sup_value, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The baseline is the mean forward 10-bar log return over every tested bar with a "
                    "within-window forward return, blocks are rows 0, 10, 20, ... of each window, the slope "
                    "is OLS of excess log return on the forecast with its ordinary t, and the mean excess in "
                    "the confirm rule is taken over the short blocks."),
    }
