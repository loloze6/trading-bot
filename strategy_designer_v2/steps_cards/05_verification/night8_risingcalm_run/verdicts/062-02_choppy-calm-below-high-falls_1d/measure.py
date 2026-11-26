import numpy as np
import pandas as pd
from scipy import stats

RAW = "debug_info.components.drop_from_high.last_history_value"
H = 5


def _recompute_raw(close):
    # (close - highest close of last 5 bars incl. t) / that high / std of last 30 daily returns
    hi = close.rolling(5, min_periods=5).max()
    ret = close.pct_change()
    sd = ret.rolling(30, min_periods=30).std()
    return (close - hi) / hi / sd


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), _recompute_raw(close))
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: close below its 5-day high (raw < 0); expected side: short
            agree = active & (raw < 0) & (fc < 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of 5-bar excess forward return on forecast, day-pooled"
    threshold = "confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct days of grid cases with non-zero forecast": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the close sits below "
                           "its 5-day high with a short forecast, so the config does not do what the Fidelity says."),
            "reading": "Situation taken as raw drop_from_high < 0 (recomputed from prices where missing), side short.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                coin_rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].floor("D"),
                    "fwd": c1 / c0 - 1.0,
                    "forecast": fc[i],
                })
        if not coin_rows:
            continue
        cdf = pd.DataFrame(coin_rows)
        drift = cdf["fwd"].mean()  # coin's mean 5-bar return over all windows (grid)
        cdf["excess"] = cdf["fwd"] - drift
        rows.append(cdf)

    if rows:
        g = pd.concat(rows, ignore_index=True)
        g = g[g["forecast"].notna() & (g["forecast"] != 0)]
    else:
        g = pd.DataFrame(columns=["coin", "day", "fwd", "forecast", "excess"])

    n_cases = int(len(g))
    daily = g.groupby("day")[["forecast", "excess"]].mean() if n_cases else pd.DataFrame(columns=["forecast", "excess"])
    n_days = int(len(daily))

    slope = None
    t = None
    if n_days >= 3 and daily["forecast"].nunique() > 1:
        res = stats.linregress(daily["forecast"].values.astype(float), daily["excess"].values.astype(float))
        slope = float(res.slope)
        t = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    deep = g[g["forecast"] <= -10]
    n_deep = int(len(deep))
    deep_mean = float(deep["excess"].mean()) if n_deep > 0 else None
    check_pass = (deep_mean < 0) if deep_mean is not None else None

    counts = {
        "distinct days of grid cases with non-zero forecast": n_days,
        "grid cases with non-zero forecast": n_cases,
        "grid cases with forecast <= -10": n_deep,
    }

    if n_days < 50:
        status = "not observable"
        decided_by = f"Only {n_days} distinct days of grid cases with a non-zero forecast, below the plan's minimum of 50."
    elif slope is None or t is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2 and check_pass is True:
        status = "confirmed"
        decided_by = "The slope is positive with t >= 2 and grid bars with forecast <= -10 have a negative mean excess return."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2: deeper drops are followed by rebounds beyond drift."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided_by = "The slope is positive with t >= 2 but the supporting check fails, which the plan rules inconclusive."
    else:
        status = "inconclusive"
        decided_by = "The slope's |t| is below 2, which the plan rules inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS t of slope on day cases", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 5-bar return on grid bars with forecast <= -10 below 0",
            "value": deep_mean,
            "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Day pooling is read as averaging the forecast and excess return of the grid cases sharing a UTC day "
                    "into one case and regressing those day means by OLS (t on n_days-2 df), the drift is each coin's mean "
                    "5-bar return over all grid bars of all its windows, the supporting check is the plain mean over grid "
                    "bars, and the plan's 50-day minimum, when unmet, gives 'not observable' per the workflow."),
    }
