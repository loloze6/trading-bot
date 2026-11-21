import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_CASES = 300
    comps = {
        "mom28": 60,
        "near_high90": 90,
        "offset": 60,
    }
    weights = {"mom28": 1.0, "near_high90": 1.0, "offset": 1.0}

    def col_raw(cid):
        return f"debug_info.components.{cid}.last_history_value"

    def col_post(cid):
        return f"debug_info.components.{cid}.post_pipeline_value"

    def rebuild_standardised(df, cid, window):
        # standardise: x * 10 / mean(|x| over the last `window` raw values, bar t left out), capped at +-20.
        # Exact only when `window` past raw values are recorded in this window; otherwise use the recorded value.
        n = len(df)
        rc, pc = col_raw(cid), col_post(cid)
        raw = pd.to_numeric(df[rc], errors="coerce") if rc in df.columns else pd.Series(np.nan, index=df.index)
        post = pd.to_numeric(df[pc], errors="coerce") if pc in df.columns else pd.Series(np.nan, index=df.index)
        absprev = raw.abs().shift(1)
        denom = absprev.rolling(window, min_periods=window).mean()
        val = raw * 10.0 / denom
        val = val.where(denom != 0, 0.0)
        val = val.clip(-20, 20)
        val = val.where(denom.notna() & raw.notna(), post)
        return val.values.astype(float)

    # ---------- 1. situation check ----------
    agree, active = 0, 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0 or "forecast" not in df.columns:
                continue
            total = np.zeros(len(df))
            ok = np.ones(len(df), dtype=bool)
            for cid, win in comps.items():
                v = rebuild_standardised(df, cid, win)
                ok &= ~np.isnan(v)
                total = total + weights[cid] * np.nan_to_num(v)
            score = np.clip(total / sum(weights.values()), -20, 20)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            act = (~np.isnan(fc)) & (fc != 0)
            active += int(act.sum())
            match = act & ok & (np.sign(score) == np.sign(fc)) & (score != 0)
            agree += int(match.sum())
    agreement = float(agree / active) if active > 0 else 0.0
    passed = active > 0 and agreement >= 0.9

    main_name = "slope of next 10-bar return minus coin drift on forecast (non-overlapping grid, pooled)"
    threshold = "confirm: t >= 2 with timing gain > 0; reject: t <= -2; at least 300 non-overlapping cases"
    reading = ("Every bar is a bar of the graded situation, its expected side being the sign of the sum rebuilt "
               "from the raw components with the engine's standardise (recorded post-pipeline values where fewer "
               "than a full window of past raw values is recorded); the regression is OLS with intercept over all "
               "grid bars with a forecast and a full 10-bar return; the drift is the coin's mean grid 10-bar return; "
               "the timing gain is the mean over days of the coins' mean of position x (daily return minus the coin's "
               "mean daily return), before costs; fewer than 300 cases gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active), "non-overlapping cases": None},
            "decided_by": (f"Only {agreement:.1%} of the active bars have a forecast whose sign matches the sign of "
                           "the plan's sum (28-bar momentum plus nearness to the 90-bar high, centred by +10), "
                           "below the 90% required."),
            "reading": reading,
        }

    # ---------- 2. main measure ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            for t in range(0, len(df), H):
                if t + H < len(df):
                    r = c[t + H] / c[t] - 1
                    rows.append((coin, f[t], r))
    g = pd.DataFrame(rows, columns=["coin", "f", "r"])
    g = g.replace([np.inf, -np.inf], np.nan)
    drift = g.dropna(subset=["r"]).groupby("coin")["r"].mean()
    g = g.dropna(subset=["f", "r"])
    g["ex"] = g["r"] - g["coin"].map(drift)
    n_cases = int(len(g))

    slope, tval = None, None
    if n_cases >= 3 and np.std(g["f"].values) > 0:
        lr = stats.linregress(g["f"].values, g["ex"].values)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. supporting check: timing gain before costs ----------
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            r_next = (c.shift(-1) / c - 1)
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            for i in range(len(df) - 1):
                recs.append((coin, day.iloc[i], pos.iloc[i], r_next.iloc[i]))
    d = pd.DataFrame(recs, columns=["coin", "day", "pos", "r"]).replace([np.inf, -np.inf], np.nan)
    mu = d.dropna(subset=["r"]).groupby("coin")["r"].mean()
    d = d.dropna(subset=["pos", "r"])
    timing = None
    if len(d) > 0:
        d["timing"] = d["pos"] * (d["r"] - d["coin"].map(mu))
        timing = float(d.groupby("day")["timing"].mean().mean())
    sup_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, below the plan's minimum of 300."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing gain is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book's timing gain before costs (mean daily return minus market part)",
            "value": timing,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping cases": n_cases, "active bars": int(active)},
        "decided_by": decided,
        "reading": reading,
    }
