import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.rsi_low.last_history_value"
    FC = "forecast"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. Situation check ----------
    # Fidelity: graded RSI below 50 (raw value (50 - RSI) * 0.4 > 0); the expected rise means long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[[FC, RAW]].dropna()
            active = d[FC] != 0
            n_active += int(active.sum())
            situ = (d[RAW] > 0) & (d[FC] > 0)
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "24-bar forward return, top-decile forecast minus zero-forecast bars"
    thr_words = ("confirm if positive with t >= 2 (and supporting check holds); reject if negative with t <= -2, "
                 "or |t| < 2 with >= 150 cases and estimate within +/-0.1% per 24 bars; "
                 "fewer than 150 non-overlapping top-decile cases is inconclusive")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is RSI below 50 taken long, but fewer than 90% of the bars with a "
                           "non-zero forecast are long bars with RSI below 50."),
            "reading": "none",
        }

    # ---------- 2. Main measure ----------
    # Top-decile cut-off: 90th percentile of forecast over all pooled bars (all coins, all windows).
    all_fc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            all_fc.append(df[FC].dropna().values)
    all_fc = np.concatenate(all_fc) if all_fc else np.array([])
    q90 = float(np.quantile(all_fc, 0.9)) if all_fc.size else np.nan

    top_rets, zero_rets = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].values.astype(float)
            fc = df[FC].values.astype(float)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1, f = close[i], close[i + H], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                if f > 0 and f >= q90:
                    top_rets.append(r)
                elif f == 0:
                    zero_rets.append(r)

    top_rets = np.array(top_rets)
    zero_rets = np.array(zero_rets)
    n_top = int(len(top_rets))
    n_zero = int(len(zero_rets))

    diff = None
    tstat = None
    if n_top >= 2 and n_zero >= 2:
        diff = float(top_rets.mean() - zero_rets.mean())
        t = stats.ttest_ind(top_rets, zero_rets, equal_var=False).statistic
        tstat = float(t) if np.isfinite(t) else None

    # ---------- 3. Supporting check ----------
    coin_vals = {}
    for coin, wins in bars.items():
        gains, holds, exps = [], [], []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            r1 = close.shift(-1) / close - 1.0
            a = df[ALLOC].astype(float)
            m = r1.notna() & a.notna()
            gains.append((a[m] * r1[m]).values)
            holds.append(r1[m].values)
            exps.append(a[m].abs().values)
        g = np.concatenate(gains) if gains else np.array([])
        hld = np.concatenate(holds) if holds else np.array([])
        e = np.concatenate(exps) if exps else np.array([])
        if g.size == 0:
            continue
        avg_exp = e.mean()
        if avg_exp > 0:
            coin_vals[coin] = float(g.sum() / avg_exp - hld.sum())
        else:
            coin_vals[coin] = float(-hld.sum())
    n_pos = int(sum(1 for v in coin_vals.values() if v > 0))
    support_ok = bool(n_pos >= 2)

    # ---------- 4. Decision ----------
    if n_top < 150:
        status = "inconclusive"
        decided = "Fewer than 150 non-overlapping top-decile cases in the pool is too few for any verdict."
    elif diff is None or tstat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so no confirm or reject rule is met."
    elif diff > 0 and tstat >= 2:
        if support_ok:
            status = "confirmed"
            decided = "The top-decile minus neutral forward return is positive with t >= 2 and the supporting check holds."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif diff < 0 and tstat <= -2:
        status = "rejected"
        decided = "The top-decile minus neutral forward return is negative with t <= -2 (continuation rather than recovery)."
    elif abs(tstat) < 2 and abs(diff) <= 0.001:
        status = "rejected"
        decided = ("|t| < 2 with at least 150 cases and the estimate within +/-0.1% per 24 bars: "
                   "no difference from neutral readings.")
    else:
        status = "inconclusive"
        decided = "|t| < 2 but the estimate lies outside the +/-0.1% near-zero bound."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": {"name": "Welch t (non-overlapping 24-bar grid)", "value": tstat} if tstat is not None else None,
            "threshold": thr_words,
        },
        "supporting_check": {
            "name": "coins with return per unit avg exposure minus buy-and-hold > 0 (need >= 2)",
            "value": n_pos,
            "passed": support_ok,
        },
        "counts": {
            "non-overlapping top-decile cases": n_top,
            "non-overlapping zero-forecast cases": n_zero,
            "coins": int(len(coin_vals)),
        },
        "decided_by": decided,
        "reading": ("Top decile is forecast >= the 90th percentile of all pooled bars' forecasts (and > 0), returns are "
                    "sampled on each window's 0, 24, 48... grid, the per-coin supporting measure sums bar gains over all "
                    "windows divided by mean |allocation| minus the summed coin returns over the same bars, and 'at least "
                    "2 of the 3 coins' is applied literally as at least 2 positive coins among those present."),
    }
