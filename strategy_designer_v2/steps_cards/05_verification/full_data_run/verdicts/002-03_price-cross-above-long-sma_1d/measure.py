import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    LHV = "debug_info.components.above_ma.last_history_value"

    # ---------- 1. Situation check: close above its 200-day SMA (raw distance > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            d = pd.to_numeric(df[LHV], errors="coerce") if LHV in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & (f > 0) & d.notna() & (d > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else (agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {
                "name": "mean excess forward 10-bar return on positioned blocks vs all blocks",
                "value": None,
                "statistic": None,
                "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"active_bars": int(n_active), "active_bars_in_situation_long": int(n_agree)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars where the close is above its 200-day SMA (raw component distance > 0), so the forecast does not follow the plan's situation.",
            "reading": "The situation is taken as the raw last_history_value of above_ma (percent distance from the 200-day SMA) being above 0, with the expected side long.",
        }

    # ---------- 2. Criterion ----------
    excess_all = []
    pos_fwd = []
    pos_fc = []
    all_fwd = []
    per_coin = {}

    for coin, wins in bars.items():
        per_coin.setdefault(coin, 0)
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            grid = np.arange(0, n - H, H)
            if len(grid) == 0:
                continue
            fwd = close[grid + H] / close[grid] - 1.0
            fcg = fc[grid]
            ok = np.isfinite(fwd)
            if ok.sum() == 0:
                continue
            win_mean = float(np.mean(fwd[ok]))
            all_fwd.extend(fwd[ok].tolist())
            posm = ok & np.isfinite(fcg) & (fcg > 0)
            if posm.sum() > 0:
                excess_all.extend((fwd[posm] - win_mean).tolist())
                pos_fwd.extend(fwd[posm].tolist())
                pos_fc.extend(fcg[posm].tolist())
                per_coin[coin] += int(posm.sum())

    excess_all = np.asarray(excess_all, dtype=float)
    pos_fwd = np.asarray(pos_fwd, dtype=float)
    pos_fc = np.asarray(pos_fc, dtype=float)
    all_fwd = np.asarray(all_fwd, dtype=float)

    n_pos = int(len(excess_all))
    min_per_coin = int(min(per_coin.values())) if per_coin else 0

    mean_ex = float(np.mean(excess_all)) if n_pos > 0 else None
    t_val = None
    if n_pos > 1:
        sd = float(np.std(excess_all, ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_pos)))

    hit_diff = None
    if n_pos > 0 and len(all_fwd) > 0:
        hit_diff = float(np.mean(pos_fwd > 0) - np.mean(all_fwd > 0))

    slope = None
    if n_pos > 2 and np.std(pos_fc) > 0:
        slope = float(stats.linregress(pos_fc, pos_fwd).slope)

    counts = {"positioned_blocks_pooled": n_pos, "positioned_blocks_min_per_coin": min_per_coin}
    for c, k in per_coin.items():
        counts["positioned_blocks_" + str(c)] = int(k)

    if n_pos < 100 or min_per_coin < 10:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 100 pooled non-overlapping positioned 10-bar blocks, or fewer than 10 for some coin."
    elif t_val is None:
        status = "inconclusive"
        decided = "Inconclusive: the t-statistic of the mean excess could not be computed."
    elif mean_ex > 0 and t_val >= 2 and hit_diff is not None and hit_diff > 0:
        status = "confirmed"
        decided = "Confirmed: mean excess forward 10-bar return is above 0 with t >= 2 and the hit-rate difference is above 0."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Rejected: mean excess forward 10-bar return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t is between -2 and 2, or the confirm rule's hit-rate condition is not met."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": {
            "name": "mean excess forward 10-bar return on positioned blocks vs window mean",
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": "mean > 0 with t >= 2 (and hit-rate difference > 0) confirms; mean < 0 with t <= -2 rejects",
        },
        "supporting_check": {
            "name": "hit rate of positioned blocks minus hit rate of all blocks (slope of forward return on forecast reported in slope_value)",
            "value": hit_diff,
            "passed": (None if hit_diff is None else bool(hit_diff > 0)),
            "slope_value": slope,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Blocks are the bars at positions 0, 10, 20, ... of each window, and the coin's window mean (\"all bars\") is taken over that same grid. Positioned means forecast > 0 on the block's first bar. The t is the ordinary t of the pooled mean excess. The per-coin minimum applies to every coin present. The forecast-size slope is reported but not required, because the confirm rule names only the hit-rate difference.",
    }
