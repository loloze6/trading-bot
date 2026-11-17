import json
import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    COMP = "stall"
    HORIZON = 30
    MIN_CASES = 30
    PERIOD = 365

    def comp_series(df, cid, field):
        flat = f"debug_info.components.{cid}.{field}"
        if flat in df.columns:
            return pd.to_numeric(df[flat], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                val = np.nan
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(cid)
                    if isinstance(c, dict):
                        x = c.get(field)
                        try:
                            val = float(x) if x is not None else np.nan
                        except Exception:
                            val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            # price-based necessary condition: the close must exceed every earlier
            # in-window close within the prior 365 bars (the prior 365-bar high is at least that)
            price_ok = np.ones(len(df), dtype=bool)
            for i in range(1, len(df)):
                lo = max(0, i - PERIOD)
                prior = close[lo:i]
                prior = prior[~np.isnan(prior)]
                if len(prior) and not np.isnan(close[i]) and close[i] <= prior.max():
                    price_ok[i] = False
            situation = (reg == "trending") & price_ok
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else (agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "OLS slope of excess 30-bar forward return on stall post_pipeline_value",
                             "value": None, "statistic": None,
                             "threshold": "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {},
            "decided_by": "Fewer than 90% of active bars are long bars where the close is above the prior 365-day closing high (trending regime), as the plan's Fidelity requires.",
            "reading": "Situation taken as regime 'trending' (the detector's close > prior 365-close-high rule) plus the in-window price check that the close exceeds all earlier in-window closes of the prior 365 bars; side long.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            reg = df["regime"].astype(str).values
            stall = comp_series(df, COMP, "post_pipeline_value").values
            n = len(df)
            for t in range(0, n, HORIZON):
                if t + HORIZON >= n:
                    continue
                c0, c1 = close[t], close[t + HORIZON]
                if np.isnan(c0) or np.isnan(c1) or c0 == 0:
                    continue
                rows.append({"coin": coin, "ret": c1 / c0 - 1.0,
                             "trending": reg[t] == "trending", "x": stall[t]})

    grid = pd.DataFrame(rows, columns=["coin", "ret", "trending", "x"])
    if len(grid):
        coin_mean = grid.groupby("coin")["ret"].mean()
        grid["excess"] = grid["ret"] - grid["coin"].map(coin_mean)
        sample = grid[grid["trending"] & grid["x"].notna() & grid["excess"].notna()]
    else:
        sample = grid
    n_cases = int(len(sample))

    main = {"name": "OLS slope of excess 30-bar forward return on stall post_pipeline_value",
            "value": None, "statistic": None,
            "threshold": "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; on at least 30 cases"}
    counts = {"trending grid bars": n_cases}
    reading = ("Situation taken as regime 'trending' plus an in-window price check, side long; the coin mean "
               "is over all its complete grid bars in all windows (trending or not); grid bars without a full "
               "30-bar forward return inside the window or without a recorded stall value are left out; the "
               "slope's t is the ordinary OLS t pooled across coins.")

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
            "main_measure": main,
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_cases} trending grid bars, fewer than the plan's minimum of 30 cases.",
            "reading": reading,
        }

    x = sample["x"].values.astype(float)
    y = sample["excess"].values.astype(float)
    if np.allclose(x, x[0]):
        main["value"] = None
        return {
            "status": "inconclusive",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
            "main_measure": main,
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The stall value does not vary over the sample, so no slope or t can be estimated; neither confirm nor reject is met.",
            "reading": reading,
        }

    lr = stats.linregress(x, y)
    slope = float(lr.slope)
    tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else float("nan")
    main["value"] = slope
    main["statistic"] = {"name": "OLS slope t", "value": tval}

    if slope > 0 and tval >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {tval:.2f} >= 2 on {n_cases} cases (confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {tval:.2f} <= -2 on {n_cases} cases (reject rule)."
    else:
        status = "inconclusive"
        decided = f"t = {tval:.2f} lies between -2 and 2 on {n_cases} cases (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
