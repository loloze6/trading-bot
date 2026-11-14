import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    DROP_COL = "debug_info.components.drop.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if active.sum() == 0:
                continue
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            uptrend = regime == "trending"
            px_move = df["close"] / df["close"].shift(1) - 1
            if DROP_COL in df.columns:
                drop = pd.to_numeric(df[DROP_COL], errors="coerce")
                drop = drop.where(drop.notna(), px_move)
            else:
                drop = px_move
            down = drop < 0
            situ = uptrend & down & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are uptrend (trending regime) "
                           "down days with a long forecast, as the Fidelity's situation and side require."),
            "reading": "Situation taken as regime 'trending' and a negative one-day move, side long.",
        }

    # ---------- 2. Criterion ----------
    def cluster_first(positions, values):
        out = []
        last = None
        for p, v in zip(positions, values):
            if last is None or p - last > H:
                out.append(v)
            last = p
        return out

    big_cases, mild_cases = [], []
    n_big_bars, n_mild_bars = 0, 0
    for coin, wins in bars.items():
        # coin mean 3-bar return over all its windows
        all_fwd = []
        fwd_by_w = {}
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fwd = np.full(len(c), np.nan)
            if len(c) > H:
                fwd[:-H] = c[H:] / c[:-H] - 1
            fwd_by_w[w] = fwd
            all_fwd.append(fwd[np.isfinite(fwd)])
        allv = np.concatenate(all_fwd) if all_fwd else np.array([])
        if len(allv) == 0:
            continue
        mu = float(np.mean(allv))
        for w, df in wins.items():
            fwd = fwd_by_w[w]
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ok = np.isfinite(fwd) & np.isfinite(fc)
            ex = fwd - mu
            big_idx = np.where(ok & (fc >= 5))[0]
            mild_idx = np.where(ok & (fc > 0) & (fc < 2))[0]
            n_big_bars += len(big_idx)
            n_mild_bars += len(mild_idx)
            big_cases += cluster_first(big_idx, ex[big_idx])
            mild_cases += cluster_first(mild_idx, ex[mild_idx])

    def tstat(x):
        x = np.asarray(x, dtype=float)
        if len(x) < 2:
            return (float(np.mean(x)) if len(x) else None), None, None
        m = float(np.mean(x))
        s = float(np.std(x, ddof=1))
        if s == 0:
            return m, None, None
        se = s / np.sqrt(len(x))
        return m, m / se, se

    m_big, t_big, _ = tstat(big_cases)
    m_mild, t_mild, se_mild = tstat(mild_cases)

    sup_passed = None
    if m_mild is not None and se_mild is not None:
        q = stats.t.ppf(0.975, len(mild_cases) - 1)
        sup_passed = bool(m_mild - q * se_mild <= 0 <= m_mild + q * se_mild)

    n_cases = len(big_cases)
    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} de-overlapped forecast-5-or-more cases, below the plan's minimum of 30."
    elif t_big is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero variance), so neither confirm nor reject is met."
    elif m_big > 0 and t_big >= 2:
        status = "confirmed"
        decided = "Mean excess 3-bar return after forecast-5-or-more bars is positive with t >= 2 (confirm rule)."
    elif m_big < 0 and t_big <= -2:
        status = "rejected"
        decided = "Mean excess 3-bar return after forecast-5-or-more bars is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean excess 3-bar forward return after forecast >= 5 bars",
            "value": None if m_big is None else float(m_big),
            "statistic": None if t_big is None else {"name": "t of the mean", "value": float(t_big)},
            "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 30 de-overlapped cases",
        },
        "supporting_check": {
            "name": "mean excess 3-bar return on mild down days (0 < forecast < 2), 95% CI includes 0",
            "value": None if m_mild is None else float(m_mild),
            "passed": sup_passed,
        },
        "counts": {
            "de-overlapped cases (forecast >= 5)": int(n_cases),
            "forecast >= 5 bars": int(n_big_bars),
            "de-overlapped mild cases (0 < forecast < 2)": int(len(mild_cases)),
        },
        "decided_by": decided,
        "reading": ("The coin's mean 3-bar return is over all bars of all its windows; events within 3 bars of the "
                    "previous event in the same window are chained into one case valued at its first event; the "
                    "mild group is de-overlapped the same way, and the supporting check is reported but does not "
                    "change the plan's t rule."),
    }
