import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RET_P = 30
    RAW = "debug_info.components.hp_mom.last_history_value"
    MIN_NONZERO = 200

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # expected side = sign of the 30-day return (raw component value keeps that sign)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            ret30 = close / close.shift(RET_P) - 1.0
            side = np.sign(raw)
            side = side.where(raw.notna(), np.sign(ret30))
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & side.notna() & (side != 0) & (np.sign(fc) == side)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars have a forecast whose sign matches the sign of the "
                          "coin's 30-day return (long when up, short when down), as the Fidelity's situation requires.",
            "reading": "The expected side is the sign of the 30-day return, read from the component's raw value "
                       "(recomputed from closes where it is missing).",
        }

    # ---------- 2. main measure: grid regression ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    c0, c1 = close[i], close[i + H]
                    if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                        rows.append((coin, c1 / c0 - 1.0, fc[i]))
    grid = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(grid):
        grid["mu"] = grid.groupby("coin")["ret"].transform("mean")
        grid["ex"] = grid["ret"] - grid["mu"]
        g = grid.dropna(subset=["ex", "fc"])
    else:
        g = grid
    n_cases = int(len(g))
    n_nonzero = int((g["fc"] != 0).sum()) if n_cases else 0

    slope = None
    tval = None
    if n_cases >= 3 and g["fc"].nunique() > 1:
        lr = stats.linregress(g["fc"].values, g["ex"].values)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. supporting check: book timing gain before costs ----------
    per_coin = []
    coin_daily = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            rets.append((close / close.shift(1) - 1.0).iloc[1:])
        allr = pd.concat(rets).dropna() if rets else pd.Series(dtype=float)
        coin_daily[coin] = float(allr.mean()) if len(allr) else np.nan
    for coin, wins in bars.items():
        mu = coin_daily[coin]
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").shift(1)
            r = close / close.shift(1) - 1.0
            timing = pos * r - pos * mu
            d = pd.DataFrame({"day": pd.to_datetime(df["timestamp"], utc=True).dt.floor("D"),
                              "x": timing})
            d = d.iloc[1:].dropna()
            d = d.groupby("day")["x"].sum().reset_index()
            per_coin.append(d)
    if per_coin:
        allp = pd.concat(per_coin)
        daily = allp.groupby("day")["x"].mean()
        check_val = float(daily.mean()) if len(daily) else None
    else:
        check_val = None
    check_pass = None if check_val is None else bool(check_val > 0)

    # ---------- 4. decision ----------
    if n_nonzero < MIN_NONZERO:
        status = "not observable"
        decided = f"Only {n_nonzero} grid cases have a non-zero forecast, below the plan's minimum of 200."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and slope > 0:
        if check_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the book's timing gain before costs is above 0."
        else:
            status = "inconclusive"
            decided = "The slope has t >= 2 but the supporting check is at or below 0, which the plan calls inconclusive."
    elif tval <= -2 and slope < 0:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "OLS slope of demeaned 5-day grid return on forecast",
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": "confirm: slope > 0 with t >= 2 and check > 0; reject: slope < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "book mean daily return before costs minus position x coin mean daily return",
            "value": check_val,
            "passed": check_pass,
        },
        "counts": {
            "grid cases with a non-zero forecast": n_nonzero,
            "grid cases": n_cases,
        },
        "decided_by": decided,
        "reading": "The regression uses all grid cases (zero forecasts included) with an intercept and the ordinary "
                   "OLS slope t, the coin's mean 5-day return is the mean of its grid returns over all its windows, "
                   "the check's before-cost book uses the held position times the next bar's close-to-close return, "
                   "averaged over coins each day, and the minimum of 200 non-zero cases is applied as 'not observable'.",
    }
