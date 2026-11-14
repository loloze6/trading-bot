import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    NEUTRAL_MAX = 1.0
    TOP_FRAC = 0.20
    MIN_CASES = 30
    T_CONFIRM = 2.0
    MIN_POS_COINS = 2

    # ---- Pooled top-20% cut-off over all non-zero forecasts (all coins, all windows, all rows) ----
    nz_all = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            f = f[np.isfinite(f) & (f != 0)]
            nz_all.append(f)
    nz_all = np.concatenate(nz_all) if nz_all else np.array([])
    cut = float(np.quantile(nz_all, 1 - TOP_FRAC)) if nz_all.size > 0 else np.nan

    ext_all, neu_all = [], []
    per_coin = {}
    excess_per_coin = {}
    excess_total = 0.0
    excess_any = False

    for coin, wins in bars.items():
        ext_c, neu_c = [], []
        coin_excess = 0.0
        coin_has = False
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)

            # Non-overlapping grid 0, H, 2H, ... inside the window
            for t in range(0, n - H, H):
                c0, c1, f = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                if np.isfinite(cut) and f != 0 and f >= cut:
                    ext_c.append(r)
                elif f < NEUTRAL_MAX:
                    neu_c.append(r)

            # Supporting: strategy gain minus buy-and-hold scaled to average exposure (before costs)
            alloc = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce").to_numpy(dtype=float)
            if n >= 2:
                r1 = close[1:] / close[:-1] - 1.0
                a = alloc[:-1]
                ok = np.isfinite(r1) & np.isfinite(a)
                if ok.sum() > 0:
                    strat = float(np.sum(a[ok] * r1[ok]))
                    bh = float(np.mean(a[ok]) * np.sum(r1[ok]))
                    coin_excess += strat - bh
                    coin_has = True

        ext_all += ext_c
        neu_all += neu_c
        diff_c = (float(np.mean(ext_c)) - float(np.mean(neu_c))) if (ext_c and neu_c) else None
        per_coin[coin] = diff_c
        if coin_has:
            excess_per_coin[coin] = coin_excess
            excess_total += coin_excess
            excess_any = True

    n_ext, n_neu = len(ext_all), len(neu_all)
    diff = None
    t_stat = None
    if n_ext > 0 and n_neu > 0:
        diff = float(np.mean(ext_all) - np.mean(neu_all))
    if n_ext >= 2 and n_neu >= 2:
        res = stats.ttest_ind(np.array(ext_all), np.array(neu_all), equal_var=False)
        t_stat = float(res.statistic) if np.isfinite(res.statistic) else None

    pos_coins = sum(1 for v in per_coin.values() if v is not None and v > 0)
    support_val = float(excess_total) if excess_any else None
    support_pass = (support_val > 0) if support_val is not None else None

    if n_ext < MIN_CASES or n_neu < MIN_CASES:
        status = "inconclusive"
        decided = f"Fewer than {MIN_CASES} non-overlapping extreme ({n_ext}) or neutral ({n_neu}) cases pooled, so the result is inconclusive."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so the result is inconclusive."
    elif t_stat <= 0:
        status = "rejected"
        if t_stat <= -2:
            decided = "The pooled extreme-minus-neutral difference has t <= -2, which rejects and points to reversal."
        else:
            decided = "The pooled extreme-minus-neutral difference is zero or negative (t <= 0), which rejects."
    elif t_stat >= T_CONFIRM and pos_coins >= MIN_POS_COINS and support_pass:
        status = "confirmed"
        decided = "The difference is positive with t >= 2, positive in at least 2 coins, and the pooled supporting excess is positive, which confirms."
    elif t_stat >= T_CONFIRM:
        status = "inconclusive"
        decided = "t >= 2 but the per-coin (at least 2 positive coins) or pooled supporting-excess condition fails, so neither the confirm nor the reject rule is met."
    else:
        status = "inconclusive"
        decided = "The t-statistic is between 0 and 2, which is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 5-bar forward return, extreme minus neutral bars",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t_stat} if t_stat is not None else None,
            "threshold": "positive with t >= 2 to confirm; t <= 0 rejects",
        },
        "supporting_check": {
            "name": "strategy return minus exposure-scaled buy-and-hold, pooled, before costs",
            "value": support_val,
            "passed": support_pass,
        },
        "counts": {
            "non-overlapping extreme cases pooled": n_ext,
            "neutral cases": n_neu,
            "coins with positive difference": pos_coins,
            "coins present": len(per_coin),
        },
        "decided_by": decided,
        "reading": (
            "The top-20% cut-off is the 80th percentile of all non-zero forecasts pooled over every coin, window and row "
            "(extreme means forecast >= the cut-off). Neutral means forecast < 1, including 0. Only the grid bars 0, 5, 10, ... "
            "of each window are used. The 'at least 2 of 3 coins' rule is applied as at least 2 positive coins among those "
            "present. The supporting excess is the sum of daily allocation x next-bar return minus the mean allocation x the "
            "summed daily coin returns, added over windows and coins, and it is judged by the sign of the pooled total."
        ),
    }
