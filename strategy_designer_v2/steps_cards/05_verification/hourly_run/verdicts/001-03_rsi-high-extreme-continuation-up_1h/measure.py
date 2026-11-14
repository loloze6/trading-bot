import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    RAW = "debug_info.components.rsi_strength.last_history_value"
    TH = 2.0
    MIN_N = 200

    # ---------- 1. Situation check ----------
    # Fidelity: situation = RSI above 50 (raw = (50 - RSI) * 0.4 < 0); outcome = rise -> long (forecast > 0).
    n_active = 0
    n_agree = 0
    all_fc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce")
            ok = fc.notna() & raw.notna()
            act = ok & (fc != 0)
            n_active += int(act.sum())
            n_agree += int((act & (raw < 0) & (fc > 0)).sum())
            all_fc.append(fc[fc.notna()].values)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "6-bar return after top-decile forecast bars minus after neutral RSI bars",
                "value": None,
                "statistic": None,
                "threshold": "difference > 0 with t >= 2 to confirm; < 0 with t <= -2 to reject",
            },
            "supporting_check": None,
            "counts": {"top_decile_cases": 0, "neutral_cases": 0},
            "decided_by": (
                "Fewer than 90% of the bars with a non-zero forecast are long bars with RSI above 50, "
                "so the config does not trade the plan's situation (RSI above 50, long) as the Fidelity states."
            ),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    fc_all = np.concatenate(all_fc) if all_fc else np.array([])
    q90 = float(np.quantile(fc_all, 0.9)) if fc_all.size else np.nan

    top_rets = []
    neu_rets = []
    per_coin = {}
    for coin, wins in bars.items():
        c_top = []
        c_all = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            raw = pd.to_numeric(df[RAW], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                c_all.append(r)
                if np.isfinite(fc[t]) and fc[t] > 0 and fc[t] >= q90:
                    top_rets.append(r)
                    c_top.append(r)
                if np.isfinite(raw[t]) and -2.0 <= raw[t] <= 2.0:
                    neu_rets.append(r)
        per_coin[coin] = (c_top, c_all)

    top = np.array(top_rets, dtype=float)
    neu = np.array(neu_rets, dtype=float)
    n_top, n_neu = int(top.size), int(neu.size)

    diff = None
    tstat = None
    if n_top >= 2 and n_neu >= 2:
        diff = float(top.mean() - neu.mean())
        tt = stats.ttest_ind(top, neu, equal_var=False)
        tstat = float(tt.statistic) if np.isfinite(tt.statistic) else None

    excess = {}
    for coin, (c_top, c_all) in per_coin.items():
        if len(c_top) > 0 and len(c_all) > 0:
            excess[coin] = float(np.mean(c_top) - np.mean(c_all))
    n_pos = int(sum(1 for v in excess.values() if v > 0))
    support_ok = n_pos >= 2

    if n_top < MIN_N or n_neu < MIN_N or diff is None or tstat is None:
        status = "inconclusive"
        decided = "Fewer than 200 non-overlapping top-decile or neutral cases pooled (or no computable t), so the plan rules the test inconclusive."
    elif diff > 0 and tstat >= TH and support_ok:
        status = "confirmed"
        decided = "The pooled difference is above 0 with t >= 2 and the supporting excess is positive in at least 2 coins, so the plan confirms."
    elif diff < 0 and tstat <= -TH:
        status = "rejected"
        decided = "The pooled difference is below 0 with t <= -2, so the plan rejects."
    elif diff > 0 and tstat >= TH:
        status = "inconclusive"
        decided = "A confirming t without the supporting excess positive in at least 2 coins is inconclusive under the plan."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and 2, so the plan rules the test inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "6-bar return after top-decile forecast bars minus after neutral RSI (45-55) bars",
            "value": diff,
            "statistic": {"name": "Welch t", "value": tstat} if tstat is not None else None,
            "threshold": "difference > 0 with t >= 2 to confirm; difference < 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "coins with positive top-decile excess over unconditional 6-bar mean",
            "value": n_pos,
            "passed": bool(support_ok),
        },
        "counts": {
            "top_decile_cases": n_top,
            "neutral_cases": n_neu,
            "coins": int(len(per_coin)),
        },
        "decided_by": decided,
        "reading": (
            "Top decile is forecast >= the 90th percentile of all forecast values pooled over coins and windows (and > 0), "
            "cases and the unconditional mean use the non-overlapping 6-bar grid from each window's first row, neutral is raw "
            "value in [-2, 2] inclusive, and with only 2 coins in the record the '2 of 3 coins' rule requires both coins positive."
        ),
    }
