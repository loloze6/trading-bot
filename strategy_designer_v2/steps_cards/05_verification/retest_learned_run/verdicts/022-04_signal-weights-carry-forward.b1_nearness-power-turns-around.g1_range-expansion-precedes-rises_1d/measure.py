import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_ratio.last_history_value"
    POST = "debug_info.components.range_ratio.post_pipeline_value"
    OFF = "debug_info.components.offset.post_pipeline_value"
    STD_WIN = 60

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            raw = pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns else np.full(len(df), np.nan)
            post = pd.to_numeric(df[POST], errors="coerce").values if POST in df.columns else np.full(len(df), np.nan)
            off = pd.to_numeric(df[OFF], errors="coerce").values if OFF in df.columns else np.full(len(df), np.nan)
            for t in range(len(df)):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                # rebuild the standardised range ratio from raw values where a full past window is recorded
                x = np.nan
                if t >= STD_WIN and np.isfinite(raw[t]):
                    past = raw[t - STD_WIN:t]
                    if np.all(np.isfinite(past)):
                        m = np.mean(np.abs(past))
                        x = 0.0 if m == 0 else float(np.clip(raw[t] * 10.0 / m, -20, 20))
                if not np.isfinite(x):
                    x = post[t]
                o = off[t] if np.isfinite(off[t]) else -10.0
                n_active += 1
                if not np.isfinite(x):
                    continue
                expected = np.sign(x + o)  # long when range wider than usual, short when narrower
                if expected != 0 and np.sign(f) == expected:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of slope of 5-bar excess return on forecast (pooled, non-overlapping grid)"
    thr = "confirm if t >= 2 with timing > 0; reject if t <= -2; else inconclusive; at least 500 non-overlapping cases with non-zero forecast"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "The forecast's sign agrees with the plan's situation (long when today's range is wider than its usual size, short when narrower) on fewer than 90% of active bars.",
            "reading": "The expected side is the sign of the standardised range ratio (rebuilt from raw values where 60 past values are recorded, else its recorded post-pipeline value) plus the -10 offset.",
        }

    # ---------- 2. main measure ----------
    rows = []
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            for t in range(0, len(df), H):
                if t + H >= len(df):
                    break
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r) and np.isfinite(fc[t]):
                    rows.append((coin, r, fc[t]))
    samp = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(samp) > 0:
        samp["drift"] = samp.groupby("coin")["ret"].transform("mean")
        samp["excess"] = samp["ret"] - samp["drift"]
    n_cases = int(len(samp))
    n_nonzero = int((samp["fc"] != 0).sum()) if n_cases else 0

    slope = None
    t_slope = None
    if n_cases >= 3 and samp["fc"].nunique() > 1:
        lr = stats.linregress(samp["fc"].values, samp["excess"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    # ---------- 3. supporting check: timing ----------
    gains = []
    for coin in sorted(bars):
        coin_rets = []
        per_w = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values
            ts = df["timestamp"].values
            for t in range(1, len(df)):
                r = close[t] / close[t - 1] - 1.0
                if np.isfinite(r):
                    coin_rets.append(r)
                    per_w.append((w, ts[t], alloc[t - 1], r))
        if not coin_rets:
            continue
        mu = float(np.mean(coin_rets))
        for w, ts_, a, r in per_w:
            if np.isfinite(a):
                gains.append((w, ts_, a * r, a * mu))
    timing = None
    sup_pass = None
    if gains:
        g = pd.DataFrame(gains, columns=["w", "ts", "gross", "market"])
        daily = g.groupby(["w", "ts"])[["gross", "market"]].mean()
        total = float(daily["gross"].mean())
        market = float(daily["market"].mean())
        timing = total - market
        sup_pass = bool(timing > 0)

    # ---------- 4. decision ----------
    if n_nonzero < 500:
        status = "not observable"
        decided = f"Only {n_nonzero} non-overlapping cases with a non-zero forecast, below the plan's minimum of 500."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and timing is above 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but timing is at or below 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "book timing (mean daily gain before costs minus market-rise part)",
            "value": timing,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping cases with a non-zero forecast": n_nonzero,
            "non-overlapping cases": n_cases,
        },
        "decided_by": decided,
        "reading": "The regression uses every grid bar (forecast zero included) with a complete 5-bar return inside its window, the drift is each coin's mean grid 5-bar return over all windows, the book before costs is position held x next-bar coin return averaged over coins per day, and the plan's 'fewer than 500 cases' minimum is applied as 'not observable'.",
    }
