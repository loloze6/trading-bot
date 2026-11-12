import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_SHORT_BLOCKS = 15

    def find_raw_col(df):
        cols = [c for c in df.columns
                if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        for c in cols:
            if ".below_ma." in c:
                return c
        for c in cols:
            if "below_sma200" in c:
                return c
        return cols[0] if cols else None

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            rc = find_raw_col(df)
            if rc is None:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[rc], errors="coerce")
            ok = f.notna() & raw.notna()
            act = ok & (f != 0)
            n_active += int(act.sum())
            # situation: close below SMA200 (raw distance < 0), expected side short (forecast < 0)
            n_agree += int((act & (raw < 0) & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of excess forward 10-bar log return on forecast, short-bar non-overlapping blocks"
    threshold = "slope t >= +2 (with mean excess < 0 and higher decline share) confirms; t <= -2 rejects; otherwise inconclusive"
    reading_base = ("Situation taken as raw SMA200 distance < 0 with forecast < 0; baseline is the mean forward 10-bar "
                    "log return over every bar with a valid in-window forward return; short blocks are grid bars "
                    "(positions 0,10,20,... per window) with forecast < 0 and the regression uses forecast as x; "
                    "the plan's minimum of 15 short blocks is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": (f"Only {agreement:.1%} of active bars are short bars with close below the SMA200; "
                           "the plan requires the short-only position to exist exactly while the close is below its 200-day SMA."),
            "reading": reading_base,
        }

    # ---------- 2. Criterion ----------
    all_fwd = []
    grid_rows = []  # (forecast, fwd_log)
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                with np.errstate(divide="ignore", invalid="ignore"):
                    fwd[:n - H] = np.log(c[H:] / c[:n - H])
            valid = np.isfinite(fwd)
            all_fwd.extend(fwd[valid].tolist())
            for i in range(0, n, H):
                if np.isfinite(fwd[i]) and np.isfinite(f[i]):
                    grid_rows.append((f[i], fwd[i]))

    all_fwd = np.array(all_fwd)
    baseline = float(all_fwd.mean()) if len(all_fwd) else np.nan
    g = np.array(grid_rows) if grid_rows else np.empty((0, 2))
    n_blocks_all = int(len(g))
    short = g[g[:, 0] < 0] if len(g) else g
    n_short = int(len(short))

    counts = {"non-overlapping 10-bar blocks with forecast < 0": n_short,
              "non-overlapping 10-bar blocks, all": n_blocks_all}

    share_short = float(np.mean(short[:, 1] < 0)) if n_short else None
    share_all = float(np.mean(g[:, 1] < 0)) if n_blocks_all else None
    sup_val = (share_short - share_all) if (share_short is not None and share_all is not None) else None
    sup_passed = bool(sup_val > 0) if sup_val is not None else None
    supporting = {"name": "decline share on short blocks minus decline share on all blocks",
                  "value": sup_val, "passed": sup_passed}

    slope = None
    t = None
    mean_excess = None
    if n_short >= 3:
        x = short[:, 0]
        y = short[:, 1] - baseline
        mean_excess = float(np.mean(y))
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
                t = float(lr.slope / lr.stderr)
    elif n_short > 0:
        mean_excess = float(np.mean(short[:, 1] - baseline))

    main = {"name": main_name, "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": threshold}

    if n_short < MIN_SHORT_BLOCKS:
        status = "not observable"
        decided = f"Only {n_short} non-overlapping 10-bar blocks with forecast < 0, below the plan's minimum of 15."
    elif t is None:
        status = "inconclusive"
        decided = "The slope t-statistic could not be computed (no variation in forecast), so no confirm or reject rule is met."
    elif t >= 2 and mean_excess is not None and mean_excess < 0 and sup_passed:
        status = "confirmed"
        decided = "Slope t >= +2, mean excess forward return on short bars below 0, and decline share on short blocks higher than on all blocks."
    elif t <= -2:
        status = "rejected"
        decided = "Slope t <= -2: price rebounds more strongly the deeper the close is below the SMA200."
    else:
        status = "inconclusive"
        if t >= 2:
            decided = "Slope t >= +2 but the mean excess or the decline-share condition of the confirm rule is not met, so the result is inconclusive."
        else:
            decided = "Slope t-statistic lies between -2 and +2, which the plan defines as inconclusive."

    counts["mean excess forward return on short blocks (not a count)"] = None
    counts.pop("mean excess forward return on short blocks (not a count)")
    main["mean_excess_short"] = mean_excess

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
