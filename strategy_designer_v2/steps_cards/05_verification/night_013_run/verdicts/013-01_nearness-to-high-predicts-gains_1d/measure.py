import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 30
    MIN_CASES = 300
    FC = "forecast"
    CL_RAW = "debug_info.components.closeness.last_history_value"
    CL_POST = "debug_info.components.closeness.post_pipeline_value"
    OF_POST = "debug_info.components.offset.post_pipeline_value"
    ALLOC = "postRebalance_current_allocation"

    def _standardise(raw, window=364, min_periods=91):
        # value(t) * 10 / mean(|last `window` raw values|, bar t left out), capped; 0 before min_periods
        raw = pd.Series(raw, dtype=float).reset_index(drop=True)
        out = np.zeros(len(raw))
        vals = raw.values
        for i in range(len(vals)):
            past = vals[max(0, i - window):i]
            past = past[~np.isnan(past)]
            if len(past) < min_periods or np.isnan(vals[i]):
                out[i] = 0.0 if not np.isnan(vals[i]) else np.nan
                continue
            m = np.mean(np.abs(past))
            out[i] = 0.0 if m == 0 else float(np.clip(vals[i] * 10.0 / m, -20, 20))
        return out

    # ---------------- 1. Situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if FC not in df.columns:
                continue
            fc = pd.to_numeric(df[FC], errors="coerce").values
            if CL_POST in df.columns and OF_POST in df.columns:
                x = pd.to_numeric(df[CL_POST], errors="coerce").values
                off = pd.to_numeric(df[OF_POST], errors="coerce").values
            elif CL_RAW in df.columns:
                x = _standardise(pd.to_numeric(df[CL_RAW], errors="coerce").values)
                off = np.full(len(df), 10.0)
            else:
                x = np.full(len(df), np.nan)
                off = np.full(len(df), np.nan)
            raw = (pd.to_numeric(df[CL_RAW], errors="coerce").values
                   if CL_RAW in df.columns else np.full(len(df), np.nan))
            expected = (1.0 * x + 1.0 * off) / 2.0
            for i in range(len(df)):
                if np.isnan(fc[i]) or fc[i] == 0:
                    continue
                n_active += 1
                # situation: the close sits at or below its 364-bar high (distance <= 0), graded on every bar
                in_situation = (not np.isnan(raw[i])) and raw[i] <= 1e-12
                exp_sign = np.sign(expected[i]) if not np.isnan(expected[i]) else 0.0
                if in_situation and exp_sign != 0 and exp_sign == np.sign(fc[i]):
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "pooled slope of demeaned 30-bar forward return on forecast"
    thr = "t >= 2 confirms (with timing gain > 0); t <= -2 rejects; otherwise inconclusive; >= 300 non-overlapping cases"
    reading = ("Coin's mean 30-bar return taken as the mean of that coin's non-overlapping 30-bar samples over all its "
               "windows; slope is OLS with intercept on pooled samples at positions 0,30,60,90 with t+30 inside the "
               "window; timing gain uses position x next-bar return averaged across coins per date; the forecast's "
               "expected sign is rebuilt as the equal-weight mean of the components' post-pipeline values, since the "
               "364-bar standardisation history is not in the record.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"non-overlapping 30-bar cases": 0},
            "decided_by": ("Fewer than 90% of active bars have a forecast whose sign matches the plan's side "
                           "(long when nearer the 364-bar high than usual, short when farther)."),
            "reading": reading,
        }

    # ---------------- 2. Main measure ----------------
    samples = []  # (coin, forecast, ret)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            for t in range(0, len(df), H):
                if t + H >= len(df):
                    break
                if np.isnan(close[t]) or np.isnan(close[t + H]) or np.isnan(fc[t]) or close[t] == 0:
                    continue
                samples.append((coin, float(fc[t]), close[t + H] / close[t] - 1.0))
    sdf = pd.DataFrame(samples, columns=["coin", "f", "r"])
    n_cases = int(len(sdf))
    slope = None
    tstat = None
    if n_cases >= 3:
        sdf["rd"] = sdf["r"] - sdf.groupby("coin")["r"].transform("mean")
        if sdf["f"].std() > 0:
            lr = stats.linregress(sdf["f"].values, sdf["rd"].values)
            slope = float(lr.slope)
            tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------------- 3. Supporting check: timing gain ----------------
    rows = []
    coin_mu = {}
    per_coin = {}
    for coin, wins in bars.items():
        allr = []
        parts = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            alloc = pd.to_numeric(df[ALLOC], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for t in range(len(df) - 1):
                if np.isnan(close[t]) or np.isnan(close[t + 1]) or close[t] == 0:
                    continue
                r = close[t + 1] / close[t] - 1.0
                allr.append(r)
                if not np.isnan(alloc[t]):
                    parts.append((ts.iloc[t].floor("D"), alloc[t], r))
        coin_mu[coin] = float(np.mean(allr)) if allr else np.nan
        per_coin[coin] = parts
    for coin, parts in per_coin.items():
        mu = coin_mu[coin]
        for d, a, r in parts:
            rows.append((d, coin, a * r, a * mu))
    timing = None
    if rows:
        bdf = pd.DataFrame(rows, columns=["day", "coin", "book", "mkt"])
        bdf = bdf.dropna()
        daily = bdf.groupby("day")[["book", "mkt"]].mean()
        timing = float(daily["book"].mean() - daily["mkt"].mean())
    sup_pass = None if timing is None else bool(timing > 0)

    # ---------------- 4. Decision ----------------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping 30-bar cases, below the plan's minimum of 300."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing gain is above zero."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: closer to the high is followed by lower returns than usual."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is zero or below."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": thr,
        },
        "supporting_check": {"name": "book timing gain (mean daily, before costs)", "value": timing, "passed": sup_pass},
        "counts": {"non-overlapping 30-bar cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
