import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    COMP = "debug_info.components.fall20.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            if COMP in df.columns:
                raw = pd.to_numeric(df[COMP], errors="coerce")
                # situation: the coin has fallen over 20 days (raw 20-bar change < 0); side: long
                sit = raw.notna() & (raw < 0)
                n_agree += int((active & sit & (fc > 0)).sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {
                "name": "mean excess forward 20-bar return after top-decile positive forecasts",
                "value": None, "statistic": None,
                "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2",
            },
            "supporting_check": None,
            "counts": {"non-overlapping top-decile episodes": 0},
            "decided_by": "No bar has a nonzero forecast, so the minimum of 30 non-overlapping top-decile episodes is not reached.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {
                "name": "mean excess forward 20-bar return after top-decile positive forecasts",
                "value": None, "statistic": None,
                "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2",
            },
            "supporting_check": None,
            "counts": {},
            "decided_by": (f"Only {agreement:.1%} of active bars are long bars where the coin's raw 20-bar change "
                           "is negative, below the 90% needed: the config's long positions do not follow the plan's 20-day fall."),
            "reading": "The situation is taken as a negative raw 20-bar change of the fall20 component, on the long side.",
        }

    # ---------- 2. Build pooled rows ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or "close" not in df.columns:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            pos = np.arange(n)
            rows.append(pd.DataFrame({
                "coin": coin, "window": w, "pos": pos,
                "forecast": fc, "fwd": fwd, "grid": (pos % H) == 0,
            }))
    if not rows:
        allr = pd.DataFrame(columns=["coin", "window", "pos", "forecast", "fwd", "grid"])
    else:
        allr = pd.concat(rows, ignore_index=True)

    # coin's mean 20-bar return over all test windows together (all bars, within-window returns)
    coin_mean = allr.dropna(subset=["fwd"]).groupby("coin")["fwd"].mean()
    allr["excess"] = allr["fwd"] - allr["coin"].map(coin_mean)

    posf = allr[allr["forecast"] > 0]
    if len(posf) > 0:
        q90 = float(np.quantile(posf["forecast"].to_numpy(dtype=float), 0.9))
        top = posf[posf["forecast"] >= q90]
    else:
        q90 = None
        top = posf

    ep = top[top["grid"]].dropna(subset=["excess"])
    n_ep = int(len(ep))
    vals = ep["excess"].to_numpy(dtype=float)
    mean_ex = float(np.mean(vals)) if n_ep > 0 else None
    if n_ep >= 2:
        sd = float(np.std(vals, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n_ep))) if sd > 0 else None
    else:
        t = None

    # supporting check: slope of excess fwd return on forecast across all nonzero-forecast bars
    nz = allr[(allr["forecast"] != 0)].dropna(subset=["forecast", "excess"])
    slope = None
    if len(nz) >= 3 and np.ptp(nz["forecast"].to_numpy(dtype=float)) > 0:
        slope = float(stats.linregress(nz["forecast"].to_numpy(dtype=float),
                                       nz["excess"].to_numpy(dtype=float)).slope)
    sup_pass = None if slope is None else bool(slope > 0)

    # ---------- 3. Decision ----------
    if n_ep < 30:
        status = "not observable"
        decided = f"Only {n_ep} non-overlapping 20-bar top-decile episodes, below the plan's minimum of 30."
    elif t is not None and mean_ex > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean excess forward return after top-decile forecasts is positive with t >= 2."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "The mean excess forward return after top-decile forecasts is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "With at least 30 episodes, the t of the mean excess forward return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean excess forward 20-bar return after top-decile positive forecasts",
            "value": mean_ex,
            "statistic": None if t is None else {"name": "t of the mean (non-overlapping episodes)", "value": t},
            "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "slope of excess forward 20-bar return on forecast, nonzero-forecast bars",
            "value": slope, "passed": sup_pass,
        },
        "counts": {"non-overlapping top-decile episodes": n_ep},
        "decided_by": decided,
        "reading": ("The situation is a negative raw 20-bar change on the long side; the top decile is forecasts at or "
                    "above the pooled 90th percentile of all positive forecasts, episodes are top-decile bars at "
                    "positions 0, 20, 40, ... of each window, the coin's mean is over all its within-window 20-bar "
                    "returns, and the supporting slope uses all nonzero-forecast bars by OLS."),
    }
