import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_BLOCKS = 50
    MIN_POS_BLOCKS = 20

    # Find the raw value column of the config's component. The config names it 'ma_dist';
    # if that is absent, fall back to the single component present in the record.
    def raw_col(df):
        pref = "debug_info.components.ma_dist.last_history_value"
        if pref in df.columns:
            return pref
        cands = [c for c in df.columns
                 if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        return cands[0] if cands else None

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            col = raw_col(df)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if col is None:
                raw = pd.Series(np.nan, index=df.index)
            else:
                raw = pd.to_numeric(df[col], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            # Situation: close above its 200-day SMA (raw distance > 0); expected side: long.
            agree = active & raw.notna() & (raw > 0) & (f > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope (with intercept) of next-10-bar log return on forecast at block start"
    threshold = "slope t-stat >= 2 confirms (with supporting share higher), <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active forecast bars are long bars with the close above "
                           "its 200-day SMA (raw component distance > 0), as the plan's situation requires."),
            "reading": ("Situation taken as the component's raw distance value > 0 with a positive "
                        "forecast; the record's single component column is used as the config's ma_dist."),
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, ft = close[t], close[t + H], f[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(ft)) or c0 <= 0 or c1 <= 0:
                    continue
                xs.append(float(ft))
                ys.append(float(np.log(c1 / c0)))

    x = np.array(xs)
    y = np.array(ys)
    n_blocks = int(len(x))
    n_pos = int((x > 0).sum())

    counts = {"non-overlapping blocks": n_blocks, "blocks starting with forecast > 0": n_pos}

    slope = None
    tstat = None
    if n_blocks >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        if res.stderr is not None and res.stderr > 0:
            tstat = float(res.slope / res.stderr)

    share_pos = float((y[x > 0] > 0).mean()) if n_pos > 0 else None
    share_all = float((y > 0).mean()) if n_blocks > 0 else None
    if share_pos is not None and share_all is not None:
        sup_value = float(share_pos - share_all)
        sup_pass = bool(share_pos > share_all)
    else:
        sup_value = None
        sup_pass = None

    if n_blocks < MIN_BLOCKS or n_pos < MIN_POS_BLOCKS:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_blocks} blocks (need 50) and {n_pos} blocks "
                   f"with forecast > 0 (need 20).")
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope t-stat could not be computed, so neither the confirm nor the reject rule is met."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = ("Slope t-stat >= 2 and the share of positive 10-bar returns is higher in forecast > 0 "
                   "blocks than in all blocks.")
    elif tstat <= -2:
        status = "rejected"
        decided = "Slope t-stat <= -2: moves above the average reverse."
    else:
        status = "inconclusive"
        if tstat >= 2:
            decided = ("Slope t-stat >= 2 but the supporting share is not higher in forecast > 0 blocks, "
                       "so the confirm rule is not met and the reject rule is not met.")
        else:
            decided = "Slope t-stat lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tstat} if tstat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "share of positive 10-bar returns in forecast>0 blocks minus share over all blocks",
            "value": sup_value,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Blocks start at rows 0,10,20,... of each window and need a close 10 rows later in the "
                    "same window; the slope t is the ordinary OLS slope over its standard error; the plan's "
                    "'inconclusive if too few blocks' is treated as 'not observable'; the record's single "
                    "component column stands for the config's ma_dist."),
    }
