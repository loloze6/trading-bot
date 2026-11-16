import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.rsi_low.last_history_value"
    FC = "forecast"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. Situation check: RSI below 50 (raw > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            sub = df[[FC, RAW]].dropna()
            act = sub[FC] != 0
            n_active += int(act.sum())
            ok = act & (sub[RAW] > 0) & (sub[FC] > 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is RSI below 50 traded long (raw RSI pullback > 0 with a "
                           "positive forecast), but fewer than 90% of the bars with a nonzero forecast are such bars."),
            "reading": "Situation taken as raw (50 - RSI) value > 0, i.e. RSI < 50, with the expected side long.",
        }

    # ---------- 2. Main measure ----------
    # Top-decile cut-off: 90th percentile of all pooled forecasts (all coins, windows, bars).
    all_fc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            all_fc.append(df[FC].dropna().values)
    all_fc = np.concatenate(all_fc) if all_fc else np.array([])
    q90 = float(np.quantile(all_fc, 0.9)) if all_fc.size else np.nan

    top_rets, neu_rets = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].values.astype(float)
            fc = d[FC].values.astype(float)
            n = len(d)
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
                    neu_rets.append(r)

    top_rets = np.array(top_rets)
    neu_rets = np.array(neu_rets)
    n_top, n_neu = int(top_rets.size), int(neu_rets.size)

    diff = None
    t = None
    if n_top >= 2 and n_neu >= 2:
        diff = float(top_rets.mean() - neu_rets.mean())
        tt = stats.ttest_ind(top_rets, neu_rets, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    # ---------- 3. Supporting check ----------
    coins_pos = 0
    n_coins = 0
    per_coin = {}
    for coin, wins in bars.items():
        gains, bh, expo = [], [], []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            r1 = close.shift(-1) / close - 1.0
            a = d[ALLOC].astype(float)
            m = r1.notna() & a.notna() & np.isfinite(r1)
            gains.append((a[m] * r1[m]).values)
            bh.append(r1[m].values)
            expo.append(a[m].abs().values)
        g = np.concatenate(gains) if gains else np.array([])
        b = np.concatenate(bh) if bh else np.array([])
        e = np.concatenate(expo) if expo else np.array([])
        if g.size == 0:
            continue
        n_coins += 1
        avg_exp = e.mean()
        if avg_exp > 0:
            val = g.sum() / avg_exp - b.sum()
        else:
            val = np.nan
        per_coin[coin] = float(val) if np.isfinite(val) else None
        if np.isfinite(val) and val > 0:
            coins_pos += 1
    support_passed = bool(coins_pos >= 2)

    # ---------- 4. Decision ----------
    if n_top < 150 or diff is None or t is None:
        status = "inconclusive"
        decided_by = "Fewer than 150 non-overlapping top-decile cases in the pool (or no computable t) is too few for any verdict."
    elif diff > 0 and t >= 2:
        if support_passed:
            status = "confirmed"
            decided_by = "Top-decile minus neutral forward return is positive with t >= 2 and the supporting check holds."
        else:
            status = "inconclusive"
            decided_by = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided_by = "Top-decile minus neutral forward return is negative with t <= -2 (continuation rather than recovery)."
    elif abs(t) < 2 and abs(diff) <= 0.001:
        status = "rejected"
        decided_by = "|t| < 2 with at least 150 cases and the estimate within +/-0.1% per 24 bars: no difference from neutral readings."
    else:
        status = "inconclusive"
        decided_by = "|t| < 2 but the estimate lies outside the +/-0.1% near-zero bound, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "24-bar forward return, top-decile forecast minus zero-forecast bars (%)",
            "value": (diff * 100.0) if diff is not None else None,
            "statistic": {"name": "Welch t (non-overlapping)", "value": t} if t is not None else None,
            "threshold": "confirm: positive with t >= 2; reject: negative with t <= -2, or |t| < 2 with >= 150 cases and |estimate| <= 0.1% per 24 bars",
        },
        "supporting_check": {
            "name": "coins with return per unit avg exposure minus buy-and-hold > 0 (need >= 2)",
            "value": int(coins_pos),
            "passed": support_passed,
        },
        "counts": {
            "non-overlapping top-decile cases": n_top,
            "non-overlapping neutral cases": n_neu,
            "coins": int(n_coins),
            "coins with positive excess": int(coins_pos),
        },
        "decided_by": decided_by,
        "reading": ("The top decile is forecast >= the 90th percentile of all pooled bars' forecasts (and > 0), "
                    "returns are sampled on the 0,24,48,... grid of each window with Welch t, the supporting check "
                    "sums per-bar gains and per-bar coin returns over each coin's pooled windows with exposure as mean "
                    "|allocation|, and with only 2 coins present 'at least 2 of the 3 coins' is applied literally as at least 2 coins."),
    }
