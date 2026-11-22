import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.upday.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce")
            # 90-day return from prices inside the window where computable,
            # else the detector's own recorded decision (regime 'trending' = ret90 >= 0)
            ret90 = close / close.shift(90) - 1.0
            regime_ok = df["regime"].astype(str) == "trending"
            trend_ok = np.where(ret90.notna(), ret90 >= 0.0, regime_ok)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            upday = (raw > 0).fillna(False).values
            active = (fc.notna() & (fc != 0)).values
            situ_long = trend_ok & upday & (fc > 0).fillna(False).values
            n_active += int(active.sum())
            n_agree += int((active & situ_long).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("The 90-day return is recomputed from closes inside each window where 90 prior bars exist, "
               "otherwise the recorded regime 'trending' (the detector's ret90 >= 0 decision) is used; the up-day is "
               "last_history_value > 0; the coin's mean 5-bar return is the mean over all grid cells of all its windows; "
               "the slope and t come from ordinary least squares of excess return on forecast over all pooled cells with forecast > 0; "
               "with no cell at forecast 5 or more the supporting check counts as failed.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on an up-day "
                           "(positive scaled one-day return) with a 90-day return at or above 0, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                rows.append((coin, fc[i], r))
    g = pd.DataFrame(rows, columns=["coin", "fc", "ret"])
    if len(g):
        coin_mean = g.groupby("coin")["ret"].mean()
        g["exc"] = g["ret"] - g["coin"].map(coin_mean)
    else:
        g["exc"] = []

    pos = g[(g["fc"].notna()) & (g["fc"] > 0)]
    n_pos = int(len(pos))
    big = g[(g["fc"].notna()) & (g["fc"] >= 5)]
    n_big = int(len(big))

    slope = None
    tval = None
    if n_pos >= 3 and pos["fc"].nunique() > 1:
        lr = stats.linregress(pos["fc"].values.astype(float), pos["exc"].values.astype(float))
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = float(big["exc"].mean()) if n_big > 0 else None
    sup_pass = bool(sup_val is not None and sup_val > 0)

    counts = {"grid cells with forecast above 0": n_pos,
              "grid cells with forecast 5 or more": n_big}

    if n_pos < 30:
        status = "not observable"
        decided = f"Only {n_pos} grid cells with forecast above 0, fewer than the 30 the plan requires."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess 5-bar return on cells with forecast 5 or more is above 0, with at least 30 cells."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less, with at least 30 grid cells with forecast above 0."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of excess 5-bar forward return on forecast, cells with forecast > 0, coins pooled",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": "confirm if t >= 2 (with the supporting check), reject if t <= -2, at least 30 cells with forecast above 0",
        },
        "supporting_check": {
            "name": "mean excess 5-bar return on cells with forecast >= 5 above 0",
            "value": sup_val,
            "passed": sup_pass if sup_val is not None else False,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
