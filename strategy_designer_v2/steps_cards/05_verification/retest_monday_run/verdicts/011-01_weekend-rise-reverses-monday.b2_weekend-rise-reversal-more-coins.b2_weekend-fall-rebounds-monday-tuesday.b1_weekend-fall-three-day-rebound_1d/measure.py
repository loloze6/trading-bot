import numpy as np
import pandas as pd
from scipy import stats


def _ts(series):
    s = series
    if pd.api.types.is_numeric_dtype(s):
        v = pd.to_numeric(s, errors="coerce")
        med = np.nanmedian(v.values) if len(v) else 0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True, errors="coerce")


def measure(bars):
    H = 3
    MIN_CASES = 100
    RAW = "debug_info.components.sun_fall.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["_ts"] = _ts(d["timestamp"])
            d["_close"] = pd.to_numeric(d["close"], errors="coerce")
            d["_fc"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            # Sunday one-bar return in percent: recorded raw value, else recomputed from prices
            ret_px = (d["_close"] / d["_close"].shift(1) - 1.0) * 100.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                sun_ret = raw.where(raw.notna(), ret_px)
            else:
                sun_ret = ret_px
            d["_sunday"] = d["_ts"].dt.dayofweek == 6
            d["_sunret"] = sun_ret
            prepared[coin][w] = d

            active = d["_fc"] != 0
            situ = d["_sunday"] & (d["_sunret"] < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (d["_fc"] > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement is None) or (agreement >= 0.90)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are Sunday bars with a Sunday fall and a long forecast, as the plan's Fidelity requires.",
            "reading": "The Sunday bar is the bar whose UTC start time is a Sunday; the Sunday fall is its one-bar return below 0 (recorded raw value, else from closes); the expected side is long.",
        }

    # ---------- criterion ----------
    case_fc = []
    case_ex = []
    for coin, wins in prepared.items():
        # coin's mean 3-bar return over all its windows, non-overlapping grid
        grid_rets = []
        for w, d in wins.items():
            c = d["_close"].values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for w, d in wins.items():
            c = d["_close"].values
            fc = d["_fc"].values
            sun = d["_sunday"].values
            for i in range(len(d)):
                if not (sun[i] and fc[i] >= 2):
                    continue
                if i + H >= len(d):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                case_fc.append(float(fc[i]))
                case_ex.append(float(r - mu))

    case_fc = np.array(case_fc)
    case_ex = np.array(case_ex)
    n = int(len(case_ex))

    value = None
    tval = None
    if n >= 2:
        prod = case_fc / 10.0 * case_ex
        value = float(np.mean(prod))
        sd = float(np.std(prod, ddof=1))
        tval = float(value / (sd / np.sqrt(n))) if sd > 0 else None
    elif n == 1:
        value = float(case_fc[0] / 10.0 * case_ex[0])

    sup_val = None
    sup_pass = None
    n_hi = n_lo = 0
    if n >= 2:
        med = float(np.median(case_fc))
        hi = case_fc > med
        lo = ~hi
        n_hi, n_lo = int(hi.sum()), int(lo.sum())
        if n_hi > 0 and n_lo > 0:
            sup_val = float(np.mean(case_ex[hi]) - np.mean(case_ex[lo]))
            sup_pass = bool(sup_val > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases (Sunday bars with forecast of 2 or more and a full 3-bar return), below the plan's minimum of 100."
    elif tval is not None and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule: t of 2 or more with at least 100 cases, and the larger-fall half's mean excess return exceeds the smaller-fall half's."
    elif tval is not None and tval >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule: t of 2 or more but the supporting check fails."
    elif tval is not None and tval <= -2:
        status = "rejected"
        decided = "Reject rule: t of -2 or less with at least 100 cases."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": {
            "name": "mean of (forecast/10) x excess 3-bar return over Sunday cases",
            "value": value,
            "statistic": ({"name": "t of the mean", "value": tval} if tval is not None else None),
            "threshold": "t >= 2 confirms (with supporting check), t <= -2 rejects, with at least 100 cases",
        },
        "supporting_check": {
            "name": "mean excess 3-bar return, larger-fall half minus smaller-fall half (median forecast split)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n, "larger-fall half": n_hi, "smaller-fall half": n_lo},
        "decided_by": decided,
        "reading": "Sunday bars are those whose UTC start is a Sunday; cases need forecast >= 2 and close[t+3] in the same window; the coin's mean 3-bar return uses the non-overlapping grid 0,3,6,... of each window pooled across windows; the larger-fall half is forecast strictly above the median and the smaller-fall half the rest.",
    }
