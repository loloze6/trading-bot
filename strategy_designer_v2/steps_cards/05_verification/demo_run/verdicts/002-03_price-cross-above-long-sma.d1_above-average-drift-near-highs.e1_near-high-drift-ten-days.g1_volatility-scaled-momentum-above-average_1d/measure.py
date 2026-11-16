import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    COMP = "vsr"

    def _component(df, comp, field="last_history_value"):
        col = f"debug_info.components.{comp}.{field}"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            def ext(v):
                try:
                    if isinstance(v, dict):
                        c = v.get(comp)
                        if isinstance(c, dict):
                            x = c.get(field)
                            return float(x) if x is not None else np.nan
                except Exception:
                    return np.nan
                return np.nan
            return df["debug_info.components"].apply(ext).astype(float)
        return pd.Series(np.nan, index=df.index)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            reg = df["regime"].astype(str).str.lower()
            vsr = _component(df, COMP)
            active = fc.notna() & (fc != 0)
            situation = (reg == "trending") & vsr.notna()
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("The 200-day condition is read from the recorded regime 'trending' (the detector's components are not "
               "recorded and the windows are too short to recompute a 200-day average), the situation is a trending bar "
               "with the vsr component recorded (graded, so any size counts) on the long side; the coin's mean 10-bar "
               "return is the mean over all grid bars of all its windows, the slope is an OLS slope with intercept, and "
               "the book's daily return is postRebalance_total_value bar to bar inside a window with the market part "
               "from the position held into that day.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "slope of excess 10-bar forward return on forecast, trending grid bars",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with timing gain > 0), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"trending grid cases": None},
            "decided_by": (f"Only {agreement:.1%} of active forecast bars are long on trending-regime bars with the "
                           "vsr momentum recorded, below the 90% the plan's situation requires."),
            "reading": reading,
        }

    # ---------- main measure ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).str.lower().values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({"coin": coin, "fwd": c1 / c0 - 1.0, "fc": fc[i],
                             "trend": reg[i] == "trending"})
    grid = pd.DataFrame(rows, columns=["coin", "fwd", "fc", "trend"])
    if len(grid):
        coin_mean = grid.groupby("coin")["fwd"].mean()
        grid["excess"] = grid["fwd"] - grid["coin"].map(coin_mean)
        tr = grid[grid["trend"]].dropna(subset=["excess", "fc"])
    else:
        tr = pd.DataFrame(columns=["excess", "fc"])
    n_cases = int(len(tr))

    slope = None
    t_val = None
    if n_cases >= 3 and np.nanstd(tr["fc"].values.astype(float)) > 0:
        lr = stats.linregress(tr["fc"].values.astype(float), tr["excess"].values.astype(float))
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_val = float(lr.slope / lr.stderr)

    # ---------- supporting check: timing gain ----------
    per_coin = []
    for coin, wins in bars.items():
        # coin's mean daily return over all windows
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            rets.append((c / c.shift(1) - 1.0).iloc[1:])
        mu = float(pd.concat(rets).dropna().mean()) if rets else np.nan
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.reset_index(drop=True).copy()
            d["day"] = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            d = d.groupby("day", sort=True).last().reset_index()
            if len(d) < 2:
                continue
            v = pd.to_numeric(d["postRebalance_total_value"], errors="coerce")
            pos = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce")
            book = (v / v.shift(1) - 1.0)
            mkt = pos.shift(1) * mu
            per_coin.append(pd.DataFrame({"day": d["day"].iloc[1:].values,
                                          "book": book.iloc[1:].values,
                                          "mkt": mkt.iloc[1:].values}))
    timing = None
    if per_coin:
        allc = pd.concat(per_coin).dropna(subset=["book", "mkt"])
        if len(allc):
            daily = allc.groupby("day")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    sup_pass = None if timing is None else bool(timing > 0)

    # ---------- decision ----------
    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} trending grid cases pooled across coins, below the plan's minimum of 100."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so it meets neither rule."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing gain is above 0 before costs."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is 0 or less, which the plan calls inconclusive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {"name": "slope of excess 10-bar forward return on forecast, trending grid bars",
                         "value": slope,
                         "statistic": None if t_val is None else {"name": "OLS slope t", "value": t_val},
                         "threshold": "t >= 2 confirms (with timing gain > 0), t <= -2 rejects"},
        "supporting_check": {"name": "book timing gain (mean daily return minus market part), before costs",
                             "value": timing, "passed": sup_pass},
        "counts": {"trending grid cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
