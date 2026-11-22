import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.hpmom.last_history_value"
    PPV = "debug_info.components.hpmom.post_pipeline_value"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        return d

    data = {c: {w: prep(df) for w, df in wins.items()} for c, wins in bars.items()}

    # ---------- 1. situation check ----------
    # Situation: the 30-day return, signed; expected side = its sign (continuation:
    # a larger return -> a larger rise, so a rise -> long, a fall -> short).
    n_active = 0
    n_agree = 0
    for c, wins in data.items():
        for w, d in wins.items():
            close = d["close"].astype(float)
            ret30 = close / close.shift(30) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # the component is the 30-bar return times a positive nearness weight:
            # its sign is the 30-bar return's sign; where it is not recorded, use the prices
            expected = np.sign(raw).where(raw.notna(), np.sign(ret30))
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            ok = active & expected.notna() & (expected != 0) & (np.sign(fc) == expected)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope t of 5-bar excess forward return on post_pipeline_value, pooled"
    thr = "confirm: t >= +2.0 with timing gain > 0; reject: t <= -2.0; at least 300 grid cases with non-zero forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of the active bars have a forecast whose sign is that of the "
                          "30-day return (the continuation side the Fidelity states).",
            "reading": "Expected side taken as the sign of the raw component (30-bar return times a positive "
                       "weight), from the 30-bar price return where the raw value is missing.",
        }

    # ---------- 2. main measure ----------
    rows = []
    for c, wins in data.items():
        for w, d in wins.items():
            close = d["close"].astype(float).values
            ppv = pd.to_numeric(d[PPV], errors="coerce").values if PPV in d.columns else np.full(len(d), np.nan)
            for i in range(0, len(d), H):
                if i + H < len(d):
                    rows.append((c, close[i + H] / close[i] - 1.0, ppv[i]))
    g = pd.DataFrame(rows, columns=["coin", "fwd", "x"])
    g = g[np.isfinite(g["fwd"])]
    drift = g.groupby("coin")["fwd"].mean()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    reg = g[np.isfinite(g["x"]) & np.isfinite(g["ex"])]
    n_grid = int(len(reg))
    n_nonzero = int((reg["x"] != 0).sum())

    slope = None
    t = None
    if n_grid >= 3 and reg["x"].nunique() > 1:
        lr = stats.linregress(reg["x"].values, reg["ex"].values)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    # ---------- supporting check: timing gain ----------
    coin_mean = {}
    for c, wins in data.items():
        rs = []
        for w, d in wins.items():
            dd = d.groupby(d["timestamp"].dt.floor("D")).last()
            cl = dd["close"].astype(float)
            rs.append((cl / cl.shift(1) - 1.0).dropna())
        allr = pd.concat(rs) if rs else pd.Series(dtype=float)
        coin_mean[c] = float(allr.mean()) if len(allr) else np.nan

    timing_days = []
    windows = sorted({w for wins in data.values() for w in wins})
    for w in windows:
        book_parts, mkt_parts = [], []
        for c, wins in data.items():
            if w not in wins:
                continue
            d = wins[w]
            dd = d.groupby(d["timestamp"].dt.floor("D")).last()
            v = pd.to_numeric(dd["postRebalance_total_value"], errors="coerce")
            pos = pd.to_numeric(dd["postRebalance_current_allocation"], errors="coerce")
            book_parts.append((v / v.shift(1) - 1.0).rename(c))
            mkt_parts.append((pos.shift(1) * coin_mean[c]).rename(c))
        if not book_parts:
            continue
        B = pd.concat(book_parts, axis=1)
        M = pd.concat(mkt_parts, axis=1)
        T = (B - M)
        T = T.where(B.notna() & M.notna())
        day = T.mean(axis=1, skipna=True).dropna()
        timing_days.extend(day.values.tolist())
    timing = float(np.mean(timing_days)) if timing_days else None
    sup_pass = (timing > 0) if timing is not None else None

    counts = {"grid cases with a non-zero forecast": n_nonzero, "grid cases in regression": n_grid,
              "book days": len(timing_days)}

    if n_nonzero < 300:
        status = "not observable"
        decided = f"Only {n_nonzero} grid cases with a non-zero forecast, fewer than the 300 the plan requires."
    elif t is None:
        status = "inconclusive"
        decided = "The slope t could not be computed."
    elif t >= 2.0 and sup_pass:
        status = "confirmed"
        decided = "Slope t is +2.0 or more and the mean daily timing gain is above 0."
    elif t <= -2.0:
        status = "rejected"
        decided = "Slope t is -2.0 or less."
    elif t >= 2.0:
        status = "inconclusive"
        decided = "Slope t is +2.0 or more but the timing gain is 0 or less."
    else:
        status = "inconclusive"
        decided = "Slope t is between -2.0 and +2.0."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean daily timing gain of the book", "value": timing,
                             "passed": (bool(sup_pass) if sup_pass is not None else None)},
        "counts": counts,
        "decided_by": decided,
        "reading": "Expected side = sign of the 30-day return (raw component sign); the regression uses all grid "
                   "bars (zero forecasts included) with the coin's drift as the mean 5-bar grid return over all its "
                   "windows; 'non-zero forecast' counted on post_pipeline_value; book daily returns from "
                   "postRebalance_total_value with the previous day's position for the market part; a minimum count "
                   "not reached is reported as 'not observable'.",
    }
