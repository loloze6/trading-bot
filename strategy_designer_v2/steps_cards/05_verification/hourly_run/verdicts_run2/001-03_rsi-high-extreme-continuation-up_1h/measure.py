import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    RAW = "debug_info.components.rsi_strength.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: RSI above 50, i.e. raw = (50 - RSI) * 0.4 < 0. Expected side: long (forecast > 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            n_agree += int(((d[RAW] < 0) & (d["forecast"] > 0) & act).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is RSI above 50 with a long position, but fewer than 90% of "
                           "the bars with a non-zero forecast have RSI above 50 and a positive forecast."),
            "reading": "none",
        }

    # ---------- 2. Top-decile threshold (pooled over all coins, windows and bars) ----------
    all_fc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            all_fc.append(df["forecast"].dropna().values)
    all_fc = np.concatenate(all_fc) if all_fc else np.array([])
    q90 = float(np.quantile(all_fc, 0.9)) if all_fc.size else np.nan

    # ---------- 3. Non-overlapping 6-bar forward returns ----------
    top_rets, neu_rets = [], []
    coin_top = {}
    coin_all = {}
    for coin, wins in bars.items():
        coin_top.setdefault(coin, [])
        coin_all.setdefault(coin, [])
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            grid = np.arange(0, len(df), H)
            g = df.iloc[grid]
            r = fwd.iloc[grid]
            fc = g["forecast"]
            raw = g[RAW]
            ok_r = r.notna()
            top_mask = ok_r & fc.notna() & (fc >= q90) & (fc > 0)
            neu_mask = ok_r & raw.notna() & (raw >= -2) & (raw <= 2)
            top_rets.extend(r[top_mask].tolist())
            neu_rets.extend(r[neu_mask].tolist())
            coin_top[coin].extend(r[top_mask].tolist())
            coin_all[coin].extend(r[ok_r].tolist())

    top_rets = np.array(top_rets, dtype=float)
    neu_rets = np.array(neu_rets, dtype=float)
    n_top, n_neu = int(top_rets.size), int(neu_rets.size)

    diff, t = None, None
    if n_top >= 2 and n_neu >= 2:
        diff = float(top_rets.mean() - neu_rets.mean())
        tt = stats.ttest_ind(top_rets, neu_rets, equal_var=False)
        t = float(tt.statistic)

    # ---------- 4. Supporting check: per-coin excess over unconditional mean ----------
    excess = {}
    for coin in coin_top:
        a = np.array(coin_top[coin], dtype=float)
        u = np.array(coin_all[coin], dtype=float)
        if a.size > 0 and u.size > 0:
            excess[coin] = float(a.mean() - u.mean())
    n_pos = int(sum(1 for v in excess.values() if v > 0))
    support_ok = n_pos >= 2

    # ---------- 5. Decision ----------
    if n_top < 200 or n_neu < 200 or t is None or not np.isfinite(t):
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 200 non-overlapping top-decile cases or 200 neutral cases "
                      "pooled (or no valid t-statistic).")
    elif diff > 0 and t >= 2 and support_ok:
        status = "confirmed"
        decided_by = ("Confirm: the pooled difference is above 0 with t >= 2 and the supporting excess is "
                      "positive in at least 2 coins.")
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided_by = ("Reject: the pooled difference is below 0 with t <= -2, so high RSI readings are "
                      "followed by weaker returns than neutral readings.")
    elif diff > 0 and t >= 2:
        status = "inconclusive"
        decided_by = "Inconclusive: a confirming t without the 2-of-3-coin agreement."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the t-statistic lies strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "6-bar forward return after top-decile forecast minus after neutral RSI (45-55)",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": "difference > 0 with t >= 2 to confirm; difference < 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "coins with positive top-decile excess over unconditional mean 6-bar return",
            "value": n_pos,
            "passed": bool(support_ok),
        },
        "counts": {
            "top-decile cases": n_top,
            "neutral cases": n_neu,
            "coins with positive excess": n_pos,
            "coins": int(len(excess)),
        },
        "decided_by": decided_by,
        "reading": ("Top decile is forecast at or above the 90th percentile of all forecast values pooled over "
                    "coins, windows and bars (and strictly positive), neutral is raw component in [-2, 2], the "
                    "supporting check uses the same non-overlapping grid with the unconditional mean over all grid "
                    "bars of the coin, and '2 of the 3 coins' is read as at least 2 coins positive among the "
                    "coins present."),
    }
