import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    THR = 10.0
    MIN_CASES = 30
    RET20 = "debug_info.components.ret20.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if not active.any():
                continue
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            sit = reg.eq("trending")
            if RET20 in df.columns:
                r20 = pd.to_numeric(df[RET20], errors="coerce")
                # where the raw 20-day return is recorded, it must be above 0
                sit = sit & (r20.isna() | (r20 > 0))
            ok = active & sit & (f > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {
                "name": "mean excess 5-bar return after forecast >= 10",
                "value": None, "statistic": None,
                "threshold": "positive with t >= 2 confirms; negative with t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"non-overlapping cases at forecast >= 10": 0},
            "decided_by": "No active bars in the record, so fewer than 30 non-overlapping cases at forecast >= 10.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are bars of the plan's situation "
                           "(regime 'trending': 20- and 60-day returns above 0 and volatility "
                           "percentile >= 0.5) on the long side."),
            "reading": "Situation checked on the 'regime' column (detector not recorded), plus ret20 > 0 where recorded.",
        }

    # ---------- 2. Criterion ----------
    # Non-overlapping grid: positions 0,5,10,... of each window
    rows = []  # (coin, fwd_ret, forecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, f[i]))
    data = pd.DataFrame(rows, columns=["coin", "ret", "forecast"])

    if len(data):
        coin_mean = data.groupby("coin")["ret"].mean()
        data["excess"] = data["ret"] - data["coin"].map(coin_mean)
    else:
        data["excess"] = []

    strong = data[data["forecast"].notna() & (data["forecast"] >= THR)]
    n_cases = int(len(strong))

    mean_ex = float(strong["excess"].mean()) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = strong["excess"].std(ddof=1)
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_cases)))

    # Supporting check: slope of excess on forecast across active bars (non-overlapping)
    act = data[data["forecast"].notna() & (data["forecast"] != 0)]
    slope = None
    sup_passed = None
    if len(act) >= 3 and act["forecast"].nunique() > 1:
        lr = stats.linregress(act["forecast"].to_numpy(float), act["excess"].to_numpy(float))
        slope = float(lr.slope)
        sup_passed = bool(slope > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases at forecast >= 10, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so no rule is met: inconclusive."
    elif mean_ex > 0 and t_val >= 2:
        status = "confirmed"
        decided = "Mean excess 5-bar return after forecast >= 10 is positive with t >= 2 (confirm rule)."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean excess 5-bar return after forecast >= 10 is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t-statistic is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean excess 5-bar return after forecast >= 10 (vs coin mean)",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": "positive with t >= 2 confirms; negative with t <= -2 rejects; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "slope of excess 5-bar return on forecast, active bars, non-overlapping",
            "value": slope,
            "passed": sup_passed,
        },
        "counts": {"non-overlapping cases at forecast >= 10": n_cases},
        "decided_by": decided,
        "reading": ("Situation checked on the 'regime' column (detector components not recorded) plus ret20 > 0 "
                    "where recorded; cases and the coin's mean 5-bar return both use the non-overlapping grid "
                    "(positions 0,5,10,... of each window) pooled over all windows; the supporting check is "
                    "reported but does not change the status."),
    }
