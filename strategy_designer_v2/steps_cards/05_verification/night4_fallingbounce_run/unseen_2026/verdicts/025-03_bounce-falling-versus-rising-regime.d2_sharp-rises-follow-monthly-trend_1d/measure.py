import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.month_move.last_history_value"
    PPV = "debug_info.components.month_move.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            r1 = close.pct_change(1)
            vol = r1.rolling(20, min_periods=20).std()
            day_rise = r1 / vol
            fc = df[FC].astype(float)
            raw = df[RAW].astype(float) if RAW in df.columns else pd.Series(np.nan, index=df.index)
            r30 = close / close.shift(30) - 1.0
            for i in range(len(df)):
                f = fc.iloc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                dr = day_rise.iloc[i]
                if np.isfinite(dr):
                    in_sit = dr >= 2.0 - 1e-9
                else:
                    # day_rise not computable inside the window: fall back on the detector's decision
                    in_sit = str(df["regime"].iloc[i]) == "trending"
                m = raw.iloc[i]
                if not np.isfinite(m):
                    m = r30.iloc[i]
                if np.isfinite(m) and m != 0:
                    side_ok = np.sign(f) == np.sign(m)
                else:
                    side_ok = False
                n_active += 1
                if in_sit and side_ok:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "t of the pooled slope of 5-day excess return on month_move forecast"
    threshold = "confirm: slope > 0 with t >= 2.0; reject: slope < 0 with t <= -2.0; at least 30 cases"
    reading = ("A case is the first bar in each 5-bar grid cell (positions 0,5,10,... from each window's first row) "
               "with regime 'trending' and non-zero forecast, its return taken from that bar's close over 5 bars inside the window; "
               "the coin's normal 5-day drift is the mean of its 5-bar returns at the grid positions over all windows; "
               "the slope's t is the ordinary OLS t; day_rise is recomputed as the 1-bar return over the 20-bar rolling std "
               "of 1-bar returns (current bar included), using the regime column where that std is not yet computable in the window; "
               "and a case count under 30 is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are bars with a 1-day rise of at least 2 usual daily moves "
                           "and a forecast signed like the 30-day return."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # normal drift: mean 5-bar return over grid positions of all windows
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = df[FC].astype(float).to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            ppv = df[PPV].astype(float).to_numpy() if PPV in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for start in range(0, n, H):
                for i in range(start, min(start + H, n)):
                    if reg[i] == "trending" and np.isfinite(fc[i]) and fc[i] != 0:
                        if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0 \
                                and np.isfinite(ppv[i]):
                            xs.append(ppv[i])
                            ys.append(c[i + H] / c[i] - 1.0 - drift)
                        break

    n_cases = len(xs)
    counts = {"cases": int(n_cases)}
    slope, tval = None, None
    if n_cases >= 3 and np.std(xs) > 0:
        res = stats.linregress(np.array(xs), np.array(ys))
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr > 0 else None

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 30 cases."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif slope > 0 and tval >= 2.0:
        status = "confirmed"
        decided = "The slope is positive with t >= 2.0 on at least 30 cases (confirm rule)."
    elif slope < 0 and tval <= -2.0:
        status = "rejected"
        decided = "The slope is negative with t <= -2.0 on at least 30 cases (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2.0 and 2.0 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": tval,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
