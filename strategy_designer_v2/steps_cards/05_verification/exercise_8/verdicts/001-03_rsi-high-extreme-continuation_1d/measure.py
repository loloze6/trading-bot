import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    VAL = "debug_info.components.rsi_high.last_history_value"
    NEUTRAL_BAND = 4.0

    # ---------- 1. situation check: RSI above 50 (raw value < 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", VAL]].dropna()
            act = d[d["forecast"] != 0]
            n_active += len(act)
            n_agree += int(((act[VAL] < 0) & (act["forecast"] > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_words = ("extreme-minus-neutral difference positive with Welch t >= 2 and positive in at least 2 of 3 coins "
                       "confirms; negative with t <= -2 rejects; at least 30 non-overlapping extreme and 30 neutral cases")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "extreme minus neutral forward 5-bar return", "value": None,
                             "statistic": None, "threshold": threshold_words},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is RSI above 50 with a long position, but fewer than 90% of the bars "
                           "with a non-zero forecast have RSI above 50 and a positive forecast."),
            "reading": "Situation taken as RSI(14) > 50 (raw component value < 0) with forecast > 0 on active bars.",
        }

    # ---------- 2. extreme threshold: top 20% of positive forecasts, pooled ----------
    pos_fc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = df["forecast"].dropna()
            pos_fc.append(f[f > 0].values)
    pos_fc = np.concatenate(pos_fc) if pos_fc else np.array([])
    cut = float(np.quantile(pos_fc, 0.8)) if len(pos_fc) > 0 else np.inf

    # ---------- 3. non-overlapping grid returns ----------
    ext_all, neu_all = [], []
    per_coin = {}
    for coin, wins in bars.items():
        ce, cn = [], []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            grid = np.arange(0, len(df), H)
            g = pd.DataFrame({"fc": df["forecast"].iloc[grid].values,
                              "val": df[VAL].iloc[grid].values,
                              "ret": fwd.iloc[grid].values})
            ge = g.dropna(subset=["fc", "ret"])
            ce.extend(ge.loc[(ge["fc"] > 0) & (ge["fc"] >= cut), "ret"].tolist())
            gn = g.dropna(subset=["val", "ret"])
            cn.extend(gn.loc[gn["val"].abs() <= NEUTRAL_BAND, "ret"].tolist())
        per_coin[coin] = (float(np.mean(ce)) - float(np.mean(cn))) if (ce and cn) else None
        ext_all.extend(ce)
        neu_all.extend(cn)

    n_ext, n_neu = len(ext_all), len(neu_all)
    diff = (float(np.mean(ext_all)) - float(np.mean(neu_all))) if (n_ext and n_neu) else None
    t = None
    if n_ext >= 2 and n_neu >= 2:
        tt = stats.ttest_ind(np.array(ext_all), np.array(neu_all), equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None
    coins_pos = int(sum(1 for v in per_coin.values() if v is not None and v > 0))

    # ---------- 4. supporting check ----------
    sup_pos = 0
    sup_vals = {}
    for coin, wins in bars.items():
        diffs = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            r = df["close"].astype(float).shift(-1) / df["close"].astype(float) - 1.0
            d = pd.DataFrame({"fc": df["forecast"], "a": df["postRebalance_current_allocation"], "r": r}).dropna()
            d = d[d["fc"] != 0]
            diffs.extend((d["a"] * d["r"] - d["r"]).tolist())
        s = float(np.sum(diffs)) if diffs else None
        sup_vals[coin] = s
        if s is not None and s > 0:
            sup_pos += 1
    sup_passed = bool(sup_pos >= 2)

    # ---------- 5. decision ----------
    if n_ext < 30 or n_neu < 30:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 30 non-overlapping extreme cases or fewer than 30 neutral cases in the pool."
    elif diff is None or t is None:
        status = "inconclusive"
        decided = "Inconclusive: the difference or its t-statistic could not be computed."
    elif diff > 0 and t >= 2 and coins_pos >= 2:
        status = "confirmed"
        decided = "Confirmed: the extreme-minus-neutral difference is positive with t >= 2 and positive in at least 2 coins."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "Rejected: the extreme-minus-neutral difference is negative with t <= -2."
    elif -2 < t < 2:
        status = "inconclusive"
        decided = "Inconclusive: t lies between -2 and 2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t >= 2 but the result is supported in only one coin (or fewer)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "extreme minus neutral forward 5-bar return (pooled, non-overlapping)",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": threshold_words,
        },
        "supporting_check": {
            "name": "coins where strategy minus buy-and-hold on active bars is positive (need >= 2)",
            "value": sup_pos,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping extreme cases": int(n_ext),
            "neutral cases": int(n_neu),
            "coins with positive difference": coins_pos,
            "coins in record": int(len(per_coin)),
        },
        "decided_by": decided,
        "reading": ("Extreme bars are grid bars whose forecast is positive and at or above the 80th percentile of all "
                    "positive forecasts pooled over coins and windows, neutral bars are grid bars with |raw value| <= 4, "
                    "'at least 2 of the 3 coins' is applied as at least 2 coins among those present, and the supporting "
                    "check sums per-bar (position return minus coin return) over active bars per coin."),
    }
