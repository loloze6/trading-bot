import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    PFX = "debug_info.components."
    # plan's parts: id -> (direction the plan states, standardise window, min_periods)
    parts = {
        "mom28": (1.0, 60, 20),
        "rev1": (-1.0, 60, 20),
        "high90": (1.0, 90, 22),
        "vol30": (-1.0, 60, 20),
    }

    def col(df, name):
        if name in df.columns:
            return pd.to_numeric(df[name], errors="coerce").reset_index(drop=True)
        return pd.Series(np.nan, index=range(len(df)))

    def rebuild(df, cid, direction, window, minp):
        raw = col(df, PFX + cid + ".last_history_value")
        post = col(df, PFX + cid + ".post_pipeline_value")
        # standardise rebuilt from the raw values where a full past window is inside the record
        denom = raw.abs().shift(1).rolling(window, min_periods=window).mean()
        val = raw * 10.0 / denom
        val = val.where(denom != 0, 0.0).clip(-20, 20)
        # earlier bars (history before the record): engine's size, the plan's direction on the raw sign
        fb = direction * np.sign(raw) * post.abs()
        val = direction * val
        out = val.where(denom.notna(), fb)
        return out.where(raw.notna())

    # ---------- situation check ----------
    agree_n, active_n = 0, 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = col(df, "forecast")
            vals = [rebuild(df, cid, d, win, mp) for cid, (d, win, mp) in parts.items()]
            score = (vals[0] + vals[1] + vals[2] + vals[3] + 2.0 * 10.0) / 6.0
            score = score.clip(-20, 20)
            act = f.notna() & (f != 0) & score.notna()
            active_n += int(act.sum())
            agree_n += int((np.sign(score[act]) == np.sign(f[act])).sum())
    agreement = float(agree_n / active_n) if active_n > 0 else 0.0
    passed = agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(active_n)},
            "decided_by": "The forecast's sign does not follow the sign of the plan's equal-weight score "
                          "(momentum + minus 1-day return + nearness to the 90-day high + minus volatility + 20) / 6 "
                          "on at least 90 % of its active bars.",
            "reading": "The score is rebuilt from last_history_value with the plan's directions; bars without a full "
                       "past window inside the record take the recorded size with the plan's direction.",
        }

    # ---------- criterion ----------
    # normal 5-day drift per coin: mean of non-overlapping 5-bar returns over all its windows
    per_coin = {}
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = col(df, "close").values
            f = col(df, "forecast").values
            n = len(c)
            for i in range(0, n - H, H):
                r = c[i + H] / c[i] - 1.0 if (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0) else np.nan
                rows.append((f[i], r))
        per_coin[coin] = rows

    prod, exc_pos, exc_neg = [], [], []
    n_nonzero = 0
    for coin, rows in per_coin.items():
        rets = np.array([r for _, r in rows if np.isfinite(r)], dtype=float)
        if len(rets) == 0:
            continue
        drift = rets.mean()
        for fc, r in rows:
            if not (np.isfinite(fc) and np.isfinite(r)):
                continue
            ex = r - drift
            prod.append(fc / 10.0 * ex)
            if fc > 0:
                exc_pos.append(ex)
                n_nonzero += 1
            elif fc < 0:
                exc_neg.append(ex)
                n_nonzero += 1

    prod = np.array(prod, dtype=float)
    n_cases = int(len(prod))
    mean_p = float(prod.mean()) if n_cases > 0 else None
    t_p = None
    if n_cases > 1:
        sd = prod.std(ddof=1)
        t_p = float(mean_p / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff, welch_t = None, None
    if len(exc_pos) >= 2 and len(exc_neg) >= 2:
        diff = float(np.mean(exc_pos) - np.mean(exc_neg))
        welch_t = float(stats.ttest_ind(exc_pos, exc_neg, equal_var=False).statistic)
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {
        "non-overlapping cases with a non-zero forecast": int(n_nonzero),
        "non-overlapping cases": n_cases,
        "cases with forecast > 0": len(exc_pos),
        "cases with forecast < 0": len(exc_neg),
    }

    if n_nonzero < 300:
        status = "not observable"
        decided = "Fewer than 300 non-overlapping cases with a non-zero forecast."
    elif t_p is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed."
    elif t_p >= 2 and sup_passed:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the supporting difference is above 0."
    elif t_p <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less: a higher score is followed by lower excess returns."
    elif t_p >= 2:
        status = "inconclusive"
        decided = "The main measure's t is 2 or more but the supporting difference is at or below 0."
    else:
        status = "inconclusive"
        decided = "The main measure's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean of forecast/10 x excess 5-day return, before costs",
            "value": mean_p,
            "statistic": None if t_p is None else {"name": "t of the mean", "value": t_p},
            "threshold": "t >= 2 confirms (with supporting difference > 0); t <= -2 rejects",
        },
        "supporting_check": {
            "name": "mean excess 5-day return, forecast > 0 minus forecast < 0 (Welch)",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The main mean pools every grid bar (positions 0, 5, 10, ... of each window) with a valid "
                   "5-bar return, a zero forecast giving a zero product, the drift is each coin's mean "
                   "non-overlapping 5-bar return over all its windows, and the supporting check passes on the "
                   "sign of the difference alone, as the plan states.",
    }
